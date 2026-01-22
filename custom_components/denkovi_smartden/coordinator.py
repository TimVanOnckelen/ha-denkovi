"""Data update coordinator for Denkovi SmartDEN."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class DenkoviDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Denkovi SmartDEN data."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        password: str,
        scan_interval: int,
    ) -> None:
        """Initialize."""
        self.host = host
        self.port = port
        self.password = password
        
        # Create persistent session with connection pooling
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
        )
        self._session = aiohttp.ClientSession(connector=connector)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Denkovi SmartDEN."""
        url = f"http://{self.host}:{self.port}/current_state.json?pw={self.password}"

        try:
            async with self._session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error fetching data: HTTP {response.status}")

                json_data = await response.json()
                return self._parse_json(json_data)

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    def _parse_json(self, json_data: dict[str, Any]) -> dict[str, Any]:
        """Parse JSON response from device."""
        try:
            current_state = json_data.get("CurrentState", {})
            
            # Parse relays with names
            relays = {}
            relay_names = {}
            for idx, relay in enumerate(current_state.get("Relay", [])):
                relay_id = idx + 1
                relay_value = relay.get("Value")
                # Values come as strings '0' or '1'
                relays[relay_id] = str(relay_value) == '1'
                relay_names[relay_id] = relay.get("Name", f"Relay {relay_id}")
            
            # Parse digital inputs with names
            digital_inputs = {}
            digital_input_names = {}
            counters = {}
            for idx, digital_input in enumerate(current_state.get("DigitalInput", [])):
                input_id = idx + 1
                # Values come as strings '0' or '1'
                digital_inputs[input_id] = str(digital_input.get("Value")) == '1'
                counters[input_id] = int(digital_input.get("Count", 0))
                digital_input_names[input_id] = digital_input.get("Name", f"DIN{input_id}")
            
            # Parse analog inputs with names
            analog_inputs = {}
            analog_input_names = {}
            for idx, analog_input in enumerate(current_state.get("AnalogInput", [])):
                input_id = idx + 1
                measure = analog_input.get("Measure", "")
                analog_input_names[input_id] = analog_input.get("Name", f"AIN{input_id}")
                # Parse temperature values if present (e.g., "23.5 C")
                if isinstance(measure, str) and " " in measure:
                    value = measure.split(" ")[0]
                    try:
                        analog_inputs[input_id] = float(value)
                    except ValueError:
                        analog_inputs[input_id] = measure
                else:
                    analog_inputs[input_id] = measure
            
            # Parse analog outputs with names
            analog_outputs = {}
            analog_output_names = {}
            for idx, analog_output in enumerate(current_state.get("AnalogOutput", [])):
                output_id = idx + 1
                analog_outputs[output_id] = analog_output.get("Value", 0)
                analog_output_names[output_id] = analog_output.get("Name", f"AOUT{output_id}")
            
            # Parse device info
            device_info = current_state.get("Device", {})

            return {
                "relays": relays,
                "relay_names": relay_names,
                "digital_inputs": digital_inputs,
                "digital_input_names": digital_input_names,
                "counters": counters,
                "analog_inputs": analog_inputs,
                "analog_input_names": analog_input_names,
                "analog_outputs": analog_outputs,
                "analog_output_names": analog_output_names,
                "device": device_info,
            }

        except (KeyError, ValueError) as err:
            _LOGGER.error("Error parsing JSON: %s", err)
            return {
                "relays": {},
                "relay_names": {},
                "digital_inputs": {},
                "digital_input_names": {},
                "counters": {},
                "analog_inputs": {},
                "analog_input_names": {},
                "analog_outputs": {},
                "analog_output_names": {},
                "device": {},
            }

    async def async_set_relay(self, relay_id: int, state: bool) -> None:
        """Set relay state."""
        # Optimistic update - set state immediately
        current_data = dict(self.data)
        current_data["relays"][relay_id] = state
        self.async_set_updated_data(current_data)

        # Denkovi uses 1 for ON, 0 for OFF
        state_value = 1 if state else 0
        url = f"http://{self.host}:{self.port}/current_state.json?pw={self.password}&Relay{relay_id}={state_value}"

        try:
            async with self._session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error setting relay: HTTP {response.status}")
                
                # Parse response to confirm state
                json_data = await response.json()
                self.async_set_updated_data(self._parse_json(json_data))

        except aiohttp.ClientError as err:
            # Roll back on error - request refresh to get actual state
            await self.async_request_refresh()
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    async def async_set_analog_output(self, output_id: int, value: int) -> None:
        """Set analog output value."""
        # Optimistic update - set value immediately
        current_data = dict(self.data)
        current_data["analog_outputs"][output_id] = value
        self.async_set_updated_data(current_data)

        url = f"http://{self.host}:{self.port}/current_state.json?pw={self.password}&AnalogOutput{output_id}={value}"

        try:
            async with self._session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error setting analog output: HTTP {response.status}")
                
                # Parse response to confirm value
                json_data = await response.json()
                self.async_set_updated_data(self._parse_json(json_data))

        except aiohttp.ClientError as err:
            # Roll back on error - request refresh to get actual state
            await self.async_request_refresh()
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    async def async_shutdown(self) -> None:
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()
