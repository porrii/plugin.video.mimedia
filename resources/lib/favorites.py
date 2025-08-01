import os
import json
import xbmc
import xbmcaddon

ADDON_ID = 'plugin.video.mimedia'

def _path():
    p = xbmc.translatePath(f'special://profile/addon_data/{ADDON_ID}')
    if not os.path.exists(p):
        os.makedirs(p)
    return os.path.join(p, 'favorites.json')

def load_favorites():
    f = _path()
    if os.path.exists(f):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                return json.load(fh)
        except Exception:
            return []
    return []

def save_favorites(favs):
    f = _path()
    with open(f, 'w', encoding='utf-8') as fh:
        json.dump(favs, fh)

def add_favorite(item):
    favs = load_favorites()
    if not any(f['title'] == item['title'] and f['url'] == item['url'] for f in favs):
        favs.append(item)
        save_favorites(favs)

def remove_favorite(item):
    favs = load_favorites()
    favs = [f for f in favs if not (f['title'] == item['title'] and f['url'] == item['url'])]
    save_favorites(favs)
