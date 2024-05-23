import requests
import json
import credentials
from const import CONSTANTS

# Configura tus credenciales y nombres de la base de datos
API_KEY = credentials.api_key_airtable['x-api-key']

# URL de la API de Airtable
AIRTABLE_USERS_URL = CONSTANTS['USERS']
AIRTABLE_ENTRYS_URL = CONSTANTS['RECORDS']

# Headers para la autenticación
headers = {
    'Authorization': f'Bearer {API_KEY}'
}

def check_record(request):
    # Simulando la lógica de recibir la solicitud POST desde el cliente
    rfid = request['rfid']
    lab_id = request['lab_id']

    student = get_student_by_rfid(rfid)
    if student:
        if 'Ingresos' in student:
            #Usuario registrado con ingresos anteriores.
            if student["Salida de último ingreso"] == "Pendiente":
                action = 'Exit'
            else:
                action = 'Entry'

            response_data = {
                'type': 'student',
                'action': action,
                'data': student
            }

        else:
            #Usuario registrado, pero sin ingresos anteriores.
            response_data = {
                'type': 'student-no-entries',
                'action': 'Entry',
                'data': student
            }

    else:
        response_data = {
            'type': 'nonexistent',
            'action': 'Entry',
            'data': {
                'rfid': rfid
            }
        }
    
    return response_data

def create_new_student(student_data, totem_cred=None):

    data = {
        'fields': {
            'fldDHLQB6UXdQRwx9': student_data['rfid'],
            'fldHdCHTha7Xd687o': student_data['nombre'],
            'fldYhz4PDne4E8AO7': student_data['correo'],
            'fldNwrYVKqERuCmF7': student_data['rut'],
            'fldH3TAdkYWmkhfuT': student_data['sit_academica'],
            'fldaz03UGWlIRFYB8': student_data['major'],
            'fldhejE4G4YNNmd2e': totem_cred
        }
    }
    
    # Realizar la solicitud POST para crear el nuevo registro de persona
    response = requests.post(AIRTABLE_USERS_URL, headers=headers, json=data)

    # Verificar el código de respuesta HTTP y devolver el resultado
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error al crear el registro: {response.status_code} - {response.text}'}

def get_student_by_rfid(rfid="123456"):

    params = {
        'filterByFormula': f'{{ID Persona}} = "{rfid}"'
    }
    response = requests.get(AIRTABLE_USERS_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('records'):
            return data['records'][0]['fields']
    return None

def create_new_entry(student):
    
    data = {
        'fields': {
            'fldSaKJY5vxtHib40': [student['id']],
        }
    }
    
    #Desmarcar último registro
    if "Record ID - Último ingreso" in student:
        unchecked_last_entry(student["Record ID - Último ingreso"][0])
    else:
        print("Usuario no registra ingresos.")
    
    # Realizar la solicitud POST para crear el nuevo registro de ingreso
    response = requests.post(AIRTABLE_ENTRYS_URL, headers=headers, json=data)

    # Verificar el código de respuesta HTTP y devolver el resultado
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error al crear el registro: {response.status_code} - {response.text}'}

def record_departure_time(record_id):
    # Datos a actualizar en el registro de Airtable
    AIRTABLE_RECORD_URL = AIRTABLE_ENTRYS_URL + "/"
    data = {
        'fields': {
            'fldnsGof1RrMYyRod': 'Registrada'
        }
    }
    
    # Realizar la solicitud PATCH para actualizar el registro
    response = requests.patch(AIRTABLE_RECORD_URL + record_id, headers=headers, json=data)

def unchecked_last_entry(record_id):
    # Datos a actualizar en el registro de Airtable
    AIRTABLE_RECORD_URL = AIRTABLE_ENTRYS_URL + "/"
    data = {
        'fields': {
            'fldbURdlvg5Riw5BH': False
        }
    }
    
    # Realizar la solicitud PATCH para actualizar el registro
    response = requests.patch(AIRTABLE_RECORD_URL + record_id, headers=headers, json=data)

#student = get_student_by_rfid('131313')
#create_new_entry(student)
student_data = {'rfid':  '181818',
            'nombre': 'Sebastián Velozo C',
            'correo': 'savelozo@uc.cl',
            'rut': '18584535-4',
            'sit_academica': 'Egresado',
            'major': 'Ingeniería Civil',
            'lab_id': '1234'
            }

#student = create_new_student(student_data)
#print(student)
#create_new_entry(student)
#print(check_record(student_data))
#record_departure_time('recXvKF6RYjJp1TrN')