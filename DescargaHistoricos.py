import requests
import os
import datetime
import glob
import filecmp
from datetime import date
from daterange import *
import subprocess
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

download_folder = '/media/rodrigo/covid/datasets'
#download_folder = '/home/rodrigo/Desktop'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

#Fecha inicial de datos
#https://www.gob.mx/cms/uploads/attachment/file/604001/Datos_abiertos_hist_ricos_2020.pdf
start_date = date(2020, 4, 12)
end_date   = date.today()

#Ejemplos de fechas
#http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/04/datos_abiertos_covid19_12.04.2020.zip
#http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/2022/02/datos_abiertos_covid19_22.02.2022.zip

#Latest: A partir de abril empezaron a subir este
#https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip


base_url   = 'https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos'
latest_url = 'https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip'

#Descarga por fecha
for fecha in daterange(start_date, end_date):

    #Formateo de los datos
    mes   = '{:02d}'.format(fecha.month)
    dia   = '{:02d}'.format(fecha.day)
    anio  = str(fecha.year)
    dname = "datos_abiertos_covid19_%s.%s.%s.zip" % (dia, mes, anio)

    #Checar si ya lo tenemos en carpeta
    if not os.path.isfile(os.path.join(download_folder, dname)):

        if anio == str(2020):
            url = base_url + "/" + mes + "/" + dname
        else:
            url   = base_url + "/" + anio + "/" + mes + "/" +  dname

        print('Descargando ' + fecha.strftime("%d/%m/%Y") + " de "  + url)

        # Descarga del archivo
        try:
            req = requests.get(url, verify=False)

            if req.status_code == 404:
                print("Datos no encontrados para " + fecha.strftime("%d/%m/%Y"))

            else:
                # Split URL to get the file name
                filename = os.path.join(download_folder, url.split('/')[-1])

                # Writing the file to the local file system
                with open(filename, 'wb') as output_file:
                    output_file.write(req.content)
                print('Descarga completada de ' + fecha.strftime("%d/%m/%Y"))

        except:
            print('No encontrado el archivo para ' + fecha.strftime("%d/%m/%Y"))

    else:
        print("El archivo de " + fecha.strftime("%d/%m/%Y") + " ya está descargado")

#Descarga el más reciente
#Check latest file
files = sorted(os.listdir(download_folder), key=lambda fn: - os.path.getctime(os.path.join(download_folder, fn)))

try:
    print("Buscando los más recientes...")
    req = requests.get(latest_url, verify=False)

    if req.status_code == 404:
        print("Datos más recientes no encontrados")

    else:
        # Split URL to get the file name
        filename = os.path.join(download_folder, latest_url.split('/')[-1])

        # Writing the file to the local file system
        with open(filename, 'wb') as output_file:
            output_file.write(req.content)
        print('Descarga completada de latest')

except:
    print('No encontrado el archivo para ' + fecha.strftime("%d/%m/%Y"))

#Compare both files
are_files_equal = filecmp.cmp(filename, os.path.join(download_folder, files[0]))
if are_files_equal:
    os.remove(filename)
    print("No hay datos más recientes")
else:
    os.rename(filename, os.path.join(download_folder, "datos_abiertos_covid19_" + date.today().strftime("%d.%m.%Y") + ".zip"))
    print("Datos más recientes descargados")

#To run make executable (chmod +777 upload_osf.R on command line)
subprocess.call("./upload_osf.R")