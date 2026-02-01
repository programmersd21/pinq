#!/usr/bin/env python3
"""
pinq - Comprehensive Examples

This file demonstrates EVERY feature of the pinq library with production-ready examples.
Each example is fully runnable and production-grade.

Contents:
1. Text Prompts (with defaults, help, pagination)
2. Confirmation Prompts
3. Password/Secret Prompts
4. Select Prompts (single choice)
5. MultiSelect Prompts (multiple choices)
6. Integer Prompts
7. Float Prompts
8. Date Selection Prompts
9. Editor Prompts
10. One-Liner Functions
11. Error Handling
12. Real-World Applications
13. Advanced Patterns
"""

import pinq # pyright: ignore[reportMissingModuleSource]
from datetime import datetime


# ============================================================================
# SECTION 1: TEXT PROMPTS
# ============================================================================

def example_text_basic():
    """Basic text prompt - simplest usage."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Text Prompt")
    print("="*60)
    
    name = pinq.prompt_text("What is your name?")
    print(f"Hello, {name}!")


def example_text_with_default():
    """Text prompt with default value."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Text Prompt with Default")
    print("="*60)
    
    username = pinq.TextPrompt("Enter username:").with_default("admin")
    result = username.prompt()
    print(f"Username: {result}")


def example_text_with_help():
    """Text prompt with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Text Prompt with Help Message")
    print("="*60)
    
    prompt = pinq.TextPrompt("Email address:")
    prompt.with_help_message("Format: user@example.com")
    email = prompt.prompt()
    print(f"Email: {email}")


def example_text_with_page_size():
    """Text prompt with pagination for autocompletion."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Text Prompt with Page Size")
    print("="*60)
    
    prompt = pinq.TextPrompt("Search term:")
    prompt.with_page_size(5)
    term = prompt.prompt()
    print(f"Searched for: {term}")


def example_text_all_options():
    """Text prompt with ALL options combined."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Text Prompt - All Features Combined")
    print("="*60)
    
    prompt = pinq.TextPrompt("Enter description:")
    prompt.with_default("No description")
    prompt.with_help_message("Leave blank for default, ESC to skip")
    prompt.with_page_size(10)
    
    description = prompt.prompt()
    print(f"Description: {description}")


def example_text_skippable():
    """Text prompt that can be skipped with ESC."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Skippable Text Prompt")
    print("="*60)
    
    prompt = pinq.TextPrompt("Optional comment (press ESC to skip):")
    comment = prompt.prompt_skippable()
    
    if comment is None:
        print("No comment provided")
    else:
        print(f"Comment: {comment}")


# ============================================================================
# SECTION 2: CONFIRMATION PROMPTS
# ============================================================================

def example_confirm_basic():
    """Basic yes/no confirmation."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Basic Confirmation")
    print("="*60)
    
    if pinq.prompt_confirmation("Do you want to continue?"):
        print("Continuing...")
    else:
        print("Cancelled.")


def example_confirm_with_default():
    """Confirmation with default answer."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Confirmation with Default")
    print("="*60)
    
    prompt = pinq.ConfirmPrompt("Delete file?")
    prompt.with_default(False)  # Default to NO
    
    if prompt.prompt():
        print("File deleted")
    else:
        print("File preserved")


def example_confirm_with_help():
    """Confirmation with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 9: Confirmation with Help")
    print("="*60)
    
    prompt = pinq.ConfirmPrompt("Apply changes?")
    prompt.with_help_message("This action cannot be undone")
    
    if prompt.prompt():
        print("Changes applied")
    else:
        print("Changes discarded")


def example_confirm_skippable():
    """Skippable confirmation."""
    print("\n" + "="*60)
    print("EXAMPLE 10: Skippable Confirmation")
    print("="*60)
    
    prompt = pinq.ConfirmPrompt("Proceed? (ESC to skip)")
    answer = prompt.prompt_skippable()
    
    if answer is None:
        print("Skipped")
    elif answer:
        print("Proceeding")
    else:
        print("Not proceeding")


# ============================================================================
# SECTION 3: PASSWORD PROMPTS
# ============================================================================

def example_password_basic():
    """Basic password input."""
    print("\n" + "="*60)
    print("EXAMPLE 11: Basic Password Prompt")
    print("="*60)
    
    password = pinq.PasswordPrompt("Enter password:").prompt()
    print(f"Password length: {len(password)} characters")


def example_password_with_help():
    """Password with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 12: Password with Help")
    print("="*60)
    
    prompt = pinq.PasswordPrompt("New password:")
    prompt.with_help_message("At least 8 characters")
    password = prompt.prompt()
    print(f"Password set ({len(password)} chars)")


