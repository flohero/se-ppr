import pathlib
import sys
import tempfile

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem

import utils
from converter import file_allowed, parse_file, ParsedFile
from yac import Ui_MainWindow


class YetAnotherConverterWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self._generated_path = tempfile.mkdtemp()

    @staticmethod
    def _display_error(error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.exec_()

    def setupUi(self, main_window):
        super().setupUi(main_window)
        self.action_add_file.triggered.connect(self._on_add_file)
        self.delete_button.clicked.connect(self._on_delete_entry)
        self._update_file_list()
        self.file_list.itemClicked.connect(self._select_dataset)
        self.remove_row_button.clicked.connect(self._remove_row)
        self.remove_column_button.clicked.connect(self._remove_col)
        self.export_combo_box.addItems([".csv", ".sqlite", ".json"])
        self.export_button.clicked.connect(self._export_file)
        self.export_button.setDisabled(True)

    # Event Handlers
    def _on_add_file(self):
        print("Added")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            caption="Add a new Dataset",
            filter="csv file (*.csv);;txt file (*.txt);;json file (*.json);;sqlite file (*.sqlite);;db file (*.db)",
        )
        if not file_name or file_name == "":
            # User canceled dialog
            return

        if not file_allowed(file_name):
            self._display_error("File is not allowed")
            return

        if pathlib.Path(file_name).name in utils.get_all_uploaded_files():
            self._display_error("File already exists")
            return

        utils.add_file(file_name)
        self._update_file_list()

    def _on_delete_entry(self):
        current = self.file_list.currentRow()
        if current >= 0:
            utils.remove_file(utils.get_all_uploaded_files()[current])
            self._update_file_list()
            self.dataset_table.setColumnCount(0)
            self.dataset_table.setRowCount(0)
            self.dataset_table.clear()
            self.export_button.setDisabled(True)

    def _update_file_list(self):
        files = utils.get_all_uploaded_files()
        self.file_list.clear()
        for file in files:
            self.file_list.addItem(file)

    def _select_dataset(self, file_name):
        self.export_button.setDisabled(False)
        try:
            self.dataset_table.itemChanged.disconnect()
        except:
            pass
        f = pathlib.Path(utils.path_of_uploaded_file(file_name.text()))
        pf = parse_file(f)
        headers = []
        rows, cols = pf.df.shape
        self.dataset_table.setColumnCount(cols)
        self.dataset_table.setRowCount(rows)
        for n, col in enumerate(pf.df.head()):
            headers.append(col)
            for m, item in enumerate(pf.df[col]):
                new_item = QTableWidgetItem(str(item))
                self.dataset_table.setItem(m, n, new_item)
        self.dataset_table.setHorizontalHeaderLabels(headers)
        self.dataset_table.resizeColumnsToContents()
        self.dataset_table.resizeRowsToContents()
        self.dataset_table.itemChanged.connect(self._on_table_change)

    def _on_table_change(self, item):
        current = self.file_list.currentRow()
        f = pathlib.Path(
            utils.path_of_uploaded_file(utils.get_all_uploaded_files()[current])
        )
        pf = parse_file(f)
        pf.df.iloc[item.row(), item.column()] = item.text()
        pf.out_path = utils.upload_dir
        pf.convert_file(pf.file.suffix)

    def _remove_row(self):
        row = self.dataset_table.currentRow()
        if row < 0:
            self._display_error("No row selected")
            return
        f = self._get_current_file()
        self._drop_row_or_column(f, row, True)

    def _remove_col(self):
        col = self.dataset_table.currentColumn()
        if col < 0:
            self._display_error("No column selected")
            return
        f = self._get_current_file()
        self._drop_row_or_column(f, col, False)

    def _export_file(self):
        if self.file_list.currentRow() < 0:
            self._display_error("No File to be exported")
            return
        out = QtWidgets.QFileDialog.getExistingDirectory(caption="Export To...")
        if out == "":
            # User cancelled dialog
            return
        pf = parse_file(pathlib.Path(self._get_current_file()))
        filetype = str(self.export_combo_box.currentText())
        pf.out_path = out
        pf.convert_file(filetype)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setWindowTitle("Successfully Exported Dataset")
        msg.exec_()

    # Helper functions

    def _get_current_file(self) -> str:
        current = self.file_list.currentRow()
        return utils.path_of_uploaded_file(utils.get_all_uploaded_files()[current])

    def _drop_row_or_column(self, target: str, idx, is_row: bool = True):
        pf = parse_file(pathlib.Path(target))
        if is_row:
            pf.df.drop([idx], inplace=True)
            self.dataset_table.removeRow(idx)
        else:
            label = self.dataset_table.horizontalHeaderItem(idx).text()
            pf.df = pf.df.drop(columns=[label])
            self.dataset_table.removeColumn(idx)
        pf.out_path = utils.upload_dir
        pf.convert_file(pf.file.suffix)


if __name__ == "__main__":
    pathlib.Path(utils.upload_dir).mkdir(exist_ok=True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = YetAnotherConverterWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
