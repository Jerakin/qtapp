from Qt import QtCore
from Qt import QtWidgets


class View(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def resizeEvent(self, event: QtCore.QEvent) -> None:
        # layoutAboutToBeChanged is important. Without it a ProxyModel will crash when there is a selection.
        self.model().sourceModel().layoutAboutToBeChanged.emit()
        self.model().sourceModel().size = self.size()
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.model().sourceModel().layoutChanged.emit()

