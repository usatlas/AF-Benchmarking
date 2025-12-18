"""EVNT generation log parser.

Parses logs from ATLAS Monte Carlo event generation jobs to extract timing information.
"""

from parsing.handlers.base_parser import parse_atlas_log


def parse_evnt_log(path):
    """Parse EVNT generation log file.

    Args:
        path: Path to log.generate file

    Returns:
        dict: Parsed timing data
    """
    return parse_atlas_log(path, log_name="EVNT")


# Registers this parsing script with the Class
def register(parser):
    parser.register_parsers("log.generate", parse_evnt_log)
