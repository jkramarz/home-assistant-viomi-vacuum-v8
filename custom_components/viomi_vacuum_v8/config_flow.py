"""Config flow for Viomi Vacuum V8."""

import voluptuous as vol
from miio import DeviceException, ViomiVacuum

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TOKEN
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN


class ViomiVacuumV8ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Viomi Vacuum V8."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            try:
                await self.hass.async_add_executor_job(
                    _validate_input, host, user_input[CONF_TOKEN]
                )
            except (DeviceException, OSError, ValueError):
                errors["base"] = "cannot_connect"
            else:
                name = user_input.get(CONF_NAME, DEFAULT_NAME).strip() or DEFAULT_NAME
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_HOST: host,
                        CONF_TOKEN: user_input[CONF_TOKEN],
                        CONF_NAME: name,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): vol.All(cv.string, vol.Length(min=1)),
                vol.Required(CONF_TOKEN): vol.All(
                    cv.string, vol.Length(min=32, max=32)
                ),
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


def _validate_input(host, token):
    """Verify the host and token by requesting a vacuum property."""
    ViomiVacuum(host, token).raw_command("get_prop", ["run_state"])
