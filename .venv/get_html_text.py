
from selenium import webdriver
from selenium.webdriver.common.by import By
from db_data import get_onderneming_2, insert_query
import pandas as pd
import re
import time
import openpyxl
def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'https://{}'.format(url)
    return url
def get_page(pages, ref, naam):
    print(pages)
    
    print("hallo0")

    DRIVER_PATH = "./chromedriver.exe"
    driver = webdriver.Chrome(DRIVER_PATH)
    print("hallo1,5")

    base = ref
    print(base)
    driver.get(formaturl(base))
    print("hallo1")

    url = driver.current_url
    print("TITLE " + url)
    page = driver.find_element(By.TAG_NAME, 'body')
    print("hallo")
    if(base not in pages):
        pages[base] = [page.text]
        time.sleep(6)
        print("sleeping")
        query = 'INSERT INTO dep."html_paginas"("naam","url", "text") VALUES( ' + f" '{naam}'  , '{ref}', '{page.text}' ) " 
        insert_query(query)

        print("sleeping")

        time.sleep(6)
        links = page.find_elements(By.TAG_NAME, 'a')
        print("/////////////////////////////////////////////////")
        for link in links :
            
            ref = link.get_attribute('href')
            try:
                ref_check = ref.split("//")[1].split("/")[0]
                url_check = url.split("//")[1].split("/")[0]
                print(ref_check)
                print(url_check)
                print(".......................................")
                if(ref not in pages):
                    if ref_check in url_check or url_check in ref_check:
                        print("url ok")
                        if  ".jpg" not in ref and ".png" not in ref:
                            print("dom ok")
                            print(ref)
                            
                            pages = get_page(pages ,ref, naam)
                            
                            print(len(pages))
            except (Exception) as error: print(error)
            finally : continue
            
    driver.quit()
    return pages


pages = {}
res = get_onderneming_2()
count = 0
for row in res:
 if count < 10 :
    count = count + 1
 else:
  try:
    pages = get_page(pages,row[4], row[1])
    pager = {}
    time.sleep(30)
  except (Exception) as error:
    print(error)

df = pd.DataFrame.from_dict(pages).T.reset_index()
print(df)
df.to_excel("output.xlsx") 
