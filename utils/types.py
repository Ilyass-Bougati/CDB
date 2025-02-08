from sqlalchemy import Integer, String, Float, DateTime

types: dict = {
    "int64": "BIGINT",
    "object": "VARCHAR",
    "float64": "FLOAT",
    "datetime": "TIMESTAMP"
}



def pg_type(pd_type: str) -> str:
    # turning pandas types to postgres types
    return types.get(str(pd_type))