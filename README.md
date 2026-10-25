# toolbox

Various scripts and samples to make dev life somewhat easier

### Recipes

HOW-TOs on various subjects:

- [Catch22-no space left on device](recipes/Catch22.md)
- [How to host your own secure web site](recipes/HostYourOwnSecureWebsite.md)
- [Java on MacOS](recipes/JavaOnMacOS.md)
- [Locale warnings when connecting to Debian](recipes/LinuxLocaleWaarnings.md)
- [Mac terminals Makeover](recipes/TerminalMakeover.md)
- [Microsoft Data API Builder](recipes/DataApiBuilder.md)
- [Microsoft SQL Server on MacOS using Docker](recipes/MSSQLOnMacOSDocker.md)
- [OpenVPN server on a Raspberry Pi using Docker](recipes/OpenVPNServerOnRaspberryPi.md)
- [Port 5000 is in use on MacOS](recipes/Port5000IsInUseOnMacOS.md)
- [Python's `tkint` on a Silicon Mac](recipes/PythonTKinterOnMacM2.md)
- [Run Python script as a service](recipes/RunPythonScriptAsAService.md)
- [Virtual Machines on MacOS](recipes/VirtualMachinesOnMacOS.md)
- [X11 on MacOS](recipes/X11OnMacOS.md)
- [Yarn on MacOS](recipes/YarnOnMacOS.md)

### bash

Scripts and functions

## gist

Scripts and configuration settings

## python

Scripts and configuration settings

## Oracle

Scripts and HOW-TOs

### Postman

Collection of scripts, utilities and workspaces.

## Checks

There is no shared build here, so every language is checked on its own by
[`.github/workflows/checks.yml`](.github/workflows/checks.yml), on every push
and pull request:

| Check | Tool | Settings |
| --- | --- | --- |
| shell scripts and snippets | `shellcheck --severity=warning` | [`.shellcheckrc`](.shellcheckrc) |
| Python | `ruff check` | [`ruff.toml`](ruff.toml) |
| JavaScript | `eslint` | [`eslint.config.mjs`](eslint.config.mjs) |
| secrets, tree and history | `gitleaks` | defaults |
| Python dependencies | `pip-audit` | `dab/requirements.txt`, `tests/requirements.txt` |

To run them before pushing:

```shell
shellcheck --severity=warning --shell=bash bash/* python/* **/*.sh
pip install ruff pip-audit && ruff check . && pip-audit -r dab/requirements.txt
npx --yes eslint .
gitleaks dir . && gitleaks git .
pip install -r tests/requirements.txt && pytest tests
```

`tests/` holds no tests of the scripts themselves; it checks that the workflow
keeps doing the above.