def example_password_skippable():
    """Skippable password prompt."""
    print("\n" + "="*60)
    print("EXAMPLE 13: Skippable Password")
    print("="*60)
    
    prompt = pinq.PasswordPrompt("Enter password (ESC to skip):")
    password = prompt.prompt_skippable()
    
    if password is None:
        print("Password skipped")
    else:
        print(f"Password set ({len(password)} chars)")


# ============================================================================
# SECTION 4: SELECT PROMPTS (SINGLE CHOICE)
# ============================================================================

def example_select_basic():
    """Basic single-choice selection."""
    print("\n" + "="*60)
    print("EXAMPLE 14: Basic Select Prompt")
    print("="*60)
    
    colors = ["Red", "Green", "Blue"]
    choice = pinq.SelectPrompt("Pick a color:", colors).prompt()
    print(f"You picked: {choice}")


def example_select_with_default():
    """Select with default option."""
    print("\n" + "="*60)
    print("EXAMPLE 15: Select with Default")
    print("="*60)
    
    languages = ["Python", "Rust", "Go", "JavaScript", "C++"]
    prompt = pinq.SelectPrompt("Choose language:", languages)
    prompt.with_default(0)  # Default to Python
    
    language = prompt.prompt()
    print(f"Selected: {language}")


def example_select_with_help():
    """Select with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 16: Select with Help")
    print("="*60)
    
    options = ["Development", "Staging", "Production"]
    prompt = pinq.SelectPrompt("Environment:", options)
    prompt.with_help_message("Use arrow keys to navigate")
    
    env = prompt.prompt()
    print(f"Environment: {env}")


def example_select_with_page_size():
    """Select with custom page size."""
    print("\n" + "="*60)
    print("EXAMPLE 17: Select with Page Size")
    print("="*60)
    
    items = [f"Item {i}" for i in range(1, 21)]  # 20 items
    prompt = pinq.SelectPrompt("Choose item:", items)
    prompt.with_page_size(5)  # Show 5 at a time
    
    item = prompt.prompt()
    print(f"Selected: {item}")


def example_select_all_options():
    """Select with ALL options."""
    print("\n" + "="*60)
    print("EXAMPLE 18: Select - All Features")
    print("="*60)
    
    options = ["Option A", "Option B", "Option C", "Option D"]
    prompt = pinq.SelectPrompt("Choose one:", options)
    prompt.with_default(1)
    prompt.with_help_message("Press ENTER to select")
    prompt.with_page_size(4)
    
    choice = prompt.prompt()
    print(f"Choice: {choice}")


def example_select_skippable():
    """Skippable select prompt."""
    print("\n" + "="*60)
    print("EXAMPLE 19: Skippable Select")
    print("="*60)
    
    options = ["Yes", "No", "Maybe"]
    prompt = pinq.SelectPrompt("Do you agree? (ESC to skip):", options)
    
    choice = prompt.prompt_skippable()
    if choice is None:
        print("Skipped")
    else:
        print(f"Answer: {choice}")


# ============================================================================
# SECTION 5: MULTISELECT PROMPTS
# ============================================================================

def example_multiselect_basic():
    """Basic multi-select."""
    print("\n" + "="*60)
    print("EXAMPLE 20: Basic MultiSelect")
    print("="*60)
    
    items = ["Apples", "Bananas", "Carrots", "Dates"]
    selections = pinq.MultiSelectPrompt("Select fruits:", items).prompt()
    
    if selections:
        print(f"Selected: {', '.join(selections)}")
    else:
        print("Nothing selected")


def example_multiselect_with_defaults():
    """MultiSelect with default selections."""
    print("\n" + "="*60)
    print("EXAMPLE 21: MultiSelect with Defaults")
    print("="*60)
    
    features = ["Auth", "Cache", "Logging", "Monitoring", "Analytics"]
    prompt = pinq.MultiSelectPrompt("Enable features:", features)
    prompt.with_defaults([0, 2])  # Default: Auth and Logging
    
    selected = prompt.prompt()
    print(f"Enabled: {', '.join(selected)}")


def example_multiselect_with_help():
    """MultiSelect with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 22: MultiSelect with Help")
    print("="*60)
    
    options = ["Option 1", "Option 2", "Option 3"]
    prompt = pinq.MultiSelectPrompt("Select items:", options)
    prompt.with_help_message("SPACE to select, ENTER to confirm")
    
    selected = prompt.prompt()
    print(f"Selected {len(selected)} items: {', '.join(selected)}")


