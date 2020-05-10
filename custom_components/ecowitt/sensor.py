"""Support for Ecowitt Weather Stations."""
import logging

from . import (
    TYPE_SENSOR,
    DOMAIN,
    DATA_STATION,
    SENSOR_TYPES,
    EcowittEntity,
)

from homeassistant.const import STATE_UNKNOWN

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Setup a single Ecowitt sensor."""

    if not discovery_info:
        return

    entities = []
    for sensor in discovery_info:
        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[sensor]
        if kind == TYPE_SENSOR:
            entities.append(
                EcowittSensor(
                    hass,
                    sensor,
                    name,
                    device_class,
                    uom,
                    icon,
                )
            )
    async_add_entities(entities, True)


class EcowittSensor(EcowittEntity):

    def __init__(self, hass, key, name, dc, uom, icon):
        """Initialize the sensor."""
        super().__init__(hass, key, name)
        self._icon = icon
        self._uom = uom
        self._dc = dc

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._key in self._ws.last_values:
            return self._ws.last_values[self._key]
        _LOGGER.warning("Sensor %s not in last update, check range or battery",
                        self._key)
        return STATE_UNKNOWN

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._uom

    @property
    def icon(self):
        """Return the icon to use in the fronend."""
        return self._icon

    @property
    def device_info(self):
        """Return the device class."""
        return self._dc
