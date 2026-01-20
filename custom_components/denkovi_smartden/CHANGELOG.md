# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-20

### Added
- Initial release
- Support for Denkovi SmartDEN IP-Maxi devices
- Control up to 8 relays via switches or lights
- Monitor 8 digital inputs with binary sensors
- Track pulse counters for each digital input
- Monitor 8 analog inputs (4 voltage, 4 temperature)
- Device grouping - all entities organized under single device
- Custom label support from device configuration
- Options flow to configure relays as lights or switches
- Password authentication support
- Configurable HTTP port
- Real-time polling (10-second interval)
- JSON HTTP API integration
- UI-based configuration flow
- Integration icon

### Features
- Automatic entity naming from device labels
- Device info with manufacturer, model, and uptime
- Temperature sensors with proper device class
- Counter sensors with state class for statistics
- Device actions for automations
- Reload on options change

[1.0.0]: https://github.com/timvanonckelen/ha-denkovi/releases/tag/v1.0.0
