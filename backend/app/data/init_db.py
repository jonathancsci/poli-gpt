import psycopg2
import csv
import os

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def init_db():
    conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="db")
    cur = conn.cursor()

    def is_table_empty(table_name):
        cur.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1);")
        return not cur.fetchone()[0]

    tables = ['liberal', 'conservative']
    file_paths = ['/backend/app/data/liberal_news_articles.csv', '/backend/app/data/conservative_news_articles.csv']

    for table, file_path in zip(tables, file_paths):
        if is_table_empty(table):
            print(f"Table {table} is empty. Inserting data...")

            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    headline = row['HeadLine']
                    body = row['Body']
                    url = row['URL']
                    
                    cur.execute(
                        f'INSERT INTO {table} (headline, body, url) VALUES (%s, %s, %s)',
                        (headline, body, url)
                    )
                    
                    conn.commit()
        else:
            print(f"Table {table} already contains data. Pass.")
            print(file_path)

    cur.close()
    conn.close()

    print("Data upload complete")

