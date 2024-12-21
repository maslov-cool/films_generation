import io
import sys
import sqlite3

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>600</width>
    <height>600</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>600</width>
    <height>600</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>600</width>
    <height>600</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPlainTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>201</width>
      <height>91</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>50</y>
      <width>93</width>
      <height>28</height>
     </rect>
    </property>
    <property name="text">
     <string>Запуск</string>
    </property>
   </widget>
   <widget class="QPushButton" name="saveButton">
    <property name="geometry">
     <rect>
      <x>380</x>
      <y>50</y>
      <width>93</width>
      <height>28</height>
     </rect>
    </property>
    <property name="text">
     <string>Изменить</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>110</y>
      <width>601</width>
      <height>461</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.pushButton.clicked.connect(self.act1)
        self.saveButton.clicked.connect(self.act2)

    def act1(self):
        try:
            # Подключение к БД
            con = sqlite3.connect("films_db.sqlite")

            # Создание курсора
            cur = con.cursor()
            text = f'''SELECT * FROM Films WHERE {self.textEdit.toPlainText()}'''
            # Выполнение запроса
            res = cur.execute(text).fetchall()
            con.commit()
            con.close()
            self.tableWidget.setColumnCount(5)  # Установите количество столбцов
            self.tableWidget.setRowCount(1)
            # Заполняем таблицу элементами
            for i, row in enumerate(res):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.statusbar.showMessage('')
        except Exception:
            self.statusbar.showMessage('По этому запросу ничего не найдено')

    def act2(self):
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + self.textEdit.toPlainText().split()[-1],
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if valid == QMessageBox.StandardButton.Yes:
            # Подключение к БД
            con = sqlite3.connect("films_db.sqlite")

            cur = con.cursor()
            title = cur.execute("SELECT title FROM films WHERE id = ?",
                                (self.textEdit.toPlainText().split()[-1],)).fetchall()[0][0][::-1]
            con.commit()
            con.close()

            # Подключение к БД
            con = sqlite3.connect("films_db.sqlite")

            cur = con.cursor()
            cur.execute("UPDATE films SET title = ?, year = year + 1000, duration = duration * 2 "
                        "WHERE id = ?", (title, self.textEdit.toPlainText().split()[-1]))
            con.commit()
            con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
