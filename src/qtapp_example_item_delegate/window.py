from pathlib import Path

from Qt import QtCore, QtGui, QtWidgets

from qtapp_example_item_delegate import viewmodel
from qtapp_example_item_delegate.view import item as view_item


class Window(QtWidgets.QMainWindow):
    """Application main window."""
    def __init__(self) -> None:
        super().__init__()
        # Model
        self.model = QtCore.QSortFilterProxyModel(self)
        self.model.setSourceModel(viewmodel.ViewModel())

        # View
        self.view = QtWidgets.QTableView(self)
        self.view.setModel(self.model)
        delegate = view_item.ItemDelegate()
        self.view.setItemDelegate(delegate)

        # When the source model layout changes (when an item is added) resize the view.
        self.model.sourceModel().layoutChanged.connect(self.view.resizeColumnsToContents)
        self.model.sourceModel().layoutChanged.connect(self.view.resizeRowsToContents)

        # Window Setup
        self.setCentralWidget(self.view)


    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: ARG002
        """Overloaded method.

        Try to safely close any dependencies.

        Changed in ```qtapp_example_item_delegate```
          * Added removal of the cached images.
        """
        self.model.sourceModel().close()

        # Clean up the image cache
        settings = QtCore.QSettings("QApp", "Example")
        path = settings.value("image/location")
        for p in Path(path).iterdir():
            p.unlink()
