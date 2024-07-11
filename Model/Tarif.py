from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QMessageBox, QTableWidgetItem, QDialog
from Database.koneksi import koneksiDB

class Tarif(QDialog):
    def __init__(self):
        super(Tarif, self).__init__()
        uic.loadUi('UI/Tarif.ui', self)

          #Button Aksi
        self.btnSave.clicked.connect(self.insertData) #aksi tombol save
        self.btnReset.clicked.connect(self.clearData) #aksi tombol reset
        self.btnSearch.clicked.connect(self.searchData) #aksi tombol search
        self.btnUpdate.clicked.connect(self.updateData) #aksi tombol update
        self.btnDelete.clicked.connect(self.deleteData) #aksi tombol delete
        self.edit_mode=""

    def clearData(self):
        self.kodeTarif.clear()
        self.Tarif.clear()
        self.btnSave.setEnabled(True)

    def viewTarif(self):
        cursor = koneksiDB.db.cursor()
        sql = ("SELECT id_tarif, tarif from tarif")
        cursor.execute(sql)
        result = cursor.fetchall()
        self.gridTarif.setHorizontalHeaderLabels(['ID','Tarif'])
        self.gridTarif.setRowCount(0)

        for row_number, row_data in enumerate(result):
             print(row_number)
             self.gridTarif.insertRow(row_number)
             for column_number, data in enumerate(row_data):
                  #print(column_number)
                  self.gridTarif.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self):
        Idtarif = self.kodeTarif.text().strip()
        tarif = self.Tarif.text().strip()
        # Validasi input
        if not Idtarif or not tarif:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return
        
        cursor = koneksiDB.db.cursor()
        # Periksa apakah data sudah ada
        sql_check = "SELECT COUNT(*) FROM tarif WHERE id_tarif = %s"
        cursor.execute(sql_check, (Idtarif,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            self.messagebox("Peringatan", "Data dengan ID Tarif tersebut sudah ada, silakan input ID Tarif yang berbeda")
            return
        
        sql = "INSERT INTO tarif (id_tarif, tarif) VALUES (%s,%s)"
        cursor.execute(sql, (Idtarif,tarif))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES","Data Tarif Kendaraan Berhasil Di Tambahkan")
        else:
            self.messagebox("GAGAL","Data Tarif Kendaraan Gagal Di Tambahkan")

        print("{}data berhasil disimpan".format(cursor.rowcount))

        self.clearData()
        self.viewTarif() #reload data

    def searchData(self):
        Idtarif = self.kodeTarif.text()
        cursor = koneksiDB.db.cursor()
        sql = "SELECT * FROM tarif WHERE id_tarif=%s"
        cursor.execute(sql, (Idtarif,))
        result = cursor.fetchall()
        if result:
            for x in result:
                    self.idtarif= (x[0])
                    self.Tarif.setText(str(x[1]))

            if(cursor.rowcount>0):
                self.messagebox("SUKSES", "Data tarif Kendaraan Berhasil Di Temukan")
                self.btnSave.setEnabled(False)
        else:
            self.messagebox("GAGAL", "Data tarif Kendaraan Tidak Berhasil Di Temukan")
            self.clearData()
            self.btnSave.setEnabled(True)

    def updateData(self):
        Idtarif = self.kodeTarif.text().strip()
        tarif = self.Tarif.text().strip()

        # Validasi input
        if not Idtarif:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        if not tarif:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return

        cursor = koneksiDB.db.cursor()
        sql = "UPDATE tarif SET tarif=%s WHERE id_tarif=%s"
        cursor.execute(sql, (tarif, Idtarif))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data tarif Kendaraan Berhasil Di Perbarui")
        else:
            self.messagebox("GAGAL", "Data tarif Kendaraan Gagal Di Perbarui")

        print("{} data berhasil diupdate".format(cursor.rowcount))

        self.clearData() #clear entri data
        self.viewTarif() #reload data
    
    def deleteData(self):
        Idtarif = str(self.kodeTarif.text())
        cursor = koneksiDB.db.cursor()
        sql = "DELETE FROM tarif WHERE id_tarif=%s"
        cursor.execute(sql, (Idtarif, ))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data tarif Kendaraan Berhasil Di Hapus")
        else:
            self.messagebox("GAGAL", "Data tarif Kendaraan Gagal Di Hapus")

        print("{} data berhasil di hapus".format(cursor.rowcount))

        self.clearData() # Clear entry form
        self.viewTarif() #Reload
        self.btnSave.setEnabled(True) #mematikan aksi save
    
    def messagebox(self, title, message):
            mess = QMessageBox()
            mess.setWindowTitle(title)
            mess.setText(message)
            mess.setStandardButtons (QMessageBox.Ok)
            mess.exec_()
    

                     

        
    