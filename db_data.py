
import psycopg2


def insert_query(query, comp, url, text):
    try:
        print("connecting to db")
        conn = psycopg2.connect(database='DEP', user='postgres', password='', host='vichogent.be', port='40045',options="-c search_path=dep" )
        cur = conn.cursor()
        print("doing query")
        cur.execute(query,(str(comp), str(url), str(text)))
        conn.commit()
        cur.close()
        conn.close()
    except (Exception) as error : 
        print(f"postgres error : {error}")
        print(text)

def get_ondernemingen(fiscaal_jaar):
    conn = psycopg2.connect(database='DEP', user='postgres', password='', host='vichogent.be', port='40045',options="-c search_path=dep" )
    cur = conn.cursor()
    cur.callproc('getondernemingenscrapingcodingtreewebsite', (fiscaal_jaar, ))
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result


def update_scrape_log(FiscaalJaar, OndernemingID):
    conn = psycopg2.connect(database='DEP', user='postgres', password='', host='vichogent.be', port='40045',options="-c search_path=dep" )

    cursor = conn.cursor()
    sql = """INSERT INTO "ScrapeLog" ("FiscaalJaar", "OndernemingID", "Website") VALUES (%s, %s, %s)"""

    cursor.execute(sql, (FiscaalJaar, OndernemingID, "1"))

    conn.commit()

    cursor.close()
    conn.close()

def insert_website_text(fiscaal_jaar, onderneming_id, website_text):
    conn = psycopg2.connect(database='DEP', user='postgres', password='', host='vichogent.be', port='40045',options="-c search_path=dep" )

    cursor = conn.cursor()

    sql = """INSERT INTO "OndernemingWebsite" ("FiscaalJaar", "OndernemingID", "WebsiteText") VALUES (%s, %s, %s, %s, %s)"""

    cursor.execute(sql, (fiscaal_jaar, onderneming_id, website_text))

    conn.commit()

    cursor.close()
    conn.close()