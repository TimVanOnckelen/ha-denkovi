"""Support for Denkovi SmartDEN lights."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .coordinator import DenkoviDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Denkovi SmartDEN lights from a config entry."""
    coordinator: DenkoviDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create light entities for relays configured as lights
    entities = []
    # Get relay configuration from options (empty by default)
    light_relays = entry.options.get("light_relays", [])
    
    for relay_id in light_relays:
        entities.append(DenkoviLight(coordinator, entry, relay_id))

    async_add_entities(entities)


class DenkoviLight(CoordinatorEntity, LightEntity):
    """Representation of a Denkovi SmartDEN light."""

    _attr_color_mode = ColorMode.ONOFF
    _attr_supported_color_modes = {ColorMode.ONOFF}

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        relay_id: int,
    ) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._relay_id = relay_id
        self._entry = entry
        # Use name from API, fallback to generic name
        relay_name = coordinator.data.get("relay_names", {}).get(relay_id, f"Light {relay_id}")
        self._attr_name = relay_name
        self._attr_unique_id = f"{entry.entry_id}_light_{relay_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Denkovi SmartDEN ({coordinator.host})",
            manufacturer="Denkovi",
            model=coordinator.get_device_model(),
        )

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self.coordinator.data.get("relays", {}).get(self._relay_id, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        await self.coordinator.async_set_relay(self._relay_id, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self.coordinator.async_set_relay(self._relay_id, False)
