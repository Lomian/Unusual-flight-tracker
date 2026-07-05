import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class HelloApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SurvFlight")
        self.setGeometry(1200, 100, 900, 600)

        layout = QVBoxLayout()

        table = QTableView()

        model = QStandardItemModel(100, 15)
        model.setHorizontalHeaderLabels([
            "Hex", "Flight", "Squawk", "Registry", "Type", "desc","alt_baro","gs","mach","track","track_rate","baro_rate","latitude","longitude","seen_pos","seen"





        ])

        data = [
            "a01c57",
            "N106PV",
            "SSTL",
            "JUST JA30 SuperSTOL",
            "70.1"
        ]

        for column, value in enumerate(data):
            model.setItem(0, column, QStandardItem(value))

        table.setModel(model)

        layout.addSpacing(300)
        layout.addWidget(table)

        self.setLayout(layout)


app = QApplication(sys.argv)
window = HelloApp()
window.show()
sys.exit(app.exec())