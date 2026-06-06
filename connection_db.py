import oracledb
import os 
from dotenv import load_dotenv
load_dotenv()

def connection_with_oracle():
    """
    Function for setting up the connection to ORACLE cloud
    connection_with_oracle() -> connection
    """
    wallet_password = os.getenv("wallet_password")
    wallet_path_from_env = os.getenv("wallet_path")
    wallet_path = os.path.abspath(wallet_path_from_env)
    user_from_env = os.getenv("user")
    dsn_from_env = os.getenv("dsn")

    try:
        print("Attempting secure MTS Connection")

        connection = oracledb.connect(
            user = user_from_env,
            password = wallet_password,
            dsn = dsn_from_env,
            config_dir = wallet_path,
            wallet_location = wallet_path,
            wallet_password = wallet_password
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 'Connected!' FROM dual")
        print(cursor.fetchone())
        return connection

    except oracledb.Error as e:
        print("\nStill hitting a wall. Here is the exact error:")
        print(e)
        return None