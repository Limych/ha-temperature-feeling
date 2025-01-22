"""
Custom component to calculate air temperature feeling.

For more details about this integration, please refer to
https://github.com/Limych/ha-temperature-feeling
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle setup of config entry."""
    hass.data.setdefault(DOMAIN, {})

    await hass.config_entries.async_forward_entry_setups(
        config_entry, [Platform.SENSOR]
    )

    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