def example_multiselect_with_page_size():
    """MultiSelect with pagination."""
    print("\n" + "="*60)
    print("EXAMPLE 23: MultiSelect with Page Size")
    print("="*60)
    
    items = [f"Item {i}" for i in range(1, 21)]
    prompt = pinq.MultiSelectPrompt("Select items:", items)
    prompt.with_page_size(5)
    
    selected = prompt.prompt()
    print(f"Selected: {selected}")


def example_multiselect_all_options():
    """MultiSelect with ALL options."""
    print("\n" + "="*60)
    print("EXAMPLE 24: MultiSelect - All Features")
    print("="*60)
    
    tags = ["Python", "Rust", "Go", "JavaScript", "TypeScript", "C++"]
    prompt = pinq.MultiSelectPrompt("Languages you know:", tags)
    prompt.with_defaults([0, 3])  # Default: Python, JavaScript
    prompt.with_help_message("SPACE to toggle, ENTER to submit")
    prompt.with_page_size(4)
    
    languages = prompt.prompt()
    print(f"You know: {', '.join(languages)}")


def example_multiselect_skippable():
    """Skippable multi-select."""
    print("\n" + "="*60)
    print("EXAMPLE 25: Skippable MultiSelect")
    print("="*60)
    
    options = ["A", "B", "C"]
    prompt = pinq.MultiSelectPrompt("Choose (ESC to skip):", options)
    
    selections = prompt.prompt_skippable()
    if selections is None:
        print("Skipped")
    else:
        print(f"Selected: {selections}")


# ============================================================================
# SECTION 6: INTEGER PROMPTS
# ============================================================================

def example_int_basic():
    """Basic integer input."""
    print("\n" + "="*60)
    print("EXAMPLE 26: Basic Integer Prompt")
    print("="*60)
    
    age = pinq.prompt_int("Enter your age:")
    print(f"Age: {age}")


def example_int_with_default():
    """Integer with default."""
    print("\n" + "="*60)
    print("EXAMPLE 27: Integer with Default")
    print("="*60)
    
    prompt = pinq.IntPrompt("Port number:")
    prompt.with_default(8000)
    
    port = prompt.prompt()
    print(f"Port: {port}")


def example_int_with_help():
    """Integer with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 28: Integer with Help")
    print("="*60)
    
    prompt = pinq.IntPrompt("Enter count:")
    prompt.with_help_message("Must be between 1 and 100")
    
    count = prompt.prompt()
    print(f"Count: {count}")


def example_int_all_options():
    """Integer with ALL options."""
    print("\n" + "="*60)
    print("EXAMPLE 29: Integer - All Features")
    print("="*60)
    
    prompt = pinq.IntPrompt("How many items?")
    prompt.with_default(10)
    prompt.with_help_message("Must be positive")
    
    count = prompt.prompt()
    print(f"Processing {count} items")


def example_int_skippable():
    """Skippable integer prompt."""
    print("\n" + "="*60)
    print("EXAMPLE 30: Skippable Integer")
    print("="*60)
    
    prompt = pinq.IntPrompt("Enter number (ESC to skip):")
    num = prompt.prompt_skippable()
    
    if num is None:
        print("Skipped")
    else:
        print(f"Number: {num}")


# ============================================================================
# SECTION 7: FLOAT PROMPTS
# ============================================================================

def example_float_basic():
    """Basic float input."""
    print("\n" + "="*60)
    print("EXAMPLE 31: Basic Float Prompt")
    print("="*60)
    
    price = pinq.prompt_float("Enter price: $")
    print(f"Price: ${price:.2f}")


def example_float_with_default():
    """Float with default."""
    print("\n" + "="*60)
    print("EXAMPLE 32: Float with Default")
    print("="*60)
    
    prompt = pinq.FloatPrompt("Temperature (°C):")
    prompt.with_default(20.0)
    
    temp = prompt.prompt()
    print(f"Temperature: {temp}°C")


def example_float_with_help():
    """Float with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 33: Float with Help")
    print("="*60)
    
    prompt = pinq.FloatPrompt("Enter discount (%):")
    prompt.with_help_message("Between 0 and 100")
    
    discount = prompt.prompt()
    print(f"Discount: {discount}%")


