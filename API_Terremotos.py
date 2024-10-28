import requests
import tkinter as tk
from tkinter import scrolledtext

# Función para hacer la solicitud a la API y mostrar los resultados en el panel
def get_earthquakes(min_magnitude, limit):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",  # El formato de la respuesta
        "starttime": "2023-01-01",  # Fecha de inicio
        "endtime": "2023-12-31",    # Fecha de fin
        "minmagnitude": min_magnitude,  # Mínima magnitud
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta una excepción si hay un error
        data = response.json()  # Parsear la respuesta a JSON
        
        # Obtener la lista de terremotos (features)
        earthquakes = data['features']
        
        # Limitar los resultados a la cantidad que el usuario indicó
        earthquakes = earthquakes[:limit]
        
        # Mostrar los resultados en el panel
        result_text.delete(1.0, tk.END)  # Limpiar el contenido anterior
        if not earthquakes:
            result_text.insert(tk.END, f"No se encontraron terremotos con magnitud mayor o igual a {min_magnitude}.\n")
        else:
            result_text.insert(tk.END, f"Mostrando los primeros {limit} terremotos con magnitud >= {min_magnitude}:\n\n")
            for eq in earthquakes:
                place = eq['properties']['place']
                magnitude = eq['properties']['mag']
                time = eq['properties']['time']
                result_text.insert(tk.END, f"Lugar: {place}, Magnitud: {magnitude}, Tiempo: {time}\n")
    
    except requests.exceptions.RequestException as e:
        result_text.insert(tk.END, f"Error al obtener la información: {e}\n")

# Interacción con el usuario (ventana Tkinter)
def main():
    def submit():
        try:
            limit = int(limit_entry.get())
        except ValueError:
            result_text.insert(tk.END, "Por favor ingresa un número válido para el límite.\n")
            return
        
        try:
            min_magnitude = float(magnitude_entry.get())
        except ValueError:
            result_text.insert(tk.END, "Por favor ingresa un valor válido para la magnitud.\n")
            return
        
        # Llamar a la función para obtener y mostrar los terremotos
        get_earthquakes(min_magnitude, limit)

    # Crear la ventana principal
    window = tk.Tk()
    window.title("Terremotos recientes")
    
    # Etiquetas y entradas para el límite y magnitud mínima
    tk.Label(window, text="Cantidad de terremotos:").grid(row=0, column=0, padx=10, pady=10)
    limit_entry = tk.Entry(window)
    limit_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(window, text="Magnitud mínima:").grid(row=1, column=0, padx=10, pady=10)
    magnitude_entry = tk.Entry(window)
    magnitude_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Botón para enviar la solicitud
    submit_button = tk.Button(window, text="Mostrar terremotos", command=submit)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Cuadro de texto desplazable para mostrar los resultados
    global result_text
    result_text = scrolledtext.ScrolledText(window, width=70, height=15)
    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    # Iniciar el bucle principal de la ventana
    window.mainloop()

# Ejecutar el programa
if __name__ == "__main__":
    main()
