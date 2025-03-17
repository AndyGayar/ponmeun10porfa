# config.py
import os

class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change this to a secure random key
    
    # Database settings
    DB_HOST = 'localhost'
    DB_NAME = 'notas'  # Update with your actual database name
    DB_USER = 'root'       # Update with your actual database username
    DB_PASSWORD = ''       # Update with your actual database password

    # Otras configuraciones que requieras...