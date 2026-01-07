# Changelog

All notable changes to the Gemonade framework will be documented in this file.

## [v4.2.6] - 2026-01-06 (The Memory Simplification Update)
### Removed
- **`recall.py` Command:** Removed the automated "Advanced Memory" tool and its associated command logic.
- **Recall Roadmap:** Removed plans for a dedicated recall CLI command in favor of standard manual investigation tools (`list_directory`, `read_file`).

## [v4.2.5] - 2026-01-05 (The Hygienic Installer Update)
### Fixed
- Fixed `gemonade install` to correctly strip `.git` directories when cloning from remote URLs, ensuring installed gems are treated as static packages.
- Fixed syntax errors (missing quotes) in `bin/gemonade` logging.

### Ecosystem
- Standardized `anki-forge` to v0.3.0 with Blueprint architecture and Smart Packing.
- Updated V4 Roadmap to include plans for "Graceful Uninstall" (data preservation).

## [v4.2.4] - 2026-01-05 (The Polished Notifier Update)
### Fixed
- Fixed `bin/gemonade` to automatically clear the update notification flag when the local repository is up-to-date.

## [v4.2.3] - 2026-01-03 (The Attribution Update)
### Added
- Added `generator` field to `gem.json` to track system-created gems.
- Retrofitted `homelabinator` and `innspect` with `gemonade-sys` attribution.
### Changed
- Automated GitHub metadata synchronization (description and topics) in `tools/publish.py`.
- Enforced Versioning protocol in `sys` persona maintenance workflow.

## [v4.2.2] - 2026-01-03 (The Lifecycle Update)
### Added
- Formalized "Gem Lifecycle Engineering" in the `sys` persona.
- Added "The Integrity Check" maintenance protocol to ensure existing Gems are upgraded to current standards.
### Changed
- Enforced `tools/` directory standard for all executable scripts.
- Mandated `.gitignore` in Gem scaffolds to prevent environment pollution.

## [v4.2.1] - 2026-01-03 (The Standardizer Update)
### Added
- Added "Explicit Confirmation Barrier" to safety protocols to prevent execution on ambiguous or conceptual agreement.

## [v4.2.0] - 2026-01-03 (The Memory Control Update)
### Changed
- Optimized session ingestion and context management logic.
- Established versioning for the `bin/gemonade` launcher.

## [v4.1.0] - 2026-01-02 (The Advanced Recall Update)
### Added
- Integrated semantic search functionality via `tools/recall.py`.
- Added long-term memory ingestion for cross-session knowledge retrieval.

## [v3.1.0] - 2026-01-02 (The Operational Integrity Update)
### Added
- **Context Preservation Protocol:** Strictly forbidding summarization/elision of technical data.
- **Rationale-First Communication:** Requiring plans and reasoning before state-changing commands.
- **Advisory Protocol:** Added proactive guidance for Gem graduation (Pilot vs. Skill rubric).

## [v3.0.0] - 2026-01-02 (The Ecosystem Release)
### Added
- **Discovery:** Implemented `gemonade search` to query GitHub for `gemonade-gem` tagged repositories.
- **Graduation:** Created `tools/gem_2_extension.py` to convert mature Gems into native Gemini CLI Extensions.
- **Publishing:** Created `tools/publish.py` for automated SemVer and Git tagging.

## [v2.0.0] - 2025-12-31 (The Gem Ecosystem)
### Added
- Initial implementation of the "Gem" concept for portable, shareable personas.

## [v1.6.0] - 2025-12-27 (The Gemonade Rebrand)
### Changed
- **Major Rebrand:** Transitioned the project from "Geode" to "Gemonade".
- Updated internal logic, configuration paths, and documentation to reflect the new identity.

## [v1.5.0] - 2025-12-26 (Unified Package Architecture)
### Changed
- Support for `local`, `installed`, and `core` namespaces.
- Unified package structure for consistent persona management.

## [v1.0.0] - 2025-12-26 (Initial Stable Release)
### Added
- Persona-driven CLI wrapper for the Gemini CLI.
- Session logging and context management.
- Objective-based persona summaries (`geode list`).