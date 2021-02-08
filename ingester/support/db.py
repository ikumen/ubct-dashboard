import os
import pyodbc
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
dotenv.load_dotenv(dotenv_path)


def get_conn():
    driver = '{ODBC Driver 17 for SQL Server}'
    server_host = os.environ.get('DB_SERVER_HOST')
    server_port = 1433
    db_name = os.environ.get('DB_DATABASE')
    db_user = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')
    return pyodbc.connect(f'DRIVER={driver};SERVER={server_host};PORT={server_port};DATABASE={db_name};UID={db_user};PWD={db_password}')
    

def execute_query(conn, stmt, fetchone=False, *params):
    results = None
    with conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(stmt, params)
        else:
            cursor.execute(stmt)
        results = cursor.fetchone() if fetchone else cursor.fetchall()
    return results


def execute_stmt(conn, stmt, *params):
    """Execute the given statement.
    
    :param conn: the db connection to use
    :param stmt: the SQL statement to execute
    :param params: the bind parameters to our statement
    """
    with conn.cursor() as cursor:
        cursor.execute(stmt, params)
    return True
