"""Support for Ecowitt Weather Stations."""
import logging
import homeassistant.util.dt as dt_util

from . import EcowittEntity
from .const import (
    DOMAIN,
    TYPE_SENSOR,
    SENSOR_TYPES,
    REG_ENTITIES,
    NEW_ENTITIES,
)

from homeassistant.const import (
    STATE_UNKNOWN,
    DEVICE_CLASS_TIMESTAMP
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Add sensors if new."""
    _LOGGER.warning("sensor setup entry called")
    ecowitt_data = hass.data[DOMAIN][entry.entry_id]
    new_ent = ecowitt_data[NEW_ENTITIES][TYPE_SENSOR]
    reg_ent = ecowitt_data[REG_ENTITIES][TYPE_SENSOR]
    entities = []

    for new_entity in new_ent:
        if new_entity in reg_ent:
            continue
        reg_ent.append(new_entity)
        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[new_entity]
        entities.append(EcowittSensor(hass, entry, new_entity, name,
                                      device_class, uom, icon))
    # clear the list
    new_ent = []
    async_add_entities(entities, True)


class EcowittSensor(EcowittEntity):

    def __init__(self, hass, entry, key, name, dc, uom, icon):
        """Initialize the sensor."""
        super().__init__(hass, entry, key, name)
        self._icon = icon
        self._uom = uom
        self._dc = dc

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.warning("sensor: request for " + self._key)
        if self._key in self._ws.last_values:
            # The lightning time is reported in UTC, hooray.
            if self._dc == DEVICE_CLASS_TIMESTAMP:
                return dt_util.as_local(
                    dt_util.utc_from_timestamp(self._ws.last_values[self._key])
                ).isoformat()
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
    def device_class(self):
        """Return the device class."""
        return self._dc
