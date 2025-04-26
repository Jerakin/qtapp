import math

from Qt import QtCore

from qtapp_example_model_update import model


class ViewModel(QtCore.QAbstractTableModel):
    """ViewModel for our app.

    This displays our model.
    """
    def __init__(self, parent: QtCore.QObject = None) -> None:
        super().__init__(parent)
        self.model = model.Model()
        self.model.initialized.connect(self.model.update)
        self.model.addItem.connect(self.add_item)
        self.model.initialize()

        self.items: list[model.ProductItem] = []

    def close(self) -> None:
        """Attempts to safely close this object."""
        self.model.close()

    def add_item(self, item: model.ProductItem) -> None:
        """Slot for adding item from the model."""
        # layoutAboutToBeChanged is important. Without it a ProxyModel will crash.
        self.layoutAboutToBeChanged.emit()
        self.items.append(item)
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:  # noqa: ARG002
        """Overloaded method.

        Calculate the rowCount by dividing the current items with columns.
        """
        # math.ceil because we want to show a row even if there is only
        # one item in it.
        return math.ceil(len(self.items) / self.columnCount())

    def columnCount(self, parent: QtCore.QModelIndex = None) -> int:  # noqa: ARG002
        """Overloaded method.

        We arbitrarily decide we are going to use 3 columns.
        """
        return 3

    def data(self, index: QtCore.QModelIndex, role: int) -> None | str:
        """Overloaded method."""
        if not index.isValid():
            return None

        try:
            item = self.items[index.row() * self.columnCount() + index.column()]
        except IndexError:
            # If we have empty cells.
            return None

        if role == QtCore.Qt.DisplayRole:
            return item["title"]
        return None
