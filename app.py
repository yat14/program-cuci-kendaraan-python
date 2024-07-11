import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QCheckBox, QRadioButton, QWidgetAction, QActionGroup, QDialog, QLabel
from Model.Pemilik import Pemilik
from Model.Transaksi import Transaksi
from Model.Merek import Merek
from Model.Tarif import Tarif
from Model.Petugas import Petugas
from Model.Kendaraan import Kendaraan


class Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        #Memanggil file UI
        super(Dashboard, self).__init__()
        uic.loadUi('UI/Dashboard.ui', self) #Di Sesuaikan dengan nama file UI nya
        self.show()

        #EvenKlik
        self.menuExit.setShortcut("Ctrl+Q")
        self.menuExit.triggered.connect(self.Exit)
        self.menuPemilik.triggered.connect(self.Menu_Pemilik)
        self.menuTransaksi.triggered.connect(self.Menu_Transaksi)
        self.menuMerek.triggered.connect(self.Menu_Merek)
        self.menuTarif.triggered.connect(self.Menu_Tarif)
        self.menuPetugas.triggered.connect(self.Menu_Petugas)
        self.menuKendaraan.triggered.connect(self.Menu_Kendaraan)

    #Sebagai Method Exit/Keluar dari Aplikasi
    def Exit(self):
        sys.exit()

    #Sebagai method untuk memanggil menu pemilik
    def Menu_Pemilik(self):
        winpemilik.setWindowModality(QtCore.Qt.ApplicationModal)
        winpemilik.show()

    #Sebagai method untuk memanggil menu transaksi
    def Menu_Transaksi(self):
        wintransaksi.setWindowModality(QtCore.Qt.ApplicationModal)
        wintransaksi.show()

    #Sebagai method untuk memanggil menu merek
    def Menu_Merek(self):
        winmerek.setWindowModality(QtCore.Qt.ApplicationModal)
        winmerek.show()

    #Sebagai method untuk memanggil menu tarif
    def Menu_Tarif(self):
        wintarif.setWindowModality(QtCore.Qt.ApplicationModal)
        wintarif.show()

    #Sebagai method untuk memanggil menu petugas
    def Menu_Petugas(self):
        winpetugas.setWindowModality(QtCore.Qt.ApplicationModal)
        winpetugas.show()
    
    #Sebagai method untuk memanggil menu kendaraan
    def Menu_Kendaraan(self):
        winkendaraan.setWindowModality(QtCore.Qt.ApplicationModal)
        winkendaraan.show()

#Untuk Memanggil Class Dashboard
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windashboard = Dashboard()
    winpemilik = Pemilik()
    winpemilik.viewPemilik()
    winmerek = Merek()
    winmerek.viewMerek()
    wintarif = Tarif()
    wintarif.viewTarif()
    wintransaksi = Transaksi()
    wintransaksi.viewTransaksi()
    winpetugas = Petugas()
    winpetugas.viewPetugas()
    winkendaraan = Kendaraan()
    winkendaraan.viewKendaraan()
    app.exec_()