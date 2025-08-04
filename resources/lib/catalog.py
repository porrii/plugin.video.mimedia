import json
import urllib.request

def load_catalog(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                data = response.read().decode('utf-8')
                return json.loads(data)
    except Exception:
        pass
    # En caso de error o sin conexión, devolver catálogo vacío
    return {"movies": [], "series": []}
