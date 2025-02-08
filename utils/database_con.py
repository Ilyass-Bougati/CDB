import psycopg2
import pandas as pd
from plog.plog import Logger

class DBConnection:
    def __init__(self, uri: str, db_name: str, user: str, password: str, port: str):
        self.logger = Logger("DBConnection")
        self.uri = uri
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port

        self.logger.Info(f"Connecting to {uri}:{port}")
        self.conn = psycopg2.connect(
            database="postgres",
            host=uri,
            user=user,
            password=password,
            port=port
        )


    def set_cols(self, db_cols: list) -> None:
        self.db_cols = db_cols

        # Creating the table
        cursor = self.conn.cursor()
        query = f"CREATE TABLE {self.db_name}("
        for col in self.db_cols:
            query += f"{col[0]} {col[1]},"

        cursor.execute(query[:-1] + ")")
        self.conn.commit()
        self.logger.Info(f"Created Table {self.db_name}")
        self.logger.Info(f"Schema:\n {query[:-1] + ")"}")

