# pinq Error Handling Reference

Complete guide to error handling in pinq.

---

## Error Model

All prompt operations can fail. pinq converts Rust's `Result` type to Python exceptions, raising `RuntimeError` with descriptive messages.

### Exception Type

All errors from pinq prompts are raised as `RuntimeError`.

```python
try:
    result = prompt.prompt()
except RuntimeError as e:
    print(f"Error: {e}")
```

---

## Error Types and Messages

### NotTTY Error

**Message:** `"Input is not a TTY"`

**Cause:** The prompt is being run in an environment that is not a terminal (TTY). This typically happens when:
- Running in a non-interactive environment
- Input is redirected from a pipe or file
- Running in certain IDEs without proper terminal support

**Recoverable:** No - The application cannot proceed with interactive prompts

**Example:**
```python
import pinq
import sys
import subprocess

# This will fail
result = subprocess.run([sys.executable, "-c", 
    "import pinq; pinq.prompt_text('Name: ')"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# RuntimeError: Input is not a TTY
```

### IOError

**Message:** `"IO Error: <details>"`

**Cause:** An operating system IO error occurred while:
- Reading from stdin
- Writing to stdout
- Interacting with the terminal

**Common Sub-causes:**
- Permission denied
- Broken pipe
- Terminal disconnection
- Disk read/write failure

**Recoverable:** Possibly - depends on the underlying cause

**Example:**
```python
import pinq
import os

try:
    result = pinq.prompt_text("Input: ")
except RuntimeError as e:
    if "IO Error" in str(e):
        print("Terminal communication failed")
```

### OperationCanceled

**Message:** `"Operation canceled by user"`

**Cause:** The user explicitly canceled the prompt by pressing:
- `Ctrl+C` (SIGINT interrupt)
- `ESC` key (for skippable prompts)

**Recoverable:** Yes - Expected behavior, application can handle gracefully

**Example:**
```python
import pinq

try:
    name = pinq.prompt_text("Enter name: ")
except RuntimeError as e:
    if "canceled" in str(e).lower():
        print("User canceled - exiting")
        exit(0)
```

### InvalidConfiguration

**Message:** `"Invalid configuration: <details>"`

**Cause:** The prompt was configured with invalid parameters. Common causes:
- Empty options list for Select/MultiSelect
- Default index out of range
- Invalid page size
- Incompatible settings

**Recoverable:** No - Fix the code

**Example:**
```python
import pinq

# This will fail immediately
try:
    prompt = pinq.SelectPrompt("Choose:", [])  # Empty list!
except RuntimeError as e:
    print(f"Configuration error: {e}")
```

---

## Error Handling Patterns

### Pattern 1: Basic Error Handling

```python
import pinq

try:
    result = pinq.prompt_text("Input: ")
    print(f"Got: {result}")
except RuntimeError as e:
    print(f"Error: {e}")
```

### Pattern 2: Specific Error Type Detection

```python
import pinq

try:
    result = pinq.prompt_int("Number: ")
except RuntimeError as e:
    error_msg = str(e).lower()
    
    if "not a tty" in error_msg:
        print("Not running in a terminal")
    elif "canceled" in error_msg:
        print("User canceled")
    elif "io error" in error_msg:
        print("Terminal communication error")
    else:
        print(f"Other error: {e}")
```

### Pattern 3: Retry Loop

```python
import pinq

max_retries = 3
for attempt in range(max_retries):
    try:
        age = pinq.prompt_int("Your age: ")
        if age >= 0:
            break
        else:
            print("Age must be non-negative")
    except RuntimeError as e:
        if "canceled" in str(e).lower():
            print("Canceled")
            break
        else:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                print("Max retries reached")
```

### Pattern 4: Graceful Degradation

```python
import pinq

def get_user_input(prompt_text, default_value):
    try:
        result = pinq.prompt_text(prompt_text)
        return result
    except RuntimeError as e:
        error_msg = str(e).lower()
        
        if "not a tty" in error_msg:
            # Running non-interactively, use default
            print(f"Non-interactive mode, using default: {default_value}")
            return default_value
        elif "canceled" in error_msg:
            # User canceled, return None
            return None
        else:
            raise
```

### Pattern 5: Context Manager Pattern

```python
import pinq
from contextlib import contextmanager

@contextmanager
def safe_prompt():
    try:
        yield
    except RuntimeError as e:
        if "not a tty" in str(e).lower():
            print("Warning: Not in a terminal")
        elif "canceled" in str(e).lower():
            print("Operation canceled")
        else:
            raise

with safe_prompt():
    name = pinq.prompt_text("Name: ")
```

---

## Parsing and Validation Errors

### Integer Parsing Error

**Message:** `"Error parsing input"` or similar

**Cause:** Input cannot be parsed as the requested type

**Example:**
```python
import pinq

try:
    age = pinq.prompt_int("Age: ")
except RuntimeError as e:
    print(f"Invalid age input: {e}")
```

User enters: `"abc"`
Error: Parsing fails

### Float Parsing Error

Same as integer, but for floats

```python
try:
    price = pinq.prompt_float("Price: ")
except RuntimeError as e:
    print(f"Invalid price: {e}")
```

User enters: `"$19.99"`
Error: Can't parse $ and currency format

### Type-Specific Errors

Each numeric type has its own range constraints:

