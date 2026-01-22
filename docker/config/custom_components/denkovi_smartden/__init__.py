"""The Denkovi SmartDEN integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_SCAN_INTERVAL, DEFAULT_PASSWORD, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import DenkoviDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SWITCH, Platform.LIGHT, Platform.SENSOR, Platform.BINARY_SENSOR, Platform.NUMBER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Denkovi SmartDEN from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    password = entry.data.get(CONF_PASSWORD, DEFAULT_PASSWORD)
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    coordinator = DenkoviDataUpdateCoordinator(hass, host, port, password, scan_interval)
    
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Unable to connect to Denkovi SmartDEN at {host}") from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Determine which platforms to load based on device capabilities
    platforms_to_load = [Platform.SENSOR, Platform.BINARY_SENSOR]
    
    # Only add switch, light, and number platforms if device has relays/outputs (IP-Maxi)
    if coordinator.data.get("relays") or coordinator.data.get("analog_outputs"):
        platforms_to_load.extend([Platform.SWITCH, Platform.LIGHT, Platform.NUMBER])

    await hass.config_entries.async_forward_entry_setups(entry, platforms_to_load)
    
    # Register options update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Determine which platforms were loaded
    coordinator = hass.data[DOMAIN][entry.entry_id]
    platforms_to_unload = [Platform.SENSOR, Platform.BINARY_SENSOR]
    
    if coordinator.data.get("relays") or coordinator.data.get("analog_outputs"):
        platforms_to_unload.extend([Platform.SWITCH, Platform.LIGHT, Platform.NUMBER])
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, platforms_to_unload):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()

    return unload_ok
