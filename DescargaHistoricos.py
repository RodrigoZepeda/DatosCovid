import requests
import os
import datetime
from datetime import date
from daterange import *

download_folder = '/media/rodrigo/COVID/datasets'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

#Fecha inicial de datos
#https://www.gob.mx/cms/uploads/attachment/file/604001/Datos_abiertos_hist_ricos_2020.pdf
start_date = date(2020, 4, 12)
end_date   = date.today() - datetime.timedelta(1)

#http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/04/datos_abiertos_covid19_12.04.2020.zip
#http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/2022/02/datos_abiertos_covid19_22.02.2022.zip

base_url = 'https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos'
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
            req = requests.get(url)

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

