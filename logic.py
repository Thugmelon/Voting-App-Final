"""
Logic for the voting app in this python file.
Add as much functionality as possible but also work on project 2
& don't spend all the time on this.

"""
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Set, Optional
import logging
from models import VoteTracker, Vote, InvalidIDError
from config import VOTES_FILE, VOTERS_FILE, CANDIDATES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoteManager:
    # Manages the voting system (mainly vote processing)

    def __init__(self) -> None:
        """Initialize the vote manager and load existing votes."""
        self._vote_tracker = VoteTracker()
        self._load_data()

    def _load_data(self) -> None:
        # Load all the info (all the voters & their votes)
        try:
            if VOTERS_FILE.exists():
                with open(VOTERS_FILE, "r", newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        voter_id = row[0]
                        self._vote_tracker._voters.add(voter_id)

            if VOTES_FILE.exists():
                with open(VOTES_FILE, "r", newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        candidate, count = row
                        self._vote_tracker._votes[candidate] = int(count)

            # Initialize the counts for all candidates
            for candidate in CANDIDATES:
                if candidate not in self._vote_tracker._votes:
                    self._vote_tracker._votes[candidate] = 0

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Initialize with empty data
            self._vote_tracker = VoteTracker()

    def _save_data(self) -> None:
        # Save current votes and voters to files
        try:
            # Save vote counts
            with open(VOTES_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                for candidate, count in self._vote_tracker.get_votes().items():
                    writer.writerow([candidate, count])

            # Save voter IDs
            with open(VOTERS_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                for voter_id in self._vote_tracker._voters:
                    writer.writerow([voter_id])

            logger.info("Vote data saved successfully")

        except Exception as e:
            logger.error(f"Error saving vote data: {e}")
            raise

    def cast_vote(self, voter_id: str, candidate: str) -> None:
        """
        Cast a vote for a candidate.

        Args:
            voter_id: ID of the voter
            candidate: Name of the candidate

        Raises:
            InvalidIDError: If the voter ID is invalid
            ValueError: If the voter has already voted
            KeyError: If the candidate doesn't exist
        """
        if candidate not in CANDIDATES:
            raise KeyError(f"Invalid candidate: {candidate}")

        try:
            self._vote_tracker.add_vote(voter_id, candidate)
            self._save_data()
            logger.info(f"Vote cast successfully for {candidate} by {voter_id}")
        except Exception as e:
            logger.error(f"Error casting vote: {e}")
            raise

    def has_voted(self, voter_id: str) -> bool:
        """
        Check if a voter has already voted.

        Args:
            voter_id: The ID to check

        Returns:
            True if the voter has already voted, False otherwise
        """
        return self._vote_tracker.has_voted(voter_id)

    def get_votes(self) -> Dict[str, int]:
        """
        Get current vote counts.

        Returns:
            Dictionary mapping candidates to their vote counts
        """
        return self._vote_tracker.get_votes()