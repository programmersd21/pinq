# pinq Functions Reference

Convenience one-liner functions for quick prompt creation without manual instantiation.

---

## prompt_text

Quick text input prompt.

### Signature

```python
def prompt_text(message: str) -> str:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `str`: The user's input text

### Raises

- `RuntimeError` - If not a TTY, IO error, or operation canceled

### Example

```python
import pinq

name = pinq.prompt_text("What is your name? ")
print(f"Hello, {name}!")
```

### Equivalent To

```python
prompt = pinq.TextPrompt("What is your name? ")
name = prompt.prompt()
```

---

## prompt_secret

Quick password/secret input prompt.

### Signature

```python
def prompt_secret(message: str) -> str:
    ...
```

### Parameters

- `message` (str): The prompt text (usually "Password: ")

### Returns

- `str`: The entered password/secret

### Raises

- `RuntimeError` - If not a TTY, IO error, or operation canceled

### Example

```python
import pinq

password = pinq.prompt_secret("Enter password: ")
# Characters not echoed to terminal
```

### Equivalent To

```python
prompt = pinq.PasswordPrompt("Enter password: ")
password = prompt.prompt()
```

---

## prompt_confirmation

Quick yes/no confirmation prompt.

### Signature

```python
def prompt_confirmation(message: str) -> bool:
    ...
```

### Parameters

- `message` (str): The yes/no question

### Returns

- `bool`: `True` for yes, `False` for no

### Raises

- `RuntimeError` - If not a TTY, IO error, or operation canceled

### Example

```python
import pinq

if pinq.prompt_confirmation("Continue? "):
    print("Continuing...")
else:
    print("Canceled.")
```

### Equivalent To

```python
prompt = pinq.ConfirmPrompt("Continue? ")
result = prompt.prompt()
```

---

## prompt_int

Quick integer input prompt.

### Signature

```python
def prompt_int(message: str) -> int:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `int`: The parsed integer (64-bit signed)

### Raises

- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

### Example

```python
import pinq

count = pinq.prompt_int("How many items? ")
print(f"Processing {count} items...")
```

### Equivalent To

```python
prompt = pinq.IntPrompt("How many items? ")
count = prompt.prompt()
```

### Notes

- Parses as 64-bit signed integer (i64)
- Rejects non-numeric input
- No range validation (use custom validators for range checks)

---

## prompt_float

Quick float input prompt.

### Signature

```python
def prompt_float(message: str) -> float:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `float`: The parsed float (64-bit)

### Raises

- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

### Example

```python
import pinq

price = pinq.prompt_float("Enter price: $")
print(f"Total: ${price:.2f}")
```

### Equivalent To

```python
prompt = pinq.FloatPrompt("Enter price: $")
price = prompt.prompt()
```

---

## prompt_u32

Quick unsigned 32-bit integer input prompt.

### Signature

```python
def prompt_u32(message: str) -> int:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `int`: The parsed unsigned 32-bit integer (0 to 4,294,967,295)

### Raises

- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

### Example

```python
import pinq

port = pinq.prompt_u32("Enter port number: ")
print(f"Listening on port {port}")
```

### Notes

- Accepts 0 to 4,294,967,295
- Rejects negative numbers
- Rejects numbers > 4,294,967,295

---

## prompt_u64

Quick unsigned 64-bit integer input prompt.

### Signature

```python
def prompt_u64(message: str) -> int:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `int`: The parsed unsigned 64-bit integer

### Raises

- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

### Example

```python
import pinq

timestamp = pinq.prompt_u64("Enter Unix timestamp: ")
print(f"Timestamp: {timestamp}")
```

---

## prompt_f32

Quick 32-bit float input prompt.

### Signature

```python
def prompt_f32(message: str) -> float:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `float`: The parsed 32-bit float

### Raises

- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

### Example

```python
import pinq

temperature = pinq.prompt_f32("Temperature (°C): ")
print(f"Temperature: {temperature:.1f}°C")
```

### Notes

- Lower precision than f64
- Useful for embedded or space-constrained applications

---

## prompt_f64

Quick 64-bit float input prompt.

### Signature

```python
def prompt_f64(message: str) -> float:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `float`: The parsed 64-bit float

### Raises

- `RuntimeError` - If not a TTY, IO error, operation canceled, or parse error

### Example

```python
import pinq

amount = pinq.prompt_f64("Enter amount: $")
print(f"Total: ${amount:.2f}")
```

### Notes

- Higher precision than f32
- Default choice for floating-point numbers

---

## prompt_date

Quick date selection using interactive calendar.

### Signature

```python
def prompt_date(message: str) -> str:
    ...
```

### Parameters

- `message` (str): The prompt text

### Returns

- `str`: The selected date in YYYY-MM-DD format

### Raises

- `RuntimeError` - If not a TTY, IO error, or operation canceled

### Example

```python
import pinq
from datetime import datetime

date_str = pinq.prompt_date("Select a date: ")
print(f"Selected: {date_str}")

# Parse for further use
date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
```

### Equivalent To

```python
prompt = pinq.DateSelectPrompt("Select a date: ")
date_str = prompt.prompt()
```

---

## One-Liner Comparison

### Quick Prompts vs Full Builder Pattern

**Using one-liners:**
```python
import pinq

name = pinq.prompt_text("Name: ")
age = pinq.prompt_int("Age: ")
confirmed = pinq.prompt_confirmation("Continue? ")
```

**Using builder pattern:**
```python
import pinq

prompt = pinq.TextPrompt("Name: ")
name = prompt.prompt()

prompt = pinq.IntPrompt("Age: ")
age = prompt.prompt()

prompt = pinq.ConfirmPrompt("Continue? ")
confirmed = prompt.prompt()
```

**Using builder with configuration:**
```python
import pinq

prompt = pinq.TextPrompt("Username: ")
prompt.with_default("admin")
prompt.with_help_message("Default: admin")
username = prompt.prompt()
```

### When to Use

- **One-liners**: Simple prompts without configuration
- **Builder pattern**: Complex prompts with defaults, help messages, etc.

---

## Error Handling

All functions can raise `RuntimeError` with messages like:

- `"Input is not a TTY"` - Not running in a terminal
- `"IO Error: ..."` - Operating system error
- `"Operation canceled by user"` - User pressed Ctrl+C or ESC
- `"Invalid configuration: ..."` - Invalid setup
- Custom parsing errors for typed prompts

### Example Error Handling

```python
import pinq

try:
    age = pinq.prompt_int("Your age: ")
except RuntimeError as e:
    print(f"Error: {e}")
    age = 0  # Default fallback
```

---

## Function Reference Table

| Function | Input Type | Return Type | Use Case |
|----------|-----------|-------------|----------|
| `prompt_text` | Free text | str | General text input |
| `prompt_secret` | Hidden text | str | Passwords, secrets |
| `prompt_confirmation` | Yes/No | bool | Confirmations |
| `prompt_int` | Integer | int | Whole numbers |
| `prompt_float` | Float | float | Decimal numbers (f64) |
| `prompt_u32` | Unsigned 32-bit | int | Port numbers, IDs |
| `prompt_u64` | Unsigned 64-bit | int | Large numbers, timestamps |
| `prompt_f32` | Float 32-bit | float | Space-constrained floats |
| `prompt_f64` | Float 64-bit | float | Precise decimals |
| `prompt_date` | Calendar | str | Date selection |

---

## See Also

- [Classes Reference](classes.md) - Detailed prompt class documentation
- [Builders Reference](builders.md) - Builder pattern examples
- [Examples](examples.md) - Real-world usage examples
