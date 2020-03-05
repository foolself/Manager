import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from faker import Faker
from MtplWidget import MyMplCanvas
from myModel import MyModel
from dbUtil import Dbhandler


class MainWin(QMainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setWindowTitle("水平布局管理例子")
        self.resize(800, 500)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['class'])
        school = QTreeWidgetItem(self.tree)
        school.setText(0, 'school')

        for i in range(1, 4):
            grade = QTreeWidgetItem(school)
            grade.setText(0, '- grade %d -' % (i))
            for j in range(1, 4):
                class_ = QTreeWidgetItem(grade)
                class_.setText(0, '- class %d -' % (j))
                # 第二个值（两位数，grade+class）用来标记班级信息
                class_.setText(1, '%d' % (10 * i + j))

        self.tree.addTopLevelItem(school)
        self.tree.clicked.connect(self.onTreeClicked)

        self.tree.setLineWidth(0)  # 设置外线宽度
        self.tree.setMidLineWidth(0)  # 设置中线宽度
        self.tree.setFrameShadow(QFrame.Raised)  # 设置阴影效果：凸起
        self.tree.setFrameShape(QFrame.Box)  # 设置图形为：Box

        self.tableView = QTableView()
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)  # 设置不可编辑
        self.dbhandler = Dbhandler()
        self.model = MyModel("students")
        self.display()
        self.tableView.doubleClicked.connect(self.show_detail)
        self.mpl = None

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
        opt_select_score = menu.addAction("select score>80")
        opt_back = menu.addAction("back")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == opt_add:
            self.add()
        elif action == opt_remove:
            self.remove()
        elif action == opt_select_score:
            self.select_score()
        else:
            return

    def function():
        pass

    def display(self):
        headList = ["id", "grade", "class", "position", "category", "name", "score", "detail", "note"]
        self.model.init(headList)
        self.tableView.setModel(self.model)
        # 隐藏 id 列
        self.tableView.setColumnHidden(0, True)

    def onTreeClicked(self, qmodelindex):
        item = self.tree.currentItem()
        if item.text(1):
            # print("text=%s ,class=%s" % (item.text(0), item.text(1)))
            self.model.select_class(item.text(1))
        else:
            pass

        # it not use now
    def table_update(self):
        row_select = self.tableView.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        new_name = row_select[1].text()
        print("id: {}, save_name: {}".format(id, new_name))

    def add(self):
        row = self.dbhandler.get_test_row()
        self.model.add_row(row)

    def remove(self):
        indexs = self.tableView.selectionModel().selection().indexes()
        if len(indexs) > 0:
            self.model.remove_row(indexs[0])

    def select_grade(self):
        self.model.select_grade()

    def select_class(self):
        self.model.select_class()

    def select_score(self):
        self.model.select_score()

    def show_detail(self, index):
        row = index.row()
        content = []
        # TODO 不用循环，如何获取一整行的数据
        for x in range(9):
            content.append(self.model.data(self.model.index(row, x)))
        hlayout_top = QHBoxLayout()
        info = QLabel("personal detail information: \n" + str(content))
        btn_back = QPushButton()
        btn_back.setText("back")
        btn_back.clicked.connect(self.back_to_table)
        hlayout_top.addWidget(info)
        hlayout_top.addWidget(btn_back)
        self.mpl = MyMplCanvas(self, data=content[7])
        # self.mpl.start_static_plot()  # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        # self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        # mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        vLayout = QVBoxLayout()
        vLayout.addLayout(hlayout_top)
        vLayout.addWidget(self.mpl)
        # self.layout.addLayout(self.vLayout, 0, 1, 0, 5)
        self.detailWidget = QWidget()
        self.detailWidget.setLayout(vLayout)
        self.layout.addWidget(self.detailWidget, 0, 1, 0, 5)
        self.tableView.setVisible(False)
        # self.layout.addWidget(self.mpl, 0, 1, 0, 5)
        # self.layout.addWidget(self.mpl_ntb)

    def back_to_table(self):
        self.detailWidget.setVisible(False)
        self.tableView.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWin()
    form.show()
    sys.exit(app.exec_())
