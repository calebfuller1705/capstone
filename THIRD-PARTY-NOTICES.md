# Third-Party Software Notices

This project (`SPDX-License-Identifier: MIT`) incorporates third-party open-source Python packages installed in `.venv` (`requirements.lock` plus audit/test tooling). All 59 dependencies use permissive or weak file-level copyleft licenses compatible with outbound MIT distribution; none carry strong copyleft (`GPL`/`AGPL`) obligations.

## Summary of Obligation Categories
- **Weak File-Level Copyleft (`MPL-2.0`) ? 1 package (`certifi`):** If `certifi` files themselves are modified and distributed, those modified files must remain under MPL-2.0; unmodified use as a library requires only notice retention.
- **Attribution & NOTICE Retention (`Apache-2.0`) ? 12 packages:** Requires retaining copyright/license text, preserving any upstream `NOTICE` file, and marking modified files.
- **Notice Retention & Non-Endorsement (`BSD-3-Clause`, `BSD-2-Clause`, `PSF-2.0`) ? 14 packages:** Requires preserving copyright notices and disclaimers in source/binary distributions (`BSD-3-Clause` also bars using upstream contributor names to endorse derived products).
- **Standard Notice Retention (`MIT`) ? 32 packages:** Requires including the upstream copyright and permission notice in copies or substantial portions.

## Complete Dependency License & Obligation Inventory

| Package | Version | SPDX License | Obligation Flag | Required Compliance Action |
|---|---|---|---|---|
| `annotated-doc` | `0.0.5` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `annotated-types` | `0.8.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `anyio` | `4.15.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `boolean.py` | `5.0` | `BSD-2-Clause` | FLAG ? Notice Retention | Retain copyright notice, conditions, and disclaimer in source and binary redistributions. |
| `CacheControl` | `0.14.4` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `certifi` | `2026.10.23` | `MPL-2.0` | FLAG ? Weak Copyleft + Notice | File-level copyleft: any modifications to MPL-2.0 source files must remain under MPL-2.0; retain license notice and provide source access if redistributed. |
| `charset-normalizer` | `3.5.2` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `click` | `8.5.0` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `colorama` | `0.4.6` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `cyclonedx-python-lib` | `11.12.0` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `defusedxml` | `0.7.1` | `PSF-2.0` | FLAG ? Notice + Change Summary | Retain PSF copyright/license notice and summarize any modifications if redistributed. |
| `Deprecated` | `3.0.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `fastapi` | `0.143.2` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `filelock` | `4.2.9` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `flake8` | `7.4.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `h11` | `0.16.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `httpcore` | `1.0.9` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `httptools` | `0.9.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `httpx` | `0.28.1` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `idna` | `3.20` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `iniconfig` | `2.3.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `license-expression` | `30.4.4` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `limits` | `5.8.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `markdown-it-py` | `4.2.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `mccabe` | `0.7.0` | `MIT (Expat)` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `mdurl` | `0.1.2` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `msgpack` | `1.2.4` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `opentelemetry-api` | `1.45.1` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `packageurl-python` | `0.17.6` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `packaging` | `26.3` | `Apache-2.0 OR BSD-2-Clause` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `pip-requirements-parser` | `32.0.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pip_api` | `0.0.35` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `pip_audit` | `2.10.1` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `platformdirs` | `4.14.5` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pluggy` | `1.7.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `py-serializable` | `2.1.0` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `pycodestyle` | `2.15.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pydantic` | `2.14.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pydantic_core` | `2.50.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pyflakes` | `4.0.3` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `Pygments` | `2.21.0` | `BSD-2-Clause` | FLAG ? Notice Retention | Retain copyright notice, conditions, and disclaimer in source and binary redistributions. |
| `pyparsing` | `3.3.3` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pytest` | `9.1.1` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `pytest-asyncio` | `1.4.1.post1` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `python-dotenv` | `1.2.4` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `PyYAML` | `6.0.3` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `requests` | `2.34.2` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `rich` | `15.0.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `slowapi` | `0.1.10` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `sortedcontainers` | `2.4.0` | `Apache-2.0` | FLAG ? Attribution + NOTICE | Retain copyright, license, and any upstream NOTICE file; state significant changes if modified; includes express patent grant. |
| `starlette` | `1.8.0` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `tomli` | `2.5.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `tomli_w` | `1.2.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `typing-inspection` | `0.4.4` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `typing_extensions` | `4.16.0` | `PSF-2.0` | FLAG ? Notice + Change Summary | Retain PSF copyright/license notice and summarize any modifications if redistributed. |
| `urllib3` | `2.8.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `uvicorn` | `0.54.0` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `watchfiles` | `1.3.0` | `MIT` | Permissive ? Notice Retention | Retain copyright and MIT permission notice in copies or substantial portions of the software. |
| `websockets` | `17.2` | `BSD-3-Clause` | FLAG ? Notice + Non-Endorsement | Retain copyright notice, conditions, and disclaimer in source/binary redistributions; do not use author/organization names for endorsement. |
| `wrapt` | `2.5.1` | `BSD-2-Clause` | FLAG ? Notice Retention | Retain copyright notice, conditions, and disclaimer in source and binary redistributions. |
