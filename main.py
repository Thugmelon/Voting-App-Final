"""
Main entry point for the voting application.

This module initializes and starts the voting application.
"""
import logging
from gui import VotingApp

def main() -> None:
    """Initialize and run the voting application."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create and run the application
    app = VotingApp()
    app.mainloop()


if __name__ == "__main__":
    main()