# NeuralWorks Test

## Construir imagen y levantar contenedores

Este test construye dos images, una para `apifast` que utiliza un `Dockerfile` para su construccion y otra para la base de datos Postgres la cual se utilizara para la carga masiva de datos. Ambos se encuentran sincronizados a traves de `docker-compose` la cual debe ejecutarse con el siguiente comando:

`docker-compose up --build`

Luego de la ejecucion del comando, se ejecutaran una serie de comandos de manera automatica para el levantamiento de una API la cual nos entregara a una perspectiva de solucion al test planteado por NeuralWorks. Si todo se ejecuto sin novedad aparecera lo siguiente en su consola de comandos:

![](/img/docker_compose.png)


## Localhost
Todo la solucion se ha levantado en localhost por lo que ya podemos acceder al link `http://localhost:8080` el cual nos llevara al swagger del proyecto donde podemos ejecutar distintos endpoint para resolver cada pregunta planteada en el test:

![](/img/localhost.png)

## Endpoints

Los endpoints disponibles en esta API son los siguientes:

### `http://localhost:8080/extract_trips`

Este endpoint nos permite la carga masiva desde el archivo `trips.csv` adjunto en el repositorio hacia nuestra base de datos Postgres. Este endpoint se encarga de realizar una serie de transformaciones al archivo de entrada las cuales seran explicadas en la seccion [Base de datos](#base-de-datos).

* Params: None

![](/img/extract_load.png)

**IMPORTANTE:** En primera instacia este endpoint debe ejecutarse para poder ejecutar los otros endpoints disponibles en esta API.

### `http://localhost:8080/similar_trips`

Este endpoint entrega viajes similares con coordenadas de origen y destino separadas por longitud y latitud (origen, destino) incluyendo un margen de similitud.

* Params:
  * id : string
  * from_date : string
  * to_date : string
  * margin : string
  * lon_o : string (longitud de origen)
  * lat_o : string (latitud de origen)
  * lon_d : string (longitud de destino)
  * lat_d : string (latitud de destino)

![](/img/similar_trips.png)

![](/img/similar_trips_r.png)

### `http://localhost:8080/boundbox_trips`

Este endpoint entrega la cantidad de viajes realizados en una region, boundbox delimitado por coordenadas minimas y maximas (lat, lon) y periodo de dias en conjunto con su promedio con referencia a la cantidad de viajes realizados en el mes del periodo indicado.

* Params:
  * id : string
  * from_date : string
  * region : string
  * lon_min : string (longitud minima boundbox)
  * lat_min : string (latitud minima boundbox)
  * lon_max : string (longitud maxima boundbox)
  * lat_max : string (latitud maxima boundbox)

![](/img/boundbox.png)

![](/img/boundbox_r.png)

Ambas fechas deben pertenecer al mismo mes y anio, de lo contrario el endpoint solicitara fechas validas para la consulta como en el siguiente ejemplo:

![](/img/boundbox_error.png)

## Base de datos

La carga del archivo `trips.csv` se realiza de manera directa en la tabla `trips` con el siguiente esquema: 

![](/img/db.png)

Como se puede apreciar, para una interaccion simplificada de la API con los datos se agregaron las columnas `lon_o`, `lat_o`, `lon_d` y `lat_d` las cuales corresponden a la longitud y latitud de los campos originales `origin_coord` y `destination_coord`. Esto nos permite realizar consultas directas en bases de datos con instrucciones simples sin necesidad de utilizar librerias de geometria, ya que las conversiones de este tipo se realizaron previamente por el endpoint [`extract_trips`](#httplocalhost8080extracttrips)

Tambien esta base de datos puede ser accedida por un cliente utilizando la siguiente configuracion:

![](/img/db_config.png)

Las credenciales pueden ser facilmente revisadas en el archivo `docker-compose.yml`




