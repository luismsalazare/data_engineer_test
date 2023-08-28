from common import PostgresConnection

def create_trips_table() -> None:

    query = """
    CREATE TABLE trips (
    trip_id SERIAL PRIMARY KEY,
    user_id INT,
    vehicle_id INT,
    booking_time TIMESTAMP,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status_id INT,
    travel_dist FLOAT,
    );    
    """

    with PostgresConnection() as postrgres:
        postrgres.execute_query(query)

    return print('trips table created!')

def create_users_table() -> None:

    query = """
    CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name_user VARCHAR(255),
    rut_user VARCHAR(255)
    );
    """

    with PostgresConnection() as postrgres:
        postrgres.execute_query(query)

    return print('users table created!')

def create_prices_table() -> None:

    query = """
    CREATE TABLE prices (
    trip_id INT PRIMARY KEY,
    price_amount FLOAT
    );
    """

    with PostgresConnection() as postrgres:
        postrgres.execute_query(query)

    return print('prices table created!')

def create_vehicles_table():

    query = """
    CREATE TABLE vehicles (
    vehicle_id INT PRIMARY KEY,
    membership_id INT
    ); 
    """

    with PostgresConnection() as postrgres:
        postrgres.execute_query(query)

    return print('vehicles table created!')


def create_locations_table() -> None:

    query = """
    CREATE TABLE locations (
    trip_id INT PRIMARY KEY,
    start_lat FLOAT,
    start_lon FLOAT,
    end_lat FLOAT,
    end_lon FLOAT
    );
    """

    with PostgresConnection() as postrgres:
        postrgres.execute_query(query)

    return print('locations table created!')

if __name__ == "__main__":
    create_trips_table()
    create_users_table()
    create_vehicles_table()
    create_prices_table()
    create_locations_table()

