# pinq Classes Reference

Complete documentation of all prompt classes in pinq.

---

## TextPrompt

Interactive text input prompt with support for default values and help messages.

### Constructor

```python
prompt = pinq.TextPrompt(message: str)
```

**Parameters:**
- `message` (str): The question or prompt text shown to the user

**Raises:**
- None (construction never fails)

### Methods

#### `with_default(default: str) -> TextPrompt`

Set a default value for the prompt. If the user presses Enter without typing, this value is returned.

```python
prompt = pinq.TextPrompt("Username: ")
prompt.with_default("admin")
```

**Returns:** Self for method chaining

#### `with_help_message(help: str) -> TextPrompt`

Set a help message displayed below the main prompt question.

```python
prompt = pinq.TextPrompt("Email: ")
prompt.with_help_message("Format: user@example.com")
```

**Returns:** Self for method chaining

#### `with_page_size(size: int) -> TextPrompt`

Set the page size for autocompletion display.

```python
prompt = pinq.TextPrompt("Name: ")
prompt.with_page_size(5)
```

**Returns:** Self for method chaining

#### `prompt() -> str`

Display the prompt and block until the user submits an answer.

```python
name = prompt.prompt()
```

**Returns:** The user's input text

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[str]`

Display the prompt, but allow the user to skip it by pressing ESC.

```python
optional_input = prompt.prompt_skippable()
if optional_input is None:
    print("User skipped this prompt")
```

**Returns:** User's input or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

prompt = pinq.TextPrompt("What is your name?")
prompt.with_default("User")
prompt.with_help_message("Press ENTER for default")

name = prompt.prompt()
print(f"Hello, {name}!")
```

---

## ConfirmPrompt

Simple yes/no confirmation prompt.

### Constructor

```python
prompt = pinq.ConfirmPrompt(message: str)
```

**Parameters:**
- `message` (str): The yes/no question shown to the user

### Methods

#### `with_default(default: bool) -> ConfirmPrompt`

Set the default answer: `True` for yes, `False` for no.

```python
prompt = pinq.ConfirmPrompt("Continue?")
prompt.with_default(True)  # Default to yes
```

**Returns:** Self for method chaining

#### `with_help_message(help: str) -> ConfirmPrompt`

Set a help message.

```python
prompt.with_help_message("This action cannot be undone")
```

**Returns:** Self for method chaining

#### `prompt() -> bool`

Display the prompt and wait for yes/no response.

```python
if prompt.prompt():
    print("User said yes")
else:
    print("User said no")
```

**Returns:** `True` for yes, `False` for no

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[bool]`

Display the prompt, allowing ESC to skip.

```python
answer = prompt.prompt_skippable()
if answer is None:
    print("User skipped")
elif answer:
    print("User said yes")
else:
    print("User said no")
```

**Returns:** `True`, `False`, or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

if pinq.ConfirmPrompt("Delete file?").with_default(False).prompt():
    print("Deleting...")
else:
    print("Canceled")
```

---

## PasswordPrompt

Hidden password/secret input prompt.

### Constructor

```python
prompt = pinq.PasswordPrompt(message: str)
```

**Parameters:**
- `message` (str): The prompt text (usually "Password: ")

### Methods

#### `with_help_message(help: str) -> PasswordPrompt`

Set a help message.

```python
prompt.with_help_message("At least 8 characters")
```

**Returns:** Self for method chaining

#### `prompt() -> str`

Display the prompt and wait for password input (characters not echoed).

```python
password = prompt.prompt()
```

**Returns:** The entered password

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[str]`

Display the prompt, allowing ESC to skip.

```python
password = prompt.prompt_skippable()
if password is None:
    print("Skipped")
```

**Returns:** The password or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

prompt = pinq.PasswordPrompt("Enter password: ")
password = prompt.prompt()
print(f"Got password of length {len(password)}")
```

---

## SelectPrompt

Single-choice selection from a list of options.

### Constructor

```python
prompt = pinq.SelectPrompt(message: str, options: List[str])
```

