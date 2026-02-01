"""Type stubs for pinq - Python binding for inquire CLI prompts.

This file provides complete type information for the pinq module.
All classes support method chaining with &mut self pattern returning Self.
"""

from typing import List, Optional
from enum import Enum

__version__: str
"""pinq version (0.9.2)"""


# ============================================================================
# ENUMS
# ============================================================================

class PasswordDisplayMode(Enum):
    """Display mode for password input.
    
    Controls how password characters are displayed while typing.
    """
    Masked: PasswordDisplayMode
    """Characters shown as asterisks or dots"""
    
    Hidden: PasswordDisplayMode
    """Characters completely hidden"""


class InputAction(Enum):
    """Text input action type.
    
    Describes the action performed during text input.
    """
    NoChange: InputAction
    """No action, input continues normally"""
    
    Submit: InputAction
    """User submitted the input"""
    
    Cancel: InputAction
    """User canceled input with ESC"""
    
    Interrupt: InputAction
    """User interrupted with Ctrl+C"""


# ============================================================================
# TEXT PROMPT
# ============================================================================

class TextPrompt:
    """Interactive text input prompt.
    
    Allows users to input free-form text with optional default value,
    help message, and pagination settings.
    
    All builder methods return Self for method chaining.
    
    Example:
        prompt = TextPrompt("Enter name:").with_default("John").with_help_message("3-20 chars")
        name = prompt.prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new text prompt.
        
        Args:
            message: The prompt message displayed to the user
        """
        ...
    
    def with_default(self, default: str) -> TextPrompt:
        """Set a default value returned if user presses Enter.
        
        Args:
            default: The default text value
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_help_message(self, help: str) -> TextPrompt:
        """Set a help message displayed below the main prompt.
        
        Args:
            help: The help message text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_page_size(self, size: int) -> TextPrompt:
        """Set pagination size for autocompletion suggestions.
        
        Args:
            size: Number of items to display per page
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> str:
        """Display the prompt and collect input.
        
        Blocks until user submits (Enter) or cancels (Ctrl+C).
        
        Returns:
            The user's input text
            
        Raises:
            RuntimeError: If not TTY, IO error, or operation canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[str]:
        """Display prompt allowing user to skip with ESC.
        
        Returns None if user presses ESC instead of Enter.
        
        Returns:
            The input text or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# CONFIRM PROMPT
# ============================================================================

class ConfirmPrompt:
    """Yes/No confirmation prompt.
    
    Displays a simple yes/no question to the user.
    
    All builder methods return Self for method chaining.
    
    Example:
        confirmed = ConfirmPrompt("Delete?").with_default(False).prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new confirmation prompt.
        
        Args:
            message: The yes/no question
        """
        ...
    
    def with_default(self, default: bool) -> ConfirmPrompt:
        """Set default answer (returned if user presses Enter).
        
        Args:
            default: True for yes, False for no
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_help_message(self, help: str) -> ConfirmPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> bool:
        """Display the confirmation and collect answer.
        
        Returns:
            True if yes, False if no
            
        Raises:
            RuntimeError: If not TTY, IO error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[bool]:
        """Display confirmation allowing user to skip with ESC.
        
        Returns:
            True/False or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# PASSWORD PROMPT
# ============================================================================

class PasswordPrompt:
    """Password/secret input prompt.
    
    Text input that doesn't echo characters to terminal for secure input.
    
    All builder methods return Self for method chaining.
    
    Example:
        password = PasswordPrompt("Enter password:").with_help_message("8+ chars").prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new password prompt.
        
        Args:
            message: The prompt message
        """
        ...
    
    def with_help_message(self, help: str) -> PasswordPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> str:
        """Display prompt and collect password input.
        
        Characters are not echoed to the terminal.
        
        Returns:
            The entered password
            
        Raises:
            RuntimeError: If not TTY, IO error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[str]:
        """Display prompt allowing user to skip with ESC.
        
        Returns:
            The password or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# SELECT PROMPT
# ============================================================================

