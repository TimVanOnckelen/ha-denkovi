"""Support for Denkovi SmartDEN switches."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
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
    """Set up Denkovi SmartDEN switches from a config entry."""
    coordinator: DenkoviDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create switch entities for each relay, excluding those configured as lights
    light_relays = entry.options.get("light_relays", [])
    entities = []
    relays = coordinator.data.get("relays", {})
    
    for relay_id in relays:
        # relay_id is already an integer (1-8)
        # Skip if this relay is configured as a light
        if relay_id not in light_relays:
            entities.append(DenkoviSwitch(coordinator, entry, relay_id))

    async_add_entities(entities)


class DenkoviSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Denkovi SmartDEN switch."""

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        relay_id: int,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._relay_id = relay_id
        self._entry = entry
        # Use name from API, fallback to generic name
        relay_name = coordinator.data.get("relay_names", {}).get(relay_id, f"Relay {relay_id}")
        self._attr_name = relay_name
        self._attr_unique_id = f"{entry.entry_id}_relay_{relay_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Denkovi SmartDEN ({coordinator.host})",
            manufacturer="Denkovi",
            model=coordinator.get_device_model(),
            sw_version=coordinator.data.get("device", {}).get("sysUpTime", "Unknown"),
        )

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.coordinator.data.get("relays", {}).get(self._relay_id, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.async_set_relay(self._relay_id, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.async_set_relay(self._relay_id, False)
