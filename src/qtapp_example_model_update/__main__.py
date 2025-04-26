import sys

from Qt import QtWidgets

from qtapp_example_model_update import window

app = QtWidgets.QApplication(sys.argv)
win = window.Window()
win.show()
sys.exit(app.exec_())
