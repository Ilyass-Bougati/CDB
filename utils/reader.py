import pandas as pd
from utils.types import pg_type
from utils.database_con import DBConnection
from plog.plog import Logger
from dotenv import load_dotenv
import os

load_dotenv()

class Reader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.db_cols = []
        self.table_name = os.getenv("TABLE_NAME")
        self.logger = Logger("Reader")

        # reading the databse columns
        self.read_cols()
        
        # connecting to the databse
        self.db_conn = DBConnection(
            "localhost",
            self.table_name,
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            "5432"
        )

        self.db_conn.set_cols(self.db_cols)
        self.insert_to_db()

    def read_cols(self):
        # Reading the beggining of the file
        data = pd.read_csv(
            self.file_path,
            nrows=5
        )

        # Getting the column names and their types
        for i in range(0, len(data.dtypes)):
            self.db_cols.append((
                data.columns[i], 
                pg_type(data.dtypes.tolist()[i])
            ))
    
    def insert_to_db(self):
        self.logger.Info(f"Reading and inserting the {self.file_path}")

        # getting the column names
        # column_names = [col[0] for col in self.db_cols]
        
        # Reading line by line
        cursor = self.db_conn.conn.cursor()

        chunk_size = 10000  # Process 100k rows at a time  
        i = 0
        for chunk in pd.read_csv(self.file_path, chunksize=chunk_size):
            query = f"INSERT INTO {self.table_name} VALUES "
            for index, row in chunk.iterrows():
                values = ""
                for val in row.tolist():
                    try:
                        values += str(val) if (int(val) == val or float(val) == val) else f"'{val.replace("'"," ")}'"
                    except:
                        values += f"'{val.replace("'"," ")}'"

                    values += ","

                query += f"({values[:-1]}),\n"
            cursor.execute(query[:-2])
            self.db_conn.conn.commit()
            self.logger.Good("Commited")
            

                
                
                