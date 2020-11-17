"""Support for Ecowitt Weather Stations."""
import logging

from . import EcowittEntity
from .const import (
    DATA_ECOWITT,
    DOMAIN,
    TYPE_BINARY_SENSOR,
    SENSOR_TYPES,
    REG_ENTITIES,
    NEW_ENTITIES,
)
from homeassistant.components.binary_sensor import BinarySensorEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Add sensors if new."""
    ecowitt_data = hass.data[DOMAIN][entry.entry_id]
    new_ent = ecowitt_data[NEW_ENTITIES][TYPE_BINARY_SENSOR]
    reg_ent = ecowitt_data[REG_ENTITIES][TYPE_BINARY_SENSOR]
    entities = []

    for new_entity in new_ent:
        if new_entity in reg_ent:
            continue
        reg_ent.append(new_entity)
        _LOGGER.warning(TYPE_BINARY_SENSOR + " " + new_entity)
        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[new_entity]
        entities.append(EcowittBinarySensor(hass, entry, new_entity, name,
                                            device_class, uom, icon))
    # clear the list
    new_ent = []
    async_add_entities(entities, True)


class EcowittBinarySensor(EcowittEntity, BinarySensorEntity):

    def __init__(self, hass, entry, key, name, dc, uom, icon):
        """Initialize the sensor."""
        super().__init__(hass, entry, key, name)
        self._icon = icon
        self._uom = uom
        self._dc = dc

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        _LOGGER.warning("hello sensor")
        if self._key in self._ws.last_values:
            if self._ws.last_values[self._key] > 0:
                return True
        else:
            _LOGGER.warning("Sensor %s not in last update, check range or battery",
                            self._key)
        return False

    # @property
    # def icon(self):
    #     """Return the icon to use in the fronend."""
    #     return self._icon

    @property
    def device_class(self):
        """Return the device class."""
        return self._dc
