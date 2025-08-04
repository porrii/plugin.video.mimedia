import sys
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcaddon
from favorites import load_favorites
from resources.lib.catalog import load_catalog

addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
addon_url = sys.argv[0]

catalog_url = addon.getSetting('catalog_url')
if not catalog_url:
    # URL por defecto, cámbiala en settings si quieres
    catalog_url = 'https://github.com/porrii/plugin.video.mimedia/blob/main/resources/data/catalog.json'

catalog = load_catalog(catalog_url)

def build_url(query):
    return addon_url + '?' + urllib.parse.urlencode(query)

def list_categories():
    # Mostrar categorías: Películas y Series
    li = xbmcgui.ListItem('Películas')
    url = build_url({'mode': 'list_movies'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    li = xbmcgui.ListItem('Series')
    url = build_url({'mode': 'list_series'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # Mostrar Favoritos
    li = xbmcgui.ListItem('Favoritos')
    url = build_url({'mode': 'list_favorites'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

def list_movies():
    for movie in catalog.get('movies', []):
        li = xbmcgui.ListItem(movie['title'])
        li.setInfo('video', {'title': movie['title']})
        li.setProperty('IsPlayable', 'true')
        li.setArt({'thumb': movie.get('thumb', '')})
        url = build_url({'mode': 'play', 'url': movie['url'], 'title': movie['title']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def list_series():
    for serie in catalog.get('series', []):
        li = xbmcgui.ListItem(serie['title'])
        url = build_url({'mode': 'list_seasons', 'serie': serie['title']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_seasons(serie_title):
    serie = next((s for s in catalog.get('series', []) if s['title'] == serie_title), None)
    if not serie:
        xbmcgui.Dialog().notification('Error', 'Serie no encontrada', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    for season in serie.get('seasons', []):
        li = xbmcgui.ListItem(f"Temporada {season['season']}")
        url = build_url({'mode': 'list_episodes', 'serie': serie_title, 'season': str(season['season'])})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_episodes(serie_title, season_number):
    serie = next((s for s in catalog.get('series', []) if s['title'] == serie_title), None)
    if not serie:
        xbmcgui.Dialog().notification('Error', 'Serie no encontrada', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    season = next((se for se in serie.get('seasons', []) if str(se['season']) == str(season_number)), None)
    if not season:
        xbmcgui.Dialog().notification('Error', 'Temporada no encontrada', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    for ep in season.get('episodes', []):
        li = xbmcgui.ListItem(ep['title'])
        url = build_url({'mode': 'list_links', 'serie': serie_title, 'season': str(season_number), 'episode': ep['title']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_links(serie_title, season_number, episode_title):
    serie = next((s for s in catalog.get('series', []) if s['title'] == serie_title), None)
    if not serie:
        xbmcgui.Dialog().notification('Error', 'Serie no encontrada', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    season = next((se for se in serie.get('seasons', []) if str(se['season']) == str(season_number)), None)
    if not season:
        xbmcgui.Dialog().notification('Error', 'Temporada no encontrada', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    episode = next((ep for ep in season.get('episodes', []) if ep['title'] == episode_title), None)
    if not episode:
        xbmcgui.Dialog().notification('Error', 'Capítulo no encontrado', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    for link in episode.get('links', []):
        li = xbmcgui.ListItem(link.get('label', 'Link'))
        li.setInfo('video', {'title': episode_title})
        li.setProperty('IsPlayable', 'true')
        url = build_url({'mode': 'play', 'url': link['url'], 'title': episode_title})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def play_video(url, title):
    play_item = xbmcgui.ListItem(path=url)
    play_item.setInfo('video', {'title': title})
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def list_favorites():
    favs = load_favorites()
    if not favs:
        xbmcgui.Dialog().notification('Info', 'No tienes favoritos', xbmcgui.NOTIFICATION_INFO)
        xbmcplugin.endOfDirectory(addon_handle)
        return
    for item in favs:
        li = xbmcgui.ListItem(item['title'])
        li.setProperty('IsPlayable', 'true')
        li.setInfo('video', {'title': item['title']})
        url = build_url({'mode': 'play', 'url': item['url'], 'title': item['title']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    mode = params.get('mode')
    if mode is None:
        list_categories()
    elif mode == 'list_movies':
        list_movies()
    elif mode == 'list_series':
        list_series()
    elif mode == 'list_seasons':
        list_seasons(params.get('serie'))
    elif mode == 'list_episodes':
        list_episodes(params.get('serie'), params.get('season'))
    elif mode == 'list_links':
        list_links(params.get('serie'), params.get('season'), params.get('episode'))
    elif mode == 'play':
        play_video(params.get('url'), params.get('title'))
    elif mode == 'list_favorites':
        list_favorites()
    else:
        xbmcgui.Dialog().notification('Error', 'Opción no soportada', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    router(sys.argv[2][1:])
