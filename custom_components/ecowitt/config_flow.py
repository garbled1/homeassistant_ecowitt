"""Config flow for ecowitt."""
import logging

from pyecowitt import (
    EcoWittListener,
    WINDCHILL_OLD,
    WINDCHILL_NEW,
    WINDCHILL_HYBRID,
)

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries, core, exceptions

from homeassistant.const import (
    CONF_PORT,
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
)

from .const import (
    CONF_NAME,
    CONF_UNIT_BARO,
    CONF_UNIT_WIND,
    CONF_UNIT_RAIN,
    CONF_UNIT_WINDCHILL,
    CONF_UNIT_LIGHTNING,
    DEFAULT_PORT,
    DOMAIN,
    DATA_CONFIG,
    DATA_ECOWITT,
    DATA_STATION,
    DATA_PASSKEY,
    DATA_STATIONTYPE,
    DATA_FREQ,
    DATA_MODEL,
    DATA_READY,
    W_TYPE_NEW,
    W_TYPE_OLD,
    W_TYPE_HYBRID,
)

UNIT_OPTS = [CONF_UNIT_SYSTEM_METRIC, CONF_UNIT_SYSTEM_IMPERIAL]
WINDCHILL_OPTS = [W_TYPE_HYBRID, W_TYPE_NEW, W_TYPE_OLD]


_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_UNIT_BARO,
                     default=CONF_UNIT_SYSTEM_METRIC): vol.In(UNIT_OPTS),
        vol.Optional(CONF_UNIT_WIND,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): vol.In(UNIT_OPTS),
        vol.Optional(CONF_UNIT_RAIN,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): vol.In(UNIT_OPTS),
        vol.Optional(CONF_UNIT_LIGHTNING,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): vol.In(UNIT_OPTS),
        vol.Optional(CONF_UNIT_WINDCHILL,
                     default=W_TYPE_HYBRID): vol.In(WINDCHILL_OPTS),
    }
)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate user input."""
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.data[CONF_PORT] == data[CONF_PORT]:
            raise AlreadyConfigured
    return {"title": f"Ecowitt on port {data[CONF_PORT]}"}


class EcowittConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the Ecowitt."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_import(self, device_config):
        """Import a configuration.yaml config, if any."""

        port = device_config[CONF_PORT]
        _LOGGER.error(device_config)
        return self.async_create_entry(
            title=f"Ecowitt on port {port}",
            data=device_config
        )

    async def async_step_user(self, user_input=None):
        """Give initial instructions for setup."""
        if user_input is not None:
            return await self.async_step_initial_options()

        return self.async_show_form(step_id="user")

    async def async_step_initial_options(self, user_input=None):
        """Ask the user for the setup options."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"],
                                               data=user_input)
            except AlreadyConfigured:
                return self.async_abort(reason="already_configured")

        return self.async_show_form(
            step_id="initial_options", data_schema=DATA_SCHEMA, errors=errors
        )


class AlreadyConfigured(exceptions.HomeAssistantError):
    """Error to indicate this device is already configured."""
