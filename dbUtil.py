from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from faker import Faker
import xlwings as xw
import os


class Dbhandler(object):
    def __init__(self):
        super(Dbhandler, self).__init__()
        self.db = None
        self.db_connect()

    def __del__(self):
        print("__del__")
        if not self.db.open():
            print("==== not open")
        self.db.close()

    def db_connect(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not os.path.isfile("mydb.db"):
            self.db.setDatabaseName('mydb.db')
            if not self.db.open():
                # QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())
                print("==== not open")

            print("create...")
            query = QSqlQuery()
            query.exec_(
                "CREATE TABLE students (id integer PRIMARY KEY AUTOINCREMENT, "
                "grade integer NOT NULL, class integer NOT NULL, position varchar(20), "
                "category varchar(20), name varchar(20) NOT NULL, "
                "score float, detail varchar(200), note varchar(200))")
            print("create db ok")
        else:
            self.db.setDatabaseName('mydb.db')
            if not self.db.open():
                # QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())
                print("==== not open")

    def add_rows_to_db(self, rows):
        print("========== add_rows_to_db")
        query = QSqlQuery()
        for x in rows:
            print(x)
            s = "INSERT INTO students (grade, class, position, category, name, score, detail, note) VALUES ({0[0]},{0[1]},'{0[2]}','{0[3]}','{0[4]}',{0[5]},'{0[6]}','{0[7]}')".format(
                x)
            query.exec_(s)

    def get_db_all(self):
        query = QSqlQuery()
        result = []
        query.exec_("SELECT * FROM students")
        print("====== get_db_all")
        while query.next():
            a = []
            for x in range(1, 9):
                a.append(query.value(x))
            print(a)
            result.append(a)
        return result

    def output_to_xls(self, filepath="output.xlsx"):
        app = xw.App(visible=False, add_book=False)
        if not os.path.isfile(filepath):
            print("create file", filepath)
            wb = xw.Book()
            wb.save(filepath)
            wb.close()
        wb = app.books.open(filepath)
        sht0 = wb.sheets[0]
        sht0.range("A1").value = ["grade", "class", "position", "category", "name", "score", "detail", "note"]
        sht0.range("A2").value = self.get_db_all()
        wb.save()
        wb.close()
        app.quit()

    def get_test_row(self):
        f = Faker(locale="zh_CN")
        detail = str(f.random_int(max=100)) + "," + str(f.random_int(max=100)) + "," + \
            str(f.random_int(max=100)) + "," + str(f.random_int(max=100))
        row = [f.random_number(digits=2), f.random_number(digits=2), f.job(),
               f.random_letter(), f.name(), f.pyfloat(left_digits=2, right_digits=1), detail, f.sentence()]
        return row

    def get_test_rows(self, count):
        rows = []
        f = Faker(locale="zh_CN")
        for x in range(count):
            detail = str(f.random_int(max=100)) + "," + str(f.random_int(max=100)) + "," + \
                str(f.random_int(max=100)) + "," + str(f.random_int(max=100))
            rows.append([f.random_number(digits=2), f.random_number(digits=2), f.job(),
                         f.random_letter(), f.name(), f.pyfloat(left_digits=2, right_digits=1), detail, f.sentence()])
        return rows

    def gen_test_db(self):
        rows = self.get_test_rows(10)
        self.add_rows_to_db(rows)

    def input_by_xls(self, filepath, rowCount, columnCount):
        app = xw.App(visible=False, add_book=False)
        if not os.path.isfile(filepath):
            print("not found ", filepath)
            return False
        wb = app.books.open(filepath)
        sht0 = wb.sheets[0]
        rows = sht0.range((2, 1), (1 + rowCount, columnCount)).value
        print(rows)
        self.add_rows_to_db(rows)
        wb.close()
        app.quit()


if __name__ == '__main__':
    dbhandler = Dbhandler()
    print(dbhandler.get_db_all())
    # dbhandler.gen_test_db()
    # dbhandler.output_to_xls()
    # dbhandler.input_by_xls("a.xlsx", 20, 8)
