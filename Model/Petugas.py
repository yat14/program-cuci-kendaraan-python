from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QMessageBox, QTableWidgetItem, QDialog
from Database.koneksi import koneksiDB

class Petugas(QDialog):
    def __init__(self):
        super(Petugas, self).__init__()
        uic.loadUi('UI/Petugas.ui', self)
        self.btnReset.clicked.connect(self.clearData) #aksi tombol reset
        self.btnSave.clicked.connect(self.insertData) #aksi tombol save
        self.btnSearch.clicked.connect(self.searchData) #aksi tombol search
        self.btnUpdate.clicked.connect(self.updateData) #aksi tombol update
        self.btnDelete.clicked.connect(self.deleteData) #aksi tombol delete
        self.edit_mode=""
       
    def clearData(self):
        self.kodePetugas.clear()
        self.namaPetugas.clear()
        self.kodeUmur.clear()
        self.kodeAlamat.clear()
        self.btnSave.setEnabled(True)

    def viewPetugas(self):
        cursor = koneksiDB.db.cursor()
        sql = ("SELECT id_petugas, nama_petugas, umur, alamat FROM petugas")
        cursor.execute(sql)
        result = cursor.fetchall()
        self.gridPetugas.setHorizontalHeaderLabels(['ID','Nama', 'umur', 'Alamat'])
        self.gridPetugas.setRowCount(0)

        for row_number, row_data in enumerate(result):
             print(row_number)
             self.gridPetugas.insertRow(row_number)
             for column_number, data in enumerate(row_data):
                  #print(column_number)
                  self.gridPetugas.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self):
        IDPet = self.kodePetugas.text().strip()
        NamaPet = self.namaPetugas.text().strip()
        UmurPet = self.kodeUmur.text().strip()
        AlamatPet = self.kodeAlamat.text().strip()

        cursor = koneksiDB.db.cursor()
        # Periksa apakah data sudah ada
        sql_check = "SELECT COUNT(*) FROM petugas WHERE id_petugas = %s"
        cursor.execute(sql_check, (IDPet,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            self.messagebox("Peringatan", "Data dengan ID Petugas tersebut sudah ada, silakan input ID Petugas yang berbeda")
            return
        
        sql = "INSERT INTO petugas (id_petugas, nama_petugas, umur, alamat) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (IDPet,NamaPet,UmurPet,AlamatPet))
        koneksiDB.db.commit()

        # Validasi input
        if not IDPet or not NamaPet or not UmurPet or not AlamatPet:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return
       

        if(cursor.rowcount>0):
            self.messagebox("SUKSES","Data Petugas Kendaraan Berhasil Di Tambahkan")
        else:
            self.messagebox("GAGAL","Data Petugas Kendaraan Gagal Di Tambahkan")

        print("{}data berhasil disimpan".format(cursor.rowcount))

        self.clearData()
        self.viewPetugas() #reload data

    def searchData(self):
        idPet = self.kodePetugas.text()
        cursor = koneksiDB.db.cursor()
        sql = "SELECT * FROM petugas WHERE id_petugas=%s"
        cursor.execute(sql, (idPet,))
        result = cursor.fetchall()
        if result:
            for x in result:
                    self.idPet= (x[0])
                    self.namaPetugas.setText(str(x[1]))
                    self.kodeUmur.setText(str(x[2]))
                    self.kodeAlamat.setText(str(x[3]))

            if(cursor.rowcount>0):
                self.messagebox("SUKSES", "Data Petugas Kendaraan Berhasil Di Temukan")
                self.btnSave.setEnabled(False)
        else:
            self.messagebox("GAGAL", "Data Petugas Kendaraan Tidak Berhasil Di Temukan")
            self.clearData()
            self.btnSave.setEnabled(True)

    def updateData(self):
        IDPet = self.kodePetugas.text().strip()
        NamaPet = self.namaPetugas.text().strip()
        UmurPet = self.kodeUmur.text().strip()
        AlamatPet = self.kodeAlamat.text().strip()

        cursor = koneksiDB.db.cursor()
        sql = "UPDATE petugas SET nama_petugas=%s, umur=%s, alamat=%s WHERE id_petugas=%s"
        cursor.execute(sql, (NamaPet, UmurPet, AlamatPet, IDPet))
        koneksiDB.db.commit()

        if not IDPet:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        if not NamaPet or not AlamatPet or not UmurPet:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data Petugas Kendaraan Berhasil Di Perbarui")
        else:
            self.messagebox("GAGAL", "Data Petugas Kendaraan Gagal Di Perbarui")

        print("{} data berhasil diupdate".format(cursor.rowcount))

        self.clearData() #clear entri data
        self.viewPetugas() #reload data

            
    def deleteData(self):
        IDPet = str(self.kodePetugas.text())
        cursor = koneksiDB.db.cursor()
        sql = "DELETE FROM petugas WHERE id_petugas=%s"
        cursor.execute(sql, (IDPet, ))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data Petugas Kendaraan Berhasil Di Hapus")
        else:
            self.messagebox("GAGAL", "Data Petugas Kendaraan Gagal Di Hapus")

        print("{} data berhasil di hapus".format(cursor.rowcount))

        self.clearData() # Clear entry form
        self.viewPetugas() #Reload
        self.btnSave.setEnabled(True) #mematikan aksi save
    
    def messagebox(self, title, message):
            mess = QMessageBox()
            mess.setWindowTitle(title)
            mess.setText(message)
            mess.setStandardButtons (QMessageBox.Ok)
            mess.exec_()
