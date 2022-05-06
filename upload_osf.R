#! /usr/bin/Rscript
rm(list = ls())
library(rdrop2)
library(magrittr)
library(glue)
library(stringr)

#Dropbox
drop_auth(rdstoken = "dropbox_token.rds")

#Get files
uploaded_files  <- drop_dir("COVID-OSF/Datos Abiertos COVID")

downloaded_data <- list.files(path = "/media/rodrigo/covid/datasets/",
                              pattern = ".*.zip", full.names = T)


for (fname in downloaded_data){
  if (!(basename(fname) %in% uploaded_files$name)){
    
    message(glue("Uploading {str_remove_all(basename(fname),'datos_abiertos_covid19_|.zip')}"))
    
    #Upload file
    drop_upload(fname, path = "/COVID-OSF/Datos Abiertos COVID",
                verbose = FALSE)
    
    message(glue("Success!"))
    
  }
}
