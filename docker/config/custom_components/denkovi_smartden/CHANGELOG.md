# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-01-22

### Added
- Full support for Denkovi SmartDEN Notifier devices
- Support for up to 16 digital inputs (Notifier)
- Support for 8 dedicated temperature sensors (Notifier)
- Automatic device type detection based on capabilities
- Dynamic platform loading - only loads relevant platforms for each device type

### Changed
- Device model now automatically detected (IP-Maxi vs Notifier)
- Improved device info display with correct model names
- Coordinator now supports both device types seamlessly

## [1.2.0] - 2026-01-22

### Added
- Configurable polling interval (5-60 seconds) in options
- Persistent session with connection pooling for improved performance
- Optimistic updates - UI responds instantly before API confirmation

### Changed
- Improved connection performance with TCP connector pooling
- Reduced network overhead by reusing HTTP sessions
- UI feedback is now instant with automatic rollback on errors

### Fixed
- Proper session cleanup on integration unload
- Memory leak from unclosed HTTP sessions

## [1.1.0] - 2026-01-22

### Added

- Number entities for analog output control (0-1023 range)
- Slider controls for each analog output with custom labels

### Changed

- Optimized state updates for instant UI feedback
- Control commands now parse API response immediately instead of waiting for next poll
- Reduced UI update delay from up to 10 seconds to network latency (~50-200ms)

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
