from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os
import time

#### Setting the download Path
###object of ChromeOptions class
op = webdriver.ChromeOptions()
######browser preferences
######p = {'download.default_directory': 'C:/Users/Downloads/Test'}

## Creating the list of codes

## Opening the file in read mode
my_file = open("CODIGOS/CODIGOS_OLIVEIRA_TRUST.txt", "r")
  
# Reading the file
data = my_file.read()
  
# Replacing end splitting the text 
# when newline ('\n') is seen.
list_of_codes = data.split("\n")
#print(list_of_codes)
my_file.close()


for code in list_of_codes:
    ## Setting the Chrome Driver
    driver = webdriver.Chrome(options=op)

    ## Setting the URL we are going to open
    url = 'https://webapp.oliveiratrust.com.br/home'

    ## Sending a GET request to this URL
    driver.get(url)

    ## This is the Search Bar XPath
    ##### /html/body/div/div/header/div/div[5]/div[2]/div[1]/div[1]/input

    ## Telling the driver to wait until the element pops on screen
    driver.implicitly_wait(5)

    ## Telling the driver to find the element we need (with XPath)
    input = driver.find_element_by_xpath('/html/body/div/div/header/div/div[5]/div[2]/div[1]/div[1]/input')
    input.send_keys(code)


    ## Telling the driver to wait until the CRI element pops on screen
    driver.implicitly_wait(0.5)

    try:
        ## Telling the driver to click onto the link that appeared from our code
        cri = driver.find_element_by_xpath('//*[@id="root"]/div/header/div/div[5]/div[3]/div[1]')
        cri.click()


        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(10)

        ## Telling the driver to click on the link that will take us to the file webpage
        link_to_file = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div/div[1]/div[3]/div[6]/a')
        link_to_file.click()

        ## Getting the link to the next page
        link = link_to_file.get_attribute("href")
        ## Telling the driver to navigate to the new window
        driver.get(link)

        ## Telling the driver to wait until the LINK element pops on screen
        driver.implicitly_wait(10)

        ## Telling the driver to click on the download button
        download_button = driver.find_element_by_xpath('/html/body/table/tbody/tr[1]/td[8]')
        download_button.click()

        ## Waiting for the download
        time.sleep(1)
        
        #close browser

        driver.quit()

    except NoSuchElementException:
        driver.quit()
    


    