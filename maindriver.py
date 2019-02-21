# -*- coding: utf-8 -*-

# Import CMD
import os

# Import GUI Module
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QIcon

# Import Parser
from ktisparser import KTISParser


# MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bar = QStatusBar()
        self.setStatusBar(self.bar)
        self.bar.showMessage("ID와 PW를 입력 후 엔터를 누르세요.")
        self.setCentralWidget(Organizer())
        self.setWindowTitle("Kookmin Lecture Organizer")
        self.setWindowIcon(QIcon('kmu.ico'))
        self.show()


# CentralWidget
class Organizer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.subjects = []

        self.setGeometry(300, 300, 800, 480)

        # Title
        label = QLabel('Kookmin Lecture Organizer')
        font = label.font()
        font.setPointSize(font.pointSize() + 10)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)

        # Search 영역
        year_label = QLabel('학년도: ')
        year_label.setAlignment(Qt.AlignVCenter)
        semester_label = QLabel('학기: ')
        semester_label.setAlignment(Qt.AlignVCenter)
        self.year_input = QLineEdit(self)
        self.semester_selector = QComboBox(self)
        self.semester_selector.addItem("1학기")
        self.semester_selector.addItem("여름학기")
        self.semester_selector.addItem("2학기")
        self.semester_selector.addItem("겨울학기")
        self.search = QPushButton("찾기")
        self.search.clicked.connect(self.search_clicked)

        self.search_hbox = QHBoxLayout()
        self.search_hbox.addWidget(year_label)
        self.search_hbox.addWidget(self.year_input)
        self.search_hbox.addWidget(semester_label)
        self.search_hbox.addWidget(self.semester_selector)
        self.search_hbox.addStretch()
        self.search_hbox.addWidget(self.search)

        self.search_vbox = QVBoxLayout()
        self.welcome = QLabel()
        self.welcome.setVisible(False)
        self.search_vbox.addWidget(self.welcome)
        self.search_vbox.addLayout(self.search_hbox)

        searchLayout = QGroupBox("검색")
        searchLayout.setLayout(self.search_vbox)

        # Login 영역
        id_label = QLabel('ID: ')
        id_label.setAlignment(Qt.AlignVCenter)
        pw_label = QLabel('PW: ')
        pw_label.setAlignment(Qt.AlignVCenter)
        self.id_input = QLineEdit(self)
        self.id_input.returnPressed.connect(self.request_login)
        self.pw_input = QLineEdit(self)
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.returnPressed.connect(self.request_login)

        self.login_hbox1 = QHBoxLayout()
        self.login_hbox1.addWidget(id_label)
        self.login_hbox1.addWidget(self.id_input)
        self.login_hbox2 = QHBoxLayout()
        self.login_hbox2.addWidget(pw_label)
        self.login_hbox2.addWidget(self.pw_input)

        self.login_vbox = QVBoxLayout()
        self.login_vbox.addLayout(self.login_hbox1)
        self.login_vbox.addLayout(self.login_hbox2)

        loginLayout = QGroupBox("로그인")
        loginLayout.setLayout(self.login_vbox)

        # Subject 영역
        self.subView = QTreeView()
        self.subView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.subView.setAlternatingRowColors(True)
        self.model = self.createCategoryModel(self)
        self.subView.setModel(self.model)

        ratio = [250, 100, 50, 100]
        for i in range(4):
            self.subView.setColumnWidth(i, ratio[i])

        subjectLayout = QGroupBox("KTIS 수강신청과목")
        subjectLayout.setFixedWidth(550)
        subLayout = QVBoxLayout()
        subLayout.addWidget(self.subView)
        subjectLayout.setLayout(subLayout)

        # Option 영역
        self.chk_assn = QCheckBox("과제")
        self.chk_lecinfo = QCheckBox("강의자료")

        self.chk_userdef1 = QCheckBox()
        self.txt_userdef1 = QLineEdit()
        self.chk_userdef2 = QCheckBox()
        self.txt_userdef2 = QLineEdit()

        self.chklist = (
            self.chk_assn,
            self.chk_lecinfo,
            self.chk_userdef1,
            self.chk_userdef2
        )

        self.chk_hbox1 = QHBoxLayout()
        self.chk_hbox1.addWidget(self.chk_userdef1)
        self.chk_hbox1.addWidget(self.txt_userdef1)
        self.chk_hbox2 = QHBoxLayout()
        self.chk_hbox2.addWidget(self.chk_userdef2)
        self.chk_hbox2.addWidget(self.txt_userdef2)

        self.chk_vbox = QVBoxLayout()
        self.chk_vbox.addWidget(self.chk_assn)
        self.chk_vbox.addWidget(self.chk_lecinfo)
        self.chk_vbox.addLayout(self.chk_hbox1)
        self.chk_vbox.addLayout(self.chk_hbox2)

        optionLayout = QGroupBox("옵션(과목 내 생성)")
        optionLayout.setLayout(self.chk_vbox)

        # Directory 영역
        self.destination = QLineEdit('C:/')
        self.destination.setReadOnly(True)
        self.setButton = QPushButton("경로변경")
        self.setButton.clicked.connect(self.set_destination)

        self.directory_hbox = QHBoxLayout()
        self.directory_hbox.addWidget(self.destination)
        self.directory_hbox.addWidget(self.setButton)

        directoryLayout = QGroupBox("폴더 생성 위치")
        directoryLayout.setLayout(self.directory_hbox)

        # Generate 영역
        self.generator = QPushButton("폴더 생성!")
        self.generator.clicked.connect(self.make_folder)
        self.generator.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.generator.setFixedHeight(directoryLayout.sizeHint().height() - 10)

        # mainLayout
        mainLayout = QGridLayout()
        mainLayout.addWidget(searchLayout, 0, 0, 1, 6)
        mainLayout.addWidget(loginLayout, 0, 6)
        mainLayout.addWidget(subjectLayout, 1, 0, 5, 6)
        mainLayout.addWidget(optionLayout, 1, 6, 5, 1)
        mainLayout.addWidget(directoryLayout, 6, 0, 1, 6)
        mainLayout.addWidget(self.generator, 6, 6, Qt.AlignBottom)

        self.setLayout(mainLayout)

        # 사용자 변수 초기화
        self.user = None

    def make_folder(self):
        subfolder = []
        for i in range(2):
            chkbox = self.chklist[i]
            if chkbox.isChecked():
                subfolder.append(chkbox.text())

        if self.chk_userdef1.isChecked():
            subfolder.append(self.txt_userdef1.text())
        if self.chk_userdef2.isChecked():
            subfolder.append(self.txt_userdef2.text())

        path = self.destination.text() + "/" \
               + self.year_input.text() \
               + "-" + self.semester_selector.currentText()[:-2]

        if not os.path.exists(path):
            os.makedirs(path)
            for i in range(1, len(self.subjects)):

                subpath = path + "/" + self.subjects[i][0]

                if not os.path.exists(subpath):
                    os.makedirs(subpath)

                for option in subfolder:
                    os.makedirs(subpath + "/" + option)

                self.parent().bar.showMessage("성공적으로 폴더를 생성했습니다!", 10000)
        else:
            self.parent().bar.showMessage("이미 해당 경로에 폴더가 존재합니다.", 5000)

    def set_destination(self):
        dialog = QFileDialog()
        path = dialog.getExistingDirectory()
        self.destination.setText(path)

    def request_login(self):
        self.parent().bar.showMessage("로그인 중...")

        uid = self.id_input.text()
        pw = self.pw_input.text()

        self.user = KTISParser(uid, pw)

        login_msg = self.user.login(KTISParser.headless_mod())
        self.parent().bar.showMessage(login_msg, 7000)

        # 이름 출력부
        if self.user.LOGIN['status']:
            self.welcome.setVisible(True)
            s = self.user.name + "님의 강의를 검색합니다."
            self.welcome.setText(s)
        else:
            self.welcome.setVisible(False)

    def search_clicked(self):

        # 목록 초기화
        for _ in range(20):
            self.model.removeRow(0)

        year = self.year_input.text()
        semester = self.semester_selector.currentText()

        if self.user is None:
            self.parent().bar.showMessage(
                "로그인이 필요한 기능입니다.", 10000)
            return

        if self.user.LOGIN['status']:
            self.subjects = self.user.get_lecture(year, semester)

            if len(self.subjects) > 2 and len(self.subjects[1]) > 1:
                for sub in self.subjects[1:]:
                    self.addSubject(self.model, str(sub[0]), str(sub[3]),
                                    str(sub[4]), str(sub[5]))

                self.parent().bar.showMessage(
                    "총 %d개의 강의를 찾았습니다." % (len(self.subjects) - 1), 10000)
            else:
                self.parent().bar.showMessage(
                    "해당 학기에 강의가 존재하지 않습니다.", 10000)

    SUBJECT, TYPE, CREDIT, PROFESSOR = range(4)

    def createCategoryModel(self, parent):
        model = QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "교과목명")
        model.setHeaderData(self.TYPE, Qt.Horizontal, "이수구분")
        model.setHeaderData(self.CREDIT, Qt.Horizontal, "학점")
        model.setHeaderData(self.PROFESSOR, Qt.Horizontal, "담당교수")
        return model

    def addSubject(self, model, subject, typeof, credit, professor):
        self.model.insertRow(0)
        self.model.setData(model.index(0, self.SUBJECT), subject)
        self.model.setData(model.index(0, self.TYPE), typeof)
        self.model.setData(model.index(0, self.CREDIT), credit)
        self.model.setData(model.index(0, self.PROFESSOR), professor)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
