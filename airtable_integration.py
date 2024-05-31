import requests
import json
import credentials
from const import CONSTANTS
import logging

logging.info("Obteniendo API KEY Airtable...")
# Configura tus credenciales y nombres de la base de datos
API_KEY = credentials.api_key_airtable['x-api-key']
logging.info("API KEY Airtable obtenida: {0}".format(API_KEY))

# URL de la API de Airtable
logging.info("Estableciendo URLS para requests...")
AIRTABLE_USERS_URL = CONSTANTS['USERS']
AIRTABLE_ENTRYS_URL = CONSTANTS['RECORDS']
logging.info("URLS para requests establecidas...")

def check_record(request):
    logging.info("Entrando a check_record...")
    # Simulando la lógica de recibir la solicitud POST desde el cliente
    rfid = request['rfid']
    lab_id = request['lab_id']

    student = get_student_by_rfid(rfid)
    logging.info('Datos obtenidos de student: {}'.format(student))  
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

def create_new_student(student_data, totem_cred=None, API_KEY=credentials.api_key_airtable['x-api-key']):

    logging.info("Entrando a create new student...")
    logging.info("Student data: {0}".format(student_data))
    # Headers para la autenticación
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'fields': {
            'fldDHLQB6UXdQRwx9': student_data['rfid'],
            'fldHdCHTha7Xd687o': student_data['nombre'],
            'fldQxqlM4ac3JPy4x': student_data['correo'],
            'fldNwrYVKqERuCmF7': student_data['rut'],
            'fldH3TAdkYWmkhfuT': student_data['sit_academica'],
            'fldaz03UGWlIRFYB8': student_data['major'],
            'fldhejE4G4YNNmd2e': totem_cred
        }
    }
    
    logging.info("Enviando POST a Airtable para crear estudiante...")
    logging.info("API KEY obtenida: {0}".format(API_KEY))
    # Realizar la solicitud POST para crear el nuevo registro de persona
    response = requests.post(AIRTABLE_USERS_URL, headers=headers, json=data)
    logging.info("Response recibida desde Airtable...")

    # Verificar el código de respuesta HTTP y devolver el resultado
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error al crear el registro: {response.status_code} - {response.text}'}

def get_student_by_rfid(rfid="123456",API_KEY=credentials.api_key_airtable['x-api-key']):

    logging.info("Entrando a get student by rfid...")

    # Headers para la autenticación
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    params = {
        'filterByFormula': f'{{ID Persona}} = "{rfid}"'
    }
    response = requests.get(AIRTABLE_USERS_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('records'):
            return data['records'][0]['fields']
    return None

def create_new_entry(student,API_KEY=credentials.api_key_airtable['x-api-key']):
    
    logging.info("Entrando a create new entry: {0}".format(student))

    # Headers para la autenticación
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'fields': {
            'fldSaKJY5vxtHib40': [student['id']],
        }
    }
    
    #Desmarcar último registro
    if "Record ID - Último ingreso" in student:
        logging.info("Chequeando si marcó salida de última ingreso...")
        unchecked_last_entry(student["Record ID - Último ingreso"][0])
    else:
        logging.info("Usuario no registra ingresos.")
    
    logging.info("Enviando POST para crear nuevo ingreso...")
    # Realizar la solicitud POST para crear el nuevo registro de ingreso
    response = requests.post(AIRTABLE_ENTRYS_URL, headers=headers, json=data)
    logging.info("Response Airtable: {0}".format(response))

    # Verificar el código de respuesta HTTP y devolver el resultado
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error al crear el registro: {response.status_code} - {response.text}'}

def record_departure_time(record_id, API_KEY=credentials.api_key_airtable['x-api-key']):
    logging.info("Entrando a record departure time...")
    # Datos a actualizar en el registro de Airtable
    AIRTABLE_RECORD_URL = AIRTABLE_ENTRYS_URL + "/"

    # Headers para la autenticación
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    data = {
        'fields': {
            'fldnsGof1RrMYyRod': 'Registrada'
        }
    }
    
    # Realizar la solicitud PATCH para actualizar el registro
    response = requests.patch(AIRTABLE_RECORD_URL + record_id, headers=headers, json=data)

def unchecked_last_entry(record_id, API_KEY=credentials.api_key_airtable['x-api-key']):
    logging.info("Entrando a unchecked last entry...")
    # Datos a actualizar en el registro de Airtable
    AIRTABLE_RECORD_URL = AIRTABLE_ENTRYS_URL + "/"

    # Headers para la autenticación
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    data = {
        'fields': {
            'fldbURdlvg5Riw5BH': False
        }
    }
    
    # Realizar la solicitud PATCH para actualizar el registro
    response = requests.patch(AIRTABLE_RECORD_URL + record_id, headers=headers, json=data)