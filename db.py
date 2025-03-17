# db.py
import pymysql
from config import Config

# Database connection variable
_connection = None

def get_connection():
    """Get a database connection or create a new one if none exists"""
    global _connection
    
    if _connection is None or not _connection.open:
        _connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            db=Config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    return _connection

def query(query_string, params=None):
    """Execute a query and return all results"""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query_string, params or ())
        result = cursor.fetchall()
    return result

def query_one(query_string, params=None):
    """Execute a query and return the first result"""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query_string, params or ())
        result = cursor.fetchone()
    return result

def execute(query_string, params=None):
    """Execute a query without returning results (INSERT, UPDATE, DELETE)"""
    conn = get_connection()
    with conn.cursor() as cursor:
        affected_rows = cursor.execute(query_string, params or ())
        conn.commit()
    return affected_rows