"""Support for Ecowitt Weather Stations."""
import logging

from . import (
    TYPE_BINARY_SENSOR,
    SENSOR_TYPES,
    EcowittEntity,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Setup a single Ecowitt sensor."""

    if not discovery_info:
        return

    entities = []
    for sensor in discovery_info:
        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[sensor]
        if kind == TYPE_BINARY_SENSOR:
            entities.append(
                EcowittBinarySensor(
                    hass,
                    sensor,
                    name,
                    device_class,
                    uom,
                    icon,
                )
            )
    async_add_entities(entities, True)


class EcowittBinarySensor(EcowittEntity):

    def __init__(self, hass, key, name, dc, uom, icon):
        """Initialize the sensor."""
        super().__init__(hass, key, name)
        self._icon = icon
        self._uom = uom
        self._dc = dc

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self._key in self._ws_last_values:
            if self._ws.last_values[self._key] > 0:
                return True
        else:
            _LOGGER.warning("Sensor %s not in last update, check range or battery",
                            self._key)
        return False

    @property
    def icon(self):
        """Return the icon to use in the fronend."""
        return self._icon

    @property
    def device_class(self):
        """Return the device class."""
        return self._dc