**Parameters:**
- `message` (str): The selection prompt text
- `options` (List[str]): Non-empty list of options to choose from

**Raises:**
- `RuntimeError` - If options list is empty

### Methods

#### `with_default(index: int) -> SelectPrompt`

Set the default selected option by its index.

```python
options = ["Red", "Green", "Blue"]
prompt = pinq.SelectPrompt("Pick a color:", options)
prompt.with_default(1)  # Default to "Green"
```

**Returns:** Self for method chaining

**Raises:**
- `RuntimeError` - If index is out of range

#### `with_help_message(help: str) -> SelectPrompt`

Set a help message.

```python
prompt.with_help_message("Use arrow keys to navigate")
```

**Returns:** Self for method chaining

#### `with_page_size(size: int) -> SelectPrompt`

Set how many options are visible at once.

```python
prompt.with_page_size(10)  # Show 10 options per page
```

**Returns:** Self for method chaining

#### `prompt() -> str`

Display the selection prompt and wait for user choice.

```python
choice = prompt.prompt()
```

**Returns:** The selected option text

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[str]`

Display the prompt, allowing ESC to skip.

```python
choice = prompt.prompt_skippable()
if choice is None:
    print("User skipped")
```

**Returns:** Selected option or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

options = ["Python", "Rust", "Go", "C++"]
prompt = pinq.SelectPrompt("Choose a language:", options)
prompt.with_page_size(4)

language = prompt.prompt()
print(f"You chose: {language}")
```

---

## MultiSelectPrompt

Multiple-choice selection from a list (select zero or more).

### Constructor

```python
prompt = pinq.MultiSelectPrompt(message: str, options: List[str])
```

**Parameters:**
- `message` (str): The prompt text
- `options` (List[str]): Non-empty list of options

**Raises:**
- `RuntimeError` - If options list is empty

### Methods

#### `with_defaults(indices: List[int]) -> MultiSelectPrompt`

Set which options are selected by default (by index).

```python
prompt = pinq.MultiSelectPrompt("Select tags:", ["rust", "python", "js"])
prompt.with_defaults([0, 2])  # Default select "rust" and "js"
```

**Returns:** Self for method chaining

**Raises:**
- `RuntimeError` - If any index is out of range

#### `with_help_message(help: str) -> MultiSelectPrompt`

Set a help message.

```python
prompt.with_help_message("SPACE to select, arrows to navigate")
```

**Returns:** Self for method chaining

#### `with_page_size(size: int) -> MultiSelectPrompt`

Set how many options are visible at once.

```python
prompt.with_page_size(5)
```

**Returns:** Self for method chaining

#### `prompt() -> List[str]`

Display the prompt and wait for user selections.

```python
selections = prompt.prompt()
```

**Returns:** List of selected option texts (may be empty)

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[List[str]]`

Display the prompt, allowing ESC to skip.

```python
selections = prompt.prompt_skippable()
if selections is None:
    print("User skipped")
```

**Returns:** List of selections or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

options = ["Apples", "Bananas", "Carrots", "Dates"]
prompt = pinq.MultiSelectPrompt("Select fruits:", options)

fruits = prompt.prompt()
print(f"You chose: {', '.join(fruits)}")
```

---

## IntPrompt

Integer input with parsing and validation.

### Constructor

```python
prompt = pinq.IntPrompt(message: str)
```

**Parameters:**
- `message` (str): The prompt text

### Methods

#### `with_default(default: int) -> IntPrompt`

Set a default integer value.

```python
prompt = pinq.IntPrompt("Enter count: ")
prompt.with_default(5)
```

**Returns:** Self for method chaining

#### `with_help_message(help: str) -> IntPrompt`

Set a help message.

```python
prompt.with_help_message("Must be between 1 and 100")
```

**Returns:** Self for method chaining

#### `prompt() -> int`

Display and get an integer from the user.

```python
count = prompt.prompt()
```

**Returns:** The parsed integer

**Raises:**
- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

#### `prompt_skippable() -> Optional[int]`

