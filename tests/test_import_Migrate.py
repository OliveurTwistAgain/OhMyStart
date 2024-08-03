try:
    from flask_migrate import Migrate
    print("Flask-Migrate imported successfully.")
except ImportError as e:
    print(f"ImportError: {e}")
