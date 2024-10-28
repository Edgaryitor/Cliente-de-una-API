import requests

# Función para hacer la solicitud a la API y mostrar resultados en consola
def get_earthquakes():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",  # El formato de la respuesta
        "starttime": "2023-01-01",  # Fecha de inicio para los terremotos
        "endtime": "2023-12-31",    # Fecha de fin
        "minmagnitude": 5,  # Mínima magnitud de terremotos
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta una excepción si hay un error
        data = response.json()  # Parsear la respuesta a JSON
        
        # Mostrar los primeros 5 terremotos en la consola
        earthquakes = data['features'][:5]
        for eq in earthquakes:
            place = eq['properties']['place']
            magnitude = eq['properties']['mag']
            time = eq['properties']['time']
            print(f"Lugar: {place}, Magnitud: {magnitude}, Tiempo: {time}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la información: {e}")

# Llamar a la función
get_earthquakes()
