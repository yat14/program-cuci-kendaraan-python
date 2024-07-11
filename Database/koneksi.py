import mysql.connector

class koneksiDB:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="cucikendaraan")
    
    print('koneksi berhasil')