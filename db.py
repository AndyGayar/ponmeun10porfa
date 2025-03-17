# db.py
import mysql.connector
from mysql.connector import Error
from config import Config

def get_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def query(sql, params=None):
    """Execute a query and return all results"""
    connection = get_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def query_one(sql, params=None):
    """Execute a query and return the first result"""
    connection = get_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute(sql, params=None):
    """Execute a query that modifies data (INSERT, UPDATE, DELETE)"""
    connection = get_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, params or ())
        connection.commit()
        return True
    except Error as e:
        print(f"Error executing query: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()