# is-healthy
Mini healthcheck CLI

![Python package](https://github.com/carlskeide/is-healthy/workflows/Python%20package/badge.svg)

## Installation
Recommended: `pip install is-healthy`

## Usage
```
usage: is-healthy [-h] [-H HOST] [-P PORT] [-s] [-p PATH] [-t TIMEOUT] [--status] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  default: localhost
  -P PORT, --port PORT  default: 80 (443 with -s)
  -s, --ssl             default: no
  -p PATH, --path PATH  default: /health
  -t TIMEOUT, --timeout TIMEOUT
                        default: 5s
  --status              check for status: pass instead of healthy: true
  -v, --verbose         verbose output
```

Invoking the script without parameters will check http://localhost:80/health for `"healthy": true`, a common usecase for microservice containers. For services compatible with the [IETF Healthcheck RFC Draft](https://tools.ietf.org/html/draft-inadarei-api-health-check-04), invoke the CLI with `--status`.
