# pinq Examples and Use Cases

Complete, runnable examples demonstrating pinq usage patterns.

---

## Quick Start Examples

### Example 1: Simple Greeting

```python
import pinq

name = pinq.prompt_text("What is your name? ")
print(f"Hello, {name}!")
```

**Output:**
```
What is your name? Alice
Hello, Alice!
```

### Example 2: Confirmation Dialog

```python
import pinq

if pinq.prompt_confirmation("Do you want to continue? "):
    print("Processing...")
else:
    print("Canceled.")
```

**Output:**
```
Do you want to continue? (y/n) y
Processing...
```

### Example 3: Selection Menu

```python
import pinq

colors = ["Red", "Green", "Blue"]
choice = pinq.SelectPrompt("Pick a color:", colors).prompt()
print(f"You chose: {choice}")
```

**Output:**
```
Pick a color:
> Red
  Green
  Blue
You chose: Red
```

### Example 4: Multiple Selection

```python
import pinq

fruits = ["Apple", "Banana", "Orange", "Grape"]
selected = pinq.MultiSelectPrompt("Select fruits:", fruits).prompt()
print(f"Selected: {', '.join(selected)}")
```

**Output:**
```
Select fruits:
[X] Apple
[ ] Banana
[X] Orange
[ ] Grape
Selected: Apple, Orange
```

### Example 5: Number Input

```python
import pinq

age = pinq.prompt_int("Enter your age: ")
print(f"In 10 years, you will be {age + 10}")
```

**Output:**
```
Enter your age: 25
In 10 years, you will be 35
```

---

## Real-World Application Examples

### Example: User Registration Form

```python
import pinq

def register_user():
    """Interactive user registration."""
    
    print("=== User Registration ===\n")
    
    # Get basic information
    username = (pinq.TextPrompt("Username: ")
        .with_default("user")
        .with_help_message("3-20 alphanumeric characters")
        .prompt())
    
    email = pinq.prompt_text("Email: ")
    
    password = pinq.PasswordPrompt("Password: ").prompt()
    
    # Confirm details
    country = (pinq.SelectPrompt("Country:", 
        ["USA", "Canada", "UK", "Australia", "Other"])
        .with_default(0)
        .prompt())
    
    subscribe = pinq.prompt_confirmation("Subscribe to newsletter? ")
    
    # Summary
    print("\n=== Registration Summary ===")
    print(f"Username:  {username}")
    print(f"Email:     {email}")
    print(f"Country:   {country}")
    print(f"Newsletter: {subscribe}")
    
    confirm = pinq.prompt_confirmation("\nConfirm registration? ")
    return confirm

if __name__ == "__main__":
    if register_user():
        print("✓ Registration complete!")
    else:
        print("✗ Registration canceled")
```

### Example: Interactive CLI Tool

```python
import pinq

def file_manager():
    """Simple file management interface."""
    
    while True:
        action = pinq.SelectPrompt("What do you want to do?",
            ["Create", "Read", "Update", "Delete", "Exit"]
        ).prompt()
        
        if action == "Exit":
            break
        
        filename = pinq.prompt_text("Filename: ")
        
        if action == "Create":
            content = pinq.EditorPrompt("File content:").prompt()
            print(f"Created {filename} with {len(content)} bytes")
        
        elif action == "Read":
            print(f"Reading {filename}...")
        
        elif action == "Update":
            new_content = pinq.EditorPrompt(f"Edit {filename}:").prompt()
            print(f"Updated {filename}")
        
        elif action == "Delete":
            confirm = pinq.prompt_confirmation(f"Delete {filename}? ")
            if confirm:
                print(f"Deleted {filename}")

if __name__ == "__main__":
    file_manager()
```

### Example: Configuration Wizard

```python
import pinq

def setup_server():
    """Interactive server configuration wizard."""
    
    print("=== Server Setup Wizard ===\n")
    
    # Step 1: Basic settings
    hostname = (pinq.TextPrompt("Server hostname: ")
        .with_default("localhost")
        .prompt())
    
    port = (pinq.IntPrompt("Port: ")
        .with_default(8000)
        .with_help_message("1024-65535")
        .prompt())
    
    # Step 2: Features
    features = (pinq.MultiSelectPrompt("Enable features:",
        ["Authentication", "Caching", "Logging", "Monitoring", "Analytics"])
        .with_defaults([0, 2])  # Default: Auth and Logging
        .with_help_message("SPACE to toggle, ENTER to confirm")
        .prompt())
    
    # Step 3: Environment
    env = (pinq.SelectPrompt("Environment:",
        ["Development", "Staging", "Production"])
        .with_default(0)
        .prompt())
    
    # Step 4: Advanced options
    advanced = pinq.prompt_confirmation("Configure advanced options? ")
    
    ssl = False
    workers = 4
    
    if advanced:
        ssl = pinq.prompt_confirmation("Enable SSL/TLS? ")
        workers = (pinq.IntPrompt("Worker threads: ")
            .with_default(4)
            .prompt())
    
    # Display summary
    print("\n=== Configuration Summary ===")
    print(f"Hostname:   {hostname}")
    print(f"Port:       {port}")
    print(f"Features:   {', '.join(features) if features else 'None'}")
    print(f"Environment: {env}")
    print(f"SSL:        {ssl}")
    print(f"Workers:    {workers}")
    
    if pinq.prompt_confirmation("Apply configuration? "):
        print("✓ Configuration applied!")
        return True
    else:
        print("✗ Configuration canceled")
        return False

if __name__ == "__main__":
    setup_server()
```

