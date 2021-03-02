
import requests

def check():
    print("cheking internet")
    try:
        print("in try")
        _ = requests.head('https://google.com', timeout=1)
        return True
    except requests.ConnectionError:
        print("No existe conexión a internet disponible.")
    return False