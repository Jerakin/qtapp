from typing import TypedDict

import requests
from Qt import QtCore, QtWidgets


class _Rating(TypedDict):
    rate: float
    count: int


class ProductItem(TypedDict):
    """Item within our Model."""
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: _Rating


class Model(QtCore.QAbstractItemModel):
    """Model for our app.

    It handles syncing our items.
    """
    initialized = QtCore.Signal()
    addItem = QtCore.Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget=None) -> None:
        super().__init__(parent)
        self._initialized = False
        self._thread: QtCore.QThread | None = None
        self.destroyed.connect(self.close)

    def _add_item(self, item: ProductItem) -> None:
        """Slot for adding item.

        We currently do not have a need to store an internal list
         of the items. This might be needed in any proper usage to
         compare the current items with any newly synced items. To
         remove any duplicates and update existing.
        """
        self.addItem.emit(item)

    def close(self) -> None:
        """Attempts to safely close the model."""
        self._thread.exiting = True
        self._thread.quit()
        self._thread.wait()

    def initialize(self) -> None:
        """Initialize the model.

        This is done outside the __init__ as to not stall the gui thread.
        """
        self._initialized = True
        self._thread = UpdateThread()
        self._thread.addItem.connect(self.addItem.emit)

        self.initialized.emit()

    def update(self) -> None:
        """Starts the thread to update the model.

        Call after the model has initialized.
        """
        if not self._initialized:
            return
        if self._thread.isRunning():
            return

        self._thread.start()


class UpdateThread(QtCore.QThread):
    """Thread that updates the model.

    It does some time-consuming task and yields items
     back by emitting the signal.
    """
    addItem = QtCore.Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.exiting = False

    def run(self) -> None:
        """Overloaded function.

        Does an HTTP request to get a list of products, which
        it then yields back.
        """
        r = requests.get("https://fakestoreapi.com/products", timeout=5)
        if r.status_code != requests.codes.ok:
            return

        data = r.json()
        for item in data:
            if self.exiting:
                return
            self.sleep(1)  # Synthetic delay
            self.addItem.emit(item)
