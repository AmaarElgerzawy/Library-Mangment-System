from PyQt6.QtWidgets import QApplication
from Core import LibrarySyatem
import sys

app = QApplication([])
window = LibrarySyatem()
sys.exit(app.exec())
