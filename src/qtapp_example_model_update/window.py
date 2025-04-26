from Qt import QtCore, QtGui, QtWidgets

from qtapp_example_model_update import viewmodel


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

        # Window Setup
        self.setCentralWidget(self.view)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: ARG002
        """Overloaded method.

        Try to safely close any dependencies.
        """
        self.model.sourceModel().close()
