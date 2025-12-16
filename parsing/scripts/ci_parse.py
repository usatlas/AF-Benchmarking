#!/usr/bin/env python3
"""
Parse benchmark logs and generate JSON payload for upload to LogStash/Kibana.
"""

import argparse
import json
import sys
from pathlib import Path

import jsonschema
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# Add parent directory to path to import parsing modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from handlers import (
    rucio_parser,
    coffea_parser,
    fastframes_parser,
    truth3_parser,
    evnt_parser,
)

# Initialize rich console
console = Console()

# Load JSON schema for validation
SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "payload.schema.json"
with SCHEMA_PATH.open() as f:
    PAYLOAD_SCHEMA = json.load(f)


def validate_payload(data):
    """
    Validate payload data against JSON schema.

    Args:
        data: Dictionary to validate

    Raises:
        jsonschema.ValidationError: If data doesn't match schema
    """
    jsonschema.validate(instance=data, schema=PAYLOAD_SCHEMA)


def parse_log(log_file, log_type, job, cluster, token, kind, host):
    """
    Parse log file and return data dictionary.

    Args:
        log_file: Path to log file
        log_type: Type of parser to use (rucio, athena, coffea, eventloop, fastframes)
        job: Job name
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
    elif log_type == "evnt":
        data = evnt_parser.parse_evnt_log(log_path)
    elif log_type == "truth3":
        data = truth3_parser.parse_truth3_log(log_path)
    elif log_type == "coffea":
        data = coffea_parser.parse_coffea_log(log_path)
    elif log_type == "eventloop":
        # Placeholder for eventloop parser
        # TODO: Implement eventloop log parsing
        data = {
            "submitTime": 0,
            "queueTime": 0,
            "runTime": 0,
            "payloadSize": 0,
            "status": 0,
        }
    elif log_type == "fastframes":
        data = fastframes_parser.parse_fastframes_log(log_path)
    else:
        raise ValueError(f"Unknown log type: {log_type}")

    # Add common fields to all parsed data
    data["job"] = job
    data["cluster"] = cluster
    data["token"] = token
    data["kind"] = kind
    data["host"] = host

    return data


def main():
    parser = argparse.ArgumentParser(
        description="Parse benchmark logs and generate JSON payload"
    )
    parser.add_argument("--job", required=True, help="Job name")
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
        console.print(f"[bold cyan]Parsing log file:[/bold cyan] {args.log_file}")
        console.print(f"[bold cyan]Log type:[/bold cyan] {args.log_type}")
        console.print(f"[bold cyan]Job:[/bold cyan] {args.job}")

        data = parse_log(
            args.log_file,
            args.log_type,
            args.job,
            args.cluster,
            args.token,
            args.kind,
            args.host,
        )

        # Validate payload against schema
        try:
            validate_payload(data)
            console.print("✓ [bold green]Payload validation successful[/bold green]")
        except jsonschema.ValidationError as e:
            console.print(
                Panel(
                    f"[bold red]Validation failed:[/bold red] {e.message}\n"
                    f"[bold red]Failed at:[/bold red] {' -> '.join(str(p) for p in e.path)}",
                    title="[bold white on red] ERROR [/bold white on red]",
                    border_style="red",
                ),
                style="bold red",
            )
            return 1

        # Write to output file
        output_path = Path(args.output)
        with output_path.open("w") as f:
            json.dump(data, f, indent=2)

        console.print(
            f"✓ [bold green]Successfully generated payload:[/bold green] {args.output}"
        )

        # Display payload with syntax highlighting
        json_str = json.dumps(data, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(Panel(syntax, title="[bold cyan]Payload Data[/bold cyan]"))

        return 0

    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Error parsing log file:[/bold red] {e}",
                title="[bold white on red] ERROR [/bold white on red]",
                border_style="red",
            ),
            style="bold red",
        )
        import traceback

        console.print("[dim]Traceback:[/dim]")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
