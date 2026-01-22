# Home Assistant Denkovi SmartDEN Integration

[![GitHub Release](https://img.shields.io/github/release/timvanonckelen/ha-denkovi.svg?style=flat-square)](https://github.com/timvanonckelen/ha-denkovi/releases)
[![License](https://img.shields.io/github/license/timvanonckelen/ha-denkovi.svg?style=flat-square)](LICENSE)

A custom Home Assistant integration for controlling Denkovi SmartDEN relay boards with full support for relays, digital inputs, analog inputs, and temperature sensors.

## Features

- 🔌 **Full Device Support**: Control up to 8 relays and 8 analog outputs, monitor 8 digital inputs, 8 analog inputs, and temperature sensors
- 🏠 **Device Grouping**: All entities grouped under a single device for clean organization
- 💡 **Flexible Entity Types**: Configure relays as switches or lights
- 🎚️ **Analog Output Control**: Slider controls for analog outputs (0-1023 range)
- 🏷️ **Custom Labels**: Automatically uses device-configured names for entities
- ⚡ **Instant Feedback**: Optimized state updates with no polling delay
- 🔐 **Secure**: Password authentication support
- ⚙️ **Easy Configuration**: Simple UI-based setup through Home Assistant

## Supported Devices

- Denkovi SmartDEN IP-Maxi
- Other Denkovi SmartDEN devices using the JSON HTTP API

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/timvanonckelen/ha-denkovi`
6. Select category: "Integration"
7. Click "Add"
8. Find "Denkovi SmartDEN" in HACS and click "Download"
9. Restart Home Assistant
10. Go to **Settings** → **Devices & Services** → **Add Integration**
11. Search for "Denkovi SmartDEN"

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/timvanonckelen/ha-denkovi/releases)
2. Copy the `custom_components/denkovi_smartden` directory to your Home Assistant's `config/custom_components` directory
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "Denkovi SmartDEN" and follow the setup wizard

## Configuration

### Initial Setup

1. Navigate to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "Denkovi SmartDEN"
4. Enter your device details:
   - **Host**: IP address or hostname of your device
   - **Port**: HTTP port (default: 80)
   - **Password**: Device password (default: admin)

### Configuring Relays as Lights

1. Go to **Settings** → **Devices & Services**
2. Find your Denkovi SmartDEN integration
3. Click **CONFIGURE**
4. Select which relays should appear as lights instead of switches
5. Click **Submit** (integration will reload automatically)

## Entity Types

The integration creates the following entities:

| Entity Type          | Description                                          | Count        |
| -------------------- | ---------------------------------------------------- | ------------ |
| Switch               | Relay switches (excludes those configured as lights) | Up to 8      |
| Light                | Relays configured as lights                          | Configurable |
| Number               | Analog output controls (0-1023 slider)               | Up to 8      |
| Binary Sensor        | Digital input states                                 | Up to 8      |
| Sensor (Counter)     | Pulse counters for digital inputs                    | Up to 8      |
| Sensor (Analog)      | Analog input values                                  | Up to 4      |
| Sensor (Temperature) | Temperature sensor readings                          | Up to 4      |

All entities are automatically grouped under a single device for easy management.

## Custom Labels

The integration automatically uses the custom labels you've configured on your Denkovi device. For example:

- If you name Relay 5 as "Kitchen Light" on the device, it will appear as "Kitchen Light" in Home Assistant
- Change labels on the device web interface and they'll sync automatically (within 10 seconds)

## API Reference

The integration uses the Denkovi SmartDEN JSON HTTP API:

**Get Device State:**

```
http://[device-ip]:[port]/current_state.json?pw=[password]
```

**Set Relay:**

```
http://[device-ip]:[port]/current_state.json?pw=[password]&Relay[N]=[0|1]
```

**Set Analog Output:**

```
http://[device-ip]:[port]/current_state.json?pw=[password]&AnalogOutput[N]=[value]
```

Parameters:

- `[device-ip]`: Device IP address
- `[port]`: HTTP port (default: 80)
- `[password]`: Device password (default: admin)
- `[N]`: Relay/output number (1-8)
- `[0|1]`: OFF (0) or ON (1)
- `[value]`: Analog output value

## Troubleshooting

### Cannot Connect to Device

- ✓ Verify the IP address is correct
- ✓ Check the port (default: 80)
- ✓ Verify the password (default: "admin")
- ✓ Ensure device is on the same network
- ✓ Check Home Assistant logs for detailed error messages

### Entities Not Appearing

- Reload the integration: **Settings** → **Devices & Services** → **Denkovi SmartDEN** → **⋮** → **Reload**
- Check if relays are configured as lights (they won't appear as switches)
- Verify device is responding: `http://[device-ip]:[port]/current_state.json?pw=[password]`

### Debug Logging

Add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.denkovi_smartden: debug
```

## Development

### Local Testing with Docker

1. Navigate to the docker directory:

   ```bash
   cd docker
   ```

2. Start Home Assistant:

   ```bash
   docker-compose up -d
   ```

3. Access Home Assistant at http://localhost:8123

4. View logs:
   ```bash
   docker-compose logs -f
   ```

The integration is automatically loaded via volume mount. Changes to code are reflected after restarting Home Assistant.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issue Tracker](https://github.com/timvanonckelen/ha-denkovi/issues)
- **Documentation**: [GitHub Wiki](https://github.com/timvanonckelen/ha-denkovi/wiki) _(coming soon)_

## Acknowledgments

- Thanks to Denkovi for creating great relay boards
- Home Assistant community for the excellent platform
