# ---------------------------------------------------------------------------------------------
# index.py
# Python 3.X required to run
# Created by Julian Smith

# Import mySQL library into python
import pymysql


def index_links(index_title, index_url, index_desc, index_key, index_def, index_code):
    # Set up mySql environment
    try:
        conn = pymysql.connect(host='212.48.67.136', port=3306, user='apropos_julian', password='Sr0rwccd605', autocommit=True,
                               use_unicode=True, charset="utf8")
        cur = conn.cursor()
        # Edit main database
        cur.execute("USE apropos_indexedResultsDB")
        # Insert values into database
        cur.execute("INSERT INTO indexTable (title, url, description, keywords, definition, code_example) VALUES (%s,%s,%s,%s,%s,%s)"
                     "",(index_title, index_url, index_desc, index_key, index_def, index_code))
        # Close connection
        cur.close()
        conn.close()
    # If an error occurs, print error details
    except pymysql.OperationalError as e:
        print("--------------------------------------------------------------------------------------")
        print("ERROR |", e, "| ITEM NOT INDEXED")