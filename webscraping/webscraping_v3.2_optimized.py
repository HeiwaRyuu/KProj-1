from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

## Defining chrome driver path
chrome_driver_path = 'DRIVER/chromedriver.exe'

##########################################################################################################################
##########################################################################################################################
#********************************************** Creating the list of codes **********************************************#
##########################################################################################################################
##########################################################################################################################
## Opening the file in read mode - ACTUAL FILE
my_file = open("CODIGOS/codigos_resumido.txt", "r")
# Reading the file
data = my_file.read()
# Replacing End: splitting the text when newline ('\n') is seen.
list_of_codes = data.split("\n")
#print(list_of_codes)
my_file.close()



##########################################################################################################################
##########################################################################################################################
#**************************************** Telling Chrome to run silently ************************************************#
##########################################################################################################################
##########################################################################################################################
options = Options()
# Option that actually makes chrome run silently
options.headless = True



##########################################################################################################################
##########################################################################################################################
#***************************************************** SCRAPING *********************************************************#
##########################################################################################################################
##########################################################################################################################

#***************************** Defining vectors that will be used to store important data *******************************#
## Stores already used codes, so the next website loop won't have to wate time looping through them again
codes_to_remove = []
## Stores the final data we collected from the website
code_and_download_link = []
## A vector containing the name of the websites we are scraping so we can map each code to its own website
fiduciaria = ['Oliveira Trust', 'Vortx', 'Planeta']

##########################################################################################################################
##########################################################################################################################
#*************************************** Collecting Links for Oliveira TRUST ********************************************#
##########################################################################################################################
##########################################################################################################################
for code in list_of_codes:
    ## Setting the Chrome Driver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)

    ## Setting the URL we are going to open
    url = 'https://webapp.oliveiratrust.com.br'

    ## Sending a GET request to this URL
    driver.get(url)

    ## Telling the driver to wait until the INPUT shows up on screen
    driver.implicitly_wait(5)

    ## Telling the driver to find the INPUT element
    input = driver.find_element_by_xpath('//*[@id="root"]/div/header/div/div[5]/div[2]/div[1]/div[1]/input')
    input.send_keys(code)

    ## Telling the driver to wait until the CRI element pops on screen
    driver.implicitly_wait(5)

    try:
        ## Telling the driver to click on the link that appeared from our code
        cri = driver.find_element_by_xpath('//*[@id="root"]/div/header/div/div[5]/div[3]/div[1]')
        cri.click()
        
        ## Printing the CETIP code to check if we are looping through correctly
        print(code)

        ##########################################################################################################################
        ##########################################################################################################################
        #**************************************** GRABBING DATA *****************************************************************#
        ##########################################################################################################################
        ##########################################################################################################################
        #informações de indexador, taxa, data de emissão(OK), data de vencimento(OK),
        # preço unitário inicial (valor nominal, normalmente é 1.000) (OK), número de cotas(OK).
        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(5)

        ## Grabbing the NUMBER OF UNITS that have been released
        units_element = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[3]/div[9]/div[2]')
        units = units_element.text

        ## Grabbing EMISSION date
        emission_date_element = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[3]/div[5]/div[2]')
        emission_date = emission_date_element.text

        ## Grabbing MATURITY date
        maturiy_date_element = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[3]/div[6]/div[2]')
        maturiy_date = maturiy_date_element.text

        ## Grabbing NOMINAL VALUE
        nominal_value_element = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[3]/div[8]/div[2]')
        nominal_value = nominal_value_element.text
        #************************************ TREATING THE NOMINAL VALUE **************************************************#
        # Mapping each unwanted charcter to none
        nominal_value = str(nominal_value).translate(str.maketrans('','',' R$(*)'))

        ## Grabbing REMUNERATION
        remuneration_element = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[3]/div[11]/div[2]')
        remuneration = remuneration_element.text

        ## Grabbing CRI INDEX
        cri_index_element = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[3]/div[10]/div[2]')
        cri_index = cri_index_element.text

        ##########################################################################################################################
        ##########################################################################################################################

        
        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(5)

        ## Telling the driver to click on the link that will take us to the file webpage
        link_to_file = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[1]/div[3]/div[6]/a')
        #link_to_file.click()
        ## Getting the link to the next page
        link = link_to_file.get_attribute("href")
        ## Telling the driver to navigate to the new window
        driver.get(link)

        ## Telling the driver to wait until the download button shows up on screen
        driver.implicitly_wait(5)

        ## Grabbing the download button element and its "href" tag data, as it contains the download link
        download_button = driver.find_element_by_xpath('/html/body/a')
        download_link = download_button.get_attribute("href")

        ## Printing download link to check if we are getting the expected output
        #print(download_link)
        
        ## Appending the CETIP code and download link to the list that wil pair them
        code_and_download_link.append((code, download_link, fiduciaria[0], cri_index, remuneration, units, emission_date, maturiy_date, nominal_value))


        ## Adding the code to a list of already used codes to remove it after it has already been used (so we don't waste time on treated codes)
        codes_to_remove.append(code)


        ## Closing browser
        driver.quit()

    ####### This treats the error where the code does not belong to the website
    except NoSuchElementException:
        ## Closing browser
        driver.quit()

