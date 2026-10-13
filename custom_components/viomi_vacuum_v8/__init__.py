"""The Viomi Vacuum V8 integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Viomi Vacuum V8 from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Viomi Vacuum V8 config entry."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False

    devices = hass.data.get(DOMAIN, {})
    devices.pop(entry.entry_id, None)
    if not devices:
        hass.data.pop(DOMAIN, None)
    return True
