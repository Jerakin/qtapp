from pathlib import Path

from Qt import QtCore, QtGui, QtWidgets

from qtapp_example_themes_and_icons import view, viewmodel
from qtapp_example_themes_and_icons.view import item as view_item

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files


class Window(QtWidgets.QMainWindow):
    """Application main window."""
    def __init__(self) -> None:
        super().__init__()
        # Style
        company_qss = files("qtapp_example_themes_and_icons").joinpath(
            "assets", "company_theme", "company.qss",
        ).read_text()
        app_qss = files("qtapp_example_themes_and_icons").joinpath(
            "assets", "app.qss",
        ).read_text()
        self.setStyleSheet(f"{company_qss}\n{app_qss}")

        # Model
        self.model = QtCore.QSortFilterProxyModel(self)
        self.model.setSourceModel(viewmodel.ViewModel())

        # View
        self.view = view.View(self)
        self.view.setModel(self.model)

        self.view.selectionModel().selectionChanged.connect(self._selection_changed)

        delegate = view_item.ItemDelegate()
        self.view.setItemDelegate(delegate)

        # Dockable
        self.right_dock = QtWidgets.QDockWidget()
        self.right_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.right_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable |
            QtWidgets.QDockWidget.DockWidgetClosable
        )
        self.info_widget = view.InfoWidget(self)
        self.right_dock.setWidget(self.info_widget)
        self.right_dock.hide()
        self.right_dock.visibilityChanged.connect(self.update_action_state)

        # Toolbar for the dockable
        self.right_toolbar = QtWidgets.QToolBar()
        self.right_toolbar.setAllowedAreas(QtCore.Qt.RightToolBarArea)
        # Change in ``qtapp_example_themes_and_icon``
        #    * Added an icon to the action
        self.info_action = QtWidgets.QAction(
            QtGui.QIcon("icons:info-circle.svg"),
            "info",
        )

        self.right_toolbar.addAction(self.info_action)
        self.info_action.setCheckable(True)
        self.info_action.triggered.connect(self.info_toggle)

        # When the source model layout changes (when an item is added) resize the view.
        self.model.sourceModel().layoutChanged.connect(self.view.resizeColumnsToContents)
        self.model.sourceModel().layoutChanged.connect(self.view.resizeRowsToContents)

        # Window Setup
        QtGui.QIcon.setThemeName("light")
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock, QtCore.Qt.Orientations.Horizontal)
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.right_toolbar)
        self.setCentralWidget(self.view)

    def update_action_state(self):
        if not self.right_dock.isVisible():
            self.info_action.setChecked(False)

    def info_toggle(self):
        self.info_action.setChecked(False)
        if not self.right_dock.isVisible():
            if self.right_dock.widget() != self.info_widget:
                self.right_dock.setWidget(self.info_widget)
            self.info_action.setChecked(True)
        self.right_dock.setVisible(not self.right_dock.isVisible())

    def _selection_changed(self, new_selection: QtCore.QItemSelection, old_selection: QtCore.QItemSelection):
        selection = new_selection.indexes()
        if selection:
            self.info_widget.dataChanged(selection[0])
        else:
            self.info_widget.dataChanged(QtCore.QModelIndex())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.model.sourceModel().close()

        # Clean up the image cache
        settings = QtCore.QSettings("QApp", "Example")
        path = settings.value("image/location")
        for p in Path(path).iterdir():
            p.unlink()

    def eventFilter(self, watched, event):
        if event == QtCore.QEvent.ThemeChange:
            print("Theme changed")