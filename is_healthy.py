#!/bin/env python3
import sys
import logging
import argparse
import json
from typing import Union

import requests
from requests.exceptions import ConnectionError, ReadTimeout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger('is_healthy')

__all__ = [
    "parse_healthy",
    "parse_status",
    "check_health"
]

CLI_ARGS = argparse.ArgumentParser()
CLI_ARGS.add_argument(
    '-H', '--host', default='localhost', help='default: localhost')
CLI_ARGS.add_argument(
    '-P', '--port', default=None, help='default: 80 (443 with -s)')
CLI_ARGS.add_argument(
    '-s', '--ssl', action='store_true', help='default: no')
CLI_ARGS.add_argument(
    '-p', '--path', default="/health", help='default: /health')
CLI_ARGS.add_argument(
    '-t', '--timeout', default="5.0", help='default: 5s')
CLI_ARGS.add_argument(
    '--status', action='store_true',
    help='check for status: pass instead of healthy: true')
CLI_ARGS.add_argument(
    '-v', '--verbose', action='store_true', help='verbose output')


def parse_healthy(data: dict) -> bool:
    """
    Health Parser for endpoints that report "healthy": True

    None or missing will be considered unhealthy
    """

    return str(data.get('healthy', False)).lower() == "true"


def parse_status(data: dict) -> bool:
    """
    Health Parser for endpoints that report status: pass
    warn or fail are both considered unhealthy

    See also: https://tools.ietf.org/html/draft-inadarei-api-health-check-04
    """

    return str(data.get('status', '')).lower() in ("pass", "ok", "up")


def check_health(
    url: str,
    timeout: float = 5.0,
    parser: Union[parse_status, parse_healthy] = parse_healthy
) -> bool:
    """ Check whether a given HTTP(S) endpoint is healthy """

    try:
        logger.debug('Checking URL: %s', url)
        response = requests.get(url, timeout=timeout).text

        logger.debug("Got response: %r", response)
        data = json.loads(response)

        is_healthy = parser(data)
        logger.info('Healthy: %s', is_healthy)
        return is_healthy

    except ConnectionError:
        logger.error('Unable to connect to service')

    except ReadTimeout:
        logger.error('Health check timed out')

    except Exception:
        logger.exception('Health check failed!')

    return False


def cli() -> None:
    args = CLI_ARGS.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    url = "{proto}://{host}:{port}/{path}".format(
        proto="https" if args.ssl else "http",
        port=args.port or (443 if args.ssl else 80),
        host=args.host,
        path=args.path.lstrip('/')
    )

    is_healthy = check_health(
        url=url,
        timeout=float(args.timeout),
        parser=(parse_status if args.status else parse_healthy)
    )

    sys.exit(0 if is_healthy else 1)
