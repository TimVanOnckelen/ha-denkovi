"""Support for Denkovi SmartDEN binary sensors."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
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
    """Set up Denkovi SmartDEN binary sensors from a config entry."""
    coordinator: DenkoviDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create binary sensor entities for each digital input
    entities = []
    digital_inputs = coordinator.data.get("digital_inputs", {})
    
    for input_id in digital_inputs:
        entities.append(DenkoviBinarySensor(coordinator, entry, input_id))

    async_add_entities(entities)


class DenkoviBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Denkovi SmartDEN digital input."""

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        input_id: int,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._input_id = input_id
        # Use name from API, fallback to generic name
        input_name = coordinator.data.get("digital_input_names", {}).get(input_id, f"Digital Input {input_id}")
        self._attr_name = input_name
        self._attr_unique_id = f"{entry.entry_id}_digital_input_{input_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Denkovi SmartDEN ({coordinator.host})",
            manufacturer="Denkovi",
            model=coordinator.get_device_model(),
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get("digital_inputs", {}).get(self._input_id, False)
