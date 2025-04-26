import sys
import tempfile

from Qt import QtCore, QtWidgets

from qtapp_example_item_delegate import window

app = QtWidgets.QApplication(sys.argv)

# Changed in ``qtapp_example_item_delegate``
#   * generating a temporary folder and saving it into the settings.
settings = QtCore.QSettings("QApp", "Example")
settings.setValue("image/location", tempfile.mkdtemp())

win = window.Window()
win.show()
sys.exit(app.exec_())
