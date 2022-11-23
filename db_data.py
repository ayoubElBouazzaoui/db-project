
import psycopg2

def connect_to_db():

    connection_config_dict = {
        'host': 'vichogent.be',
        'port': 40045,
        'database': 'DEP',
        'user': 'postgres',
        'password': '',
        'options': "-c search_path=dep"
    }

    try:
        connection = psycopg2.connect(**connection_config_dict)
        return connection

    except (Exception, psycopg2.DatabaseError) as e:
        print("Error while connecting to PostgreSQL", e)
        exit()


def insert_query(query, comp, url, text):
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(query,(str(comp), str(url), str(text)))
        conn.commit()
        cur.close()
        conn.close()


def get_ondernemingen(fiscaal_jaar):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.callproc('getondernemingenscrapingcodingtreewebsite', (fiscaal_jaar, ))
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result


def update_scrape_log(FiscaalJaar, OndernemingID):
    conn = connect_to_db()

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