Display the prompt, allowing ESC to skip.

```python
count = prompt.prompt_skippable()
```

**Returns:** The integer or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or parse error

### Example

```python
import pinq

prompt = pinq.IntPrompt("How many items?")
count = prompt.prompt()
print(f"Processing {count} items...")
```

---

## FloatPrompt

Floating-point number input with parsing.

### Constructor

```python
prompt = pinq.FloatPrompt(message: str)
```

**Parameters:**
- `message` (str): The prompt text

### Methods

#### `with_default(default: float) -> FloatPrompt`

Set a default float value.

```python
prompt = pinq.FloatPrompt("Enter price: ")
prompt.with_default(9.99)
```

**Returns:** Self for method chaining

#### `with_help_message(help: str) -> FloatPrompt`

Set a help message.

```python
prompt.with_help_message("Use decimal point (e.g., 19.99)")
```

**Returns:** Self for method chaining

#### `prompt() -> float`

Display and get a float from the user.

```python
price = prompt.prompt()
```

**Returns:** The parsed float

**Raises:**
- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

#### `prompt_skippable() -> Optional[float]`

Display the prompt, allowing ESC to skip.

```python
price = prompt.prompt_skippable()
```

**Returns:** The float or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or parse error

### Example

```python
import pinq

prompt = pinq.FloatPrompt("Enter amount: $")
amount = prompt.prompt()
print(f"Total: ${amount:.2f}")
```

---

## DateSelectPrompt

Interactive calendar date picker.

### Constructor

```python
prompt = pinq.DateSelectPrompt(message: str)
```

**Parameters:**
- `message` (str): The prompt text

**Note:** Requires the `date` feature (enabled in standard pinq builds)

### Methods

#### `with_help_message(help: str) -> DateSelectPrompt`

Set a help message.

```python
prompt.with_help_message("Navigate with arrow keys")
```

**Returns:** Self for method chaining

#### `prompt() -> str`

Display the interactive calendar and wait for date selection.

```python
date_str = prompt.prompt()
```

**Returns:** Selected date as string in YYYY-MM-DD format

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[str]`

Display the calendar, allowing ESC to skip.

```python
date_str = prompt.prompt_skippable()
if date_str is None:
    print("User skipped date selection")
```

**Returns:** Date string or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

prompt = pinq.DateSelectPrompt("Select a meeting date: ")
date_str = prompt.prompt()
print(f"Meeting on: {date_str}")

# Parse the date for further use
from datetime import datetime
date = datetime.strptime(date_str, "%Y-%m-%d").date()
```

---

## EditorPrompt

Multi-line text input using an external text editor.

### Constructor

```python
prompt = pinq.EditorPrompt(message: str)
```

**Parameters:**
- `message` (str): The prompt text

**Note:** Requires the `editor` feature (enabled in standard pinq builds)

### Methods

#### `with_help_message(help: str) -> EditorPrompt`

Set a help message.

```python
prompt.with_help_message("Press e to open editor, ENTER to submit")
```

**Returns:** Self for method chaining

#### `prompt() -> str`

Display the prompt and open an editor for text input.

```python
text = prompt.prompt()
```

**Returns:** The text entered in the editor

**Raises:**
- `RuntimeError` - If not a TTY, IO error, or operation canceled

#### `prompt_skippable() -> Optional[str]`

Display the prompt, allowing ESC to skip.

```python
text = prompt.prompt_skippable()
if text is None:
    print("User canceled editor")
```

**Returns:** Text or `None` if skipped

**Raises:**
- `RuntimeError` - If not a TTY or IO error

### Example

```python
import pinq

prompt = pinq.EditorPrompt("Write your message: ")
prompt.with_help_message("(opens in your default editor)")

message = prompt.prompt()
print(f"Message length: {len(message)} characters")
```

---

## See Also

- [Functions Reference](functions.md) - One-liner convenience functions
- [Builders Reference](builders.md) - Builder pattern examples
- [Overview](overview.md) - Architecture and design
