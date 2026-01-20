# Denkovi SmartDEN Integration

Control your Denkovi SmartDEN relay boards directly from Home Assistant!

## Features

- 🔌 **Full Device Support**: Control up to 8 relays, monitor 8 digital inputs, 8 analog inputs, and temperature sensors
- 🏠 **Device Grouping**: All entities grouped under a single device for clean organization
- 💡 **Flexible Entity Types**: Configure relays as switches or lights
- 🏷️ **Custom Labels**: Automatically uses device-configured names for entities
- 🔄 **Real-time Updates**: Local polling for instant state updates (10-second interval)
- 🔐 **Secure**: Password authentication support
- ⚙️ **Easy Configuration**: Simple UI-based setup through Home Assistant

## Supported Devices

- Denkovi SmartDEN IP-Maxi
- Other Denkovi SmartDEN devices using the JSON HTTP API

## Quick Setup

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "Denkovi SmartDEN"
3. Enter your device IP address, port (default: 80), and password (default: admin)
4. Click Submit and you're done!

## Configuration Options

After setup, you can configure which relays should appear as lights instead of switches:

1. Go to **Settings** → **Devices & Services**
2. Find your Denkovi SmartDEN integration
3. Click **CONFIGURE**
4. Select which relays should appear as lights
5. Click **Submit**

## Entity Types

The integration creates:

- **Switches**: Control relays as on/off switches
- **Lights**: Control relays as light entities (configurable)
- **Binary Sensors**: Monitor digital input states
- **Sensors**: Pulse counters, analog values, and temperature readings

All entities use custom labels from your device configuration!

## Support

For issues, feature requests, or questions:

- [GitHub Issues](https://github.com/timvanonckelen/ha-denkovi/issues)
- [Documentation](https://github.com/timvanonckelen/ha-denkovi)
