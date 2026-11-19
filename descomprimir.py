#!/usr/bin/env python3
"""
Descomprime todos los archivos comprimidos (.zip, .tar, .tar.gz, .tgz, .7z, .rar)
que se encuentren en una carpeta y los extrae en esa misma carpeta.

Uso:
    python descomprimir.py                      # usa la ruta por defecto
    python descomprimir.py "D:\\otra\\ruta"      # usa otra ruta
"""

import shutil
import sys
import tarfile
import zipfile
from pathlib import Path

# ----------------------------- CONFIGURACIÓN -----------------------------
RUTA_POR_DEFECTO = r"D:\Documentos\Modulos QX\22.13\Ejecutables"

# True  -> cada archivo se extrae en una subcarpeta con su mismo nombre
# False -> el contenido se extrae directamente en la ruta
EXTRAER_EN_SUBCARPETA = True

# True -> borra el archivo comprimido después de extraerlo correctamente
ELIMINAR_ORIGINAL = False
# -------------------------------------------------------------------------

EXTENSIONES = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".7z", ".rar")


def nombre_sin_extension(archivo: Path) -> str:
    """Quita la extensión (incluyendo dobles como .tar.gz)."""
    nombre = archivo.name
    for ext in sorted(EXTENSIONES, key=len, reverse=True):
        if nombre.lower().endswith(ext):
            return nombre[: -len(ext)]
    return archivo.stem


def extraer(archivo: Path, destino: Path) -> None:
    nombre = archivo.name.lower()
    destino.mkdir(parents=True, exist_ok=True)

    if nombre.endswith(".zip"):
        with zipfile.ZipFile(archivo) as z:
            z.extractall(destino)

    elif nombre.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2")):
        with tarfile.open(archivo) as t:
            t.extractall(destino)

    elif nombre.endswith(".7z"):
        try:
            import py7zr
        except ImportError:
            raise RuntimeError("Falta la librería 'py7zr'. Instálala con: pip install py7zr")
        with py7zr.SevenZipFile(archivo, mode="r") as z:
            z.extractall(path=destino)

    elif nombre.endswith(".rar"):
        try:
            import rarfile
        except ImportError:
            raise RuntimeError("Falta la librería 'rarfile'. Instálala con: pip install rarfile")
        with rarfile.RarFile(archivo) as r:
            r.extractall(destino)

    else:
        raise RuntimeError("Formato no soportado")


def iniciar_interfaz() -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox

    ventana = tk.Tk()
    ventana.title("Descompresor de archivos")
    ventana.resizable(False, False)

    archivo_var = tk.StringVar()
    destino_var = tk.StringVar()

    def seleccionar_archivo() -> None:
        archivo = filedialog.askopenfilename(
            parent=ventana,
            title="Selecciona el archivo comprimido",
            filetypes=[
                ("Archivos comprimidos", "*.zip *.tar *.tar.gz *.tgz *.tar.bz2 *.7z *.rar"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if archivo:
            archivo_var.set(archivo)

    def seleccionar_destino() -> None:
        destino = filedialog.askdirectory(
            parent=ventana,
            title="Selecciona dónde descomprimir",
            mustexist=True,
        )
        if destino:
            destino_var.set(destino)

    def ejecutar() -> None:
        archivo = Path(archivo_var.get().strip())
        destino = Path(destino_var.get().strip())

        if not archivo.is_file():
            messagebox.showerror("Falta el archivo", "Selecciona un archivo comprimido válido.", parent=ventana)
            return
        if not archivo.name.lower().endswith(EXTENSIONES):
            messagebox.showerror("Formato no compatible", "El archivo no tiene un formato compatible.", parent=ventana)
            return
        if not destino.is_dir():
            messagebox.showerror("Falta la carpeta", "Selecciona una carpeta de destino válida.", parent=ventana)
            return

        boton_ejecutar.config(state=tk.DISABLED)
        estado_var.set("Descomprimiendo...")
        ventana.update_idletasks()
        try:
            extraer(archivo, destino)
        except Exception as error:
            estado_var.set("")
            messagebox.showerror("Error al descomprimir", str(error), parent=ventana)
        else:
            estado_var.set("Descompresión completada.")
            messagebox.showinfo(
                "Descompresión completada",
                f"Archivo: {archivo.name}\nDestino: {destino}",
                parent=ventana,
            )
        finally:
            boton_ejecutar.config(state=tk.NORMAL)

    marco = tk.Frame(ventana, padx=14, pady=14)
    marco.grid(sticky="nsew")
    marco.columnconfigure(1, weight=1)

    tk.Label(marco, text="Archivo comprimido:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
    tk.Entry(marco, textvariable=archivo_var, width=62).grid(row=0, column=1, sticky="ew", pady=6)
    tk.Button(marco, text="Examinar...", command=seleccionar_archivo).grid(row=0, column=2, padx=(8, 0), pady=6)

    tk.Label(marco, text="Carpeta de destino:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
    tk.Entry(marco, textvariable=destino_var, width=62).grid(row=1, column=1, sticky="ew", pady=6)
    tk.Button(marco, text="Examinar...", command=seleccionar_destino).grid(row=1, column=2, padx=(8, 0), pady=6)

    estado_var = tk.StringVar()
    tk.Label(marco, textvariable=estado_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))
    boton_ejecutar = tk.Button(marco, text="Aceptar y descomprimir", command=ejecutar)
    boton_ejecutar.grid(row=2, column=2, sticky="e", padx=(8, 0), pady=(8, 0))

    ventana.mainloop()


def main() -> int:
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO)

    if not ruta.is_dir():
        print(f"[ERROR] La ruta no existe o no es una carpeta: {ruta}")
        return 1

    archivos = sorted(
        f for f in ruta.iterdir()
        if f.is_file() and f.name.lower().endswith(EXTENSIONES)
    )

    if not archivos:
        print(f"No se encontraron archivos comprimidos en: {ruta}")
        return 0

    print(f"Ruta: {ruta}")
    print(f"Archivos comprimidos encontrados: {len(archivos)}\n")

    ok, fallidos = 0, []

    for i, archivo in enumerate(archivos, start=1):
        destino = ruta / nombre_sin_extension(archivo) if EXTRAER_EN_SUBCARPETA else ruta
        print(f"[{i}/{len(archivos)}] Descomprimiendo: {archivo.name} ...", end=" ")
        try:
            extraer(archivo, destino)
            if ELIMINAR_ORIGINAL:
                archivo.unlink()
            print("OK")
            ok += 1
        except Exception as e:
            print("FALLÓ")
            fallidos.append((archivo.name, str(e)))

    print("\n----------- RESUMEN -----------")
    print(f"Correctos: {ok}")
    print(f"Fallidos : {len(fallidos)}")
    for nombre, error in fallidos:
        print(f"  - {nombre}: {error}")

    return 0 if not fallidos else 2


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        iniciar_interfaz()
    elif len(sys.argv) > 1:
        sys.exit(main())
    elif getattr(sys, "frozen", False):
        iniciar_interfaz()
    else:
        sys.exit(main())
