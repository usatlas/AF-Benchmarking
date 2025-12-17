"""Test suite for benchmark log parsers.

This module tests all parsers against example logs to ensure
they correctly extract timing and status information. These tests
serve as a regression suite when refactoring parser code.
"""

from pathlib import Path

# Import all parsers
from parsing.handlers.truth3_parser import parse_truth3_log
from parsing.handlers.evnt_parser import parse_evnt_log
from parsing.handlers.rucio_parser import parse_rucio_log
from parsing.handlers.coffea_parser import parse_coffea_log
from parsing.handlers.fastframes_parser import parse_fastframes_log

# Path to example logs directory
EXAMPLE_LOGS = Path(__file__).parent.parent / "example-logs"


class TestTruth3Parser:
    """Tests for TRUTH3 derivation log parser."""

    def test_parse_truth3_example_log(self):
        """Test parsing of example TRUTH3 derivation log."""
        log_file = EXAMPLE_LOGS / "log.Derivation"
        result = parse_truth3_log(log_file)

        # Validate actual values from example log (not just key existence)
        # These expected values come from running parser on example log
        # Timestamps are in UTC (logs are from UTC timezone systems)
        assert result["submitTime"] == 1765216819000, "Submit time mismatch"
        assert result["queueTime"] == 0, "Queue time should be 0"
        assert result["runTime"] == 48, "Runtime should be 48 seconds"
        assert result["status"] == 0, "Status should be 0 (success)"


class TestEvntParser:
    """Tests for EVNT generation log parser."""

    def test_parse_evnt_example_log(self):
        """Test parsing of example EVNT generation log."""
        log_file = EXAMPLE_LOGS / "log.generate"
        result = parse_evnt_log(log_file)

        # Validate actual values to catch calculation regressions
        # Timestamps are in UTC (logs are from UTC timezone systems)
        assert result["submitTime"] == 1765216848000, "Submit time mismatch"
        assert result["queueTime"] == 0, "Queue time should be 0"
        assert result["runTime"] == 2418, "Runtime should be 2418 seconds"
        assert result["status"] == 0, "Status should be 0 (success)"


class TestRucioParser:
    """Tests for Rucio data download log parser."""

    def test_parse_rucio_example_log(self):
        """Test parsing of example Rucio download log."""
        log_file = EXAMPLE_LOGS / "rucio.log"
        result = parse_rucio_log(log_file)

        # Check actual parsed values
        # Timestamps are in UTC (logs are from UTC timezone systems)
        assert result["submitTime"] == 1765216822000, "Submit time mismatch"
        assert result["queueTime"] == 0, "Queue time should be 0"
        assert result["runTime"] == 31, "Runtime should be 31 seconds"
        assert result["status"] == 0, "Status should be 0 (success)"


class TestFastFramesParser:
    """Tests for FastFrames analysis log parser."""

    def test_parse_fastframes_example_log(self):
        """Test parsing of example FastFrames log."""
        log_file = EXAMPLE_LOGS / "ff.log"
        result = parse_fastframes_log(log_file)

        # Check actual parsed values including frequency
        # Timestamps are in UTC (logs are from UTC timezone systems)
        assert result["submitTime"] == 1765217167000, "Submit time mismatch"
        assert result["queueTime"] == 0, "Queue time should be 0"
        assert result["runTime"] == 345, "Runtime should be 345 seconds"
        assert result["frequency"] == 53, "Frequency should be 53"
        assert result["status"] == 0, "Status should be 0 (success)"


class TestCoffeaParser:
    """Tests for Coffea analysis log parser."""

    def test_parse_coffea_example_log(self):
        """Test parsing of example Coffea log."""
        log_file = EXAMPLE_LOGS / "coffea_hist.log"
        result = parse_coffea_log(log_file)

        # Check actual parsed values including frequency
        # Timestamps are in UTC (parsed from ISO 8601 format with Z suffix)
        assert result["submitTime"] == 1765932487953, "Submit time mismatch"
        assert result["queueTime"] == 0, "Queue time should be 0"
        assert result["runTime"] == 205, "Runtime should be 205 seconds"
        assert result["frequency"] == 89, "Frequency should be 89 kHz"
        assert result["status"] == 0, "Status should be 0 (success)"
