from Qt import QtCore, QtWidgets

from qtapp_example_dockable import viewmodel, model


class View(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def resizeEvent(self, event: QtCore.QEvent) -> None:
        self.model().sourceModel().layoutAboutToBeChanged.emit()
        self.model().sourceModel().size = self.size()
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.model().sourceModel().layoutChanged.emit()


class InfoWidget(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info = _InfoWidget()
        self.addWidget(_Empty())
        self.addWidget(self.info)

    def dataChanged(self, index: QtCore.QModelIndex):
        if index.isValid():
            data: model.ProductItem = index.model().data(index, viewmodel.DataRole)
            if data:
                self.info.dataChanged(index)
                self.setCurrentIndex(1)
                return
        self.setCurrentIndex(0)


class _Empty(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel("No selection"))


class _InfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.title = QtWidgets.QLabel(self)
        self.title.setWordWrap(True)
        self.price = QtWidgets.QLabel(self)
        self.description = QtWidgets.QLabel(self)
        self.description.setWordWrap(True)
        self.category = QtWidgets.QLabel(self)
        self.rating = QtWidgets.QLabel(self)

        self.layout().addWidget(self.title)
        self.layout().addWidget(self.price)
        self.layout().addWidget(self.description)
        self.layout().addWidget(self.category)
        self.layout().addWidget(self.rating)

    def dataChanged(self, index: QtCore.QModelIndex):
        data: model.ProductItem = index.model().data(index, viewmodel.DataRole)
        self.title.setText(data["title"])
        self.price.setText(f"${data['price']}")
        self.description.setText(data["description"])
        self.category.setText(data["category"])
        self.rating.setText(f"{data['rating']['rate']} / 5.0")