import pandas as pd
from utils.types import pg_type
from utils.database_con import DBConnection
from plog.plog import Logger
import csv

class Reader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.db_cols = []
        self.table_name = file_path.split("/")[-1].split(".")[0]
        self.logger = Logger("Reader")

        # reading the databse columns
        self.read_cols()
        
        # connecting to the databse
        self.db_conn = DBConnection(
            "localhost",
            self.table_name,
            "postgres",
            "root",
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

        chunk_size = 1_000_000  # Process 100k rows at a time  
        i = 0
        for chunk in pd.read_csv(self.file_path, chunksize=chunk_size):
            for index, row in chunk.iterrows():
                values = ""
                for val in row.tolist():
                    try:
                        values += str(val) if (int(val) == val or float(val) == val) else f"'{val}'"
                    except:
                        values += f"'{val}'"

                    values += ","

                try:
                    query = f"INSERT INTO {self.table_name} VALUES ({values[:-1]})"
                    cursor.execute(query)
                    self.db_conn.conn.commit()
                except:
                    self.logger.Warn(f"Error inserting, {str(row)[1:-1]}")

                print(f"{i}", end="\r")
                i += 1
                
                