import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from faker import Faker
from MtplWidget import MyMplCanvas


class MainWin(QMainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setWindowTitle("水平布局管理例子")
        self.resize(800, 500)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['grade', ])
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'root')

        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')

        self.tree.addTopLevelItem(root)
        self.tree.clicked.connect(self.onTreeClicked)

        self.tree.setLineWidth(0)  # 设置外线宽度
        self.tree.setMidLineWidth(0)  # 设置中线宽度
        self.tree.setFrameShadow(QFrame.Raised)  # 设置阴影效果：凸起
        self.tree.setFrameShape(QFrame.Box)  # 设置图形为：Box

        self.db = None
        self.db_connect()
        self.sql_create()
        self.tableView = QTableView()
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)  # 设置不可编辑
        self.model = QSqlTableModel()
        self.display()

        # self.setCentralWidget(self.tableView)
        # self.left = QDockWidget("left", self)
        # self.left.setWidget(self.tree)

        # self.addDockWidget(Qt.LeftDockWidgetArea, self.left)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_menu)
        self.tableView.setSortingEnabled(True)

        self.layout = QGridLayout()
        self.layout.addWidget(self.tree, 0, 0, 0, 0)
        self.layout.addWidget(self.tableView, 0, 1, 0, 5)

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.fk = Faker(locale='zh_CN')

    def right_menu(self, pos):
        menu = QMenu(self.tableView)
        opt_add = menu.addAction("add")
        opt_remove = menu.addAction("remove")
        opt_hide = menu.addAction("hide")
        opt_show = menu.addAction("show")
        opt_plot = menu.addAction("plot")
        action = menu.exec_(self.tableView.mapToGlobal(pos))
        if action == opt_add:
            print("right menu add")
            self.add()
        elif action == opt_remove:
            print("right menu remove")
            self.remove()
        elif action == opt_hide:
            print("right menu hide")
            self.tableView.setVisible(False)
        elif action == opt_show:
            print("right menu show")
            self.tableView.setVisible(True)
        elif action == opt_plot:
            print("right menu plot")
            self.show_plot()
            # self.tree.show()
        else:
            return

    def function():
        pass

    def display(self):
        self.model.setTable('students')
        # QSqlTableModel.OnRowChange: Changes to a row will be applied when the user selects a different row.
        self.model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.model.setHeaderData(0, Qt.Horizontal, 'ID')
        self.model.setHeaderData(1, Qt.Horizontal, 'Class')
        self.model.setHeaderData(2, Qt.Horizontal, 'Name')
        self.model.setHeaderData(3, Qt.Horizontal, 'Score')
        self.model.select()
        print(self.model.rowCount())
        self.tableView.setModel(self.model)

    def db_connect(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not os.path.isfile("./test.db"):
            self.db.setDatabaseName('./test.db')
            self.sql_create()
        self.db.setDatabaseName('./test.db')
        if not self.db.open():
            QMessageBox.critical(self, 'Database Connection', self.db.lastError().text())

    def sql_create(self):
        query = QSqlQuery()
        query.exec_(
            "CREATE TABLE students (id integer PRIMARY KEY AUTOINCREMENT, class varchar(20) NOT NULL, name varchar(20) NOT NULL, score float)")
        # query.exec_("INSERT INTO students (class, name, score) "
        #             "VALUES ('0104', 'Louis', 59.5)")

    def closeEvent(self, QCloseEvent):
        self.db.close()

    def onTreeClicked(self, qmodelindex):
        item = self.tree.currentItem()
        # self.model.setText
        print("key=%s ,value=%s" % (item.text(0), item.text(1)))

    # it not use now
    def table_update(self):
        row_select = self.tableView.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        new_name = row_select[1].text()
        print("id: {}, save_name: {}".format(id, new_name))

    def add(self):
        index_end = self.model.rowCount()
        self.model.insertRow(self.model.rowCount())
        self.model.setData(self.model.index(index_end, 1), self.fk.random_number(digits=4))
        self.model.setData(self.model.index(index_end, 2), self.fk.name())
        self.model.setData(self.model.index(index_end, 3), self.fk.random_int(max=100))
        self.model.submit()

        self.tableView.setModel(self.model)

    def remove(self):
        indexs = self.tableView.selectionModel().selection().indexes()
        if len(indexs) > 0:
            index = indexs[0]
            self.model.removeRows(index.row(), 1)
        self.model.select()

    def show_plot(self):
        # self.layout = QVBoxLayout(self)
        mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        mpl.start_static_plot()  # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        # self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        # mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(mpl, 0, 1, 0, 5)
        self.tableView.setVisible(False)
        # self.layout.addWidget(self.mpl)
        # self.layout.addWidget(self.mpl_ntb)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWin()
    form.show()
    sys.exit(app.exec_())