class SelectPrompt:
    """Single-choice selection prompt.
    
    Allows user to select exactly one option from a list using arrow keys.
    
    All builder methods return Self for method chaining.
    
    Example:
        choice = SelectPrompt("Pick color:", ["Red", "Green", "Blue"]).with_default(0).prompt()
    """
    
    def __init__(self, message: str, options: List[str]) -> None:
        """Create a new select prompt.
        
        Args:
            message: The selection prompt message
            options: Non-empty list of options to choose from
            
        Raises:
            RuntimeError: If options list is empty
        """
        ...
    
    def with_default(self, index: int) -> SelectPrompt:
        """Set default selected option by index.
        
        Args:
            index: Index of the default option (0-based)
            
        Returns:
            Self for method chaining
            
        Raises:
            RuntimeError: If index is out of range
        """
        ...
    
    def with_help_message(self, help: str) -> SelectPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_page_size(self, size: int) -> SelectPrompt:
        """Set how many options are visible at once.
        
        Args:
            size: Number of options to display per page
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> str:
        """Display prompt and collect selection.
        
        User navigates with arrow keys and selects with Enter.
        
        Returns:
            The selected option text
            
        Raises:
            RuntimeError: If not TTY, IO error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[str]:
        """Display prompt allowing user to skip with ESC.
        
        Returns:
            The selected option or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# MULTISELECT PROMPT
# ============================================================================

class MultiSelectPrompt:
    """Multiple-choice selection prompt.
    
    Allows user to select zero or more options from a list.
    Uses Space to toggle selection and Enter to confirm.
    
    All builder methods return Self for method chaining.
    
    Example:
        items = MultiSelectPrompt("Pick fruits:", ["Apple", "Banana"]).prompt()
    """
    
    def __init__(self, message: str, options: List[str]) -> None:
        """Create a new multi-select prompt.
        
        Args:
            message: The selection prompt message
            options: Non-empty list of options to choose from
            
        Raises:
            RuntimeError: If options list is empty
        """
        ...
    
    def with_defaults(self, indices: List[int]) -> MultiSelectPrompt:
        """Set default selected options by indices.
        
        Args:
            indices: List of option indices to select by default (0-based)
            
        Returns:
            Self for method chaining
            
        Raises:
            RuntimeError: If any index is out of range
        """
        ...
    
    def with_help_message(self, help: str) -> MultiSelectPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_page_size(self, size: int) -> MultiSelectPrompt:
        """Set how many options are visible at once.
        
        Args:
            size: Number of options to display per page
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> List[str]:
        """Display prompt and collect selections.
        
        User navigates with arrow keys, toggles with Space, submits with Enter.
        
        Returns:
            List of selected option texts (may be empty)
            
        Raises:
            RuntimeError: If not TTY, IO error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[List[str]]:
        """Display prompt allowing user to skip with ESC.
        
        Returns:
            List of selections or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# INT PROMPT
# ============================================================================

class IntPrompt:
    """64-bit signed integer input prompt.
    
    Parses user input as i64 integer with validation.
    
    All builder methods return Self for method chaining.
    
    Example:
        count = IntPrompt("Count:").with_default(5).with_help_message("1-100").prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new integer prompt.
        
        Args:
            message: The prompt message
        """
        ...
    
    def with_default(self, default: int) -> IntPrompt:
        """Set default value returned if user presses Enter.
        
        Args:
            default: The default integer value
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_help_message(self, help: str) -> IntPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> int:
        """Display prompt and collect integer input.
        
        Returns:
            The parsed integer value
            
        Raises:
            RuntimeError: If not TTY, IO error, parse error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[int]:
        """Display prompt allowing user to skip with ESC.
        
        Returns:
            The parsed integer or None if skipped
            
        Raises:
            RuntimeError: If not TTY, IO error, or parse error
        """
        ...


# ============================================================================
# FLOAT PROMPT
# ============================================================================

