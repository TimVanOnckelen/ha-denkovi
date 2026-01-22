"""Support for Denkovi SmartDEN sensors."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
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
    """Set up Denkovi SmartDEN sensors from a config entry."""
    coordinator: DenkoviDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    
    # Create counter sensors for each digital input
    counters = coordinator.data.get("counters", {})
    for input_id in counters:
        entities.append(DenkoviCounterSensor(coordinator, entry, input_id))
    
    # Create analog input sensors
    analog_inputs = coordinator.data.get("analog_inputs", {})
    for input_id in analog_inputs:
        # Inputs 5-8 are typically temperature sensors on IP-Maxi
        is_temperature = input_id >= 5
        entities.append(DenkoviAnalogSensor(coordinator, entry, input_id, is_temperature))
    
    # Create dedicated temperature input sensors (Notifier only)
    temperature_inputs = coordinator.data.get("temperature_inputs", {})
    for input_id in temperature_inputs:
        entities.append(DenkoviTemperatureSensor(coordinator, entry, input_id))

    async_add_entities(entities)


class DenkoviCounterSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Denkovi SmartDEN counter sensor."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        input_id: int,
    ) -> None:
        """Initialize the counter sensor."""
        super().__init__(coordinator)
        self._input_id = input_id
        # Use name from API, fallback to generic name
        input_name = coordinator.data.get("digital_input_names", {}).get(input_id, f"DIN{input_id}")
        self._attr_name = f"{input_name} Counter"
        self._attr_unique_id = f"{entry.entry_id}_counter_{input_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Denkovi SmartDEN ({coordinator.host})",
            manufacturer="Denkovi",
            model="SmartDEN IP-Maxi",
        )

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("counters", {}).get(self._input_id)


class DenkoviAnalogSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Denkovi SmartDEN analog input sensor."""

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        input_id: int,
        is_temperature: bool = False,
    ) -> None:
        """Initialize the analog sensor."""
        super().__init__(coordinator)
        self._input_id = input_id
        self._is_temperature = is_temperature
        # Use name from API, fallback to generic name
        input_name = coordinator.data.get("analog_input_names", {}).get(input_id, f"Analog Input {input_id}")
        self._attr_name = input_name
        self._attr_unique_id = f"{entry.entry_id}_analog_input_{input_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Denkovi SmartDEN ({coordinator.host})",
            manufacturer="Denkovi",
            model=coordinator.get_device_model(),
        )
        
        if is_temperature:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | str | None:
        """Return the state of the sensor."""
        value = self.coordinator.data.get("analog_inputs", {}).get(self._input_id)
        # Return None for invalid values like '---' when sensor expects numeric
        if self._is_temperature and isinstance(value, str) and not value.replace('.', '', 1).replace('-', '', 1).isdigit():
            return None
        return value


class DenkoviTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Denkovi SmartDEN dedicated temperature sensor (Notifier)."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: DenkoviDataUpdateCoordinator,
        entry: ConfigEntry,
        input_id: int,
    ) -> None:
        """Initialize the temperature sensor."""
        super().__init__(coordinator)
        self._input_id = input_id
        # Use name from API, fallback to generic name
        input_name = coordinator.data.get("temperature_input_names", {}).get(input_id, f"Temperature {input_id}")
        self._attr_name = input_name
        self._attr_unique_id = f"{entry.entry_id}_temperature_{input_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Denkovi SmartDEN ({coordinator.host})",
            manufacturer="Denkovi",
            model=coordinator.get_device_model(),
        )

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("temperature_inputs", {}).get(self._input_id)
