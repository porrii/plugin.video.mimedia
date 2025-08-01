import json
import requests

def load_catalog(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    # En caso de error o sin conexión, carga catálogo local si quieres (aquí vacio)
    return {"movies": [], "series": []}
