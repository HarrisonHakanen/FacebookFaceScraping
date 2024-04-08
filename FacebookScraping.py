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


usr="facehbrasil01@gmail.com"
pwd="eunaosei1997"

raiz = "C:\\Users\\harri\\Documents\\Programacao\\Python\\FacebookFaces\\"
pessoasCadastradas = raiz+"Pessoas\\"
pessoasCadastradasFile = raiz+"PessoasCadastradas.txt"


if not os.path.exists(pessoasCadastradas):
    os.mkdir(pessoasCadastradas)



facebookUrl = "https://www.facebook.com"

driver.get(facebookUrl)

driver.find_element(By.NAME, "email").send_keys(usr)
driver.find_element(By.NAME, "pass").send_keys(pwd)
driver.find_element(By.NAME,"login").click()

time.sleep(4)



listaNomesFile = ["NomesBrasileiros.txt","NomesAmericanos.txt"]
listaCidadesFile = ["CidadesBrasileiras.txt","CidadesAmericanas.txt"]


contador = 0


for nomesFile in listaNomesFile:
    
    listaNomes = open(nomesFile, "r",encoding="latin-1")


    nomes = listaNomes.readlines()
    
    for nome in nomes:
                    
        
        for cidadesFile in listaCidadesFile: 
            
                    
            listaCidades = open(cidadesFile, "r",encoding="latin-1")
            
            
            cidadesParaPesquisar = listaCidades.readlines()
            
            
            for cidadePesquisa in cidadesParaPesquisar:
            
                nome = nome.strip()
                cidadePesquisa = cidadePesquisa.strip()
                
                
                
                
                pesquisaUrl = "https://www.facebook.com/search/people/?q="+nome+"&sde=AbqYQQCuIq_5M5MKYA4Iw2z-7xyPApveqAXCe28_Flb57xRVS02IPjGGG4DWRathWwaD0uN042zmnORXBhq4wEPf"
                
                driver.get(pesquisaUrl)
                time.sleep(4)
                
                
                driver.find_element(By.XPATH,"//input[@aria-label='Cidade']").send_keys(cidadePesquisa);
                
                time.sleep(2)
                
                cidades = driver.find_elements(By.TAG_NAME, "li")
                
                entrouEmAlgumaCidade = False
                
                for cidade in cidades:
                    
                    try:
                        
                        if cidade.text == cidadePesquisa:
                            entrouEmAlgumaCidade = True            
                            cidade.click()
                    except:
                        print("Erro ao entrar na cidade")
                        
                if entrouEmAlgumaCidade:
                
                    try:
                        
                        achouFim = False
                        htmlString = driver.page_source
                    
                        while achouFim == False:
                            
                            
                            if "Fim dos resultados" not in htmlString:
                                driver.execute_script("window.scrollBy(0, arguments[0]);", 2000)
                                htmlString = driver.page_source
                                time.sleep(1)            
                            else:
                                achouFim = True
                        
                            
                        
                        divs = driver.find_elements(By.XPATH, "//a[@href]")
                    
                        
                        
                        listaDeAlbunsDePerfis = []
                    
                        for elem in divs:
                               
                            link = elem.get_attribute("href")
                            if "profile" in link:    
                                            
                                linkPartes = link.split("&")
                                
                                linkIdPartes = linkPartes[0].split("id=")                        
                                
                                listaDeAlbunsDePerfis.append(linkPartes[0]+"&sk=photos_albums");            
                                
                                
                        listaDeAlbunsDePerfis = list(dict.fromkeys(listaDeAlbunsDePerfis))
                        
                    
                        for album in listaDeAlbunsDePerfis:
                            
                            idPessoa = album.split("id=")[1].split("&")[0]        
                            path = pessoasCadastradas+str(idPessoa)
                            
                            print("Analisando a pessoa:" +str(idPessoa))
                            
                            pessoaJaCadastrada = False
                            
                            if not os.path.isfile(pessoasCadastradasFile):
                                
                                file1 = open(pessoasCadastradasFile, "w")            
                                file1.writelines(str(idPessoa))
                                file1.close()
                            
                            else:
                                
                    
                                file1 = open(pessoasCadastradasFile, 'r')
                                Lines = file1.readlines()
                                 
                                count = 0
                    
                                for line in Lines:
                                    count += 1
                                    if line.strip() == str(idPessoa):
                                        pessoaJaCadastrada = True
                                    
                                file1.close()
                                
                                
                                if pessoaJaCadastrada == False:
                                
                                    file1 = open(pessoasCadastradasFile, "a")  # append mode
                                    file1.write(str("\n"+idPessoa))
                                    file1.close()
                                
                            
                            
                            if pessoaJaCadastrada == False:
                            
                                if not os.path.exists(path):
                                    os.mkdir(path)
                                
                                try:
                                    driver.get(album)
                                    time.sleep(6)
                                    
                                      
                                    a_class = driver.find_elements(By.XPATH, "//a[@href]")
                                    
                                    
                                    fotosDoPerfilLink = ""
                                    for i in range(len(a_class)):
                                        
                                        try:                        
                                            if "Fotos do perfil" in a_class[i].text:
                                                                    
                                                fotosDoPerfilLink = a_class[i].get_attribute("href")
                                                i = len(a_class)
                                                
                                        except:
                                            print("")
                                            
                                    
                                    if fotosDoPerfilLink != "":
                                                                        
                                        try:
                                            
                                            driver.get(fotosDoPerfilLink)
                                            time.sleep(6)
                                            
                                            a_fotos = driver.find_elements(By.TAG_NAME, "img")
                                            
                                            indexImagem = 0
                                            
                                            for a_foto in a_fotos:
                                                                
                                                img_url = a_foto.get_attribute("src")
                                                img_data = requests.get(img_url).content
                                                with open(path+"\\Foto"+str(indexImagem)+".jpg", 'wb') as handler:
                                                    
                                                    handler.write(img_data)
                                                
                                                indexImagem += 1
                                                
                                        except:
                                            print("Erro ao acessar o album de fotos do perfil: "+fotosDoPerfilLink)
                                except:            
                                    print("Erro ao acessar o album: "+album)        
                    except:
                        print("Erro ao acessar o nome: "+nome)
                        
                contador+=1
            
            listaCidades.close()
            
    listaNomes.close()
        
        
        