class FloatPrompt:
    """64-bit float input prompt.
    
    Parses user input as f64 floating point number with validation.
    
    All builder methods return Self for method chaining.
    
    Example:
        price = FloatPrompt("Price: $").with_default(9.99).prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new float prompt.
        
        Args:
            message: The prompt message
        """
        ...
    
    def with_default(self, default: float) -> FloatPrompt:
        """Set default value returned if user presses Enter.
        
        Args:
            default: The default float value
            
        Returns:
            Self for method chaining
        """
        ...
    
    def with_help_message(self, help: str) -> FloatPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> float:
        """Display prompt and collect float input.
        
        Returns:
            The parsed float value
            
        Raises:
            RuntimeError: If not TTY, IO error, parse error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[float]:
        """Display prompt allowing user to skip with ESC.
        
        Returns:
            The parsed float or None if skipped
            
        Raises:
            RuntimeError: If not TTY, IO error, or parse error
        """
        ...


# ============================================================================
# DATE SELECT PROMPT
# ============================================================================

class DateSelectPrompt:
    """Interactive date selection prompt.
    
    Opens an interactive calendar for user to select a date.
    Returns date as string in YYYY-MM-DD format.
    
    All builder methods return Self for method chaining.
    
    Example:
        date_str = DateSelectPrompt("Meeting date:").prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new date selection prompt.
        
        Args:
            message: The prompt message
        """
        ...
    
    def with_help_message(self, help: str) -> DateSelectPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> str:
        """Display calendar and collect date selection.
        
        User navigates calendar and selects date with Enter.
        
        Returns:
            Selected date as string in YYYY-MM-DD format
            
        Raises:
            RuntimeError: If not TTY, IO error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[str]:
        """Display calendar allowing user to skip with ESC.
        
        Returns:
            Date string in YYYY-MM-DD format or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# EDITOR PROMPT
# ============================================================================

class EditorPrompt:
    """Multi-line text editor prompt.
    
    Opens the system text editor for user to write longer text.
    Editor used is determined by EDITOR environment variable.
    
    All builder methods return Self for method chaining.
    
    Example:
        text = EditorPrompt("Write message:").prompt()
    """
    
    def __init__(self, message: str) -> None:
        """Create a new editor prompt.
        
        Args:
            message: The prompt message
        """
        ...
    
    def with_help_message(self, help: str) -> EditorPrompt:
        """Set help message displayed below the prompt.
        
        Args:
            help: The help text
            
        Returns:
            Self for method chaining
        """
        ...
    
    def prompt(self) -> str:
        """Open editor and collect text input.
        
        Returns:
            The text entered in editor
            
        Raises:
            RuntimeError: If not TTY, IO error, or canceled
        """
        ...
    
    def prompt_skippable(self) -> Optional[str]:
        """Open editor allowing user to skip with ESC.
        
        Returns:
            The entered text or None if skipped
            
        Raises:
            RuntimeError: If not TTY or IO error
        """
        ...


# ============================================================================
# ONE-LINER FUNCTIONS
# ============================================================================

def prompt_text(message: str) -> str:
    """Quick text input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The user's input text
        
    Raises:
        RuntimeError: If not TTY, IO error, or canceled
    """
    ...


def prompt_secret(message: str) -> str:
    """Quick password input one-liner.
    
    Doesn't echo input to terminal.
    
    Args:
        message: The prompt message
        
    Returns:
        The entered password
        
    Raises:
        RuntimeError: If not TTY, IO error, or canceled
    """
    ...


def prompt_confirmation(message: str) -> bool:
    """Quick yes/no confirmation one-liner.
    
    Args:
        message: The yes/no question
        
    Returns:
        True for yes, False for no
        
    Raises:
        RuntimeError: If not TTY, IO error, or canceled
    """
    ...


def prompt_int(message: str) -> int:
    """Quick i64 integer input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The parsed integer
        
    Raises:
        RuntimeError: If not TTY, IO error, parse error, or canceled
    """
    ...


def prompt_float(message: str) -> float:
    """Quick f64 float input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The parsed float
        
    Raises:
        RuntimeError: If not TTY, IO error, parse error, or canceled
    """
    ...


def prompt_u32(message: str) -> int:
    """Quick u32 unsigned integer input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The parsed u32 value as int
        
    Raises:
        RuntimeError: If not TTY, IO error, parse error, or canceled
    """
    ...


def prompt_u64(message: str) -> int:
    """Quick u64 unsigned integer input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The parsed u64 value as int
        
    Raises:
        RuntimeError: If not TTY, IO error, parse error, or canceled
    """
    ...


def prompt_f32(message: str) -> float:
    """Quick f32 32-bit float input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The parsed f32 value as float
        
    Raises:
        RuntimeError: If not TTY, IO error, parse error, or canceled
    """
    ...


def prompt_f64(message: str) -> float:
    """Quick f64 64-bit float input one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        The parsed f64 value as float
        
    Raises:
        RuntimeError: If not TTY, IO error, parse error, or canceled
    """
    ...


def prompt_date(message: str) -> str:
    """Quick date selection one-liner.
    
    Args:
        message: The prompt message
        
    Returns:
        Selected date as string in YYYY-MM-DD format
        
    Raises:
        RuntimeError: If not TTY, IO error, or canceled
    """
    ...
    