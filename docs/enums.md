# pinq Enums Reference

This document describes all enum types available in the pinq module.

## PasswordDisplayMode

Controls how password input is displayed on screen.

### Variants

#### `PasswordDisplayMode.Masked`
Characters are shown but masked (e.g., as asterisks or dots).

```python
import pinq
# Implicitly used by PasswordPrompt
```

#### `PasswordDisplayMode.Hidden`
Characters are completely hidden; nothing appears as the user types.

```python
import pinq
# Implicitly used by PasswordPrompt
```

### Usage

`PasswordDisplayMode` is primarily used internally by `PasswordPrompt`. Currently, the Python binding uses the default behavior. Future versions may expose configuration of this mode.

### Related

- `PasswordPrompt` - Uses password display modes internally

---

## InputAction

Describes actions available during text input.

### Variants

#### `InputAction.NoChange`
No action was triggered; input continues normally.

#### `InputAction.Submit`
User submitted the input (pressed Enter).

#### `InputAction.Cancel`
User canceled input (pressed ESC).

#### `InputAction.Interrupt`
User interrupted input (pressed Ctrl+C).

### Usage

`InputAction` is part of inquire's internal action system. It may be exposed in future versions for custom input handling.

### Related

- `TextPrompt` - Uses input actions internally
- `ConfirmPrompt` - Uses input actions internally

---

## Enum Mapping from Rust

### Complete Enum List

| Rust Enum | Python Enum | Purpose |
|-----------|-------------|---------|
| `PasswordDisplayMode` | `PasswordDisplayMode` | Password display mode selection |
| `InputAction` | `InputAction` | Text input action types |

### Future Enums

The following enums exist in inquire but are not yet exposed in the Python binding:

- `Action` - Prompt-level action types
- `CustomTypePromptAction` - Custom type prompt actions
- `DateSelectPromptAction` - Date select prompt actions
- `EditorPromptAction` - Editor prompt actions
- `MultiSelectPromptAction` - Multi-select prompt actions
- `PasswordPromptAction` - Password prompt actions
- `SelectPromptAction` - Select prompt actions
- `TextPromptAction` - Text prompt actions

These will be exposed in future releases as the binding expands.

---

## Enum Features

### Equality

All enums support equality comparison:

```python
import pinq

mode1 = pinq.PasswordDisplayMode.Masked
mode2 = pinq.PasswordDisplayMode.Masked

if mode1 == mode2:
    print("Same mode")
```

### String Representation

All enums have proper string representation:

```python
import pinq

print(pinq.PasswordDisplayMode.Masked)  # PasswordDisplayMode.Masked
print(pinq.InputAction.Submit)          # InputAction.Submit
```

### Pattern Matching (Python 3.10+)

With Python 3.10+, you can use pattern matching:

```python
import pinq

action = pinq.InputAction.Submit

match action:
    case pinq.InputAction.Submit:
        print("User submitted")
    case pinq.InputAction.Cancel:
        print("User canceled")
    case _:
        print("Other action")
```

---

## Future Enum Exposure

When additional enums are exposed, they will follow the same patterns:

1. **Direct import from pinq module**
   ```python
   from pinq import SomeEnum
   ```

2. **Module access**
   ```python
   import pinq
   pinq.SomeEnum.Variant
   ```

3. **Full type hints**
   ```python
   def handle_action(action: pinq.SomeAction) -> None:
       ...
   ```

---

## See Also

- [Classes Reference](classes.md) - All prompt classes
- [Overview](overview.md) - Architecture and design
