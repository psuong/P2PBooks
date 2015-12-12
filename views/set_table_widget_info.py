from PySide import QtGui
from views.img_widget_view import ImageWidget


def set_contents_to_table_widget(table_widget, book_list, main_window_inst):
    for row, book in enumerate(book_list):
        table_widget.insertRow(row)
        table_widget.setItem(row, 0, QtGui.QTableWidgetItem(book.title))
        table_widget.setItem(row, 1, QtGui.QTableWidgetItem(book.author))
        table_widget.setItem(row, 2, QtGui.QTableWidgetItem(book.isbn))
        table_widget.setItem(row, 3, QtGui.QTableWidgetItem(str(book.price)))
        table_widget.setItem(row, 4, QtGui.QTableWidgetItem(book.uploader.username))
        table_widget.setItem(row, 5, QtGui.QTableWidgetItem(str(book.rating)))
        table_widget.setCellWidget(row, 6, ImageWidget(book.cover_img, main_window_inst))
        table_widget.setRowHeight(row, 150)
        table_widget.setColumnWidth(row, 250)
