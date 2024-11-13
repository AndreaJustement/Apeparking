import requests

# Base URL de la API
url = "http://127.0.0.1:8000/add-parking-space"

# Espacios de estacionamiento
parking_spaces = [
    {"id": "1A", "floor": "1", "space_number": "A", "available": True},
    {"id": "1B", "floor": "1", "space_number": "B", "available": True},
    {"id": "1C", "floor": "1", "space_number": "C", "available": False},
    {"id": "1D", "floor": "1", "space_number": "D", "available": True},
    {"id": "1E", "floor": "1", "space_number": "E", "available": True},
]

# Función para agregar cada espacio de estacionamiento
for space in parking_spaces:
    print(f"Sending request to add: {space['id']}")  # DEBUG: Imprime antes de enviar la solicitud
    response = requests.post(url, json=space)
    print(f"Response from server: {response.status_code}")  # DEBUG: Muestra el código de respuesta
    if response.status_code == 200:
        print(f"Added space: {space['id']} - {space['space_number']}")
    else:
        print(f"Failed to add space: {space['id']}. Status code: {response.status_code}. Error: {response.text}")
