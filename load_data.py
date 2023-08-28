import pandas as pd
from common import PostgresConnection, schema_fixer


if __name__ == "__main__":
    data = pd.read_csv("trip.csv")

    for table_name in ["trips", "users", "vehicles", "prices", "locations"]:

        df = schema_fixer(data, table_name).drop_duplicates()

        with PostgresConnection() as postgres:
            postgres.insert_data(table_name, df, "append")