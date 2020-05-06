"""The Ecowitt Weather Station Component."""
import asyncio
import logging
import time

from pyecowitt import EcoWittListener
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.entity import Entity

from homeassistant.const import (
    DEGREE,
    EVENT_HOMEASSISTANT_STOP,
    CONF_PORT,
    POWER_WATT,
    TEMP_CELSIUS,
    UNIT_PERCENTAGE,
    PRESSURE_HPA,
    LENGTH_INCHES,
    SPEED_KILOMETERS_PER_HOUR,
    UV_INDEX,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_PRESSURE,
)

_LOGGER = logging.getLogger(__name__)

TYPE_SENSOR = "sensor"
DOMAIN = "ecowitt"
DATA_CONFIG = "config"
DATA_ECOWITT = "ecowitt_listener"
DATA_STATION = "station"
DATA_PASSKEY = "PASSKEY"
DATA_STATIONTYPE = "stationtype"
DATA_FREQ = "freq"
DATA_MODEL = "model"

TYPE_BAROMABSHPA = "baromabshpa"
TYPE_BAROMRELHPA = "baromrelhpa"
TYPE_RAINRATEIN = "rainratein"
TYPE_EVENTRAININ = "eventrainin"
TYPE_DAILYRAININ = "dailyrainin"
TYPE_WEEKLYRAININ = "weeklyrainin"
TYPE_MONTHLYRAININ = "monthlyrainin"
TYPE_YEARLYRAININ = "yearlyrainin"
TYPE_HUMIDITY = "humidity"
TYPE_HUMIDITYIN = "humidityin"
TYPE_WINDDIR = "winddir"
TYPE_WINDSPEEDKMH = "windspeedkmh"
TYPE_WINDGUSTKMH = "windgustkmh"
TYPE_TEMPC = "tempc"
TYPE_TEMPINC = "tempinc"
TYPE_TEMP1C = "temp1c"
TYPE_TEMP2C = "temp2c"
TYPE_TEMP3C = "temp3c"
TYPE_DEWPOINTC = "dewpointc"
TYPE_WINDCHILLC = "windchillc"
TYPE_SOLARRADIATION = "solarradiation"
TYPE_UV = "uv"

