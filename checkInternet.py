
import requests

def check():
    print("cheking internet")
    try:
        _ = requests.head('https://google.com')
        return True
    except requests.ConnectionError:
        print("No existe conexión a internet disponible.")
    return False
