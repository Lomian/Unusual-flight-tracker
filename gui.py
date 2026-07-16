import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QTableWidgetItem, QTableWidget, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import polars as pl

class HelloApp(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget()
        self.setWindowTitle("SurvFlight")
        self.setGeometry(1000, 100, 900, 600)
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(2000)

        self.load_data()


        layout = QVBoxLayout()
        label = QLabel("Flight track epic track")

        layout.addWidget(label)

        layout.addSpacing(300)

        layout.addWidget(self.table)

        self.setLayout(layout)



        self.setLayout(layout)

    def load_data(self):
        try:
            df = pl.read_json("aircraft_data.json") #reads the json file here
        except Exception:
            return
        self.table.setRowCount(df.height)
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for row_i, row in enumerate(df.iter_rows()):
            for col_i, value in enumerate(row):
                self.table.setItem(row_i, col_i, QTableWidgetItem(str(value)))


app = QApplication(sys.argv)
window = HelloApp()
window.show()
sys.exit(app.exec())