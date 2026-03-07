from typing import override

from Qt import QtCore, QtGui, QtWidgets, QtSvg


class SvgIconEngine(QtGui.QIconEngine):
    """QIconEngine for SVG icon."""
    def __init__(self, svg_content: str) -> None:
        super().__init__()
        self.svg_content = svg_content
        self.svg_renderer = QtSvg.QSvgRenderer(svg_content)

    @override
    def pixmap(
            self,
            size: QtCore.QSize,
            mode: QtGui.QIcon.Mode,
            state: QtGui.QIcon.State,
    ) -> QtGui.QPixmap:
        px = QtGui.QPixmap(size)
        px.fill(QtCore.Qt.GlobalColor.transparent)
        self.paint(QtGui.QPainter(px), px.rect(), mode, state)
        return px

    @override
    def paint(
            self,
            painter: QtGui.QPainter,
            rect: QtCore.QRect,
            mode: QtGui.QIcon.Mode,
            state: QtGui.QIcon.State,
    ) -> None:
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pixmap = QtGui.QPixmap(rect.size())
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)

        svg_painter = QtGui.QPainter(pixmap)
        self.svg_renderer.render(svg_painter)

        # We need this hacky workaround to print in the correct color,
        # since Qt won't pass in an external color to the `currentColor`
        svg_painter.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_SourceIn,
        )
        svg_painter.fillRect(pixmap.rect(), self.color_for(mode))
        svg_painter.end()

        painter.drawPixmap(rect, pixmap)

    @override
    def clone(self) -> "SvgIconEngine":
        return SvgIconEngine(self.svg_content)

    @override
    def actualSize(
            self,
            size: QtCore.QSize,
            mode: QtGui.QIcon.Mode,
            state:QtGui.QIcon.State,
    ) -> QtCore.QSize:
        return self.svg_renderer.defaultSize()

    @staticmethod
    def color_for(mode: QtGui.QIcon.Mode) -> QtGui.QColor:
        """Pick color from the applications palette depending on icon mode."""
        if mode == QtGui.QIcon.Mode.Normal:
            return QtWidgets.QApplication.palette().color(
                QtGui.QPalette.ColorRole.WindowText,
            )
        if mode == QtGui.QIcon.Mode.Disabled:
            return QtWidgets.QApplication.palette().color(
                QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText,
            )
        if mode == QtGui.QIcon.Mode.Active:
            return QtWidgets.QApplication.palette().color(
                QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText,
            )
        if mode == QtGui.QIcon.Mode.Selected:
            return QtWidgets.QApplication.palette().color(
                QtGui.QPalette.ColorRole.HighlightedText,
            )

        return QtWidgets.QApplication.palette().color(
            QtGui.QPalette.ColorRole.WindowText,
        )
