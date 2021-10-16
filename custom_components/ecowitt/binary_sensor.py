"""Support for Ecowitt Weather Stations."""
import logging

from . import EcowittEntity, async_add_ecowitt_entities
from .const import (
    DOMAIN,
    TYPE_BINARY_SENSOR,
    REG_ENTITIES,
    SIGNAL_ADD_ENTITIES,
)
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNKNOWN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Add sensors if new."""

    def add_entities(discovery_info=None):
        async_add_ecowitt_entities(hass, entry, EcowittBinarySensor,
                                   BINARY_SENSOR_DOMAIN, async_add_entities,
                                   discovery_info)

    signal = f"{SIGNAL_ADD_ENTITIES}_{BINARY_SENSOR_DOMAIN}"
    async_dispatcher_connect(hass, signal, add_entities)
    add_entities(hass.data[DOMAIN][entry.entry_id][REG_ENTITIES][TYPE_BINARY_SENSOR])


class EcowittBinarySensor(EcowittEntity, BinarySensorEntity):

    def __init__(self, hass, entry, key, name, dc, uom, icon, sc):
        """Initialize the sensor."""
        super().__init__(hass, entry, key, name)
        self._icon = icon
        self._uom = uom
        self._dc = dc

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self._key in self._ws.last_values:
            if self._ws.last_values[self._key] > 0:
                return True
        else:
            _LOGGER.warning("Sensor %s not in last update, check range or battery",
                            self._key)
            return None
        return False

    @property
    def state(self):
        """Return the state of the binary sensor."""
        # Don't claim a leak is cleared if the sensor is out of range
        if self.is_on is None:
            return STATE_UNKNOWN
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def device_class(self):
        """Return the device class."""
        return self._dc
