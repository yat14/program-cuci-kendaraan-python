from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QMessageBox, QTableWidgetItem, QDialog
from Database.koneksi import koneksiDB
from PyQt5.QtCore import QDate

class Transaksi(QDialog):
    def __init__(self):
        super(Transaksi, self).__init__()
        uic.loadUi('UI/Transaksi.ui', self)

        # Initialize ComboBox
        self.comboKendaraan()
        self.comboMerek()
        self.comboTarif()
        self.comboPemilik()
        self.comboPetugas()

        self.btnSave.clicked.connect(self.insertData) #aksi tombol save
        self.btnReset.clicked.connect(self.clearData) #aksi tombol reset
        self.btnSearch.clicked.connect(self.searchData) #aksi tombol search
        self.btnUpdate.clicked.connect(self.updateData) #aksi tombol update
        self.btnDelete.clicked.connect(self.deleteData) #aksi tombol delete
        self.edit_mode=""

        # View data in the table when the form loads
        self.viewTransaksi()

    def comboPemilik(self):
        cursor = koneksiDB.db.cursor()
        sql = "SELECT nama FROM pemilik_kendaraan"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # Clear existing items in ComboBox
        #self.comIdTarif.clear()
        
        for row in result:
            self.comIdPemilik.addItem(str(row[0]))

    def comboKendaraan(self):
        cursor = koneksiDB.db.cursor()
        sql = "SELECT jenis_kendaraan FROM kendaraan"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # Clear existing items in ComboBox
        #self.comIdKendaraan.clear()
        
        for row in result:
            self.comIdKendaraan.addItem(str(row[0]))

    def comboMerek(self):
        cursor = koneksiDB.db.cursor()
        sql = "SELECT merek FROM merek"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # Clear existing items in ComboBox
        #self.comIdMerek.clear()
        
        for row in result:
            self.comIdMerek.addItem(str(row[0]))

    def comboTarif(self):
        cursor = koneksiDB.db.cursor()
        sql = "SELECT tarif FROM tarif"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # Clear existing items in ComboBox
        #self.comIdTarif.clear()
        
        for row in result:
            self.comIdTarif.addItem(str(row[0]))


    def comboPetugas(self):
        cursor = koneksiDB.db.cursor()
        sql = "SELECT nama_petugas FROM petugas"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # Clear existing items in ComboBox
        #self.comIdPetugas.clear()
        
        for row in result:
            self.comIdPetugas.addItem(str(row[0]))

    def clearData(self):
        self.idTransaksi.clear()
        self.comIdPemilik.setCurrentIndex(-1)
        self.comIdKendaraan.setCurrentIndex(-1)
        self.comIdMerek.setCurrentIndex(-1)
        self.comIdTarif.setCurrentIndex(-1)
        self.comIdPetugas.setCurrentIndex(-1)
        self.tanggalTransaksi.clear()
        self.btnSave.setEnabled(True)

    def insertData(self):
        idTransaksi     = self.idTransaksi.text().strip()
        Pemilik         = self.comIdPemilik.currentText().strip()
        Kendaraan       = self.comIdKendaraan.currentText().strip()
        Merek           = self.comIdMerek.currentText().strip()
        Tarif           = self.comIdTarif.currentText().strip()
        Petugas         = self.comIdPetugas.currentText().strip()
        tanggal         = self.tanggalTransaksi.date().toString("yyyy-MM-dd")

         # Validasi input
        if not idTransaksi:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        if not Pemilik or not Kendaraan  or not Merek or not Tarif or not Petugas or not tanggal:
            self.messagebox("Peringatan", "Silakan pilih data terlebih dahulu")
            return

        cursor = koneksiDB.db.cursor()
        # Periksa apakah data sudah ada
        sql_check = "SELECT COUNT(*) FROM transaksi WHERE id_transaksi = %s"
        cursor.execute(sql_check, (idTransaksi,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            self.messagebox("Peringatan", "Data dengan ID Transaksi tersebut sudah ada, silakan input ID Transaksi yang berbeda")
            return
        
        sql = "SELECT id_pemilik FROM pemilik_kendaraan WHERE nama = %s"
        cursor.execute(sql, (Pemilik,))
        idPemilik = cursor.fetchone()[0]

        cursor = koneksiDB.db.cursor()
        sql = "SELECT id_kendaraan FROM kendaraan WHERE jenis_kendaraan = %s"
        cursor.execute(sql, (Kendaraan,))
        idKendaraan = cursor.fetchone()[0]

        cursor = koneksiDB.db.cursor()
        sql = "SELECT id_merek FROM merek WHERE merek = %s"
        cursor.execute(sql, (Merek,))
        idMerek = cursor.fetchone()[0]

        cursor = koneksiDB.db.cursor()
        sql = "SELECT id_tarif FROM tarif WHERE tarif = %s"
        cursor.execute(sql, (Tarif,))
        idTarif = cursor.fetchone()[0]

        cursor = koneksiDB.db.cursor()
        sql = "SELECT id_petugas FROM petugas WHERE nama_petugas = %s"
        cursor.execute(sql, (Petugas,))
        idPetugas = cursor.fetchone()[0]

        sql = "INSERT INTO transaksi (id_transaksi, id_pemilik, id_kendaraan, id_merek, id_tarif, id_petugas, tanggal) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (idTransaksi, idPemilik, idKendaraan, idMerek, idTarif, idPetugas, tanggal))
        koneksiDB.db.commit()

        if cursor.rowcount > 0:
            self.messagebox("SUKSES", "Data Transaksi Berhasil Ditambahkan")
        else:
            self.messagebox("GAGAL", "Data Transaksi Gagal Ditambahkan")

        print("{} data berhasil disimpan".format(cursor.rowcount))

        #self.clearData()
        self.viewTransaksi()

    
    def viewTransaksi(self):
           cursor = koneksiDB.db.cursor()
           sql = (
                   "SELECT transaksi.id_transaksi, pemilik_kendaraan.nama, kendaraan.jenis_kendaraan, merek.merek, tarif.tarif, petugas.nama_petugas, transaksi.tanggal "
                   "FROM transaksi "
                   "JOIN kendaraan ON transaksi.id_kendaraan = kendaraan.id_kendaraan "
                   "JOIN pemilik_kendaraan ON transaksi.id_pemilik = pemilik_kendaraan.id_pemilik "
                   "JOIN merek ON transaksi.id_merek = merek.id_merek "
                   "JOIN tarif ON transaksi.id_tarif = tarif.id_tarif "
                   "JOIN petugas ON transaksi.id_petugas = petugas.id_petugas"
                 )
           
           cursor.execute(sql)
           result = cursor.fetchall()
           self.gridTransaksi.setRowCount(0)
           self.gridTransaksi.setHorizontalHeaderLabels(['ID Transaksi', 'Pemilik', 'Jenis Kendaraan', 'Merek', 'Tarif', 'Petugas', 'Tanggal'])

           for row_number, row_data in enumerate(result):
               self.gridTransaksi.insertRow(row_number)
               for column_number, data in enumerate(row_data):
                   self.gridTransaksi.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def searchData(self):
        Transaksi = self.idTransaksi.text()
        cursor = koneksiDB.db.cursor()
        sql = (
            "SELECT transaksi.id_transaksi, pemilik_kendaraan.nama, kendaraan.jenis_kendaraan, merek.merek, tarif.tarif, petugas.nama_petugas, transaksi.tanggal "
            "FROM transaksi "
            "JOIN kendaraan ON transaksi.id_kendaraan = kendaraan.id_kendaraan " 
            "JOIN pemilik_kendaraan ON transaksi.id_pemilik = pemilik_kendaraan.id_pemilik " 
            "JOIN merek ON transaksi.id_merek = merek.id_merek " 
            "JOIN tarif ON transaksi.id_tarif = tarif.id_tarif " 
            "JOIN petugas ON transaksi.id_petugas = petugas.id_petugas "
            "WHERE transaksi.id_transaksi = %s"
          )
        cursor.execute(sql, (Transaksi,))
        hasil = cursor.fetchall()
        if hasil:
            for x in hasil:
                self.Transaksi = x[0]
                self.comIdPemilik.setCurrentText(str(x[1]))
                self.comIdKendaraan.setCurrentText(str(x[2]))
                self.comIdMerek.setCurrentText(str(x[3]))
                self.comIdTarif.setCurrentText(str(x[4]))
                self.comIdPetugas.setCurrentText(str(x[5]))
                tanggal_transaksi = QDate(x[6].year, x[6].month, x[6].day)
                self.tanggalTransaksi.setDate(tanggal_transaksi)

            self.messagebox("SUKSES", "Data Transaksi Berhasil Ditemukan")
            self.btnSave.setEnabled(False)
        else:
            self.messagebox("GAGAL", "Data Transaksi Tidak Ditemukan")
            self.clearData()
            self.btnSave.setEnabled(True)
    
    def updateData(self):
        ComPem = self.comIdPemilik.currentText().strip()
        ComKend = self.comIdKendaraan.currentText().strip()
        ComMer = self.comIdMerek.currentText().strip()
        ComTar = self.comIdTarif.currentText().strip()
        ComPet = self.comIdPetugas.currentText().strip()
        DateTran = self.tanggalTransaksi.date().toString("yyyy-MM-dd")
        idTransaksi = self.idTransaksi.text().strip()

         # Validasi input
        if not idTransaksi:
            self.messagebox("Peringatan", "Silakan cari data terlebih dahulu sebelum memperbarui")
            return
        if not ComPem or not ComKend or not ComMer or not ComTar or not ComPet:
            self.messagebox("Peringatan", "Silakan pilih data terlebih dahulu")
            return

        cursor = koneksiDB.db.cursor()
        sql = "SELECT id_pemilik FROM pemilik_kendaraan WHERE nama = %s"
        cursor.execute(sql, (ComPem,))
        idPemilik = cursor.fetchone()[0]

        sql = "SELECT id_kendaraan FROM kendaraan WHERE jenis_kendaraan = %s"
        cursor.execute(sql, (ComKend,))
        idKendaraan = cursor.fetchone()[0]

        sql = "SELECT id_merek FROM merek WHERE merek = %s"
        cursor.execute(sql, (ComMer,))
        idMerek = cursor.fetchone()[0]

        sql = "SELECT id_tarif FROM tarif WHERE tarif = %s"
        cursor.execute(sql, (ComTar,))
        idTarif = cursor.fetchone()[0]

        sql = "SELECT id_petugas FROM petugas WHERE nama_petugas = %s"
        cursor.execute(sql, (ComPet,))
        idPetugas = cursor.fetchone()[0]

        sql = ("UPDATE transaksi SET id_pemilik = %s, id_kendaraan = %s, id_merek = %s, id_tarif = %s, id_petugas = %s, tanggal = %s "
            "WHERE id_transaksi = %s")
        cursor.execute(sql, (idPemilik, idKendaraan, idMerek, idTarif, idPetugas, DateTran, idTransaksi))
        koneksiDB.db.commit()

        if cursor.rowcount > 0:
            self.messagebox("SUKSES", "Data Transaksi Berhasil Diperbarui")
        else:
            self.messagebox("GAGAL", "Data Transaksi Gagal Diperbarui")

        print("{} data berhasil diupdate".format(cursor.rowcount))

        self.clearData()
        self.viewTransaksi()

    def deleteData(self):
        idTran = self.idTransaksi.text()
        cursor = koneksiDB.db.cursor()
        sql = "DELETE FROM transaksi WHERE id_transaksi = %s"
        cursor.execute(sql, (idTran,))
        koneksiDB.db.commit()

        if cursor.rowcount > 0:
            self.messagebox("SUKSES", "Data Transaksi Berhasil Dihapus")
        else:
            self.messagebox("GAGAL", "Data Transaksi Gagal Dihapus")

        print("{} data berhasil dihapus".format(cursor.rowcount))

        self.clearData()
        self.viewTransaksi()
        self.btnSave.setEnabled(True)
    
    
    def messagebox(self, title, message):
            mess = QMessageBox()
            mess.setWindowTitle(title)
            mess.setText(message)
            mess.setStandardButtons (QMessageBox.Ok)
            mess.exec_()
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Transaksi()
    window.show()
    sys.exit(app.exec_())


