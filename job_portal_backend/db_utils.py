import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

def get_db_connection():
    """Get PostgreSQL database connection"""
    return psycopg2.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        port=settings.db_port,
        cursor_factory=RealDictCursor  # This makes cursor return dict-like objects
    )

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute a query and return results"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
            
        connection.commit()
        cursor.close()
        connection.close()
        
        return result
    except Exception as e:
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        raise e
