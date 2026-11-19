# Descompresor de archivos

Aplicación para seleccionar un archivo comprimido y la carpeta de destino desde una ventana. También extrae los comprimidos que encuentre dentro y conserva el modo por consola para buscar en una carpeta y sus subcarpetas.

**Ruta configurada por defecto:**

```
D:\Documentos\Modulos QX\22.13\Ejecutables
```

## Formatos soportados

| Formato | Requiere instalar algo |
|---|---|
| `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2` | No (viene con Python) |
| `.7z` | `pip install py7zr` |
| `.rar` | `pip install rarfile` + tener `UnRAR` o `7-Zip` instalado |

## Requisitos

- Python 3.8 o superior. Verifica con:
  ```
  python --version
  ```
- (Opcional) Librerías para `.7z` y `.rar`:
  ```
  pip install py7zr rarfile
  ```

## Uso de la ventana

Abre `DescomprimirArchivo.exe`. Selecciona el archivo comprimido y la carpeta de destino, y pulsa **Aceptar y descomprimir**. También se extraerán los archivos comprimidos que estén dentro del archivo elegido, conservando las carpetas. Para abrir la ventana desde Python, ejecuta `python descomprimir.py --gui`.

## Modo por consola

Para procesar todos los comprimidos de una carpeta y sus subcarpetas:

1. Abre **CMD** o **PowerShell** y ve a la carpeta del script:
   ```
   cd D:\Documentos\Personal\Quipux\descomprimirpy
   ```
2. Ejecuta el script. Sin argumentos usa la carpeta configurada; también puedes indicar otra:
   ```
   python descomprimir.py
   python descomprimir.py "D:\Otra\Carpeta"
   ```

El ejecutable abre la ventana automáticamente al hacer doble clic.

## Crear el ejecutable

Con PyInstaller instalado en el entorno de Python, ejecuta desde la carpeta del proyecto:

```
pyinstaller --onefile --windowed --name DescomprimirArchivo descomprimir.py
```

El ejecutable se crea en la carpeta `dist`.

ZIP y TAR funcionan sin dependencias externas. Para que el `.exe` procese `.7z`, `py7zr` debe estar instalado al compilar; los archivos `.rar` pueden requerir UnRAR o 7-Zip en el equipo.
Se procesan hasta 50 niveles de archivos comprimidos anidados; si alguno falla, se informa en el resumen.

## Opciones de configuración

Al inicio de `descomprimir.py` puedes cambiar:

| Variable | Valor por defecto | Qué hace |
|---|---|---|
| `RUTA_POR_DEFECTO` | `D:\Documentos\Modulos QX\22.13\Ejecutables` | Carpeta donde están los comprimidos |
| `EXTRAER_EN_SUBCARPETA` | `True` | `True`: crea una carpeta por cada archivo con su mismo nombre. `False`: extrae todo directamente en la ruta |
| `ELIMINAR_ORIGINAL` | `False` | `True`: borra el comprimido después de extraerlo con éxito |

## Ejemplo de resultado

Antes:
```
Ejecutables\
├── ModuloA.zip
├── ModuloB.zip
└── ModuloC.7z
```

Después (con `EXTRAER_EN_SUBCARPETA = True`):
```
Ejecutables\
├── ModuloA.zip
├── ModuloA\
├── ModuloB.zip
├── ModuloB\
├── ModuloC.7z
└── ModuloC\
```

## Salida en consola

```
Ruta: D:\Documentos\Modulos QX\22.13\Ejecutables
Archivos comprimidos encontrados: 3

[1/3] Descomprimiendo: ModuloA.zip ... OK
[2/3] Descomprimiendo: ModuloB.zip ... OK
[3/3] Descomprimiendo: ModuloC.7z ... OK

----------- RESUMEN -----------
Correctos: 3
Fallidos : 0
```

## Solución de problemas

- **`python` no se reconoce como comando:** reinstala Python marcando la casilla *"Add Python to PATH"*, o prueba con `py descomprimir.py`.
- **La ruta no existe:** revisa que el disco `D:` esté disponible y que el nombre de la carpeta esté bien escrito.
- **Falta la librería `py7zr` / `rarfile`:** instálala con `pip install py7zr rarfile`.
- **Error con `.rar`:** `rarfile` necesita la herramienta `UnRAR` o `7-Zip` instalada y en el PATH.
- **Archivo corrupto o con contraseña:** el script lo marca como *FALLÓ*, continúa con los demás y lo muestra en el resumen final.
- **Permisos denegados:** ejecuta la terminal como administrador.
