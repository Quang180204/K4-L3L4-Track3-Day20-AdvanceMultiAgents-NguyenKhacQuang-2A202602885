---
name: rigorous-output-formatting-and-schema
description: Use this skill when generating structured output files like JSON or CSV to ensure all field names, formats, units, and headers strictly match specifications.
---
- Verify all required top-level keys, metadata objects, and schema versions in output files (e.g., `schema_version`, `generated_by`, `meta`).
- Format money values in integer cents (e.g., multiply decimal amounts by 100 and round to integer) unless specified otherwise.
- Format all timestamps strictly as ISO 8601 UTC strings ending with `Z` (`YYYY-MM-DDTHH:MM:SSZ`).
- Normalize entity names (such as service names, regions, or categories) to exact canonical spellings and casing as requested by rules (e.g., replacing hyphens with underscores, title-casing).
- Sort array/list outputs by required primary and secondary keys (e.g., service then timestamp) in ascending order.