##########################################################################################################################
##########################################################################################################################
#************************************ Removing the codes that have already been used ************************************#
##########################################################################################################################
##########################################################################################################################
for code in codes_to_remove:
    list_of_codes.remove(code)
print(code_and_download_link)

##########################################################################################################################
##########################################################################################################################
#***************************************** Collecting Links for Vortx ***************************************************#
##########################################################################################################################
##########################################################################################################################
for code in list_of_codes:
    ## Setting the Chrome Driver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)

    ## Setting the URL we are going to open
    url = 'https://vortx.com.br/investidor/cri'

    ## Sending a GET request to this URL
    driver.get(url)

    ## Telling the driver to wait until the INPUT shows up on screen
    driver.implicitly_wait(5)

    ## Telling the driver to find the INPUT element
    input = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/div[3]/div/div[1]/div[2]/div/input')
    input.send_keys(code)
    ## Telling the driver to wait until the CRI element pops on screen (i'll try to improve the way i'm doing it later)
    time.sleep(1.5)

    try:
        ## Telling the driver to click on the link that appeared from the input of the CETIP code
        cri = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/div[3]/div/div[2]/div/div/div/table/tbody/tr[1]/td[1]/a')
        cri.click()

        ## Printing the CETIP code to check if we are looping through correctly
        print(code)

        ##########################################################################################################################
        ##########################################################################################################################
        #************************************************** GRABBING DATA *******************************************************#
        ##########################################################################################################################
        ##########################################################################################################################
        # informações de indexador, taxa, data de emissão(OK), data de vencimento(OK),
        # preço unitário inicial (valor nominal, normalmente é 1.000) (OK), número de cotas(OK).

        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(5)

        ## Grabbing the NUMBER OF UNITS that have been released
        units_element = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/section/section[2]/div[2]/div[2]/div[1]/h4')
        units = units_element.text

        ## Grabbing EMISSION date
        emission_date_element = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/section/section[2]/div[1]/div[2]/h4')
        emission_date = emission_date_element.text

        ## Grabbing MATURITY date
        maturiy_date_element = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/section/section[2]/div[1]/div[3]/h4')
        maturiy_date = maturiy_date_element.text

        ## Grabbing NOMINAL VALUE
        nominal_value_element = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/section/section[2]/div[2]/div[2]/div[2]/h4')
        nominal_value = nominal_value_element.text
        #************************************ TREATING THE NOMINAL VALUE **************************************************#
        # Mapping each unwanted charcter to none via third parameter from "str.maketrans(x,y,z)"
        # the last parameter (z) is a list of characters to remove
        nominal_value = str(nominal_value).translate(str.maketrans('','',' R$(*)'))

        ## Grabbing REMUNERATION
        remuneration_element = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/section/section[2]/div[1]/div[1]/h4')
        remuneration = remuneration_element.text

        ## Grabbing CRI INDEX
        index_vector = ['IPCA', 'CDI', 'IGPM']
        #******************* AS THIS IS NOT EXPLICITLY STATED ON THE PAGE, WE CHECK IT FROM THE REMUNERATION INFO ***************#
        # this loop checks if theres any of these indexes associated with the tax, if there is, we use it as our (financial) index value
        for index in index_vector:
            if index in remuneration:
                cri_index = index
                break
            else:
                cri_index = 'Não informado'


        ##########################################################################################################################
        ##########################################################################################################################

        ## Telling the driver to wait until the page loads properly
        driver.implicitly_wait(5)

        ## Grabing the url from the code to extract the ID to collect the data
        current_url = driver.current_url
        url_len = len(current_url)
        
        ## Getting the last 5 digits of the url to use it as the code (code ID)
        id = current_url[len(current_url)-5:]

        ## Putting the URL togheter (this is the download link we will use to treat data and turn into CSV via another code)
        download_link = f"https://apis.vortx.com.br/vxsite/api/operacao/{id}/preco-unitario/historico-pagamentos"

        ## Appending the CETIP code and download link to the list that wil pair them
        code_and_download_link.append((code, download_link, fiduciaria[1], cri_index, remuneration, units, emission_date, maturiy_date, nominal_value))
        
        ## Adding the code to the code to remove list to remove it after it has already been used
        codes_to_remove.append(code)

        ## Closing browser
        driver.quit()

    ####### This treats the error where the code does not belong to the website
    except NoSuchElementException:
        ## Closing browser
        driver.quit()


##########################################################################################################################
##########################################################################################################################
#************************************************** CREATING CSV ********************************************************#
##########################################################################################################################
##########################################################################################################################

## Creating a dataframe for the CETIPS, LINKS AND FID.
df_cols = ['CETIP', 'Link' , 'Fiduciaria', 'Indexador', 'Remuneração', 'Quantidade de Ativos', 'Data Emissão', 'Data Vencimento', 'P.U. Inicial (Valor Nominal)']
df = pd.DataFrame(code_and_download_link, columns=df_cols)

## Creating a CSV from the data collected
df.to_excel('links.xlsx', encoding='utf8', index=False)

# Printing dataframe to check its format and data
print(df)

