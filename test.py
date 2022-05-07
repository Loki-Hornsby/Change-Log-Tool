from PyQt5 import QtWidgets, QtCore

class ReorderTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None, *args):
        super().__init__(parent, *args)
        self._data = data

    def columnCount(self, parent=None) -> int:
        return 2

    def rowCount(self, parent=None) -> int:
        return len(self._data) + 1

    def headerData(self, column: int, orientation, role: QtCore.Qt.ItemDataRole):
        return (('Regex', 'Category')[column]
                if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal
                else None)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt.ItemDataRole):
        if not index.isValid() or role not in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:
            return None
        return (self._data[index.row()][index.column()] if index.row() < len(self._data) else
                "edit me" if role == QtCore.Qt.DisplayRole else "")

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        # https://doc.qt.io/qt-5/qt.html#ItemFlag-enum
        if not index.isValid():
            return QtCore.Qt.ItemIsDropEnabled
        if index.row() < len(self._data):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    def supportedDropActions(self) -> bool:
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction

    def relocateRow(self, row_source, row_target) -> None:
        row_a, row_b = max(row_source, row_target), min(row_source, row_target)
        self.beginMoveRows(QtCore.QModelIndex(), row_a, row_a, QtCore.QModelIndex(), row_b)
        self._data.insert(row_target, self._data.pop(row_source))
        self.endMoveRows()


class ReorderTableView(QtWidgets.QTableView):
    """QTableView with the ability to make the model move a row with drag & drop"""

    class DropmarkerStyle(QtWidgets.QProxyStyle):
        def drawPrimitive(self, element, option, painter, widget=None):
            """Draw a line across the entire row rather than just the column we're hovering over.
            This may not always work depending on global style - for instance I think it won't
            work on OSX."""
            if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
                option_new = QtWidgets.QStyleOption(option)
                option_new.rect.setLeft(0)
                if widget:
                    option_new.rect.setRight(widget.width())
                option = option_new
            super().drawPrimitive(element, option, painter, widget)

    def __init__(self, parent):
        super().__init__(parent)
        self.verticalHeader().hide()
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setStyle(self.DropmarkerStyle())

    def dropEvent(self, event):
        if (event.source() is not self or
            (event.dropAction() != QtCore.Qt.MoveAction and
             self.dragDropMode() != QtWidgets.QAbstractItemView.InternalMove)):
            super().dropEvent(event)

        selection = self.selectedIndexes()
        from_index = selection[0].row() if selection else -1
        to_index = self.indexAt(event.pos()).row()
        if (0 <= from_index < self.model().rowCount() and
            0 <= to_index < self.model().rowCount() and
            from_index != to_index):
            self.model().relocateRow(from_index, to_index)
            event.accept()
        super().dropEvent(event)


class Testing(QtWidgets.QMainWindow):
    """Demonstrate ReorderTableView"""
    def __init__(self):
        super().__init__()
        view = ReorderTableView(self)
        view.setModel(ReorderTableModel([
            ("a", 1),
            ("b", 2),
            ("c", 3),
            ("d", 4),
        ]))
        self.setCentralWidget(view)

        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    test = Testing()
    raise SystemExit(app.exec_())