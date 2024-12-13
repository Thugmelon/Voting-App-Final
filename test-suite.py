"""
Putting the unit tests in here.

I still mess these up occasionally and got bad grades on the unit tests in almost every lab so
Hopefully these count but I'm not sure.
I added notes for every test.
"""
import unittest
from unittest.mock import patch, mock_open
import tempfile
from pathlib import Path
from datetime import datetime

from models import VoteTracker, InvalidIDError
from logic import VoteManager
from config import CANDIDATES

class TestVoteTracker(unittest.TestCase):
    """Test cases for the VoteTracker class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tracker = VoteTracker()
        self.valid_id = "ABC123"
        self.valid_candidate = CANDIDATES[0]

    def test_valid_vote(self):
        """Test that a valid vote is accepted."""
        self.tracker.add_vote(self.valid_id, self.valid_candidate)
        self.assertTrue(self.tracker.has_voted(self.valid_id))
        self.assertEqual(self.tracker.get_votes()[self.valid_candidate], 1)

    def test_invalid_id_too_short(self):
        """Test that an ID that's too short is rejected."""
        with self.assertRaises(InvalidIDError):
            self.tracker.add_vote("A1", self.valid_candidate)

    def test_invalid_id_too_long(self):
        """Test that an ID that's too long is rejected."""
        with self.assertRaises(InvalidIDError):
            self.tracker.add_vote("A" * 11, self.valid_candidate)

    def test_invalid_id_special_chars(self):
        """Test that an ID with special characters is rejected."""
        with self.assertRaises(InvalidIDError):
            self.tracker.add_vote("ABC@123", self.valid_candidate)

    def test_duplicate_vote(self):
        """Test that duplicate votes are rejected."""
        self.tracker.add_vote(self.valid_id, self.valid_candidate)
        with self.assertRaises(ValueError):
            self.tracker.add_vote(self.valid_id, self.valid_candidate)

    def test_get_votes(self):
        """Test that vote counts are correctly tracked."""
        # Add votes for different candidates
        self.tracker.add_vote("ABC123", CANDIDATES[0])
        self.tracker.add_vote("DEF456", CANDIDATES[1])
        self.tracker.add_vote("GHI789", CANDIDATES[0])
        
        votes = self.tracker.get_votes()
        self.assertEqual(votes[CANDIDATES[0]], 2)
        self.assertEqual(votes[CANDIDATES[1]], 1)

class TestVoteManager(unittest.TestCase):
    """Test cases for the VoteManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.votes_file = Path(self.temp_dir.name) / "votes.csv"
        self.voters_file = Path(self.temp_dir.name) / "voters.csv"
        
        # Patch the file paths
        self.file_patcher = patch('logic.VOTES_FILE', self.votes_file)
        self.voter_patcher = patch('logic.VOTERS_FILE', self.voters_file)
        self.file_patcher.start()
        self.voter_patcher.start()
        
        self.manager = VoteManager()

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        self.file_patcher.stop()
        self.voter_patcher.stop()
        self.temp_dir.cleanup()

    def test_cast_vote(self):
        """Test that votes are properly cast and saved."""
        voter_id = "TEST123"
        candidate = CANDIDATES[0]
        
        # Cast a vote
        self.manager.cast_vote(voter_id, candidate)
        
        # Verify vote was recorded
        self.assertTrue(self.manager.has_voted(voter_id))
        votes = self.manager.get_votes()
        self.assertEqual(votes[candidate], 1)

    def test_invalid_candidate(self):
        """Test that votes for invalid candidates are rejected."""
        with self.assertRaises(KeyError):
            self.manager.cast_vote("TEST123", "Invalid Candidate")

    def test_load_existing_votes(self):
        """Test that existing votes are properly loaded."""
        # Create test data
        voter_id = "TEST123"
        candidate = CANDIDATES[0]
        
        # Cast a vote
        self.manager.cast_vote(voter_id, candidate)
        
        # Create new manager instance (should load existing votes)
        new_manager = VoteManager()
        
        # Verify votes were loaded
        self.assertTrue(new_manager.has_voted(voter_id))
        self.assertEqual(new_manager.get_votes()[candidate], 1)

if __name__ == '__main__':
    unittest.main()