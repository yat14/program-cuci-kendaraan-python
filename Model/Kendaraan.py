from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QMessageBox, QTableWidgetItem, QDialog
from Database.koneksi import koneksiDB

class Kendaraan(QDialog):
    def __init__(self):
        super(Kendaraan, self).__init__()
        uic.loadUi('UI/Kendaraan.ui', self)

        #Button Aksi
        self.btnSave.clicked.connect(self.insertData) #aksi tombol save
        self.btnReset.clicked.connect(self.clearData) #aksi tombol reset
        self.btnSearch.clicked.connect(self.searchData) #aksi tombol search
        self.btnUpdate.clicked.connect(self.updateData) #aksi tombol update
        self.btnDelete.clicked.connect(self.deleteData) #aksi tombol delete
        self.edit_mode=""

    def clearData(self):
        self.kodeKendaraan.clear()
        self.jenisKendaraan.clear()
        self.btnSave.setEnabled(True)

    def viewKendaraan(self):
        cursor = koneksiDB.db.cursor()
        sql = ("SELECT id_kendaraan, jenis_kendaraan FROM kendaraan")
        cursor.execute(sql)
        result = cursor.fetchall()
        self.gridKendaraan.setHorizontalHeaderLabels(['ID','Jenis Kendaraan'])
        self.gridKendaraan.setRowCount(0)

        for row_number, row_data in enumerate(result):
             print(row_number)
             self.gridKendaraan.insertRow(row_number)
             for column_number, data in enumerate(row_data):
                  #print(column_number)
                  self.gridKendaraan.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self):
        IDKend = self.kodeKendaraan.text().strip()
        JenisKend = self.jenisKendaraan.text().strip()

        # Validasi input
        if not IDKend or not JenisKend:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return
        
        cursor = koneksiDB.db.cursor()
        # Periksa apakah data sudah ada
        sql_check = "SELECT COUNT(*) FROM kendaraan WHERE id_kendaraan = %s"
        cursor.execute(sql_check, (IDKend,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            self.messagebox("Peringatan", "Data dengan ID Kendaraan tersebut sudah ada, silakan input ID Kendaraan yang berbeda")
            return
        
        sql = "INSERT INTO kendaraan (id_kendaraan, jenis_kendaraan) VALUES (%s,%s)"
        cursor.execute(sql, (IDKend,JenisKend))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES","Data Kendaraan Berhasil Di Tambahkan")
        else:
            self.messagebox("GAGAL","Data Kendaraan Gagal Di Tambahkan")

        print("{}data berhasil disimpan".format(cursor.rowcount))

        self.clearData()
        self.viewKendaraan() #reload data
    
    def searchData(self):
        IDKend = self.kodeKendaraan.text()
        cursor = koneksiDB.db.cursor()
        sql = "SELECT * FROM kendaraan WHERE id_kendaraan=%s"
        cursor.execute(sql, (IDKend,))
        result = cursor.fetchall()
        if result:
            for x in result:
                    self.idKendaraan= (x[0])
                    self.jenisKendaraan.setText(str(x[1]))

            if(cursor.rowcount>0):
                self.messagebox("SUKSES", "Data Kendaraan Berhasil Di Temukan")
                self.btnSave.setEnabled(False)
        else:
            self.messagebox("GAGAL", "Data Kendaraan Tidak Berhasil Di Temukan")
            self.clearData()
            self.btnSave.setEnabled(True)

    def updateData(self):
        IDKend = self.kodeKendaraan.text().strip()
        JenisKend = self.jenisKendaraan.text().strip()

         # Validasi jika data belum dicari
        if not IDKend:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        
        # Validasi input
        if not JenisKend:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return
        
        cursor = koneksiDB.db.cursor()
        sql = "UPDATE kendaraan SET jenis_kendaraan=%s WHERE id_kendaraan=%s"
        cursor.execute(sql, (JenisKend, IDKend))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data Kendaraan Berhasil Di Perbarui")
        else:
            self.messagebox("GAGAL", "Data Kendaraan Gagal Di Perbarui")

        print("{} data berhasil diupdate".format(cursor.rowcount))

        self.clearData() #clear entri data
        self.viewKendaraan() #reload data
    
    def deleteData(self):
        IDKend = str(self.kodeKendaraan.text())
        cursor = koneksiDB.db.cursor()
        sql = "DELETE FROM kendaraan WHERE id_kendaraan=%s"
        cursor.execute(sql, (IDKend, ))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data Kendaraan Berhasil Di Hapus")
        else:
            self.messagebox("GAGAL", "Data Kendaraan Gagal Di Hapus")

        print("{} data berhasil di hapus".format(cursor.rowcount))

        self.clearData() # Clear entry form
        self.viewKendaraan() #Reload
        self.btnSave.setEnabled(True) #mematikan aksi save
    
    def messagebox(self, title, message):
            mess = QMessageBox()
            mess.setWindowTitle(title)
            mess.setText(message)
            mess.setStandardButtons (QMessageBox.Ok)
            mess.exec_()