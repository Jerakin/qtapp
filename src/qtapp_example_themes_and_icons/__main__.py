import sys
import tempfile

from Qt import QtCore, QtGui, QtWidgets

from qtapp_example_themes_and_icons import window

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

app = QtWidgets.QApplication(sys.argv)

# Changed in ``qtapp_example_item_delegate``
#   * generating a temporary folder and saving it into the settings.
settings = QtCore.QSettings("QApp", "Example")
settings.setValue("image/location", tempfile.mkdtemp())

# Changed in ``qtapp_example_themes_and_icons``
#   * Adding icon directory to our search path.
QtCore.QDir.addSearchPath(
    "icons",
    str(files("qtapp_example_themes_and_icons").joinpath("assets", "icons")),
)
QtCore.QDir.addSearchPath(
    "images",
    str(files("qtapp_example_themes_and_icons").joinpath(
        "assets", "company_theme", "images",
    )),
)

win = window.Window()
win.show()
sys.exit(app.exec_())
