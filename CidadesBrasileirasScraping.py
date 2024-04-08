import time 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
import requests
import os


options = webdriver.ChromeOptions() 
options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
options.page_load_strategy = "none"
driver = Chrome() 
driver.implicitly_wait(10)


raiz = "C:\\Users\\harri\\Documents\\Programacao\\Python\\FacebookFaces\\"
cidadesFile = raiz+"CidadesBrasileiras.txt"

wikpediaCidades = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil"

driver.get(wikpediaCidades)


cidades = driver.find_elements(By.TAG_NAME, "li")

for cidade in cidades:
    
    try:
        if cidade.text != "":
            cidadeFormatada = cidade.text.split("(")[0]
            
            if not os.path.isfile(cidadesFile):
                
                file1 = open(cidadesFile, "w")            
                file1.writelines(str(cidadeFormatada).strip()+"\n")
                file1.close()
            
            else:
                
                file1 = open(cidadesFile, "a")  # append mode
                file1.write(str(cidadeFormatada).strip()+"\n")
                file1.close()
    except:
        print("Erro ao pegar cidade")