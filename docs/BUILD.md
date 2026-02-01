# pinq - Build Instructions

Complete guide to building and installing the pinq Python package.

## Prerequisites

### Required

- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **Rust 1.66+** - Install from [rustup.rs](https://rustup.rs/)
- **pip** - Usually included with Python

### Recommended

- **virtualenv** - For isolated Python environments (optional)

## Installation from Source

### Step 1: Clone or Extract the Project

```bash
# Extract the pinq archive
unzip pinq-0.1.0.zip
cd pinq
```

### Step 2: Install Build Dependencies

The build system (Maturin) handles most dependencies automatically. Just ensure you have the basic tools:

```bash
# Update pip
pip install --upgrade pip

# Install build tools (if needed)
pip install --upgrade setuptools wheel
```

### Step 3: Build and Install

```bash
# Install from source (includes building the Rust extension)
pip install .
```

This command will:
1. Download Rust dependencies
2. Compile the Rust code to a Python extension
3. Package it as a wheel
4. Install the package in your Python environment

### Step 4: Verify Installation

```bash
python -c "import pinq; print(pinq.__version__)"
# Output: 0.1.0
```

## Development Installation

For development, use editable mode:

```bash
# Install in editable/development mode
pip install -e .

# Now you can edit Python code and it's immediately available
# For Rust changes, you need to rebuild: pip install --force-reinstall -e .
```

## Building Just the Wheel

To build a distributable wheel file:

```bash
# Install maturin (the build system)
pip install maturin

# Build the wheel
maturin build --release

# The wheel is now in target/wheels/
ls target/wheels/
```

This creates a `.whl` file that can be shared and installed on compatible systems.

## Platform-Specific Build Instructions

### Linux

```bash
# Ensure you have build tools
sudo apt-get install build-essential python3-dev

# Build
pip install .
```

### macOS

```bash
# Using Homebrew (recommended)
brew install python rust

# Build
pip install .
```

### Windows

```bash
# Ensure Rust is installed (from rustup.rs)
# And Python is available in PATH

# In Command Prompt or PowerShell:
pip install .
```

### WSL (Windows Subsystem for Linux)

Follow Linux instructions above. WSL provides a full Linux environment.

## Troubleshooting Build Issues

### Issue: "Rust compiler not found"

**Solution:** Install Rust from [rustup.rs](https://rustup.rs/)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Issue: "Python development headers not found"

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-dev
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-devel
```

**macOS:** Usually not needed if using Homebrew Python

### Issue: "maturin not found"

**Solution:**
```bash
pip install maturin
```

### Issue: Build fails with "permission denied"

**Solution:** Use a virtual environment or add `--user`:

```bash
# Option 1: Virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install .

# Option 2: User install
pip install --user .
```

### Issue: "error: linker `cc` not found"

**Solution:** Install a C compiler

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install build-essential
```

**macOS:**
```bash
xcode-select --install
```

**Windows:** Install Visual C++ Build Tools from [Visual Studio](https://visualstudio.microsoft.com/downloads/)

## Testing the Build

After installation, verify everything works:

```bash
# Test import
python -c "import pinq; print('✓ pinq imported successfully')"

# Test basic functionality
python << 'EOF'
import pinq

# This will hang waiting for input, so we skip the actual prompt
print("✓ All classes available:")
print(f"  - TextPrompt: {pinq.TextPrompt}")
print(f"  - ConfirmPrompt: {pinq.ConfirmPrompt}")
print(f"  - SelectPrompt: {pinq.SelectPrompt}")
print(f"  - MultiSelectPrompt: {pinq.MultiSelectPrompt}")
print(f"  - IntPrompt: {pinq.IntPrompt}")
print(f"  - FloatPrompt: {pinq.FloatPrompt}")
print(f"  - PasswordPrompt: {pinq.PasswordPrompt}")
print(f"  - DateSelectPrompt: {pinq.DateSelectPrompt}")
print(f"  - EditorPrompt: {pinq.EditorPrompt}")
EOF
```

## Uninstallation

```bash
pip uninstall pinq
```

## Advanced Build Options

### Building in Release Mode (Optimized)

```bash
# Default uses release mode, but to be explicit:
maturin build --release
```

### Building in Debug Mode

```bash
maturin build
```

Debug builds are faster to compile but slower to run.

### Building for a Specific Python Version

```bash
# Build for Python 3.10 specifically
maturin build --python 3.10
```

### Building Multiple Wheels

```bash
# Build wheels for multiple Python versions
for python in python3.8 python3.9 python3.10 python3.11; do
    maturin build -i $python
done
```

## Distribution

### Publishing to PyPI

```bash
# 1. Build wheels
maturin build --release

# 2. Install twine
pip install twine

# 3. Upload (requires PyPI account)
twine upload target/wheels/*
```

### Creating a Source Distribution

```bash
# Create a .tar.gz source distribution
python setup.py sdist
```

## Performance Optimization

The Cargo.toml is configured with optimizations for release builds:

```toml
[profile.release]
opt-level = 3
lto = true  # Link-time optimization
```

These are enabled by default when using `pip install .` for production use.

## Platform Wheels

Maturin automatically creates platform-specific wheels:

- **Linux:** `.manylinux` wheels (compatible with many Linux distributions)
- **macOS:** Universal2 wheels (support both Intel and Apple Silicon)
- **Windows:** Compatible with Windows 10+

## Environment Variables

### Customizing the Build

```bash
# Set number of parallel compilation jobs
export NUM_JOBS=4

# Specify Python interpreter
export PYTHON_INTERPRETER=/usr/bin/python3.11

# Then build
pip install .
```

## Incremental Builds

After the first build, rebuilding is faster:

```bash
# First build (takes time)
pip install -e .

# Modify src/lib.rs...

# Rebuild (faster, only changed parts)
pip install --force-reinstall -e .
```

## Troubleshooting with Verbose Output

```bash
# Verbose pip output
pip install -v .

# Verbose maturin output
maturin build -v
```

## System Requirements

Minimum:
- 512 MB disk space
- 1 GB RAM
- 10 minutes compilation time (first build)

Recommended:
- 2 GB disk space
- 4 GB RAM
- Parallel compilation (auto-detected)

## Docker Build Example

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /pinq
COPY . .

RUN pip install .

RUN python -c "import pinq; print(f'pinq {pinq.__version__} installed')"
```

## CI/CD Example (GitHub Actions)

```yaml
name: Build and Test

on: [push]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      - name: Install
        run: pip install .
      - name: Test
        run: python -c "import pinq; print(pinq.__version__)"
```

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review the [official documentation](docs/overview.md)
3. Check the [inquire repository](https://github.com/mikaelmello/inquire) for upstream issues
4. Open an issue with detailed error messages and system information

## Next Steps

After installation:

1. Read the [Quick Start Guide](README.md)
2. Explore [Examples](docs/examples.md)
3. Check [Complete API Reference](docs/overview.md)

Enjoy building interactive CLI applications with pinq! 🚀
