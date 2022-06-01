import xlwings as xw
import pandas as pd


## Grabbing workbooks
wb_template = xw.Book('template/template.xlsx')
wb_target = xw.Book('links_test.xlsx')


## Grabbing worksheets
ws_template = wb_template.sheets('Template_IPCA')
try:
    wb_target.sheets.add('clean_template')
    ws_copy_template = wb_target.sheets('clean_template')
except:
    ws_copy_template = wb_target.sheets('clean_template')

## FOR PANDAS TO READ FROM
ws_links = wb_target.sheets['Sheet1']
xlsx = pd.ExcelFile('links_test.xlsx')
## Reading the worksheet so we can get the data out of it
df = pd.read_excel(xlsx, ws_links.name)

## Gabbring all the elements from the CETIP list (the result is a Series/Column) / Converting the column into an array with the CETIP values
cetip_list_values = df['CETIP'].values
## Getting the first CETIP row code for test
row_1 = df.loc[df['CETIP'] == cetip_list_values[0]]



## Copying one template to another
ws_template.range('A1:AA20').copy(ws_copy_template.range('A1:AA20'))

## Deleting all the useless data inside this spreadsheet, to make a clean one
## Defining a new name to the same spreadsheet as it has been created
ws_full_copied = wb_target.sheets('clean_template')
## Deleteing useless values from the first table on top left corner
ws_full_copied.range('B2:B7').value = 0
## Deleting all useless data from the rest of the spreadsheet
ws_full_copied.range('C2:AA20').delete()

## Saving the changes
wb_target.save('clean_links_with_template.xlsx')
