# MiMedia Kodi Addon

Addon Kodi para reproducir películas y series desde un catálogo JSON alojado en GitHub.

## Características

- Categorías: Películas y Series
- Series organizadas en temporadas y capítulos
- Varios links por capítulo
- Favoritos almacenados localmente
- Actualización dinámica del catálogo desde GitHub

## Instalación

1. Descarga o clona este repositorio.
2. Comprime todos los archivos en un ZIP (la carpeta raíz debe contener `addon.xml`).
3. En Kodi, ve a *Add-ons* > *Instalar desde archivo ZIP*.
4. Selecciona el ZIP y espera que se instale.
5. Ejecuta el addon desde *Video Add-ons*.

## Configuración

Edita `resources/data/config.json` para poner la URL de tu catálogo JSON alojado en GitHub.

## Cómo actualizar catálogo

Sube un archivo `catalog.json` actualizado a tu repositorio GitHub en la URL indicada en `config.json`.

Kodi cargará el catálogo remoto cada vez que abras el addon.

---

## Cómo contribuir

Si quieres añadir películas o series, edita el archivo `catalog.json` y súbelo a GitHub.

---

Disfruta y comenta cualquier duda o mejora.