def example_float_all_options():
    """Float with ALL options."""
    print("\n" + "="*60)
    print("EXAMPLE 34: Float - All Features")
    print("="*60)
    
    prompt = pinq.FloatPrompt("Amount:")
    prompt.with_default(99.99)
    prompt.with_help_message("Use decimal point")
    
    amount = prompt.prompt()
    print(f"Amount: {amount}")


def example_float_skippable():
    """Skippable float prompt."""
    print("\n" + "="*60)
    print("EXAMPLE 35: Skippable Float")
    print("="*60)
    
    prompt = pinq.FloatPrompt("Enter value (ESC to skip):")
    value = prompt.prompt_skippable()
    
    if value is None:
        print("Skipped")
    else:
        print(f"Value: {value}")


# ============================================================================
# SECTION 8: DATE SELECTION PROMPTS
# ============================================================================

def example_date_basic():
    """Basic date selection."""
    print("\n" + "="*60)
    print("EXAMPLE 36: Basic Date Selection")
    print("="*60)
    
    date_str = pinq.prompt_date("Select a date:")
    print(f"Selected: {date_str}")


def example_date_with_help():
    """Date selection with help."""
    print("\n" + "="*60)
    print("EXAMPLE 37: Date with Help")
    print("="*60)
    
    prompt = pinq.DateSelectPrompt("Meeting date:")
    prompt.with_help_message("Use arrow keys to navigate")
    
    date_str = prompt.prompt()
    print(f"Meeting: {date_str}")


def example_date_skippable():
    """Skippable date selection."""
    print("\n" + "="*60)
    print("EXAMPLE 38: Skippable Date Selection")
    print("="*60)
    
    prompt = pinq.DateSelectPrompt("Date (ESC to skip):")
    date_str = prompt.prompt_skippable()
    
    if date_str is None:
        print("No date selected")
    else:
        print(f"Date: {date_str}")


def example_date_parsing():
    """Date selection with parsing."""
    print("\n" + "="*60)
    print("EXAMPLE 39: Date Selection with Parsing")
    print("="*60)
    
    date_str = pinq.prompt_date("Select date:")
    
    # Parse the date string
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    print(f"Parsed: {parsed_date}")
    print(f"Day: {parsed_date.strftime('%A')}")


# ============================================================================
# SECTION 9: EDITOR PROMPTS
# ============================================================================

def example_editor_basic():
    """Basic editor prompt."""
    print("\n" + "="*60)
    print("EXAMPLE 40: Basic Editor Prompt")
    print("="*60)
    
    text = pinq.EditorPrompt("Write message:").prompt()
    print(f"Message length: {len(text)} characters")
    print("Preview:", text[:100])


def example_editor_with_help():
    """Editor with help message."""
    print("\n" + "="*60)
    print("EXAMPLE 41: Editor with Help")
    print("="*60)
    
    prompt = pinq.EditorPrompt("Write description:")
    prompt.with_help_message("Opens in your default editor")
    
    description = prompt.prompt()
    print(f"Description: {description[:50]}...")


def example_editor_skippable():
    """Skippable editor prompt."""
    print("\n" + "="*60)
    print("EXAMPLE 42: Skippable Editor")
    print("="*60)
    
    prompt = pinq.EditorPrompt("Notes (ESC to skip):")
    text = prompt.prompt_skippable()
    
    if text is None:
        print("No notes provided")
    else:
        print(f"Notes: {len(text)} characters")


# ============================================================================
# SECTION 10: ONE-LINER FUNCTIONS
# ============================================================================

