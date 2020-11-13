"""The Ecowitt Weather Station Component."""
# import asyncio
import logging
import time

from pyecowitt import (
    EcoWittListener,
    WINDCHILL_OLD,
    WINDCHILL_NEW,
    WINDCHILL_HYBRID,
)
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.entity import Entity

from homeassistant.const import (
    CONF_PORT,
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
)

from .const import (
    CONF_UNIT_BARO,
    CONF_UNIT_WIND,
    CONF_UNIT_RAIN,
    CONF_UNIT_WINDCHILL,
    CONF_UNIT_LIGHTNING,
    DOMAIN,
    DATA_CONFIG,
    DATA_ECOWITT,
    DATA_STATION,
    DATA_PASSKEY,
    DATA_STATIONTYPE,
    DATA_FREQ,
    DATA_MODEL,
    DATA_READY,
    ECOWITT_PLATFORMS,
    IGNORED_SENSORS,
    S_IMPERIAL,
    S_METRIC,
    SENSOR_TYPES,
    TYPE_SENSOR,
    TYPE_BINARY_SENSOR,
    W_TYPE_NEW,
    W_TYPE_OLD,
    W_TYPE_HYBRID,
)

_LOGGER = logging.getLogger(__name__)

COMPONENT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT): cv.port,
        vol.Optional(CONF_UNIT_BARO,
                     default=CONF_UNIT_SYSTEM_METRIC): cv.string,
        vol.Optional(CONF_UNIT_WIND,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): cv.string,
        vol.Optional(CONF_UNIT_RAIN,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): cv.string,
        vol.Optional(CONF_UNIT_LIGHTNING,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): cv.string,
        vol.Optional(CONF_UNIT_WINDCHILL,
                     default=W_TYPE_HYBRID): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: COMPONENT_SCHEMA}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: dict):
    """Configure the Ecowitt component using flow only."""
    hass.data[DOMAIN] = {}

    if DOMAIN in config:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=config[DOMAIN]
            )
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Ecowitt component from a config entry."""

    sensor_sensors = []
    binary_sensors = []

    # Store config
    _LOGGER.error(entry.entry_id)
    hass.data[DOMAIN][entry.entry_id] = {}
    hass.data[DOMAIN][entry.entry_id][DATA_STATION] = {}
    hass.data[DOMAIN][entry.entry_id][DATA_READY] = False

    # preload some model info
    stationinfo = hass.data[DOMAIN][entry.entry_id][DATA_STATION]
    stationinfo[DATA_STATIONTYPE] = "Unknown"
    stationinfo[DATA_FREQ] = "Unknown"
    stationinfo[DATA_MODEL] = "Unknown"

    # setup the base connection
    ws = EcoWittListener(port=entry.data[CONF_PORT])
    hass.data[DOMAIN][entry.entry_id][DATA_ECOWITT] = ws

    if entry.data[CONF_UNIT_WINDCHILL] == W_TYPE_OLD:
        ws.set_windchill(WINDCHILL_OLD)
    if entry.data[CONF_UNIT_WINDCHILL] == W_TYPE_NEW:
        ws.set_windchill(WINDCHILL_NEW)
    if entry.data[CONF_UNIT_WINDCHILL] == W_TYPE_HYBRID:
        ws.set_windchill(WINDCHILL_HYBRID)

    hass.loop.create_task(ws.listen())

    async def close_server(*args):
        """ Close the ecowitt server."""
        await ws.stop()

    # hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, close_server)

    # # go to sleep until we get the first report
    # await ws.wait_for_valid_data()

    def check_imp_metric_sensor(sensor):
        """Check if this is the wrong sensor for our config (imp/metric)."""
        # Is this a metric or imperial sensor, lookup and skip
        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[sensor]
        if "baro" in sensor:
            if (entry.data[CONF_UNIT_BARO] == CONF_UNIT_SYSTEM_IMPERIAL
                    and metric == S_METRIC):
                return False
            if (entry.data[CONF_UNIT_BARO] == CONF_UNIT_SYSTEM_METRIC
                    and metric == S_IMPERIAL):
                return False
        if "rain" in sensor:
            if (entry.data[CONF_UNIT_RAIN] == CONF_UNIT_SYSTEM_IMPERIAL
                    and metric == S_METRIC):
                return False
            if (entry.data[CONF_UNIT_RAIN] == CONF_UNIT_SYSTEM_METRIC
                    and metric == S_IMPERIAL):
                return False
        if "wind" in sensor:
            if (entry.data[CONF_UNIT_WIND] == CONF_UNIT_SYSTEM_IMPERIAL
                    and metric == S_METRIC):
                return False
            if (entry.data[CONF_UNIT_WIND] == CONF_UNIT_SYSTEM_METRIC
                    and metric == S_IMPERIAL):
                return False
        if (sensor == 'lightning'
                and entry.data[CONF_UNIT_LIGHTNING] == CONF_UNIT_SYSTEM_IMPERIAL):
            return False
        if (sensor == 'lightning_mi'
                and entry.data[CONF_UNIT_LIGHTNING] == CONF_UNIT_SYSTEM_METRIC):
            return False
        return True

    def check_and_append_sensor(sensor):
        """Check the sensor for validity, and append to appropriate list."""
        if sensor not in SENSOR_TYPES:
            if sensor not in IGNORED_SENSORS:
                _LOGGER.warning("Unhandled sensor type %s", sensor)
            return None

        # Is this a metric or imperial sensor, lookup and skip
        if not check_imp_metric_sensor(sensor):
            return None

        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[sensor]
        if kind == TYPE_SENSOR:
            sensor_sensors.append(sensor)
        if kind == TYPE_BINARY_SENSOR:
            binary_sensors.append(sensor)
        return(kind)

    async def _first_data_rec(weather_data):
        _LOGGER.info("First ecowitt data recd, setting up sensors.")
        # check if we have model info, etc.
        if DATA_PASSKEY in ws.last_values:
            stationinfo[DATA_PASSKEY] = ws.last_values[DATA_PASSKEY]
            ws.last_values.pop(DATA_PASSKEY, None)
        else:
            _LOGGER.error("No passkey, cannot set unique id.")
            return False
        if DATA_STATIONTYPE in ws.last_values:
            stationinfo[DATA_STATIONTYPE] = ws.last_values[DATA_STATIONTYPE]
            ws.last_values.pop(DATA_STATIONTYPE, None)
        if DATA_FREQ in ws.last_values:
            stationinfo[DATA_FREQ] = ws.last_values[DATA_FREQ]
            ws.last_values.pop(DATA_FREQ, None)
        if DATA_MODEL in ws.last_values:
            stationinfo[DATA_MODEL] = ws.last_values[DATA_MODEL]
            ws.last_values.pop(DATA_MODEL, None)

        # load the sensors we have
        for sensor in ws.last_values.keys():
            check_and_append_sensor(sensor)

        if not sensor_sensors and not binary_sensors:
            _LOGGER.error("No sensors found to monitor, check device config.")
            return False

        if sensor_sensors:
            hass.async_create_task(
                async_load_platform(hass, "sensor", DOMAIN, sensor_sensors,
                                    entry.data)
            )
        if binary_sensors:
            hass.async_create_task(
                async_load_platform(hass, "binary_sensor", DOMAIN, binary_sensors,
                                    entry.data)
            )
        hass.data[DOMAIN][entry.entry_id][DATA_READY] = True

    async def _async_ecowitt_update_cb(weather_data):
        """Primary update callback called from pyecowitt."""
        _LOGGER.debug("Primary update callback triggered.")
        if not hass.data[DOMAIN][entry.entry_id][DATA_READY]:
            await _first_data_rec(weather_data)
            return
        for sensor in weather_data.keys():
            if sensor not in SENSOR_TYPES:
                if sensor not in IGNORED_SENSORS:
                    _LOGGER.warning("Unhandled sensor type %s value %s, "
                                    + "file a PR.", sensor, weather_data[sensor])
            elif (sensor not in sensor_sensors
                  and sensor not in binary_sensors
                  and sensor not in IGNORED_SENSORS
                  and check_imp_metric_sensor(sensor)):
                _LOGGER.warning("Unregistered sensor type %s value %s received.",
                                sensor, weather_data[sensor])
                # try to register the sensor
                new_sensor = []
                new_sensor.append(sensor)
                kind = check_and_append_sensor(sensor)
                if kind == TYPE_SENSOR:
                    hass.async_create_task(
                        async_load_platform(hass, "sensor", DOMAIN,
                                            new_sensor, entry.data)
                    )
                if kind == TYPE_BINARY_SENSOR:
                    hass.async_create_task(
                        async_load_platform(hass, "binary_sensor", DOMAIN,
                                            new_sensor, entry.data)
                    )

        async_dispatcher_send(hass, DOMAIN)

    ws.register_listener(_async_ecowitt_update_cb)

    return True


class EcowittEntity(Entity):
    """Base class for Ecowitt Weather Station."""

    def __init__(self, hass, key, name):
        """Construct the entity."""
        self.hass = hass
        self._key = key
        self._name = name
        self._stationinfo = hass.data[DOMAIN][DATA_STATION]
        self._ws = hass.data[DOMAIN][DATA_ECOWITT]

    @property
    def should_poll(self):
        """Ecowitt is a push."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID for this sensor."""
        return f"{self._stationinfo[DATA_PASSKEY]}-{self._key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_info(self):
        """Return device information for this sensor."""
        return {
            "station": self._stationinfo[DATA_STATIONTYPE],
            "model": self._stationinfo[DATA_MODEL],
            "frequency": self._stationinfo[DATA_FREQ],
        }

    async def async_added_to_hass(self):
        """Setup a listener for the entity."""
        async_dispatcher_connect(self.hass, DOMAIN, self._update_callback)

    @callback
    def _update_callback(self) -> None:
        """Call from dispatcher when state changes."""
        _LOGGER.debug("Updating state with new data. %s", self._name)
        self.async_schedule_update_ha_state(force_refresh=True)

    @property
    def assumed_state(self) -> bool:
        """Return whether the state is based on actual reading from device."""
        if (self._ws.lastupd + 5 * 60) < time.time():
            return True
        return False
