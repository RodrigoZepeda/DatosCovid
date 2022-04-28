#! /usr/bin/Rscript
rm(list = ls())
library(osfr)
library(magrittr)
library(glue)
library(stringr)
setwd("/media/rodrigo/covid/datasets/")

#Get files
zipdata <- list.files(pattern = ".*.zip", full.names = T)

#Get project
covid_project <- osf_retrieve_node("https://osf.io/9nu2d/")

#List files
osfiles <- covid_project %>%
  osf_ls_files("Datos Abiertos COVID", n_max = Inf)

#Get address
osfiles_address <- covid_project %>%
  osf_ls_files(pattern = "Datos Abiertos COVID") 

for (fname in zipdata){
  if (!(str_remove(fname,"\\./") %in% osfiles$name)){
    
    message(glue("Uploading {fname}"))
    
    #Upload file
    covid_project %>%
      osf_upload(path = fname, conflicts = "skip") %>% 
      osf_mv(osfiles_address)
    
    message(glue("Success!"))
  
  }
}