def example_one_liners():
    """All one-liner functions."""
    print("\n" + "="*60)
    print("EXAMPLE 43: One-Liner Functions")
    print("="*60)
    
    # Text
    name = pinq.prompt_text("Name: ")
    print(f"Text: {name}")
    
    # Password
    pwd = pinq.prompt_secret("Secret: ")
    print(f"Secret length: {len(pwd)}")
    
    # Confirmation
    confirmed = pinq.prompt_confirmation("Confirm? ")
    print(f"Confirmed: {confirmed}")
    
    # Integer
    count = pinq.prompt_int("Count: ")
    print(f"Count: {count}")
    
    # Float
    amount = pinq.prompt_float("Amount: ")
    print(f"Amount: {amount}")
    
    # Unsigned integers
    u32 = pinq.prompt_u32("U32: ")
    u64 = pinq.prompt_u64("U64: ")
    print(f"U32: {u32}, U64: {u64}")
    
    # Float variants
    f32 = pinq.prompt_f32("F32: ")
    f64 = pinq.prompt_f64("F64: ")
    print(f"F32: {f32}, F64: {f64}")
    
    # Date
    date_str = pinq.prompt_date("Date: ")
    print(f"Date: {date_str}")


# ============================================================================
# SECTION 11: ERROR HANDLING
# ============================================================================

def example_error_handling():
    """Proper error handling."""
    print("\n" + "="*60)
    print("EXAMPLE 44: Error Handling")
    print("="*60)
    
    try:
        age = pinq.prompt_int("Age: ")
        print(f"Age: {age}")
    except RuntimeError as e:
        error_msg = str(e).lower()
        
        if "not a tty" in error_msg:
            print("Error: Not a TTY (not interactive)")
        elif "canceled" in error_msg:
            print("Error: Operation canceled by user")
        elif "invalid" in error_msg:
            print("Error: Invalid configuration")
        else:
            print(f"Error: {e}")


def example_retry_loop():
    """Retry pattern with validation."""
    print("\n" + "="*60)
    print("EXAMPLE 45: Retry Loop with Validation")
    print("="*60)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            age = pinq.prompt_int("Age (0-150): ")
            
            if 0 <= age <= 150:
                print(f"Valid age: {age}")
                break
            else:
                print("Age must be between 0 and 150")
        
        except RuntimeError as e:
            if "canceled" in str(e).lower():
                print("Canceled")
                break
            else:
                print(f"Error: {e}")
                if attempt == max_retries - 1:
                    print("Max retries reached")


def example_graceful_degradation():
    """Graceful fallback when not interactive."""
    print("\n" + "="*60)
    print("EXAMPLE 46: Graceful Degradation")
    print("="*60)
    
    import sys
    
    def get_input(prompt_text, default):
        try:
            return pinq.prompt_text(prompt_text)
        except RuntimeError as e:
            if "not a tty" in str(e).lower():
                print(f"Non-interactive mode, using default: {default}")
                return default
            elif "canceled" in str(e).lower():
                return None
            else:
                raise
    
    result = get_input("Name: ", "DefaultUser")
    print(f"Result: {result}")


# ============================================================================
# SECTION 12: REAL-WORLD APPLICATIONS
# ============================================================================

def example_user_registration():
    """Complete user registration form."""
    print("\n" + "="*60)
    print("EXAMPLE 47: User Registration Form")
    print("="*60)
    
    print("\n=== Registration ===\n")
    
    username = (pinq.TextPrompt("Username:")
                .with_default("user")
                .with_help_message("3-20 characters"))
    username = username.prompt()
    
    email = pinq.prompt_text("Email: ")
    
    password = pinq.PasswordPrompt("Password:").prompt()
    
    country = (pinq.SelectPrompt("Country:",
                                  ["USA", "Canada", "UK", "Australia"])
               .with_default(0))
    country = country.prompt()
    
    newsletter = pinq.prompt_confirmation("Subscribe to newsletter? ")
    
    print(f"\n✓ Registered: {username} from {country}")
    print(f"Newsletter: {'Yes' if newsletter else 'No'}")


def example_configuration_wizard():
    """Interactive configuration wizard."""
    print("\n" + "="*60)
    print("EXAMPLE 48: Configuration Wizard")
    print("="*60)
    
    print("\n=== Server Configuration ===\n")
    
    host = (pinq.TextPrompt("Hostname:")
            .with_default("localhost"))
    host = host.prompt()
    
    port = (pinq.IntPrompt("Port:")
            .with_default(8000)
            .with_help_message("1024-65535"))
    port = port.prompt()
    
    features = (pinq.MultiSelectPrompt("Features:",
                                        ["Auth", "Cache", "Logging", "Monitoring"])
                .with_defaults([0, 2]))
    features = features.prompt()
    
    env = (pinq.SelectPrompt("Environment:",
                             ["dev", "staging", "prod"])
           .with_default(0))
    env = env.prompt()
    
    print(f"\n✓ Config: {host}:{port} ({env})")
    print(f"Features: {', '.join(features)}")


