"""TRUTH3 derivation log parser.

Parses logs from ATLAS TRUTH3 derivation jobs to extract timing information.
"""

from parsing.handlers.base_parser import parse_atlas_log


def parse_truth3_log(path):
    """Parse TRUTH3 derivation log file.

    Args:
        path: Path to log.EVNTtoDAOD or log.Derivation file

    Returns:
        dict: Parsed timing data
    """
    return parse_atlas_log(path, log_name="TRUTH3")


# Registers this parsing script with the Class
def register(parser):
    parser.register_parsers("log.EVNTtoDAOD", parse_truth3_log)
