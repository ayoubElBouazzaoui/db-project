from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
def fill_site(ondernemingsnummer):
    time.sleep(10)
    text = requests.get(f"https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer={ondernemingsnummer}&actionLu=Zoek").text
    
    soup = BeautifulSoup(text, 'lxml')
    rows = soup.find(id="table")
    rows = rows.find_all("tr")
    count = 0
    web_row = ""
    for row in rows:
        if count < 12:
         print(count)
         
         count = count + 1
        else : 
            count2 = 0
            for td in row:
                if count2 > 0:
                    
                    web_row = td.getText()
                    break
                else :
                    print(td) 
                    count2 = count2 + 1
            print(web_row)
            break

    time.sleep(10)
    if web_row == "Geen gegevens opgenomen in KBO.":
        return None
    else: return web_row


