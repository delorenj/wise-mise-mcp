#!/usr/bin/env python3
"""
Publication script for wise-mise-mcp package
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"🔄 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    
    if result.stdout.strip():
        print(f"✅ Output: {result.stdout.strip()}")
    
    return result

def main():
    """Main publication workflow."""
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"
    
    print("🚀 Starting PyPI publication process...")
    
    # Clean previous builds
    print("\n1. Cleaning previous builds...")
    run_command("rm -rf build dist *.egg-info")
    
    # Build the package
    print("\n2. Building package...")
    run_command("uv run python -m build")
    
    # Validate the package
    print("\n3. Validating package...")
    run_command("uv run twine check dist/*")
    
    # List built files
    print("\n4. Built files:")
    for file in dist_dir.glob("*"):
        size = file.stat().st_size
        print(f"   📦 {file.name} ({size:,} bytes)")
    
    print("\n✅ Package is ready for publication!")
    print("\n🔄 Next steps:")
    print("   1. Set PyPI token: export TWINE_PASSWORD=your_pypi_token")
    print("   2. Publish to TestPyPI (optional):")
    print("      uv run twine upload --repository testpypi dist/*")
    print("   3. Publish to PyPI:")
    print("      uv run twine upload dist/*")
    print("   4. Verify installation:")
    print("      uv add wise-mise-mcp")
    
    # Prompt for immediate publication
    response = input("\n❓ Do you want to publish to PyPI now? (y/N): ").lower().strip()
    
    if response == 'y':
        print("\n🚀 Publishing to PyPI...")
        try:
            run_command("uv run twine upload dist/*")
            print("\n🎉 Successfully published to PyPI!")
            print("   📦 Package: https://pypi.org/project/wise-mise-mcp/")
            print("   📥 Install: uv add wise-mise-mcp")
        except SystemExit:
            print("\n❌ Publication failed. Please check your PyPI token and try again.")
            print("   💡 Set token: export TWINE_PASSWORD=your_pypi_token")
    else:
        print("\n⏸️  Publication skipped. Package is ready when you are!")

if __name__ == "__main__":
    main()