from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
#import os
import time

##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
## Creating the list of codes
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
## Opening the file in read mode
my_file = open("CODIGOS/MIXED_O_V.txt", "r")
  
# Reading the file
data = my_file.read()
# Replacing end splitting the text 
# when newline ('\n') is seen.
list_of_codes = data.split("\n")
#print(list_of_codes)
my_file.close()
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
#####Telling Chrome to run silently
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
options = Options()
options.headless = True
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
### SCRAPING
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################

## Defining vectors that will be used to store important data
codes_to_remove = []
code_and_download_link = []
fiduciaria = ['Oliveira Trust', 'Vortx', 'Planeta']
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##### Collecting Links for Oliveira TRUST
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
for code in list_of_codes:
    ## Setting the Chrome Driver
    driver = webdriver.Chrome(chrome_options=options)

    ## Setting the URL we are going to open
    url = 'https://webapp.oliveiratrust.com.br/home'

    ## Sending a GET request to this URL
    driver.get(url)

    ## Telling the driver to wait until the element pops on screen
    driver.implicitly_wait(5)

    ## Telling the driver to find the element we need (with XPath)
    input = driver.find_element_by_xpath('/html/body/div/div/header/div/div[5]/div[2]/div[1]/div[1]/input')
    input.send_keys(code)

    ## Telling the driver to wait until the CRI element pops on screen
    driver.implicitly_wait(5)

    try:
        ## Telling the driver to click on the link that appeared from our code
        cri = driver.find_element_by_xpath('//*[@id="root"]/div/header/div/div[5]/div[3]/div[1]')
        cri.click()

        ##########################################################################################################################
        ##########################################################################################################################
        print(code)
        ##########################################################################################################################
        ##########################################################################################################################

        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(5)

        ## Telling the driver to click on the link that will take us to the file webpage
        link_to_file = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[1]/div[3]/div[6]/a')
        link_to_file.click()

        ## Getting the link to the next page
        link = link_to_file.get_attribute("href")
        ## Telling the driver to navigate to the new window
        driver.get(link)

        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(5)

        ## Telling the driver to click on the download button
        download_button = driver.find_element_by_xpath('/html/body/a')
        download_link = download_button.get_attribute("href")

        ## Printing to check
        print(download_link)
        
        ## Appending the CETIP code and download link to the list that wil pair them
        code_and_download_link.append((code, download_link, fiduciaria[0]))

        ##########close browser
        driver.quit()

    ####### This treats the error where the code does not belong to the website
    except NoSuchElementException:
        driver.quit()

##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
## Actually removing the codes that have been already used
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
for code in codes_to_remove:
    list_of_codes.remove(code)

##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##### Collecting Links for Vortx
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
for code in list_of_codes:
    ## Setting the Chrome Driver
    driver = webdriver.Chrome(chrome_options=options)

    ## Setting the URL we are going to open
    url = 'https://vortx.com.br/investidor/cri'

    ## Sending a GET request to this URL
    driver.get(url)

    ## Telling the driver to wait until the element pops on screen
    driver.implicitly_wait(5)

    ## Telling the driver to find the element we need (with XPath)
    input = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/div[3]/div/div[1]/div[2]/div/input')
    input.send_keys(code)
    ## Telling the driver to wait until the CRI element pops on screen
    time.sleep(1)

    try:
        ## Telling the driver to click on the link that appeared from our code
        cri = driver.find_element_by_xpath('//*[@id="__next"]/div/section[1]/div[3]/div/div[2]/div/div/div/table/tbody/tr[1]/td[1]/a')
        cri.click()

        ##########################################################################################################################
        ##########################################################################################################################
        print(code)
        ##########################################################################################################################
        ##########################################################################################################################

        ## Telling the driver to wait until the BUTTON element pops on screen
        driver.implicitly_wait(5)

        ## Grabing the code from the url to extract the ID to collect the data
        current_url = driver.current_url
        url_len = len(current_url)
        
        ## Getting the last 5 digits of the url to use it as the code
        id = current_url[len(current_url)-5:]

        ## Putting the URL togheter (this is the download link we will use to treat data and turn into CSV)
        download_link = f"https://apis.vortx.com.br/vxsite/api/operacao/{id}/preco-unitario/historico-pagamentos"

        ## Appending the CETIP code and download link to the list that wil pair them
        code_and_download_link.append((code, download_link, fiduciaria[1]))
        
        ## Adding the code to the code to remove list to remove it afterwards
        codes_to_remove.append(code)

        driver.quit()

    ####### This treats the error where the code does not belong to the website
    except NoSuchElementException:
        driver.quit()

## Creating a dataframe for the CETIPS, LINKS AND FID.
df_cols = ['CETIP', 'Link' , 'Fiduciaria']
df = pd.DataFrame(code_and_download_link, columns=df_cols)

## Creating a CSV from the data collected
df.to_csv('links_for_download.csv', encoding='utf8', index=False)

print(df)
#print('\n'.join('{}: {}'.format(*k) for k in enumerate(code_and_download_link)))
