### CURRENTLY WORKING VERSION
import requests
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import json

## Importing csv with download link
links_csv = pd.read_excel('links_from_all_codes.xlsx')

## Grabbing only Oliveira Trust Links
oliveira_links = links_csv.loc[links_csv['Fiduciaria'] == 'Oliveira Trust']
print(len(oliveira_links))
## Grabbing only Vortx Links
vortx_links = links_csv.loc[links_csv['Fiduciaria'] == 'Vortx']
print(len(vortx_links))
## Declaring the dataframe where things will get appended to
# Defining a list to store all the data frames that will get concatenated together
list_of_df = []

##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################

##################$$$$$$$$$$$$$$$$$$$$$$$$$$$$ BEGGINING OF OLIVEIRA TRUST LOOP $$$$$$$$$$$$$$$$$$$#######################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
for link in oliveira_links['Link']:
    
    ## Setting the link to grab the data
    url = link
    print(url)
    ## Reading the HTML and formatting it into a dataframe
    initial_df = pd.read_html(url, encoding='utf8', skiprows=1, header=0)[0]
    ## Renaming dataframe columns
    initial_df.rename(columns={'Juros.1':'Pagamento de Juros', 'Premio.1':'Pagamento de Premio'}, inplace=True)
    
    ## Converting "Data" to datetime format
    initial_df['Data'] = pd.to_datetime(initial_df['Data']).dt.date

    ## Defining new dataframe with only the columns im going to use
    new_df = initial_df[['Data', 'Valor Nominal', 'Juros', 'Pagamento de Juros', 'Amortização', 'Total', 'P.U.']]

    ## MONTH END
    new_df['Data'] = pd.to_datetime(new_df['Data']) + MonthEnd(1)
    ## Creating a list with the values to concat later (as oncat only accepts lists)
    ## Declaring the two vectors we need to append this data (and also so they reset on the next code in loop)
    cetip = []
    fiduciaria = []
    ## Grabbing the row with the code to this specific Likn/URL on the loop
    row = oliveira_links.loc[oliveira_links['Link'] == link]

    ## Looping to the number of elements in the dataframe so we match the dataframe to append
    for element in new_df['Data']:
        cetip.append(row['CETIP'].iat[0])
        fiduciaria.append(row['Fiduciaria'].iat[0])

    ## Adding these "CETIP" AND "FIDUCIARIA" columns to the dataframe
    new_df.insert(0, 'Fiduciaria', fiduciaria)
    new_df.insert(0, 'CETIP', cetip)


    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ## Sorting by oldest date
    new_df.sort_values(by='Data', inplace=True)

    ## Appending each formatted dataframe to the list of dataframes
    list_of_df.append(new_df)

##################$$$$$$$$$$$$$$$$$$$$$$$$$$$$ END OF OLIVEIRA TRUST LOOP $$$$$$$$$$$$$$$$$$$#############################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################

##################$$$$$$$$$$$$$$$$$$$$$$$$$$$$ BEGGINING OF VORTX LOOP $$$$$$$$$$$$$$$$$$$################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################
for link in vortx_links['Link']:
    
    url = link

    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ##########################################################################################################################################################

    ## Getting the page with the data
    response = requests.request("GET", url)
    ## Transforming it into a raw json
    raw_json_txt = response.json()
    ## Normalizing the json data into the format we need
    json_txt = pd.json_normalize(raw_json_txt, "unitPrices", ["Data", "operationId", "smartBondId", "Pagamento de Juros", "Amortização", \
        "Pagamento Total", "PU(completo)", "PU(vazio)", "Juros", "Valor Nominal"], errors='ignore',record_prefix='_')

    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ##########################################################################################################################################################

    ## Converting into Dataframe
    df = pd.DataFrame(json_txt)

    ## Renaming Columns
    df = df.rename(columns= {'_paymentDate':'Data','_interest':'Pagamento de Juros','_amortization':'Amortização','_total':'Total','_unitPriceFull':'P.U.','_interestValue':'Juros','_nominalValue':'Valor Nominal'})

    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ##########################################################################################################################################################

    ## Getting only the columns we need
    new_df = df[['Data', 'Valor Nominal', 'Juros','Pagamento de Juros', 'Amortização', 'Total', 'P.U.']]

    ## Removing duplicated column names
    new_df = new_df.loc[:,~new_df.columns.duplicated()]

    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ## MONTH END
    new_df['Data'] = pd.to_datetime(new_df['Data']) + MonthEnd(1)
    ## Creating a list with the values to concat later (as oncat only accepts lists)
    ## Declaring the two vectors we need to append this data (and also so they reset on the next code in loop)
    cetip = []
    fiduciaria = []
    ## Grabbing the row with the code to this specific Likn/URL on the loop
    row = vortx_links.loc[vortx_links['Link'] == link]

    ## Looping to the number of elements in the dataframe so we match the dataframe to append
    for element in new_df['Data']:
        cetip.append(row['CETIP'].iat[0])
        fiduciaria.append(row['Fiduciaria'].iat[0])

    ## Adding these "CETIP" AND "FIDUCIARIA" columns to the dataframe
    new_df.insert(0, 'Fiduciaria', fiduciaria)
    new_df.insert(0, 'CETIP', cetip)

    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    ## Sorting by oldest date
    new_df.sort_values(by='Data')

    ## Appending each formatted dataframe to the list of dataframes
    list_of_df.append(new_df)

##################$$$$$$$$$$$$$$$$$$$$$$$$$$$$ END OF VORTX LOOP $$$$$$$$$$$$$$$$$$$######################################################################
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################


#############################################$$$$$ PUTTING ALL DATAFRAMES TOGETHER $$$$$##################################################################
##########################################################################################################################################################
##########################################################################################################################################################


## Putting together all the dataframes we have
concatenated_list_of_df = pd.concat(list_of_df)

## Converting date to only year and month
concatenated_list_of_df['Data'] = pd.to_datetime(concatenated_list_of_df['Data'], format='%Y-%m-%d')
concatenated_list_of_df['Mes e Ano'] =  concatenated_list_of_df['Data'].dt.to_period('M')

## Summing for last day of each month
#final_dataframe = concatenated_list_of_df.groupby(['Fiduciaria', 'CETIP','Mes e Ano'])[['Amortização', 'Pagamento de Juros', 'Total']].sum().reset_index()
sum_last_day_of_month_values = concatenated_list_of_df.groupby(['Fiduciaria', 'CETIP', 'Data']).agg({'Valor Nominal':'min' ,'Amortização':'sum', 'Pagamento de Juros':'sum', 'Total':'sum'}).reset_index()

#[['Pagamento de Juros']].sum().reset_index()

## Removing duplicate date values, to only get the last date (day) of each row
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# sum_last_day_of_month_values = sum_last_day_of_month_values.drop_duplicates(subset = ['Data'], keep ='last').reset_index(drop = True)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
## Transforming the datetime with only Year/Month/Day (no hour display)
sum_last_day_of_month_values['Data'] = sum_last_day_of_month_values['Data'].dt.date
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

## Generating an excel from it, so we can check the results
sum_last_day_of_month_values.to_excel('TEST-ENV-OT_V_TEST-ALL-1.xlsx', encoding='utf8', index=False)

## Printing the concatenated list of dataframes
sum_last_day_of_month_values

#print(len(list_of_df))

#concatenated_list_of_df
#sum_last_day_of_month_values