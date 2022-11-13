import pandas as pd
import psycopg2 
from fill_website_field import fill_site

def isNaN(cell):
    return cell != cell

conn = psycopg2.connect(database='DEP', user='postgres', password='', host='vichogent.be', port='40045',options="-c search_path=dep" )
df = pd.read_excel("./kmo's_Vlaanderen_2021.xlsx", sheet_name ="Lijst")
df.info()
for row in df.iterrows():
    id = int(row[1][0])
    naam = row[1][1].replace("'", "")
    gemeente = row[1][2].replace("'", "")
    ondernemingsnummer = row[1][7]
    webadres = row[1][11]
    print(webadres)
    if isNaN(webadres):
        print(webadres)
        webadres = fill_site(row[1][7])
    if webadres is not None :
                cur = conn.cursor()
                id = int(row[1][0])
                naam = row[1][1].replace("'", "")
                gemeente = row[1][2].replace("'", "")
                ondernemingsnummer = row[1][7]
                webadres = row[1][11]
                print(id)
                print(ondernemingsnummer)
                query = 'INSERT INTO dep."Onderneming_2"("ID", "Naam", "Gemeente", "Ondernemingsnummer", "WebAdres") VALUES( '    f" '{id}'  , '{naam}', '{gemeente}', '{ondernemingsnummer}', '{webadres}' ) " 
                cur.execute(query)
                conn.commit()
    else : print("no website")








 

    
	                                                        