def example_survey():
    """Customer feedback survey."""
    print("\n" + "="*60)
    print("EXAMPLE 49: Customer Survey")
    print("="*60)
    
    print("\n=== Feedback Survey ===\n")
    
    name = pinq.prompt_text("Name: ")
    
    rating = (pinq.SelectPrompt("Satisfaction:",
                                ["Poor", "Fair", "Good", "Excellent"])
              .with_default(2))
    rating = rating.prompt()
    
    feedback = (pinq.EditorPrompt("Comments:")
                .prompt_skippable())
    
    contact = pinq.prompt_confirmation("May we contact you? ")
    
    email = None
    if contact:
        email = pinq.prompt_text("Email: ")
    
    print(f"\n✓ Survey from {name}")
    print(f"Rating: {rating}")
    if email:
        print(f"Contact: {email}")


def example_todo_app():
    """Simple todo list application."""
    print("\n" + "="*60)
    print("EXAMPLE 50: Todo App")
    print("="*60)
    
    tasks = []
    
    while True:
        print(f"\n=== Todo ({len(tasks)} tasks) ===")
        
        action = (pinq.SelectPrompt("Action:",
                                    ["Add", "List", "Done", "Remove", "Exit"])
                  .with_default(0))
        action = action.prompt()
        
        if action == "Exit":
            break
        
        elif action == "Add":
            task = pinq.prompt_text("Task: ")
            priority = (pinq.SelectPrompt("Priority:",
                                          ["Low", "Medium", "High"])
                       .with_default(1))
            priority = priority.prompt()
            tasks.append({"task": task, "priority": priority, "done": False})
            print(f"✓ Added: {task}")
        
        elif action == "List":
            if not tasks:
                print("No tasks")
            else:
                for i, t in enumerate(tasks, 1):
                    status = "✓" if t["done"] else "[ ]"
                    print(f"{i}. {status} {t['task']} ({t['priority']})")
        
        elif action == "Done":
            if tasks:
                undone = [t for t in tasks if not t["done"]]
                if undone:
                    options = [t["task"] for t in undone]
                    choice = (pinq.SelectPrompt("Mark done:",
                                                options))
                    choice = choice.prompt()
                    for t in tasks:
                        if t["task"] == choice:
                            t["done"] = True
                            print(f"✓ Marked: {choice}")
        
        elif action == "Remove":
            if tasks:
                options = [t["task"] for t in tasks]
                choice = (pinq.SelectPrompt("Remove:",
                                            options))
                choice = choice.prompt()
                tasks = [t for t in tasks if t["task"] != choice]
                print(f"✓ Removed: {choice}")


# ============================================================================
# SECTION 13: ADVANCED PATTERNS
# ============================================================================

def example_chaining_pattern():
    """Method chaining pattern."""
    print("\n" + "="*60)
    print("EXAMPLE 51: Method Chaining Pattern")
    print("="*60)
    
    # Create and chain all methods in one call
    username = (pinq.TextPrompt("Username:")
                .with_default("admin")
                .with_help_message("3-20 chars")
                .with_page_size(10)
                .prompt())
    
    print(f"Username: {username}")


def example_multiple_validations():
    """Multiple validation attempts."""
    print("\n" + "="*60)
    print("EXAMPLE 52: Multiple Validations")
    print("="*60)
    
    while True:
        age = pinq.prompt_int("Age: ")
        
        if age < 0:
            print("Age cannot be negative")
        elif age > 150:
            print("Age seems unrealistic")
        else:
            print(f"✓ Valid age: {age}")
            break


def example_conditional_prompts():
    """Conditional prompts based on previous answers."""
    print("\n" + "="*60)
    print("EXAMPLE 53: Conditional Prompts")
    print("="*60)
    
    is_admin = pinq.prompt_confirmation("Are you an admin? ")
    
    if is_admin:
        role = (pinq.SelectPrompt("Role:",
                                  ["Root", "Moderator", "Operator"])
                .with_default(0))
        role = role.prompt()
        print(f"Admin role: {role}")
    else:
        print("User role: Guest")


