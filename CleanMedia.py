# **************************************************************************
#       Limpia archivos obsoletos de los directorios "media" dentro de la
#   carpeta "ROMS", usando el gamelist.txt como guía para saber si se usa
#   el archivo.
#
#       CleanMedia.py  ver. 1.0
#
#       Creado por Daniel Serrano   -   dani.eus79@gmail.com
#
# **************************************************************************

import os
import sys
from os import remove
from time import sleep
from clear_screen import clear
from colorama import Fore, Back, Style
from colorama import init, AnsiToWin32
stream = AnsiToWin32(sys.stderr).stream
init()
init(autoreset=True)
init(wrap=False)

ruta_app = os.getcwd()
total = 0
num_archivos = 0
formato = '%d-%m-%y %H:%M:%S'
linea = '-' * 120
todos_directorios = []
todos_archivos = []
ruta_xml = ruta_app + '\\roms\\gamelist.xml'
lista_directorios = []
ruta_roms = ruta_app + '\\roms'

clear()
print(Back.BLUE + Fore.WHITE + Style.BRIGHT + f"""\n
*******************************************************************************
*                                                                             *
*      Limpia archivos obsoletos de los directorios "media" dentro de la      *
*   carpeta "ROMS", usando el gamelist.txt como guía para saber si se usa     *
*   el archivo.                                                               *
*                                                                             *
*       Versión beta, haz una copia de seguridad antes de usar este programa  *
*                                                                             *
*       CleanMedia.py  ver. 1.0                                               *
*                                                                             *
*      Creado por Daniel Serrano   -   dani.eus79@gmail.com                   *
*                                                                             *
*******************************************************************************
\n""")

# sleep(5)

for ruta, directorios, archivos in os.walk(ruta_roms, topdown=True):
    print(Back.BLUE + Style.BRIGHT + '\nRuta       :',
          Back.BLUE + Style.BRIGHT + ruta)
    print('\n')
    sleep(2)
    for elemento in archivos:
        num_archivos += 1
        archivo = ruta + os.sep + elemento
        estado = os.stat(archivo)
        tamaño = estado.st_size
        total += tamaño
        print(linea)
        print(Fore.YELLOW + 'archivo      :', Fore.LIGHTYELLOW_EX + elemento)
        print(Fore.YELLOW + 'tamaño (Kb)  :', round(tamaño/1024, 1))
        if elemento.endswith(('png', 'PNG', 'mp4', 'MP4', 'jpg', 'JPG')):
            print(Fore.MAGENTA + 'Ruta         :', Fore.LIGHTMAGENTA_EX + ruta)
            print(Back.BLACK + Fore.GREEN + Style.BRIGHT +
                  "ENCONTRADO ARCHIVO MULTIMEDIA")
            todos_directorios.append(ruta)
            todos_archivos.append(elemento)

print(linea)
print(Back.BLACK + Fore.BLUE + Style.BRIGHT + 'Núm. archivos:', num_archivos)
print(Back.BLACK + Fore.YELLOW + Style.BRIGHT +
      'Total (kb)   :', round(total/1024, 1))
peso_kb = round(total/1024)
peso_Mb = peso_kb / 1000
print(Back.BLACK + Fore.YELLOW + Style.BRIGHT + 'Total (Mb)   :', peso_Mb)

print(linea)
diccionario = dict((('directorios', todos_directorios),
                    ('archivos', todos_archivos)))
print("\n")
print(linea)
print("\n")
numero_archivos = len(todos_archivos)
print(Back.BLACK + Fore.GREEN + Style.BRIGHT +
      "Total archivos multimedia escaneados: ", numero_archivos)
if num_archivos == 0:
    sys.exit()
print("\n")
print(linea)
print("\n")
sleep(5)
clear()

diccionario_archivos = diccionario.values()
diccionario_directorios = diccionario.keys()
print(linea)
numero = 0
archivo_objetivo = diccionario['archivos'][0]
directorio_objetivo = diccionario['directorios'][0]
total = directorio_objetivo + '\\' + archivo_objetivo
total_archivos_borrados = 0
pesototal = 0

for file in todos_archivos:
    correcto = 0
    with open(ruta_xml, "r", encoding="utf8") as fichero_xml:
        for line in fichero_xml:
            archivo_objetivo = diccionario['archivos'][numero]
            if file in line:
                # clear()
                print(linea)
                print()
                print(Back.BLACK + Fore.YELLOW + Style.BRIGHT +
                      "Archivo correcto:")
                directorio_objetivo = diccionario['directorios'][numero]
                archivo_objetivo = diccionario['archivos'][numero]
                total = directorio_objetivo + '\\' + archivo_objetivo
                print(Back.BLACK + Fore.RED + Style.BRIGHT + "     ", total)
                # print(numero)
                if numero < num_archivos:
                    numero = numero + 1
                correcto = 1
                # print(file)
                print()
                break

    if correcto == 0:
        directorio_objetivo = diccionario['directorios'][numero]
        archivo_objetivo = diccionario['archivos'][numero]
        total = directorio_objetivo + '\\' + archivo_objetivo
        # clear()
        print(linea)
        print()
        print(Back.BLACK + Fore.YELLOW + Style.BRIGHT + "Archivo obsoleto:")
        print(Back.BLACK + Fore.BLUE + Style.BRIGHT + "El archivo ",
              Back.BLACK + Fore.WHITE + Style.BRIGHT + total +
              Back.BLACK + Fore.RED + Style.BRIGHT + " va a ser eliminado")
        if numero < num_archivos:
            numero = numero + 1
        print()
        archivo = total
        estado = os.stat(archivo)
        tamaño = estado.st_size
        pesototal += tamaño
        total_archivos_borrados += 1
        remove(total)

fichero_xml.close()

clear()
print()
print(linea)
print()
print(Back.BLACK + Fore.YELLOW + Style.BRIGHT +
      "Total archivos obsoletos borrados: ", total_archivos_borrados)
print(Back.BLACK + Fore.GREEN + Style.BRIGHT +
      'Total (kb)   :', round(pesototal/1024, 1))
peso_kb = round(pesototal/1024)
peso_Mb = peso_kb / 1000
print(Back.BLACK + Fore.RED + Style.BRIGHT + 'Total (Mb)   :', peso_Mb)
