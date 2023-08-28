# Test Data Engineer - Answers

A continuación las respuestas de las preguntas hechas en el test técnico para la posición de Data Engineer de la compañía Awto.

1.  Diseñar un modelo de datos. Genere una propuesta sobre cómo guardar los datos. Justifique esa propuesta y explique por qué es la mejor opción.
Basándome en la información otorgada y para simplificar la comprensión de las consultas realizadas a la base de datos, determinaría un modelo de datos tipo star, comprendido por una fact table y 4 dim tables. El modelo de datos en estrella es más simple y fácil de entender que el modelo snowflake. En este modelo, la tabla de hechos se encuentra en el centro y las tablas dimensionales se encuentran alrededor. Este modelo es adecuado para consultas simples y directas.

A continuación el desglose de las tablas:

`trips`: Contiene la información de cada viaje realizado, con los siguientes campos: 
- trip_id (identificador único del viaje)
- user_id (identificador del usuario que realizó el viaje) 
- vehicle_id (identificador del vehículo utilizado en el viaje) 
- booking_time (fecha y hora en la que se realizó la reserva del viaje)
- start_time (fecha y hora de inicio del viaje)
- end_time (fecha y hora de finalización del viaje)
- status_id (identificador del estado del viaje)
- travel_dist (distancia en metros recorrida en el viaje)

`users`: Contiene la información de los usuarios que realizaron los viajes. Los campos serían  	
- user_id (identificador único del usuario)
- name_user (nombre del usuario)
- rut_user (RUT del usuario).

`vehicles`: Contiene la información de los vehículos utilizados en los viajes. Los campos serían 
- vehicle_id (identificador único del vehículo)
- membership_id (identificador de membresía asociado al vehículo).

`prices`: Contiene la información de los precios de los viajes. Los campos serían
- trip_id (identificador único del viaje)
- price_amount (monto del precio del viaje sin impuestos).
- price_total (monto total del precio del viaje incluyendo impuestos).

`locations`: Contiene la información de las ubicaciones de inicio y finalización de los viajes. Los campos serían 
- trip_id (identificador único del viaje)
- start_lat (latitud de la ubicación de inicio del viaje)
- start_lon (longitud de la ubicación de inicio del viaje)
- end_lat (latitud de la ubicación de finalización del viaje)
- end_lon (longitud de la ubicación de finalización del viaje).


2. Crea una base de datos en Postgres usando Docker.

Refiérase al archivo `Dockerfile`. En esta parte, me apoyé en ChatGPT, debido a que no suelo trabajar con containers.



3. Crea las tablas del modelo de datos que diseñaste en el paso 1. Puede usar scripts SQL o código en Python

Refiérase a `common.py` y `create_tables.py` scripts -> 5 functions para la creación de 6 tablas



4. Genera archivos en Python para cargar los datos del archivo trips.csv en las tablas que creaste en el paso anterior.

Refiérase a `common.py` y `load_data.py` scripts -> Código genérico para poblar las 5 tablas del modelo

Se hace uso de un for loop para iterar entre las tablas y el uso de la función `schema_fixer`, para seleccionar las columnas acordes para cada tabla y ajustar al esquema requerido para su correcta inserción.


5. Cree una nueva tabla en Postgres llamada resumen_diario. Genera con Python un proceso de ETL que cargue en la tabla un resumen por día de:la cantidad de viajes -  suma de ingresos - el promedio de ingresos - la suma de metros recorridos. 

Refiérase a `common.py` y `summary_etl.py` scripts.


5.1. Explique y justifique las decisiones que tomó para generar el resumen. Considere que diariamente no habrá más de 100.000 viajes.

- `Modelado de datos`: Con base en la cantidad diaria máxima de registros y la cantidad de columnas, se filtra la información del archivo trip.csv por fecha (booking_time) y luego se procede a calcular las métricas.

- `Inserción de datos`: el diccionario obtenido se convierte en un dataframe, para hacer uso de la función schema_fixer, que ajusta el tipo de variable de cada columna y las columnas, a la tabla destino de postgres (summary), para luego ser insertado a través de la clase PostgresConnection (context manager).