def example_dynamic_options():
    """Dynamic options based on user input."""
    print("\n" + "="*60)
    print("EXAMPLE 54: Dynamic Options")
    print("="*60)
    
    category = (pinq.SelectPrompt("Category:",
                                  ["Food", "Clothing", "Electronics"])
                .with_default(0))
    category = category.prompt()
    
    # Dynamic options based on category
    options_map = {
        "Food": ["Pizza", "Burger", "Salad"],
        "Clothing": ["Shirt", "Pants", "Hat"],
        "Electronics": ["Phone", "Laptop", "Tablet"],
    }
    
    item = (pinq.SelectPrompt(f"Choose {category}:",
                              options_map[category])
            .with_default(0))
    item = item.prompt()
    
    print(f"Selected: {category} > {item}")


def example_batch_input():
    """Batch input collection."""
    print("\n" + "="*60)
    print("EXAMPLE 55: Batch Input Collection")
    print("="*60)
    
    results = {}
    
    results['name'] = pinq.prompt_text("Name: ")
    results['email'] = pinq.prompt_text("Email: ")
    results['age'] = pinq.prompt_int("Age: ")
    results['subscribe'] = pinq.prompt_confirmation("Subscribe? ")
    
    print("\n✓ Collection complete:")
    for key, value in results.items():
        print(f"  {key}: {value}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all examples."""
    import sys
    
    # List of all examples
    examples = [
        ("Text Prompts", [
            example_text_basic,
            example_text_with_default,
            example_text_with_help,
            example_text_with_page_size,
            example_text_all_options,
            example_text_skippable,
        ]),
        ("Confirmation Prompts", [
            example_confirm_basic,
            example_confirm_with_default,
            example_confirm_with_help,
            example_confirm_skippable,
        ]),
        ("Password Prompts", [
            example_password_basic,
            example_password_with_help,
            example_password_skippable,
        ]),
        ("Select Prompts", [
            example_select_basic,
            example_select_with_default,
            example_select_with_help,
            example_select_with_page_size,
            example_select_all_options,
            example_select_skippable,
        ]),
        ("MultiSelect Prompts", [
            example_multiselect_basic,
            example_multiselect_with_defaults,
            example_multiselect_with_help,
            example_multiselect_with_page_size,
            example_multiselect_all_options,
            example_multiselect_skippable,
        ]),
        ("Integer Prompts", [
            example_int_basic,
            example_int_with_default,
            example_int_with_help,
            example_int_all_options,
            example_int_skippable,
        ]),
        ("Float Prompts", [
            example_float_basic,
            example_float_with_default,
            example_float_with_help,
            example_float_all_options,
            example_float_skippable,
        ]),
        ("Date Prompts", [
            example_date_basic,
            example_date_with_help,
            example_date_skippable,
            example_date_parsing,
        ]),
        ("Editor Prompts", [
            example_editor_basic,
            example_editor_with_help,
            example_editor_skippable,
        ]),
        ("One-Liners", [
            example_one_liners,
        ]),
        ("Error Handling", [
            example_error_handling,
            example_retry_loop,
            example_graceful_degradation,
        ]),
        ("Real-World Apps", [
            example_user_registration,
            example_configuration_wizard,
            example_survey,
            example_todo_app,
        ]),
        ("Advanced Patterns", [
            example_chaining_pattern,
            example_multiple_validations,
            example_conditional_prompts,
            example_dynamic_options,
            example_batch_input,
        ]),
    ]
    
    print("\n" + "="*60)
    print("PINQ - COMPREHENSIVE EXAMPLES")
    print("="*60)
    print("\nSelect category:")
    
    categories = [cat for cat, _ in examples]
    category = pinq.SelectPrompt("Category:", categories).prompt()
    
    category_examples = next(exs for cat, exs in examples if cat == category)
    
    print("\n" + "="*60)
    print(f"SELECT EXAMPLE - {category}")
    print("="*60)
    
    example_names = [ex.__name__.replace("example_", "") for ex in category_examples]
    example_name = pinq.SelectPrompt("Example:", example_names).prompt()
    
    example_func = next(ex for ex in category_examples if example_name in ex.__name__)
    
    try:
        example_func()
    except RuntimeError as e:
        print(f"\nError: {e}")
    except KeyboardInterrupt:
        print("\n\nInterrupted")
    except EOFError:
        print("\n\nEnd of input (running in non-interactive mode?)")


if __name__ == "__main__":
    main()
    