```python
# prompt_u32: Must be 0 to 4,294,967,295
try:
    port = pinq.prompt_u32("Port: ")
except RuntimeError as e:
    print(f"Invalid port: {e}")

# User enters: -1
# Error: Negative numbers not allowed

# User enters: 5000000000 (too large for u32)
# Error: Number out of range
```

---

## Common Error Scenarios

### Scenario 1: Running in Non-Interactive Environment

```bash
# Running in pipe - will fail
echo "import pinq; pinq.prompt_text('Test: ')" | python
# RuntimeError: Input is not a TTY
```

**Solution:** Check if interactive before prompting

```python
import sys

if sys.stdin.isatty():
    name = pinq.prompt_text("Name: ")
else:
    name = "DefaultName"
```

### Scenario 2: User Interrupts (Ctrl+C)

```python
import pinq

try:
    result = pinq.prompt_text("Input: ")
except RuntimeError as e:
    if "canceled" in str(e).lower():
        print("\nInterrupted by user")
```

### Scenario 3: Invalid Configuration

```python
import pinq

# This code has a bug:
try:
    prompt = pinq.SelectPrompt("Pick one:", [])  # Empty!
except RuntimeError as e:
    print(f"Configuration error: {e}")
```

### Scenario 4: Type Mismatch in Parsing

```python
import pinq

# User enters text when number expected
try:
    count = pinq.prompt_int("How many? ")
except RuntimeError as e:
    print(f"Please enter a number, got: {e}")

# Better: use prompt_text and parse manually
text = pinq.prompt_text("How many? ")
try:
    count = int(text)
except ValueError:
    print(f"'{text}' is not a valid number")
```

---

## Error Recovery Strategies

### Strategy 1: Default Values

```python
import pinq

def safe_int_prompt(message, default):
    try:
        return pinq.prompt_int(message)
    except RuntimeError:
        return default

count = safe_int_prompt("Count: ", 1)
```

### Strategy 2: Optional Prompts

```python
import pinq

feedback = pinq.TextPrompt("Feedback: ").prompt_skippable()
# User can press ESC to skip - not an error
```

### Strategy 3: Validation Loop

```python
import pinq

def prompt_positive_int(message):
    while True:
        try:
            value = pinq.prompt_int(message)
            if value > 0:
                return value
            else:
                print("Must be positive")
        except RuntimeError as e:
            if "canceled" in str(e).lower():
                return None
            print(f"Invalid: {e}")
```

### Strategy 4: Fallback Input Method

```python
import pinq

def get_name():
    try:
        return pinq.prompt_text("Name: ")
    except RuntimeError as e:
        if "not a tty" in str(e).lower():
            # Fall back to sys.stdin
            print("Name: ", end="", flush=True)
            return input()
        raise
```

---

## Testing Error Conditions

### Testing with mock stdin

```python
import pinq
import io
import sys

# Simulate EOF (empty input)
old_stdin = sys.stdin
sys.stdin = io.StringIO("")

try:
    # This will fail appropriately
    result = pinq.prompt_text("Input: ")
except RuntimeError as e:
    print(f"Got expected error: {e}")
finally:
    sys.stdin = old_stdin
```

---

## Best Practices

1. **Always handle RuntimeError** - Prompts are fallible

```python
# Good
try:
    result = prompt.prompt()
except RuntimeError:
    ...

# Bad
result = prompt.prompt()  # Unhandled exception
```

2. **Check error message content** - Different errors need different handling

```python
# Good
except RuntimeError as e:
    if "tty" in str(e):
        # Handle non-interactive
    elif "canceled" in str(e):
        # Handle user cancellation

# Bad
except RuntimeError:
    # Treating all errors the same
```

3. **Provide user feedback** - Inform users what went wrong

```python
try:
    age = pinq.prompt_int("Age: ")
except RuntimeError as e:
    print(f"Could not get age: {e}")
```

4. **Use prompt_skippable for optional input** - Better UX than error handling

```python
# Good - User can ESC to skip
email = pinq.TextPrompt("Email (optional): ").prompt_skippable()

# Less good - Forces error handling
try:
    email = pinq.prompt_text("Email: ")
except RuntimeError:
    email = None
```

5. **Validate early** - Check configuration before prompting

```python
# Good - Check before use
options = get_options()
if not options:
    print("No options available")
else:
    choice = pinq.SelectPrompt("Choose:", options).prompt()

# Bad - Fails at runtime
choice = pinq.SelectPrompt("Choose:", get_options()).prompt()
```

---

## Debugging Tips

### Enable Verbose Errors

```python
import pinq
import traceback

try:
    result = pinq.prompt_text("Input: ")
except RuntimeError as e:
    print(f"Full error trace:")
    traceback.print_exc()
```

### Check Environment

```python
import sys
import os

print(f"Is TTY: {sys.stdin.isatty()}")
print(f"Terminal: {os.environ.get('TERM', 'unknown')}")
print(f"Platform: {sys.platform}")
```

### Log Operations

```python
import pinq
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Starting prompt...")
    result = pinq.prompt_text("Input: ")
    logging.info(f"Got result: {result}")
except RuntimeError as e:
    logging.error(f"Prompt failed: {e}")
```

---

## See Also

- [Classes Reference](classes.md) - Prompt classes that raise errors
- [Examples](examples.md) - Real-world error handling examples
- [Overview](overview.md) - Architecture and design
