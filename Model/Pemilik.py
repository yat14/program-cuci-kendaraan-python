from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QMessageBox, QTableWidgetItem, QDialog
from Database.koneksi import koneksiDB

class Pemilik(QDialog):
    def __init__(self):
        super(Pemilik, self).__init__()
        uic.loadUi('UI/Pemilik.ui', self)
    
        # Button Aksi
        self.btnSave.clicked.connect(self.insertData)  # aksi tombol save
        self.btnReset.clicked.connect(self.clearData)  # aksi tombol reset
        self.btnSearch.clicked.connect(self.searchData)  # aksi tombol search
        self.btnUpdate.clicked.connect(self.updateData)  # aksi tombol update
        self.btnDelete.clicked.connect(self.deleteData)  # aksi tombol delete
        self.edit_mode = ""

    def clearData(self):
        self.kodePemilik.clear()
        self.namaPemilik.clear()
        self.telpPemilik.clear()
        self.alamatPemilik.clear()
        self.btnSave.setEnabled(True)

    def viewPemilik(self):
        cursor = koneksiDB.db.cursor()
        sql = "SELECT id_pemilik, nama, no_telp, alamat FROM pemilik_kendaraan"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.gridPemilik.setHorizontalHeaderLabels(['ID', 'Nama', 'Nomor Telp', 'Alamat'])
        self.gridPemilik.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.gridPemilik.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.gridPemilik.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self):
        IDPem = self.kodePemilik.text().strip()
        NamaPem = self.namaPemilik.text().strip()
        TelpPem = self.telpPemilik.text().strip()
        AlamatPem = self.alamatPemilik.text().strip()

        # Validasi input
        if not IDPem or not NamaPem or not TelpPem or not AlamatPem:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return

        cursor = koneksiDB.db.cursor()
        # Periksa apakah data sudah ada
        sql_check = "SELECT COUNT(*) FROM pemilik_kendaraan WHERE id_pemilik = %s"
        cursor.execute(sql_check, (IDPem,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            self.messagebox("Peringatan", "Data dengan ID Pemilik tersebut sudah ada, silakan input ID Pemilik yang berbeda")
            return
        
        sql = "INSERT INTO pemilik_kendaraan (id_pemilik, nama, no_telp, alamat) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (IDPem, NamaPem, TelpPem, AlamatPem))
        koneksiDB.db.commit()

        if cursor.rowcount > 0:
            self.messagebox("SUKSES", "Data Pemilik Kendaraan Berhasil Ditambahkan")
        else:
            self.messagebox("GAGAL", "Data Pemilik Kendaraan Gagal Ditambahkan")

        self.clearData()
        self.viewPemilik()  # reload data

    def searchData(self):
        IDPem = self.kodePemilik.text().strip()
        cursor = koneksiDB.db.cursor()
        sql = "SELECT * FROM pemilik_kendaraan WHERE id_pemilik=%s"
        cursor.execute(sql, (IDPem,))
        result = cursor.fetchall()
        if result:
            for x in result:
                self.kodePemilik.setText(str(x[0]))
                self.namaPemilik.setText(str(x[1]))
                self.telpPemilik.setText(str(x[2]))
                self.alamatPemilik.setText(str(x[3]))

            if cursor.rowcount > 0:
                self.messagebox("SUKSES", "Data Pemilik Kendaraan Berhasil Ditemukan")
                self.btnSave.setEnabled(False)
        else:
            self.messagebox("GAGAL", "Data Pemilik Kendaraan Tidak Ditemukan")
            self.clearData()
            self.btnSave.setEnabled(True)

    def updateData(self):
        IDPem = self.kodePemilik.text().strip()
        NamaPem = self.namaPemilik.text().strip()
        TelpPem = self.telpPemilik.text().strip()
        AlamatPem = self.alamatPemilik.text().strip()

        # Validasi input
        if not IDPem:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        if not NamaPem or not TelpPem or not AlamatPem:
            self.messagebox("Peringatan", "Silakan input semua data terlebih dahulu")
            return

        cursor = koneksiDB.db.cursor()
        sql = "UPDATE pemilik_kendaraan SET nama=%s, no_telp=%s, alamat=%s WHERE id_pemilik=%s"
        cursor.execute(sql, (NamaPem, TelpPem, AlamatPem, IDPem))
        koneksiDB.db.commit()

        if cursor.rowcount > 0:
            self.messagebox("SUKSES", "Data Pemilik Kendaraan Berhasil Diperbarui")
        else:
            self.messagebox("GAGAL", "Data Pemilik Kendaraan Gagal Diperbarui")

        self.clearData()  # clear entri data
        self.viewPemilik()  # reload data

    def deleteData(self):
        IDPem = self.kodePemilik.text().strip()
        cursor = koneksiDB.db.cursor()
        sql = "DELETE FROM pemilik_kendaraan WHERE id_pemilik=%s"
        cursor.execute(sql, (IDPem,))
        koneksiDB.db.commit()


        if cursor.rowcount > 0:
            self.messagebox("SUKSES", "Data Pemilik Kendaraan Berhasil Dihapus")
        else:
            self.messagebox("GAGAL", "Data Pemilik Kendaraan Gagal Dihapus")

        self.clearData()  # Clear entry form
        self.viewPemilik()  # Reload
        self.btnSave.setEnabled(True)  # mematikan aksi save

    def messagebox(self, title, message):
        mess = QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QMessageBox.Ok)
        mess.exec_()
