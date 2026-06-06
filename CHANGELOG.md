# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `SocksConfig` class
- `is_socks` function
### Changed
- `README.md` updated
## [0.2] - 2026-06-04
### Added
- `VMESSConfig` class
- `VLESSConfig` class
- `TrojanConfig` class
- `ShadowsocksConfig` class
- `V2kitError` class
- `V2kitValidationError` class
- `V2kitParseError` class
- `parse` function
### Changed
- `README.md` updated
- Test system modified
- `is_vmess` function `config` parameter renamed to `uri`
- `is_vless` function `config` parameter renamed to `uri`
- `is_trojan` function `config` parameter renamed to `uri`
- `is_shadowsocks` function `config` parameter renamed to `uri`
- `encode_subscription` function `configs` parameter renamed to `entries`
## [0.1] - 2026-05-16
### Added
- `is_vmess` function
- `is_vless` function
- `is_trojan` function
- `is_shadowsocks` function
- `relabel` function
- `encode_subscription` function
- `decode_subscription` function

[Unreleased]: https://github.com/sepandhaghighi/v2kit/compare/v0.2...dev
[0.2]: https://github.com/sepandhaghighi/v2kit/compare/v0.1...v0.2
[0.1]: https://github.com/sepandhaghighi/v2kit/compare/bb5a2cb...v0.1