### Example: Survey Application

```python
import pinq

def survey():
    """Interactive survey with optional questions."""
    
    print("=== Customer Feedback Survey ===\n")
    
    name = pinq.prompt_text("Your name: ")
    
    rating = (pinq.SelectPrompt("How satisfied are you?",
        ["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"])
        .with_default(2)
        .prompt())
    
    # Optional detailed feedback
    feedback = (pinq.EditorPrompt("Additional feedback (optional):")
        .with_help_message("Press ESC to skip")
        .prompt_skippable())
    
    # Collect contact info
    contact_ok = pinq.prompt_confirmation("May we contact you for follow-up? ")
    
    email = None
    if contact_ok:
        email = pinq.prompt_text("Email address: ")
    
    # Topics of interest
    topics = (pinq.MultiSelectPrompt("Interested in:",
        ["Product Updates", "Tips & Tricks", "Special Offers", "Company News"])
        .with_defaults([0, 2])
        .prompt())
    
    # Summary
    print("\n=== Survey Response ===")
    print(f"Name: {name}")
    print(f"Satisfaction: {rating}")
    print(f"Feedback: {feedback[:50]}..." if feedback else "Feedback: (none)")
    print(f"Email: {email if email else '(not provided)'}")
    print(f"Interests: {', '.join(topics) if topics else '(none)'}")

if __name__ == "__main__":
    survey()
```

### Example: DevOps Deployment Tool

```python
import pinq

def deploy_app():
    """Interactive application deployment tool."""
    
    print("=== Application Deployment ===\n")
    
    # Select service
    service = (pinq.SelectPrompt("Select service to deploy:",
        ["API Server", "Web UI", "Worker", "Database", "Cache"])
        .prompt())
    
    # Select version
    version = (pinq.TextPrompt("Version to deploy: ")
        .with_default("latest")
        .prompt())
    
    # Select environment
    env = (pinq.SelectPrompt("Target environment:",
        ["Development", "Staging", "Production"])
        .with_default(1)
        .prompt())
    
    # Deployment options
    options = (pinq.MultiSelectPrompt("Deployment options:",
        ["Run migrations", "Rebuild cache", "Restart workers", 
         "Health check", "Notify team"])
        .with_defaults([0, 1, 3])
        .prompt())
    
    # Confirm high-risk operations
    if env == "Production":
        confirm = pinq.prompt_confirmation(
            f"⚠️  Deploy {service} v{version} to PRODUCTION? ")
        if not confirm:
            print("✗ Deployment canceled")
            return
    
    # Backup option for production
    if env == "Production" and "Run migrations" in options:
        backup = pinq.prompt_confirmation("Create database backup first? ")
        if backup:
            options.append("Create backup")
    
    # Execute deployment
    print(f"\n🚀 Deploying {service} {version} to {env}")
    for option in options:
        print(f"  ✓ {option}")
    
    print("✓ Deployment complete!")

if __name__ == "__main__":
    deploy_app()
```

### Example: Financial Calculator

```python
import pinq

def loan_calculator():
    """Interactive loan and interest calculator."""
    
    print("=== Loan Calculator ===\n")
    
    # Get loan parameters
    principal = (pinq.FloatPrompt("Principal amount: $")
        .with_default(100000.0)
        .with_help_message("Enter without $ or commas")
        .prompt())
    
    rate = (pinq.FloatPrompt("Annual interest rate (%): ")
        .with_default(5.0)
        .prompt())
    
    years = (pinq.IntPrompt("Loan term (years): ")
        .with_default(30)
        .prompt())
    
    # Calculate
    months = years * 12
    monthly_rate = rate / 100 / 12
    
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = (principal * monthly_rate * 
            (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    total_paid = monthly_payment * months
    total_interest = total_paid - principal
    
    # Display results
    print("\n=== Loan Summary ===")
    print(f"Principal:       ${principal:,.2f}")
    print(f"Interest Rate:   {rate:.2f}%")
    print(f"Loan Term:       {years} years ({months} months)")
    print(f"Monthly Payment: ${monthly_payment:,.2f}")
    print(f"Total Paid:      ${total_paid:,.2f}")
    print(f"Total Interest:  ${total_interest:,.2f}")
    
    # Save results?
    save = pinq.prompt_confirmation("Save results to file? ")
    if save:
        filename = (pinq.TextPrompt("Filename: ")
            .with_default("loan_calculation.txt")
            .prompt())
        print(f"Saved to {filename}")

if __name__ == "__main__":
    loan_calculator()
```

