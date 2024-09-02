import psycopg2

conn = psycopg2.connect(
    host='141.13.162.170',
    port='5432',
    user='***', #USERNAME HERE
    password='***', #PASSWORD HERE
    dbname='testdb'
)

def insertInTable(type, date, zone, hash, description):
    try:
        cursor = conn.cursor()
        query = "INSERT into cra_anomaly.anomaly_logging(type, date, zone, hash, description) VALUES(%s, %s, %s, %s, %s);"
        data = (type, date, zone, hash, description)
        cursor.execute(query, data)
        conn.commit()
        print('data inserted successfully')
    except psycopg2.Error as e:
        conn.rollback()
        print("Error inserting data:", e)
    finally:
        cursor.close()