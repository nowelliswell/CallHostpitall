import sqlite3

def save_data_to_db(queue_manager):
    conn = sqlite3.connect("hospital_queue.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS queues (poly TEXT, number INTEGER, name TEXT)")
    cursor.execute("DELETE FROM queues")  # Hapus data lama
    for poly, queue in queue_manager.queues.items():
        for patient in queue:
            cursor.execute("INSERT INTO queues VALUES (?, ?, ?)", (poly, patient[0], patient[1]))
    conn.commit()
    conn.close()