#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path
import argparse
import shutil

GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
YELLOW = "\033[33m"
NC = "\033[0m"

def write_success(msg): print(f"{GREEN}✓{NC} {msg}")
def write_info(msg):    print(f"{CYAN}ℹ{NC} {msg}")
def write_error(msg):   print(f"{RED}✗{NC} {msg}")
def write_warning(msg): print(f"{YELLOW}⚠{NC} {msg}")

parser = argparse.ArgumentParser(description="pinq Build Script for Python")
parser.add_argument("--no-install", action="store_true")
parser.add_argument("--no-force-reinstall", action="store_true")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--release", action="store_true", default=True)
parser.add_argument("--clean", action="store_true")
parser.add_argument("--python", default=sys.executable)
args = parser.parse_args()

# Set project root
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
os.chdir(project_root)
write_info(f"pinq Build Script")
write_info(f"Project root: {project_root}")

# Check Python
try:
    py_ver = subprocess.check_output([args.python, "--version"], stderr=subprocess.STDOUT, text=True).strip()
    write_success(f"Python found: {py_ver}")
except Exception:
    write_error(f"Python not found: {args.python}")
    sys.exit(1)

# Check Rust
try:
    rust_ver = subprocess.check_output(["rustc", "--version"], text=True).strip()
    write_success(f"Rust found: {rust_ver}")
except Exception:
    write_error("Rust not found. Install via https://rustup.rs/")
    sys.exit(1)

# Build mode
build_mode = ["--debug"] if args.debug else ["--release"]
write_info(f"{'DEBUG' if args.debug else 'RELEASE'} build mode")

# Clean
if args.clean:
    write_info("Cleaning build artifacts...")
    for folder in ["target", "build", "dist"]:
        shutil.rmtree(project_root / folder, ignore_errors=True)
    write_success("Cleaned")

# Create dist folder
dist_path = project_root / "dist"
dist_path.mkdir(exist_ok=True)
write_success(f"dist ready: {dist_path}")

# Check/install maturin
try:
    subprocess.run([args.python, "-m", "pip", "show", "maturin"], check=True, stdout=subprocess.DEVNULL)
    write_success("maturin already installed")
except subprocess.CalledProcessError:
    write_warning("maturin not found, installing...")
    subprocess.run([args.python, "-m", "pip", "install", "maturin", "--quiet"], check=True)
    write_success("maturin installed")

# Build wheel
write_info("Building wheel...")
# Forward-compatible build with abi3 forward compatibility for newer Python versions
build_env = os.environ.copy()
build_env["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1"
build_env["PYO3_PYTHON_VERSION"] = "3.8"
maturin_cmd = [
    args.python, "-m", "maturin", "build",
    *build_mode,
    "--out", str(dist_path)
]

try:
    subprocess.run(maturin_cmd, check=True, env=build_env)
    write_success("Build completed")
except subprocess.CalledProcessError:
    write_error("Build failed")
    sys.exit(1)
    
# Find latest wheel
wheels = sorted(dist_path.glob("*.whl"), key=lambda f: f.stat().st_mtime)
if not wheels:
    write_error(f"No wheel found in {dist_path}")
    sys.exit(1)
wheel_path = wheels[-1]
write_success(f"Wheel: {wheel_path.name}")

# Install wheel
if not args.no_install:
    install_cmd = [args.python, "-m", "pip", "install", str(wheel_path)]
    if not args.no_force_reinstall:
        install_cmd.append("--force-reinstall")
    try:
        subprocess.run(install_cmd, check=True)
        write_success("Installed successfully")
        version_check = subprocess.check_output([args.python, "-c", "import pinq; print(pinq.__version__)"], text=True).strip()
        write_success(f"Verified: {version_check}")
    except subprocess.CalledProcessError:
        write_error("Installation or verification failed")
        sys.exit(1)
else:
    write_info(f"Skipping installation. Wheel at: {wheel_path}")

write_success("Build Complete!")
sys.exit(0)
