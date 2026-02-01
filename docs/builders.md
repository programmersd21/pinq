# pinq Builder Pattern Reference

The builder pattern in pinq allows you to configure prompts step-by-step with method chaining.

---

## Builder Pattern Overview

All prompt classes follow the builder pattern:

```python
import pinq

# Create a prompt
prompt = pinq.TextPrompt("Your question: ")

# Configure it with fluent methods
prompt.with_default("default value")
prompt.with_help_message("Help text")
prompt.with_page_size(10)

# Execute it
result = prompt.prompt()
```

### Method Chaining

All `with_*` methods return `self`, enabling method chaining:

```python
import pinq

result = (pinq.TextPrompt("Name: ")
    .with_default("User")
    .with_help_message("Enter your name")
    .with_page_size(7)
    .prompt())
```

---

## Builder Methods by Class

### TextPrompt Builder Methods

```python
prompt = pinq.TextPrompt("Username: ")
prompt.with_default("admin")           # Set default value
prompt.with_help_message("Required")   # Set help text
prompt.with_page_size(5)               # Set pagination size
result = prompt.prompt()
```

**Available methods:**
- `with_default(value: str) -> TextPrompt`
- `with_help_message(text: str) -> TextPrompt`
- `with_page_size(size: int) -> TextPrompt`
- `prompt() -> str`
- `prompt_skippable() -> Optional[str]`

---

### ConfirmPrompt Builder Methods

```python
prompt = pinq.ConfirmPrompt("Delete file?")
prompt.with_default(False)             # Default to "no"
prompt.with_help_message("Cannot be undone")
result = prompt.prompt()
```

**Available methods:**
- `with_default(value: bool) -> ConfirmPrompt`
- `with_help_message(text: str) -> ConfirmPrompt`
- `prompt() -> bool`
- `prompt_skippable() -> Optional[bool]`

---

### PasswordPrompt Builder Methods

```python
prompt = pinq.PasswordPrompt("Password: ")
prompt.with_help_message("At least 8 chars")
result = prompt.prompt()
```

**Available methods:**
- `with_help_message(text: str) -> PasswordPrompt`
- `prompt() -> str`
- `prompt_skippable() -> Optional[str]`

---

### SelectPrompt Builder Methods

```python
options = ["Red", "Green", "Blue"]
prompt = pinq.SelectPrompt("Pick a color:", options)
prompt.with_default(0)                 # Default to first option
prompt.with_help_message("Use arrows")
prompt.with_page_size(10)
result = prompt.prompt()
```

**Available methods:**
- `with_default(index: int) -> SelectPrompt`
- `with_help_message(text: str) -> SelectPrompt`
- `with_page_size(size: int) -> SelectPrompt`
- `prompt() -> str`
- `prompt_skippable() -> Optional[str]`

---

### MultiSelectPrompt Builder Methods

```python
options = ["Python", "Rust", "Go"]
prompt = pinq.MultiSelectPrompt("Languages:", options)
prompt.with_defaults([0, 2])           # Default select first and third
prompt.with_help_message("SPACE to select")
prompt.with_page_size(5)
result = prompt.prompt()
```

**Available methods:**
- `with_defaults(indices: List[int]) -> MultiSelectPrompt`
- `with_help_message(text: str) -> MultiSelectPrompt`
- `with_page_size(size: int) -> MultiSelectPrompt`
- `prompt() -> List[str]`
- `prompt_skippable() -> Optional[List[str]]`

---

### IntPrompt Builder Methods

```python
prompt = pinq.IntPrompt("Count: ")
prompt.with_default(10)
prompt.with_help_message("Must be > 0")
result = prompt.prompt()
```

**Available methods:**
- `with_default(value: int) -> IntPrompt`
- `with_help_message(text: str) -> IntPrompt`
- `prompt() -> int`
- `prompt_skippable() -> Optional[int]`

---

### FloatPrompt Builder Methods

```python
prompt = pinq.FloatPrompt("Price: $")
prompt.with_default(9.99)
prompt.with_help_message("Use decimal point")
result = prompt.prompt()
```

**Available methods:**
- `with_default(value: float) -> FloatPrompt`
- `with_help_message(text: str) -> FloatPrompt`
- `prompt() -> float`
- `prompt_skippable() -> Optional[float]`

---

### DateSelectPrompt Builder Methods

```python
prompt = pinq.DateSelectPrompt("Select date: ")
prompt.with_help_message("Navigate with arrows")
result = prompt.prompt()  # Returns YYYY-MM-DD string
```

**Available methods:**
- `with_help_message(text: str) -> DateSelectPrompt`
- `prompt() -> str`
- `prompt_skippable() -> Optional[str]`

---

### EditorPrompt Builder Methods

```python
prompt = pinq.EditorPrompt("Write message: ")
prompt.with_help_message("Press e to open editor")
result = prompt.prompt()
```

**Available methods:**
- `with_help_message(text: str) -> EditorPrompt`
- `prompt() -> str`
- `prompt_skippable() -> Optional[str]`

---

## Real-World Builder Examples

### Example 1: User Registration Form

```python
import pinq

# Get username with default
username = (pinq.TextPrompt("Username: ")
    .with_default("user")
    .with_help_message("3-20 alphanumeric characters")
    .prompt())

# Get password
password = pinq.PasswordPrompt("Password: ").prompt()

# Confirm
confirmed = (pinq.ConfirmPrompt("Register this account?")
    .with_default(True)
    .prompt())

if confirmed:
    print(f"Registered user: {username}")
```

