"""Number platform for Denkovi SmartDEN."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DenkoviDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Denkovi SmartDEN number entities."""
    coordinator: DenkoviDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    
    # Create number entities for analog outputs
    analog_outputs = coordinator.data.get("analog_outputs", {})
    for output_id in analog_outputs.keys():
        entities.append(DenkoviAnalogOutputNumber(coordinator, entry, output_id))

    async_add_entities(entities)


class DenkoviAnalogOutputNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Denkovi analog output as a number entity."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 0
    _attr_native_max_value = 1023
    _attr_native_step = 1

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        output_id: int,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._output_id = output_id
        self._attr_unique_id = f"{entry.entry_id}_analog_output_{output_id}"
        
        # Use custom name from API
        output_names = coordinator.data.get("analog_output_names", {})
        self._attr_name = output_names.get(output_id, f"Analog Output {output_id}")
        
        # Device info for grouping
        device_info = coordinator.data.get("device", {})
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": device_info.get("DeviceName", "Denkovi SmartDEN"),
            "manufacturer": "Denkovi",
            "model": device_info.get("DeviceType", "SmartDEN"),
        }

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        analog_outputs = self.coordinator.data.get("analog_outputs", {})
        value = analog_outputs.get(self._output_id)
        if value is not None:
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set the analog output value."""
        try:
            await self.coordinator.async_set_analog_output(self._output_id, int(value))
        except Exception as err:
            _LOGGER.error("Failed to set analog output %s: %s", self._output_id, err)