### Example: Task Manager

```python
import pinq

def task_manager():
    """Interactive task/todo manager."""
    
    tasks = []
    
    while True:
        print(f"\n=== Task Manager ({len(tasks)} tasks) ===")
        
        action = pinq.SelectPrompt("What do you want to do?",
            ["Add Task", "View Tasks", "Complete Task", "Delete Task", "Exit"]
        ).prompt()
        
        if action == "Exit":
            break
        
        elif action == "Add Task":
            task = (pinq.TextPrompt("Task description: ")
                .with_help_message("What needs to be done?")
                .prompt())
            priority = (pinq.SelectPrompt("Priority:",
                ["Low", "Medium", "High"])
                .with_default(1)
                .prompt())
            tasks.append({"desc": task, "priority": priority, "done": False})
            print(f"✓ Added: {task}")
        
        elif action == "View Tasks":
            if not tasks:
                print("No tasks yet!")
            else:
                for i, task in enumerate(tasks, 1):
                    status = "✓" if task["done"] else "[ ]"
                    print(f"{i}. {status} {task['desc']} ({task['priority']})")
        
        elif action == "Complete Task":
            if tasks:
                task_desc = [t["desc"] for t in tasks]
                choice = (pinq.SelectPrompt("Mark as complete:",
                    task_desc)
                    .prompt())
                for task in tasks:
                    if task["desc"] == choice:
                        task["done"] = True
                        print(f"✓ Marked complete: {choice}")
        
        elif action == "Delete Task":
            if tasks:
                task_desc = [t["desc"] for t in tasks]
                choice = (pinq.SelectPrompt("Delete task:",
                    task_desc)
                    .prompt())
                tasks = [t for t in tasks if t["desc"] != choice]
                print(f"✓ Deleted: {choice}")

if __name__ == "__main__":
    task_manager()
```

---

## Error Handling Examples

### Example: Robust Integer Input

```python
import pinq

def get_positive_integer(prompt_text):
    """Get a positive integer with validation."""
    while True:
        try:
            value = pinq.prompt_int(f"{prompt_text}: ")
            if value > 0:
                return value
            else:
                print("Please enter a positive number")
        except RuntimeError as e:
            if "canceled" in str(e).lower():
                return None
            print(f"Invalid input: {e}")

count = get_positive_integer("How many items")
if count:
    print(f"Processing {count} items...")
```

### Example: Fallback for Non-Interactive

```python
import pinq
import sys

def safe_prompt(message, default=None):
    """Prompt with fallback for non-interactive mode."""
    if sys.stdin.isatty():
        try:
            return pinq.prompt_text(message)
        except RuntimeError as e:
            if "not a tty" in str(e).lower():
                pass  # Fall through to default
            else:
                raise
    
    if default is not None:
        print(f"{message} [default: {default}]")
        return default
    else:
        raise RuntimeError("Cannot prompt in non-interactive mode")
```

---

## Performance Tips

### Batch Operations

```python
import pinq

def setup_multiple_users(count):
    """Create multiple users efficiently."""
    users = []
    
    for i in range(count):
        print(f"\nUser {i+1}/{count}")
        user = pinq.prompt_text(f"Username: ")
        email = pinq.prompt_text(f"Email: ")
        users.append({"username": user, "email": email})
    
    return users
```

### Minimize Prompts

```python
import pinq

# Good: One multi-select instead of multiple confirms
selections = pinq.MultiSelectPrompt("Choose options:",
    ["Option 1", "Option 2", "Option 3"]).prompt()

# Less efficient: Three separate prompts
opt1 = pinq.prompt_confirmation("Option 1? ")
opt2 = pinq.prompt_confirmation("Option 2? ")
opt3 = pinq.prompt_confirmation("Option 3? ")
```

---

## Testing Examples

### Unit Testing with Mocks

```python
import pinq
import unittest
from unittest.mock import patch

class TestMyApp(unittest.TestCase):
    @patch('pinq.prompt_text')
    def test_user_greeting(self, mock_prompt):
        mock_prompt.return_value = "Alice"
        
        result = get_greeting()
        self.assertEqual(result, "Hello, Alice!")
        mock_prompt.assert_called_once()
```

---

## See Also

- [Classes Reference](classes.md) - All prompt classes
- [Functions Reference](functions.md) - One-liner functions
- [Builders Reference](builders.md) - Builder pattern examples
- [Error Handling](errors.md) - Error handling guide
