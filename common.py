import pandas as pd
import psycopg2

class PostgresConnection():
    """
    Context manager para la conexión a la base de datos
    """
    def __enter__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="de_applicant",
            password="de_test",
            database="awto"
        )

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        
    def retrieve_query(self, query):
        df = pd.read_sql(query, self.conn)
        return df

    def insert_data(self, table_name, df, method):
        df.to_sql(table_name, self.conn, if_exists=method)

def data_type_list(df, type):
    """
    Esta función selecciona las columnas de una dataframe que coinciden con 
    un tipo de variable en específico. 

    Args:
        df (pandas.DataFrame): Dataframe base desde donde se obtiene el schema
        type (str): typo de variable a comparar.

    Returns:
        list: lista con el nombre de las columnas que coinciden con el tipo de variable.
    """
    return list(df[df["type"] == type].columns.unique())

def schema_fixer(df, table_name):
    """
    Ajusta el esquema en cuanto a tipo de variable y cantidad de columnas de un DataFrame de Pandas 
    con base en el esquema de la tabla en Postgres. 

    Args:
        df (pandas.DataFrame): El DataFrame de Pandas a ajustar.
        table_name (str): El nombre de la tabla de Postgres.

    Returns:
        pandas.DataFrame: Un DataFrame de Pandas con el esquema ajustado.
    """

    query = f"""
    SELECT * FROM public.INFORMATION_SCHEMA.COLUMNS
    WHERE table_name = '{table_name}';
    """

    with PostgresConnection() as postgres:
        df_schema = postgres.retrieve_query(query)

    # LISTA DE COLUMNAS DE LA TABLA EN POSTGRES
    df = df[list(df_schema.column_name.unique())]

    str_fields = data_type_list(df_schema,"STRING")
    for obj in str_fields:
        df[obj] = df[obj].astype(str).str.replace(u"\r", u' ') 

    flt_fields = data_type_list(df_schema,"FLOAT64")
    for obj in flt_fields:
        df[obj] = df[obj].fillna(0).astype(float)

    int_fields = data_type_list(df_schema,"INT64")
    for obj in int_fields:
        df[obj] = df[obj].fillna(0).astype(int)

    return df
