from PySide6 import QtWidgets
from abc import ABC, abstractmethod

class WindowABC(ABC):
	@abstractmethod
	def do_something(self): ...


class MainWindow(QtWidgets.QApplication, WindowABC):
	def __init__(self):
		super().__init__()

	def do_something(self):
		return None


window = MainWindow()
print(window.__metaclass__)
