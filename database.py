# database.py
# Database connection and utility functions

import mysql.connector
from mysql.connector import Error
from database_config import DB_CONFIG

def get_connection():
    """
    Creates and returns a connection to MySQL database.

    Returns:
      connection: MySQL connection object or None if connection fails
    """
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

    return connection

def close_connection(connection):
    """
    Safely closes the database connection.

    Args:
        connection: MySQL connection object closed
    """
    if connection and connection.is_connected():
       connection.close()
       print("✅ MySQL connection closed")

def test_connection():
    """
    Simple function to test we can connect to the database.
    Useful for troubleshooting
    """
    connection = get_connection()
    if connection:
        close_connection(connection)
        return True
    return False

# Run this if you excute the file directly
if __name__ == "__main__":
    print("Testing database connection...")
    print("=" * 50)
    if test_connection():
        print("🎉 Database connection test passed!")
    else:
        print("🧨 Database connection test failed!")