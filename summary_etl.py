import pandas as pd
from common import PostgresConnection, schema_fixer

def create_daily_summary_table() -> None:

    query = """
    CREATE TABLE IF NOT EXISTS resumen_diario (
    fecha date NOT NULL,
    cantidad_viajes int NOT NULL,
    suma_ingresos numeric(10,2) NOT NULL,
    promedio_ingresos numeric(10,2) NOT NULL,
    suma_metros_recorridos int NOT NULL
    );"""

    with PostgresConnection() as postrgres:
        postrgres.execute_query(query)

    return print('dim_status table created!')


def daily_summary(fecha) -> None:
    """
    Genera un proceso ETL donde se calculan métricas y son insertadas en una tabla Postgres

    Args:
        fecha: fecha de los datos a analizar

    """
    
    datos_viajes = pd.read_csv("trips.csv")

    try:
        datos_filtrados = datos_viajes[pd.to_datetime(datos_viajes.booking_time).dt.date.astype(str) == fecha]
    except:
        datos_filtrados = None

    if datos_filtrados != None:
        try:
            cantidad_viajes = datos_filtrados.shape[0]
            suma_ingresos = datos_filtrados["price_total"].sum()
            promedio_ingresos = suma_ingresos / cantidad_viajes
            suma_metros_recorridos = datos_filtrados["travel_dist"].sum()

            kpi = {
            "fecha":                  fecha,
            "cantidad_viajes":        cantidad_viajes,
            "suma_ingresos":          suma_ingresos,
            "promedio_ingresos":      promedio_ingresos,
            "suma_metros_recorridos": suma_metros_recorridos,
            }

            data = pd.DataFrame([kpi.values()], columns=kpi.keys())

            df = schema_fixer(data, "summary")
            
            with PostgresConnection() as postgres:
                postgres.insert_data("summary", df, "append")
        
        except Exception as e:
            print(e)

    else:
        print("No data to insert")



if __name__ == "__main__":
    create_daily_summary_table()

    fecha = datetime.now().strftime('%Y-%m-%d')
    daily_summary(fecha)
