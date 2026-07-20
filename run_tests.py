#!/usr/bin/env python
# run_tests.py - Run all tests with coverage

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print the output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    return result.returncode

def main():
    """Run all tests and quality checks."""
    print("🚀 Running Test Suite for Ethiopia Financial Inclusion Forecast")
    print("="*60)
    
    tests_passed = True
    
    # 1. Run pytest with coverage
    if run_command("pytest tests/ -v --cov=. --cov-report=html", "Unit Tests with Coverage") != 0:
        tests_passed = False
    
    # 2. Run flake8
    if run_command("flake8 . --count --max-complexity=10 --max-line-length=127 --statistics", "Flake8 Linting") != 0:
        tests_passed = False
    
    # 3. Run black (check formatting)
    if run_command("black --check .", "Black Formatting Check") != 0:
        tests_passed = False
    
    # 4. Run isort (check import sorting)
    if run_command("isort --check-only .", "Import Sorting Check") != 0:
        tests_passed = False
    
    # 5. Run bandit (security)
    if run_command("bandit -r .", "Security Scanning") != 0:
        tests_passed = False
    
    print("\n" + "="*60)
    if tests_passed:
        print("✅ All tests passed! 🎉")
    else:
        print("❌ Some tests failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()