"""Support for Ecowitt Weather Stations."""
import logging

from . import (
    SENSOR_TYPES,
    TYPE_SENSOR,
    DOMAIN,
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
        name, uom, kind, device_class, icon = SENSOR_TYPES[sensor]
        if kind == TYPE_SENSOR:
            entities.append(
                EcowittSensor(
                    hass,
                    sensor,
                    name,
                    hass.data[DOMAIN][DATA_STATION],
                    device_class,
                    uom,
                    icon,
                )
            )

    async_add_entities(entities, True)


class EcowittSensor(EcowittEntity):

    def __init__(self, hass, key, name, stationinfo, dc, uom, icon):
        """Initialize the sensor."""
        super().__init__(hass, key, name, stationinfo)
        self._icon = icon
        self._uom = uom
        self._dc = dc

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._ws.last_values[self._key]

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
