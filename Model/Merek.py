from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QMessageBox, QTableWidgetItem, QDialog
from Database.koneksi import koneksiDB
class Merek(QDialog):
    def __init__(self):
        super(Merek, self).__init__()
        uic.loadUi('UI/Merek.ui', self)
    
        #Button Aksi
        self.btnSave.clicked.connect(self.insertData) #aksi tombol save
        self.btnReset.clicked.connect(self.clearData) #aksi tombol reset
        self.btnSearch.clicked.connect(self.searchData) #aksi tombol search
        self.btnUpdate.clicked.connect(self.updateData) #aksi tombol update
        self.btnDelete.clicked.connect(self.deleteData) #aksi tombol delete
        self.edit_mode=""

    def clearData(self):
        self.kodeMerek.clear()
        self.namaMerek.clear()
        self.btnSave.setEnabled(True)

    def viewMerek(self):
        cursor = koneksiDB.db.cursor()
        sql = ("SELECT id_merek, merek FROM merek")
        cursor.execute(sql)
        result = cursor.fetchall()
        self.gridMerek.setHorizontalHeaderLabels(['ID','merek'])
        self.gridMerek.setRowCount(0)

        for row_number, row_data in enumerate(result):
             print(row_number)
             self.gridMerek.insertRow(row_number)
             for column_number, data in enumerate(row_data):
                  #print(column_number)
                  self.gridMerek.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self):
        IDMer = str(self.kodeMerek.text())
        NamaMer = str(self.namaMerek.text())

        # Validasi input
        if not IDMer or not NamaMer:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return
        
        cursor = koneksiDB.db.cursor()
        # Periksa apakah data sudah ada
        sql_check = "SELECT COUNT(*) FROM merek WHERE id_merek = %s"
        cursor.execute(sql_check, (IDMer,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            self.messagebox("Peringatan", "Data dengan ID Merek tersebut sudah ada, silakan input ID Merek yang berbeda")
            return
        
        sql = "INSERT INTO merek (id_merek, merek) VALUES (%s,%s)"
        cursor.execute(sql, (IDMer, NamaMer))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES","Data Merek Kendaraan Berhasil Di Tambahkan")
        else:
            self.messagebox("GAGAL","Data Merek Kendaraan Gagal Di Tambahkan")

        print("{}data berhasil disimpan".format(cursor.rowcount))

        self.clearData()
        self.viewMerek() #reload data
    
    def searchData(self):
        IDMer = self.kodeMerek.text()
        cursor = koneksiDB.db.cursor()
        sql = "SELECT * FROM merek WHERE id_merek=%s"
        cursor.execute(sql, (IDMer,))
        result = cursor.fetchall()
        if result:
            for x in result:
                    self.idMerek= (x[0])
                    self.namaMerek.setText(str(x[1]))

            if(cursor.rowcount>0):
                self.messagebox("SUKSES", "Data Merek Kendaraan Berhasil Di Temukan")
                self.btnSave.setEnabled(False)
        else:
            self.messagebox("GAGAL", "Data Merek Kendaraan Tidak Berhasil Di Temukan")
            self.clearData()
            self.btnSave.setEnabled(True)

    def updateData(self):
        IDMer = str(self.kodeMerek.text())
        NamaMer = str(self.namaMerek.text())

        # Validasi jika data belum dicari
        if not IDMer:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        if not NamaMer:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return

        cursor = koneksiDB.db.cursor()
        sql = "UPDATE merek SET merek=%s WHERE id_merek=%s"
        cursor.execute(sql, (NamaMer, IDMer))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data Merek Kendaraan Berhasil Di Perbarui")
        else:
            self.messagebox("GAGAL", "Data Merek Kendaraan Gagal Di Perbarui")

        print("{} data berhasil diupdate".format(cursor.rowcount))

        self.clearData() #clear entri data
        self.viewMerek() #reload data
    
    def deleteData(self):
        IDMer = str(self.kodeMerek.text())
        cursor = koneksiDB.db.cursor()
        sql = "DELETE FROM merek WHERE id_merek=%s"
        cursor.execute(sql, (IDMer, ))
        koneksiDB.db.commit()

        if(cursor.rowcount>0):
            self.messagebox("SUKSES", "Data Merek Kendaraan Berhasil Di Hapus")
        else:
            self.messagebox("GAGAL", "Data Merek Kendaraan Gagal Di Hapus")

        print("{} data berhasil di hapus".format(cursor.rowcount))

        self.clearData() # Clear entry form
        self.viewMerek() #Reload
        self.btnSave.setEnabled(True) #mematikan aksi save
    
    def messagebox(self, title, message):
            mess = QMessageBox()
            mess.setWindowTitle(title)
            mess.setText(message)
            mess.setStandardButtons (QMessageBox.Ok)
            mess.exec_()