### Example 2: Configuration Wizard

```python
import pinq

# Get application settings
port = (pinq.IntPrompt("API Port: ")
    .with_default(3000)
    .with_help_message("1024-65535")
    .prompt())

debug = (pinq.ConfirmPrompt("Enable debug mode?")
    .with_default(False)
    .prompt())

env = (pinq.SelectPrompt("Environment:", 
        ["development", "staging", "production"])
    .with_default(0)
    .with_help_message("Select deployment environment")
    .prompt())

print(f"Config: port={port}, debug={debug}, env={env}")
```

### Example 3: Survey with Optional Questions

```python
import pinq

name = pinq.prompt_text("Your name: ")

# Optional feedback
feedback = (pinq.EditorPrompt("Feedback (optional): ")
    .with_help_message("Press ESC to skip")
    .prompt_skippable())

if feedback is not None:
    print(f"Feedback from {name}: {feedback[:100]}...")
else:
    print(f"No feedback from {name}")
```

### Example 4: Multi-Select with Defaults

```python
import pinq

options = [
    "Apples",
    "Bananas",
    "Carrots",
    "Dates",
    "Eggplant"
]

selected = (pinq.MultiSelectPrompt("Select fruits:", options)
    .with_defaults([0, 1])  # Default: Apples and Bananas
    .with_page_size(5)
    .with_help_message("SPACE to select/deselect, ENTER to confirm")
    .prompt())

print(f"Selected {len(selected)} items: {', '.join(selected)}")
```

### Example 5: Financial Calculator

```python
import pinq

principal = (pinq.FloatPrompt("Principal amount: $")
    .with_default(1000.0)
    .with_help_message("Enter amount without $ sign")
    .prompt())

rate = (pinq.FloatPrompt("Annual interest rate (%): ")
    .with_default(5.0)
    .prompt())

years = (pinq.IntPrompt("Time period (years): ")
    .with_default(5)
    .prompt())

total = principal * (1 + rate/100) ** years
print(f"Total after {years} years: ${total:.2f}")
```

### Example 6: Complex Configuration

```python
import pinq

print("=== Server Configuration ===\n")

host = (pinq.TextPrompt("Hostname: ")
    .with_default("localhost")
    .with_help_message("Use localhost or IP address")
    .prompt())

port = (pinq.IntPrompt("Port: ")
    .with_default(8000)
    .with_help_message("1024-65535")
    .prompt())

protocol = (pinq.SelectPrompt("Protocol:", ["HTTP", "HTTPS"])
    .with_default(0)
    .with_page_size(2)
    .prompt())

features = (pinq.MultiSelectPrompt("Features:", 
            ["Caching", "Auth", "Logging", "Monitoring"])
    .with_defaults([0, 1, 2])  # Enable first 3 by default
    .with_help_message("Use SPACE to toggle")
    .prompt())

confirm = (pinq.ConfirmPrompt(
    f"Apply: {protocol}://{host}:{port} with {len(features)} features?")
    .with_default(True)
    .prompt())

if confirm:
    print("Configuration applied!")
```

---

## Builder Pattern Best Practices

### 1. Configuration Clarity

```python
# Good: Clear what's being configured
prompt = pinq.TextPrompt("Username: ")
prompt.with_default("admin")
prompt.with_help_message("System administrator account")
username = prompt.prompt()
```

### 2. Method Chaining for Brevity

```python
# Good: Concise one-liner
username = (pinq.TextPrompt("Username: ")
    .with_default("admin")
    .with_help_message("System administrator account")
    .prompt())
```

### 3. Error Handling with Builders

```python
import pinq

try:
    age = (pinq.IntPrompt("Your age: ")
        .with_default(25)
        .with_help_message("Enter a number")
        .prompt())
except RuntimeError as e:
    print(f"Error: {e}")
```

### 4. Reusable Prompt Templates

```python
import pinq

def create_username_prompt():
    return (pinq.TextPrompt("Username: ")
        .with_default("user")
        .with_help_message("3-20 alphanumeric characters")
        .with_page_size(7))

username = create_username_prompt().prompt()
```

### 5. Conditional Configuration

```python
import pinq

is_admin = pinq.prompt_confirmation("Admin account? ")

prompt = pinq.TextPrompt("Username: ")
if is_admin:
    prompt.with_default("admin")
else:
    prompt.with_default("user")

username = prompt.prompt()
```

---

## Common Patterns

### Optional Input Pattern

```python
# User can skip by pressing ESC
name = pinq.TextPrompt("Name (optional): ").prompt_skippable()

if name is None:
    print("No name provided")
else:
    print(f"Name: {name}")
```

### Multi-Step Configuration

```python
results = {}

results['name'] = pinq.prompt_text("Name: ")
results['email'] = pinq.prompt_text("Email: ")
results['age'] = pinq.prompt_int("Age: ")
results['subscribe'] = pinq.prompt_confirmation("Subscribe? ")

print(results)
```

### Looping Until Valid

```python
import pinq

while True:
    try:
        port = pinq.prompt_int("Port (1024-65535): ")
        if 1024 <= port <= 65535:
            break
        else:
            print("Port out of range!")
    except RuntimeError:
        print("Invalid input!")
```

---

## See Also

- [Classes Reference](classes.md) - Detailed class documentation
- [Functions Reference](functions.md) - One-liner functions
- [Examples](examples.md) - More real-world examples
