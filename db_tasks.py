from postgres_conn import get_connection

def insert_mash(data):
    conn = get_connection('postmash')
    sql = "INSERT INTO mashes(winnerid, loserid, timestamp,remote_addr) VALUES (%s, %s, %s, %s)"
    conn.cursor().execute(sql, (data['winner'], data['loser'], data['timestamp'], data['remote_addr']))
    conn.commit()
