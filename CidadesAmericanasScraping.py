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
cidadesFile = raiz+"CidadesAmericanas.txt"

wikpediaCidades = "https://pt.wikipedia.org/wiki/Categoria:Listas_de_cidades_dos_Estados_Unidos_por_estado"

driver.get(wikpediaCidades)


estadosPorLetra = driver.find_elements(By.CLASS_NAME, "mw-category-group")

estadoId = 0

linksDosEstados = []

for estadoAlfabeto in estadosPorLetra:
    
    if estadoId > 0:
        
        try:
            if estadoAlfabeto.text != "":                
                estados = estadoAlfabeto.find_elements(By.TAG_NAME, "li")
                
                for estado in estados:
                    
                    try:
                         estadoLink = estado.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
                         linksDosEstados.append(estadoLink)
                         
                    except:
                        print("Erro ao pegar estado")
                                                
        except:
            print("Erro ao pegar grupo de estados")
            
    estadoId += 1
    
    

for link in linksDosEstados:
    
    cidadesContent = ""    
    
    driver.get(link)
    time.sleep(2)
    
    cidades = driver.find_elements(By.TAG_NAME, "li")
        
    driver.get(link)
    time.sleep(2)
    
    
    cidades = driver.find_elements(By.XPATH,"//div[contains(@class, 'div-col columns column-width')]")    
    
    cidadesNomes = []
    
    if len(cidadesNomes) == 0:
        cidadesTb = driver.find_elements(By.TAG_NAME, "tbody")
        
        if len(cidadesTb)>0:
            
            cidadesNomes = cidadesTb[1].find_elements(By.TAG_NAME, "th")
            if len(cidadesNomes) < 2:
                cidadesNomes = []
                
    if len(cidadesNomes) == 0:
        cidadesNomes = driver.find_elements(By.TAG_NAME, "li")
    
    if len(cidadesNomes) == 0:
        cidadesUl = driver.find_elements(By.TAG_NAME, "ul")
        
        for cidade in cidadesUl:
            nomes = cidade.find_elements(By.TAG_NAME, "li")
            
            for nome in nomes:
                cidadesNomes.append(nome.text.strip())
            
        
    for cidade in cidadesNomes:
        
        try:
            if cidade.text != "":
                cidadesContent += "\n"+cidade.text.strip()
        except:
            print("Erro ao pegar o nome da cidade")
            
    
    if not os.path.isfile(cidadesFile):
        
        file1 = open(cidadesFile, "w",encoding="utf8")            
        file1.writelines(str("\n"+cidadesContent).strip())
        file1.close()
    
    else:
        
        file1 = open(cidadesFile, "a",encoding="utf8")  # append mode
        file1.write(str("\n"+cidadesContent).strip())
        file1.close()        