# Name, unit_of_measure, type, device_class, icon
# name, uom, kind, device_class, icon = SENSOR_TYPES[x]
SENSOR_TYPES = {
    TYPE_BAROMABSHPA: ("Absolute Pressure", PRESSURE_HPA,
                       TYPE_SENSOR, DEVICE_CLASS_PRESSURE, "mdi:gauge"),
    TYPE_BAROMRELHPA: ("Relative Pressure", PRESSURE_HPA,
                       TYPE_SENSOR, DEVICE_CLASS_PRESSURE, "mdi:gauge"),
    TYPE_RAINRATEIN: ("Rain Rate", LENGTH_INCHES,
                      TYPE_SENSOR, None, "mdi:water"),
    TYPE_EVENTRAININ: ("Event Rain Rate", LENGTH_INCHES,
                       TYPE_SENSOR, None, "mdi:water"),
    TYPE_DAILYRAININ: ("Daily Rain Rate", LENGTH_INCHES,
                       TYPE_SENSOR, None, "mdi:water"),
    TYPE_WEEKLYRAININ: ("Weekly Rain Rate", LENGTH_INCHES,
                        TYPE_SENSOR, None, "mdi:water"),
    TYPE_MONTHLYRAININ: ("Monthly Rain Rate", LENGTH_INCHES,
                         TYPE_SENSOR, None, "mdi:water"),
    TYPE_YEARLYRAININ: ("Yearly Rain Rate", LENGTH_INCHES,
                        TYPE_SENSOR, None, "mdi:water"),
    TYPE_HUMIDITY: ("Humidity", UNIT_PERCENTAGE,
                    TYPE_SENSOR, DEVICE_CLASS_HUMIDITY, "mdi:water-percent"),
    TYPE_HUMIDITYIN: ("Indoor Humidity", UNIT_PERCENTAGE,
                      TYPE_SENSOR, DEVICE_CLASS_HUMIDITY, "mdi:water-percent"),
    TYPE_WINDDIR: ("Wind Direction", DEGREE,
                   TYPE_SENSOR, None, "mdi:water-percent"),
    TYPE_WINDSPEEDKMH: ("Wind Speed", SPEED_KILOMETERS_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy"),
    TYPE_WINDGUSTKMH: ("Wind Gust", SPEED_KILOMETERS_PER_HOUR,
                       TYPE_SENSOR, None, "mdi:weather-windy"),
    TYPE_TEMPC: ("Outdoor Temperature", TEMP_CELSIUS,
                 TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer"),
    TYPE_TEMP1C: ("Temperature 1", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer"),
    TYPE_TEMP2C: ("Temperature 2", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer"),
    TYPE_TEMP3C: ("Temperature 3", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer"),
    TYPE_TEMPINC: ("Indoor Temperature", TEMP_CELSIUS,
                   TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer"),
    TYPE_DEWPOINTC: ("Dewpoint", TEMP_CELSIUS,
                     TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer"),
    TYPE_WINDCHILLC: ("Windchill", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer"),
    TYPE_SOLARRADIATION: ("Solar Radiation", f"{POWER_WATT}/m^2",
                          TYPE_SENSOR, DEVICE_CLASS_ILLUMINANCE,
                          "mdi:weather-sunny"),
    TYPE_UV: ("UV Index", UV_INDEX,
              TYPE_SENSOR, None, "mdi:sunglasses"),
}

IGNORED_SENSORS = [
    'tempinf',
    'tempf',
    'temp1f',
    'temp2f',
    'temp3f',
    'baromrelin',
    'baromabsin',
    'dateutc',
    'windspeedmph',
    'windgustmph',
    'rainratein',
    'eventrainin',
    'dailyrainin',
    'weeklyrainin',
    'monthlyrainin',
    'yearlyrainin',
    'windgustms',
    'windchillf',
    'dewpointf',
]


COMPONENT_SCHEMA = vol.Schema(
    {vol.Required(CONF_PORT): cv.port}
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: COMPONENT_SCHEMA}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config):
    """Set up the Ecowitt component."""

    hass.data[DOMAIN] = {}
    all_sensors = []

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]

    # Store config
    hass.data[DOMAIN][DATA_CONFIG] = conf
    hass.data[DOMAIN][DATA_STATION] = {}

    # preload some model info
    stationinfo = hass.data[DOMAIN][DATA_STATION]
    stationinfo[DATA_STATIONTYPE] = "Unknown"
    stationinfo[DATA_FREQ] = "Unknown"
    stationinfo[DATA_MODEL] = "Unknown"

    # setup the base connection
    ws = EcoWittListener(port=conf[CONF_PORT])
    hass.data[DOMAIN][DATA_ECOWITT] = ws

    hass.async_create_task(ws.start())

    async def close_server(*args):
        """ Close the ecowitt server."""
        await ws.stop()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, close_server)

    # go to sleep until we get the first report
    await ws.wait_for_valid_data()

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
        if sensor not in SENSOR_TYPES:
            if sensor not in IGNORED_SENSORS:
                _LOGGER.warning("Unhandled sensor type %s", sensor)
            continue
        all_sensors.append(SENSOR_TYPES[sensor])

    if not all_sensors:
        _LOGGER.error("No sensors found to monitor, check device config.")
        return False

    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, all_sensors, config)
    )

    async def _async_ecowitt_update_cb(weather_data):
        """Primary update callback called from pyecowitt."""
        _LOGGER.debug("Primary update callback triggered.")
        async_dispatcher_send(hass, DOMAIN)

    ws.register_listener(_async_ecowitt_update_cb)

    return True


class EcowittEntity(Entity):
    """Base class for Ecowitt Weather Station."""

    def __init(self, hass, key, name, stationinfo):
        """Construct the entity."""
        self.hass = hass
        self._key = key
        self._name = name
        self._stationinfo = stationinfo
        self._ws = hass.data[DOMAIN][DATA_ECOWITT]

    @property
    def should_poll(self):
        """Ecowitt is a push."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID for this sensor."""
        return f"{self._stationinfo[DATA_PASSKEY]}-{self._sensor_type}-{self._key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

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
