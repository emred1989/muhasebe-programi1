import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QHBoxLayout, QSpinBox, QTextEdit, QFileDialog, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from untitled0 import CurrentAccountManager

# Giriş Diyaloğu
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        btn = QPushButton("Giriş")
        btn.clicked.connect(self.accept)
        form = QFormLayout()
        form.addRow("Kullanıcı:", self.username)
        form.addRow("Şifre:", self.password)
        form.addWidget(btn)
        self.setLayout(form)

    def get(self):
        return self.username.text(), self.password.text()

# Cari Hesaplar Sekmesi
class CariHesapTab(QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        self.init()
    def init(self):
        vb = QVBoxLayout()
        # Oluşturma
        row = QHBoxLayout()
        self.name = QLineEdit()
        self.type = QComboBox()
        self.type.addItems(["Customer","Supplier"])
        row.addWidget(QLabel("Ad:")); row.addWidget(self.name)
        row.addWidget(QLabel("Tip:")); row.addWidget(self.type)
        btn = QPushButton("Ekle")
        btn.clicked.connect(self.add)
        row.addWidget(btn)
        vb.addLayout(row)
        # Arama
        self.search = QLineEdit()
        self.search.setPlaceholderText("Ara...")
        self.search.textChanged.connect(self.load)
        vb.addWidget(self.search)
        # Tablo
        self.tbl = QTableWidget()
        vb.addWidget(self.tbl)
        vb.addWidget(QPushButton("Yenile", clicked=self.load))
        self.setLayout(vb)
        self.load()
    def add(self):
        n = self.name.text()
        t = self.type.currentText()
        if n:
            self.m.create_account(n,t)
            self.name.clear()
            self.load()
    def load(self):
        df = self.m.accounts.copy()
        term = self.search.text().lower()
        if term:
            df = df[df['account_name'].str.lower().str.contains(term)]
        self.tbl.setColumnCount(4)
        self.tbl.setRowCount(len(df))
        self.tbl.setHorizontalHeaderLabels(["ID","Ad","Tip","Bakiye"])
        for i,(_,r) in enumerate(df.iterrows()):
            self.tbl.setItem(i,0,QTableWidgetItem(str(r['account_id'])))
            self.tbl.setItem(i,1,QTableWidgetItem(r['account_name']))
            self.tbl.setItem(i,2,QTableWidgetItem(r['account_type']))
            self.tbl.setItem(i,3,QTableWidgetItem(f"{r['balance']:.2f}"))

# continue with other tabs...
