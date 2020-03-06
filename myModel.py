from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import Qt


class MyModel(QSqlTableModel):
    def __init__(self, table):
        super(MyModel, self).__init__()
        self.setTable(table)

    def init(self, headList):
        # QSqlTableModel.OnRowChange: Changes to a row will be applied when the user selects a different row.
        self.setEditStrategy(QSqlTableModel.OnRowChange)
        for x in range(9):
            self.setHeaderData(x, Qt.Horizontal, headList[x])

    def add_row(self, row):
        index_end = self.rowCount()
        self.insertRow(self.rowCount())
        for i, val in enumerate(row):
            self.setData(self.index(index_end, i + 1), val)
        self.submit()

    def remove_row(self, index):
        self.removeRows(index.row(), 1)
        self.select()

    def filter_by_name(self, name):
        print(name)
        self.setFilter("name = '%s'" % (name))
        self.select()

    def filter_by_score(self, minlim=None, maxlim=None):
        if minlim and maxlim:
            self.setFilter("score > %d and score < %d" % (int(minlim), int(maxlim)))
        elif minlim: 
            self.setFilter("score > %d" % (int(minlim)))
        elif maxlim: 
            self.setFilter("score < %d" % (int(maxlim)))
        else:
            return
        self.select()

    def filter_by_grade(self, grade):
        self.setFilter("grade = %d" % (int(grade)))
        self.select()

    def filter_by_class(self, grade, class_):
        self.setFilter("grade = %d and class = %d" % (int(grade), int(class_)))
        self.select()
    