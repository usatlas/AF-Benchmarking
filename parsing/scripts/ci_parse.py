#!/usr/bin/env python3
"""
Parse benchmark logs and generate JSON payload for upload to LogStash/Kibana.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to import parsing modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from handlers import rucio_parser


def parse_log(log_file, log_type, job_type, cluster, token, kind, host):
    """
    Parse log file and return data dictionary.

    Args:
        log_file: Path to log file
        log_type: Type of parser to use (rucio, athena, coffea, eventloop, ff)
        job_type: Job type name
        cluster: Cluster name (UC-AF, SLAC-AF, BNL-AF)
        token: Kibana token for routing
        kind: Kibana kind for routing
        host: Hostname where job executed

    Returns:
        Dictionary with benchmark data
    """
    log_path = Path(log_file)

    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    # Parse based on log type
    if log_type == "rucio":
        data = rucio_parser.parse_rucio_log(log_path)
    elif log_type == "athena":
        # Placeholder for athena parser
        # TODO: Implement athena log parsing
        data = {
            "cluster": cluster,
            "testType": f"Athena {job_type}",
            "submitTime": 0,
            "queueTime": 0,
            "runTime": 0,
            "payloadSize": 0,
            "status": 0,
            "host": host,
            "token": token,
            "kind": kind,
        }
    elif log_type == "coffea":
        # Placeholder for coffea parser
        # TODO: Implement coffea log parsing
        data = {
            "cluster": cluster,
            "testType": "Coffea Analysis",
            "submitTime": 0,
            "queueTime": 0,
            "runTime": 0,
            "payloadSize": 0,
            "status": 0,
            "host": host,
            "token": token,
            "kind": kind,
        }
    elif log_type == "eventloop":
        # Placeholder for eventloop parser
        # TODO: Implement eventloop log parsing
        data = {
            "cluster": cluster,
            "testType": f"Event Loop {job_type}",
            "submitTime": 0,
            "queueTime": 0,
            "runTime": 0,
            "payloadSize": 0,
            "status": 0,
            "host": host,
            "token": token,
            "kind": kind,
        }
    elif log_type == "ff":
        # Placeholder for fastframes parser
        # TODO: Implement fastframes log parsing
        data = {
            "cluster": cluster,
            "testType": "Fast Frames",
            "submitTime": 0,
            "queueTime": 0,
            "runTime": 0,
            "payloadSize": 0,
            "status": 0,
            "host": host,
            "token": token,
            "kind": kind,
        }
    else:
        raise ValueError(f"Unknown log type: {log_type}")

    # Override cluster, token, kind, and host from command line
    data["cluster"] = cluster
    data["token"] = token
    data["kind"] = kind
    data["host"] = host

    return data


def main():
    parser = argparse.ArgumentParser(
        description="Parse benchmark logs and generate JSON payload"
    )
    parser.add_argument("--job-type", required=True, help="Job type")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    parser.add_argument("--log-type", required=True, help="Type of log parser")
    parser.add_argument("--cluster", required=True, help="Cluster name")
    parser.add_argument("--token", required=True, help="Kibana token")
    parser.add_argument("--kind", required=True, help="Kibana kind")
    parser.add_argument("--host", required=True, help="Hostname")
    parser.add_argument(
        "--output", default="payload.json", help="Output JSON file path"
    )

    args = parser.parse_args()

    try:
        # Parse the log file
        data = parse_log(
            args.log_file,
            args.log_type,
            args.job_type,
            args.cluster,
            args.token,
            args.kind,
            args.host,
        )

        # Write to output file
        output_path = Path(args.output)
        with output_path.open("w") as f:
            json.dump(data, f, indent=2)

        print(f"Successfully generated payload: {args.output}")
        print(f"Data: {json.dumps(data, indent=2)}")

        return 0

    except Exception as e:
        print(f"Error parsing log file: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
