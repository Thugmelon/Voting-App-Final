import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import logging
from models import InvalidIDError
from logic import VoteManager
from config import (
    WINDOW_TITLE,
    WINDOW_SIZE,
    FONTS,
    COLORS,
    CANDIDATES
)

logger = logging.getLogger(__name__)

class ModernEntry(ttk.Entry):
    # Made custom styled entry widget

    def __init__(
        self,
        parent: tk.Widget,
        placeholder: str,
        validate_cmd: Optional[Callable] = None,
        **kwargs
    ) -> None:
        """
        Initialize entry widget, gonna put the arguments below

        Args:
            parent: Parent widget
            placeholder: Placeholder text
            validate_cmd: Optional validation command
            **kwargs: Additional keyword arguments
        """
        super().__init__(
            parent,
            style="Modern.TEntry",
            **kwargs
        )

        self.placeholder = placeholder
        self._is_empty = True

        # Bind the events (in focus and out of focus)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        self.insert(0, placeholder)
        self.configure(foreground=COLORS["text"])

        if validate_cmd:
            self.configure(
                validate="all",
                validatecommand=(self.register(validate_cmd), "%P")
            )

    def _on_focus_in(self, event) -> None:
        # In focus (make out of focus below too)
        if self._is_empty:
            self.delete(0, tk.END)
            self.configure(foreground=COLORS["text"])
            self._is_empty = False

    def _on_focus_out(self, event) -> None:
        # Method for when it's out of focus
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground=COLORS["text"])
            self._is_empty = True

class VotingApp(tk.Tk):
    #Make main app window (configure it in setup_window though)
    def __init__(self) -> None:
        # Initialize the window
        super().__init__()

        self._vote_manager = VoteManager()
        self._selected_candidate = tk.StringVar(value=CANDIDATES[0])
        self._error_message = tk.StringVar()

        self._setup_window()
        self._setup_styles()
        self._create_widgets()

    def _setup_window(self) -> None:
        # configure window here
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.resizable(False, False)
        self.configure(bg=COLORS["background"])

        # Setting it to the center of the screen (might change later)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_SIZE[0]) // 2
        y = (screen_height - WINDOW_SIZE[1]) // 2
        self.geometry(f"+{x}+{y}")

    def _setup_styles(self) -> None:
        """Configure custom styles."""
        style = ttk.Style()
        style.configure("Modern.TEntry",
                       padding=5,
                       background=COLORS["background"])

        style.configure("Modern.TLabel",
                       background=COLORS["background"],
                       foreground=COLORS["text"])

        style.configure("Modern.TButton",
                       padding=10,
                       background=COLORS["button"],
                       foreground=COLORS["text"])

        style.configure("Error.TLabel",
                       foreground=COLORS["error"],
                       background=COLORS["background"])

    def _create_widgets(self) -> None:
        # Create and arrange all GUI widgets here
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        title_label = ttk.Label(
            main_frame,
            text=WINDOW_TITLE,
            font=FONTS["title"],
            style="Modern.TLabel"
        )
        title_label.pack(pady=(0, 20))

        # ID Entry
        id_label = ttk.Label(
            main_frame,
            text="ID",
            font=FONTS["header"],
            style="Modern.TLabel"
        )
        id_label.pack(anchor="w")

        self._id_entry = ModernEntry(
            main_frame,
            placeholder="Enter your ID",
            width=30
        )
        self._id_entry.pack(fill="x", pady=(5, 20))

        # Candidates section
        candidates_label = ttk.Label(
            main_frame,
            text="CANDIDATES",
            font=FONTS["header"],
            style="Modern.TLabel"
        )
        candidates_label.pack(anchor="w")

        # Radio buttons for candidates
        for candidate in CANDIDATES:
            rb = ttk.Radiobutton(
                main_frame,
                text=candidate,
                variable=self._selected_candidate,
                value=candidate,
                style="Modern.TRadiobutton"
            )
            rb.pack(anchor="w", pady=5)

        # Vote Button
        self._vote_button = ttk.Button(
            main_frame,
            text="SUBMIT VOTE",
            command=self._handle_vote,
            style="Modern.TButton"
        )
        self._vote_button.pack(pady=20)

        # Error message label
        self._error_label = ttk.Label(
            main_frame,
            textvariable=self._error_message,
            style="Error.TLabel",
            font=FONTS["normal"]
        )
        self._error_label.pack(pady=10)

    def _handle_vote(self) -> None:
        """Handle the vote button click event."""
        voter_id = self._id_entry.get()
        if voter_id == self._id_entry.placeholder:
            self._show_error("Please enter your ID")
            return

        try:
            candidate = self._selected_candidate.get()
            self._vote_manager.cast_vote(voter_id, candidate)
            messagebox.showinfo("Success", "Your vote has been recorded!")
            self._error_message.set("")  # Clear any error message
            self._id_entry.delete(0, tk.END)  # Clear the ID entry
            self._id_entry._on_focus_out(None)  # Show placeholder
            #Some exception handling below here

        except InvalidIDError as e:
            self._show_error(str(e))
        except ValueError as e:
            self._show_error("You have already voted")
        except Exception as e:
            logger.error(f"Error casting vote: {e}")
            self._show_error("An error occurred while casting your vote")

    def _show_error(self, message: str) -> None:
        #Display an error message in red text.
        self._error_message.set(message)
        self._error_label.configure(foreground=COLORS["error"])