"""
Data models for the voting application.

This module contains the data models used to represent votes and voters.
"""
from dataclasses import dataclass
from typing import Dict, Set
import re
from datetime import datetime
from config import ID_PATTERN, ID_MIN_LENGTH, ID_MAX_LENGTH

class InvalidIDError(Exception):
    """Raised when voter ID is invalid."""
    pass

@dataclass
class Vote:
    """
    Represents a single vote.

    Attributes:
        voter_id (str): The ID of the voter
        candidate (str): The name of the voted candidate
        timestamp (datetime): When the vote was cast
    """
    voter_id: str
    candidate: str
    timestamp: datetime

class VoteTracker:
    """
    Tracks votes and prevents duplicate voting.
    """
    def __init__(self) -> None:
        """Initialize the vote tracker."""
        self._votes: Dict[str, int] = {}  # candidate -> vote count
        self._voters: Set[str] = set()    # set of voter IDs

    def add_vote(self, voter_id: str, candidate: str) -> None:
        """
        Add a vote for a candidate from a specific voter.

        Args:
            voter_id: The ID of the voter
            candidate: The name of the candidate

        Raises:
            InvalidIDError: If the voter ID is invalid
            ValueError: If the voter has already voted
        """
        self._validate_voter_id(voter_id)

        if voter_id in self._voters:
            raise ValueError("This ID has already voted")

        self._voters.add(voter_id)
        self._votes[candidate] = self._votes.get(candidate, 0) + 1

    def has_voted(self, voter_id: str) -> bool:
        """
        Check if a voter has already voted.

        Args:
            voter_id: The ID to check

        Returns:
            True if the voter has already voted, False otherwise
        """
        return voter_id in self._voters

    def get_votes(self) -> Dict[str, int]:
        """
        Get current vote counts.

        Returns:
            Dictionary mapping candidates to their vote counts
        """
        return self._votes.copy()

    @staticmethod
    def _validate_voter_id(voter_id: str) -> None:
        """
        Validate the format of a voter ID.

        Args:
            voter_id: The ID to validate

        Raises:
            InvalidIDError: If the ID is invalid
        """
        if not ID_MIN_LENGTH <= len(voter_id) <= ID_MAX_LENGTH:
            raise InvalidIDError(
                f"ID must be between {ID_MIN_LENGTH} and {ID_MAX_LENGTH} characters"
            )

        if not re.match(ID_PATTERN, voter_id):
            raise InvalidIDError("ID must contain only letters and numbers")