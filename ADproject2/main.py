import pickle
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets,QtCore
import os
from Game import *

class main(QWidget):

    # https://soma0sd.tistory.com/95 디자인 참고
    qss = """
        QWidget {
            color: rgb(0,0,0);
            background: rgb(255,255,255);
        }
        QWidget#windowTitle {
            color: rgb(0,0,0);
            background: rgb(240,230,250);
        }
        QWidget#windowTitle QLabel {
            color: rgb(0,0,0);
            background: rgb(240,230,250);
        }
    """

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(self.qss)

        self.dbfilename = 'data/High.dat'

        self.db = []
        self.readRankDB()
        self.initUI()
        self.showRankDB()

    def initUI(self):

        # 레이아웃과 타이틀바 위젯 생성
        window_vbox = QtWidgets.QVBoxLayout(self)
        window_vbox.setContentsMargins(0, 0, 0, 0)
        titlebar = QtWidgets.QWidget()
        titlebar.setObjectName("windowTitle")
        title_hbox = QtWidgets.QHBoxLayout(titlebar)
        content_vbox = QtWidgets.QVBoxLayout()
        content_vbox.setContentsMargins(3,3,3,3)

        # 타이틀바와 컨텐츠 박스 안의 내용물을 생성
        title_label = QtWidgets.QLabel("타자 디펜스 게임")
        title_label.setFont(QFont('Arial', 14))
        lb1 = QLabel("ID: ")
        self.tf1 = QLineEdit()  # 아이디 레이아웃
        p1 = QHBoxLayout()
        p1.addWidget(lb1)
        p1.addWidget(self.tf1)

        lb2 = QLabel("난이도 선택: ") # 난이도 레이아웃
        self.ra1 = QRadioButton("상")
        self.ra2 = QRadioButton("중")
        self.ra3 = QRadioButton("하")
        p2 = QHBoxLayout()
        p2.addWidget(lb2)
        p2.addWidget(self.ra1)
        p2.addWidget(self.ra2)
        p2.addWidget(self.ra3)
        p2.addStretch(1)

        bt1 = QPushButton("Game Start!") # 버튼 레이아웃
        bt2 = QPushButton("Exit")
        p3 = QVBoxLayout()
        p3.addWidget(bt1)
        p3.addWidget(bt2)

        lb3 = QLabel("<랭킹>", self) # 랭킹
        self.table = QTextEdit()

        grid = QGridLayout() # 랭킹 제외한 부분 grid 레이아웃으로 배치
        grid.addLayout(p1, 0, 0)
        grid.addLayout(p2, 1, 0)
        grid.addLayout(p3, 0, 1, 2, 1)

        main = QVBoxLayout()  # 다 합친 레이아웃
        main.addLayout(grid)
        main.addWidget(lb3)
        main.addWidget(self.table)
        main.setSpacing(13)

        # 각 항목을 레이아웃에 배치
        title_hbox.addWidget(title_label)
        content_vbox.addLayout(main)
        window_vbox.addWidget(titlebar)
        window_vbox.addLayout(content_vbox)
        self.setLayout(window_vbox)

        font_list=[lb1,lb2,lb3,self.ra1,self.ra2,self.ra3]  # 폰트 지정
        for a in font_list: a.setFont(QFont('Arial', 13))
        bt1.setFont(QFont('Arial', 15))
        bt2.setFont(QFont('Arial', 15))

        self.setGeometry(300, 200, 400, 350)
        self.radio_value=''
        self.ra1.setChecked(True)

        fh = open('data/difficulty.dat', 'wb') # 난이도 초기화
        pickle.dump('상', fh)
        fh.close()
    # --------------------------------------------------------디자인 완료
        bt1.clicked.connect(self.startGame)
        bt2.clicked.connect(self.exitGame)
        self.ra1.clicked.connect(self.radioClicked)
        self.ra2.clicked.connect(self.radioClicked)
        self.ra3.clicked.connect(self.radioClicked)


    def radioClicked(self): # ---------- [상중하 버튼을 클릭했을 때]

        self.radio_value=self.sender().text()

        if self.radio_value =='상':  # 난이도에 맞는 데이터 지정
            self.dbfilename='data/High.dat'
        elif self.radio_value=='중':
            self.dbfilename='data/Middle.dat'
        else: self.dbfilename='data/Low.dat'

        fh = open('data/difficulty.dat', 'wb')
        pickle.dump(self.radio_value, fh)
        fh.close()

        self.readRankDB() # dbfilename에 난이도에 맞는 데이터 불러옴
        self.showRankDB()

    def startGame(self): # ---------- [게임 시작]

        # 입력한 ID가 영어와 숫자로 이루어졌는지 판단
        id_check_al=0
        id_cehck_num=0
        for i in self.tf1.text():
            if ord('a') <= ord(i) <= ord('z'):
                id_check_al+=1
            elif i.isdecimal()==True:
                id_cehck_num+=1

        if self.tf1.text()=='':
            QMessageBox.warning(self, 'Error', "ID를 입력하세요.")          # ▼ 영어,숫자가 아닌 다른 문자가 포함된 경우         ▼ 숫자로만 이루어진 경우                     ▼ 영어로만 이루어진 경우
        elif len(self.tf1.text())> 14 or len(self.tf1.text())<7 or id_cehck_num+id_check_al != len(self.tf1.text()) or id_cehck_num == len(self.tf1.text()) or  id_check_al == len(self.tf1.text()):
            QMessageBox.warning(self, 'Error', "ID는 영어와 숫자로 이루어진 7~14자리 문자이어야 합니다.")
            self.tf1.setText('')

        else: # 조건이 맞으면
            self.addRankDB() # addRankDB안에 게임 시작 하는 부분 구현됨.
            self.writeRankDB() # 갱신된 점수 저장
            self.showRankDB()

    def exitGame(self): #----------------[게임 종료]
        self.close()

    def readRankDB(self): # ----------------------[데이터 읽어오기]
        try:
            fh = open(self.dbfilename,'rb')
        except FileNotFoundError as e:
            self.db=[]
            return
        try:
            self.db = pickle.load(fh)
        except:
            pass
        fh.close()

    def writeRankDB(self): # ---------------------[데이터 쓰기]
        fh = open(self.dbfilename,'wb')
        pickle.dump(self.db, fh)
        fh.close()

    def showRankDB(self): # ---------------------[랭킹 table에 띄우기]
        self.table.setText('')
        self.readRankDB()
        for p in sorted(self.db, key=lambda person: person['Score'] , reverse=True):
            self.table.append(' [{}]  {}\t  {} ->  {}'.format('ID',p['ID'],'Score',int(p['Score'])))
        self.table.setFont(QFont('Arial', 11))

    def addRankDB(self):  #-------------- [랭킹 갱신]
        score = 0 # 임시로 점수 지정.
        check=0 # 중복체크
        record=[]

        for p in self.db:
            if p['ID'] == self.tf1.text():
                check=1

        if check ==1:
            buttonReply = QMessageBox.question(self, '경고!', '동일한 ID가 존재합니다. \n해당 ID의 Score를 갱신하시겠습니까?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes: # 중복되어도 실행하는 경우
                os.system('python ./Game.py') # 게임 시작!!
                for p in self.db: # 게임이 끝나고 , Score가 기존의 기록보다 클 경우 점수 갱신.
                    if p['ID'] == self.tf1.text():
                        if p['Score'] < score:
                            p['Score']=score

        else: # ID가 중복되지 않았을 때 (게임 끝나고 데이터 기록)
            os.system('python ./Game.py') # 게임 시작!!
            record = {'ID': self.tf1.text(), 'Score': score}
            self.db += [record]

        self.tf1.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = main()
    ma.show()
    sys.exit(app.exec_())