`Nota`: si en un futuro aumenta la cantidad de campos calculados y los registros diarios, sugeriría hacer uso de otras librerías como PySpark o Polars.


5.2. Señale (sin necesidad de implementar) qué procesos podría desarrollar para asegurar la consistencia de los datos en la tabla resumen_diario.

El uso del `schema_fixer` garantiza la consistencia de los tipos de datos, sin embargo, se puede robustecer validando los resultados del diccionario kpi, donde no se deberían obtener campos nulos.


5.3. Señale (sin necesidad de implementar) cómo podría automatizar este proceso de ETL de manera diaria.

Dependiendo de la nube a utilizar, se puede crear un Glue Job (AWS), Cloud Function (GCP) calendarizado que ejecute el código. Dependiendo de las necesidades de monitoreo de las métricas, se ajusta la frecuencia de ejecución de la función. 

Si se planea ejecutar en varias ocasiones durante el día en curso, habría que modificar el código para que inserte en caso de no existencia del campo a analizar (fecha), es decir, si no existe la fecha = "2023-08-25" en la tabla, se insertan los valores, de lo contrario, se actualizan.


6. La empresa quiere implementar un sistema de descuentos mediante cupones. ¿Cómo modificarías el modelo de datos para agregarlo? Describa su propuesta, justifique y explique por qué es la mejor opción. No es necesario que lo implemente.
   
Agregaría la siguiente tabla a la base de datos:

`coupons`: contiene la informacion de todos los cupones aplicados por los usuarios
- coupon_id: (identificador del cupón utilizado en el viaje)
- campaing_id: (identificador de la campaña relacionada al cupón aplicado).
- trip_id (identificador único del viaje)
- user_id (identificador del usuario que realizó el viaje) 

`campaigns`: contiene información sobre las campañas de adquisición y retención de cliente, liberadas por la empresa
- campaign_id: (identificador de la campaña)
- campaign_name: (nombre de la campaña)
- campaing_status: (estado de la campaña. Activa o inactiva)
- start_date: (fecha de inicio de vigencia de la campaña)
- end_date: (fecha de finalización de vigencia de la campaña)
- discount_type: (tipo de descuento aplicado (porcentual o fijo)
- discount: (monto del descuento ofrecido por la campaña con base al tipo de descuento)
- coupon_id: (identificador del cupón perteneciente a la campaña)

A su vez, modificaría la tabla trips de la siguiente manera:
`trips`: Contiene la información de cada viaje realizado, con los siguientes campos: 
- trip_id (identificador único del viaje)
- user_id (identificador del usuario que realizó el viaje) 
- vehicle_id (identificador del vehículo utilizado en el viaje) 
- booking_time (fecha y hora en la que se realizó la reserva del viaje)
- start_time (fecha y hora de inicio del viaje)
- end_time (fecha y hora de finalización del viaje)
- status_id (identificador del estado del viaje)
- travel_dist (distancia en metros recorrida en el viaje)
- `coupon_id`: (dentificador del cupón utilizado en el viaje)

prices: Contiene la información de los precios de los viajes. Los campos serían
- trip_id (identificador único del viaje)
- price_amount (monto del precio del viaje sin impuestos).
- `discount_amount`: Descuento aplicado al viaje con base en el cupón aplicado
- `price_total`(monto total del precio del viaje incluyendo impuestos y descuentos).

Los cupones ofrecidos por Awto, deben pertenecer a una campaña de adquisición, retención o reactivación de los clientes, que son ofrecidas al cliente mediante los cupones.

Cada cupón tiene relación estricta con una campaña, que determina el tipo de descuento a aplicar (porcentual o fijo), monto del descuento, fecha validez de uso de cupón para campañas con temporalidad definida, por lo que esta tabla debe ser consultada cuando se intente hacer uso de un cupón para conocer el estatus del cupón (campaing_status).

A su vez, se crea una tabla de hechos llamada coupons, que tiene información de los cupones utilizados por usuarios y que debe ser consultada por la app o la página web, al momento de ser aplicado un cupón a un viaje, para así evitar la reutilización de cupones por parte de los usuarios.
