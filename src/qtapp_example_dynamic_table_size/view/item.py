from Qt import QtCore, QtGui, QtWidgets

from qtapp_example_item_delegate import model, viewmodel


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    """Item delegate for the main view of our app.

    It draws our cell items. A centered image with a title underneath it.
    """
    padding = 20
    text_height = 20
    item_size = QtCore.QSize(300, 200)

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionViewItem,
            index: QtCore.QModelIndex,
    ) -> None:
        """Overridden method."""
        data: model.ProductItem = index.model().data(index, viewmodel.DataRole)
        image: QtGui.QImage = index.model().data(index, viewmodel.ImageRole)

        if data is None:
            return

        width = option.rect.width() - self.padding * 2
        height = option.rect.height() - self.padding * 2

        # option.rect holds the area we are painting on the widget (our table cell)
        # scale our pixmap to fit
        scaled = image.scaled(
            width,
            height,
            aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        )
        # Position in the middle of the area.
        x = self.padding + (width - scaled.width()) / 2
        y = self.padding + (height - scaled.height() - self.text_height) / 2

        painter.drawImage(int(option.rect.x() + x), int(option.rect.y() + y), scaled)

        # Draw the title below the image, looking like a line edit
        txt_rect = QtCore.QRect(
            option.rect.x() + self.padding,
            option.rect.y() + self.padding + height,
            width,
            self.text_height,
        )
        painter.drawText(
            txt_rect,
            QtCore.Qt.AlignmentFlag.AlignLeft,
            data["title"],
        )

    def sizeHint(
            self,
            option: QtWidgets.QStyleOptionViewItem,  # noqa: ARG002
            index: QtCore.QModelIndex,  # noqa: ARG002
    ) -> QtCore.QSize:
        """Overridden method.

        All items are the same size.
        """
        return self.item_size
