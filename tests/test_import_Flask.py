# test_imports.py
try:
    from flask import Flask
    print("Flask imported successfully.")
except ImportError as e:
    print(f"Error importing Flask: {e}")
