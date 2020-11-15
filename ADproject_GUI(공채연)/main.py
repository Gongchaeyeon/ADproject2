import pickle
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets,QtCore

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

        self.dbfilename = 'High.dat'

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

        self.setGeometry(300, 200, 450, 350)
        self.radio_value=''
        self.ra1.setChecked(True)
    # --------------------------------------------------------디자인 완료
        bt1.clicked.connect(self.startGame)
        bt2.clicked.connect(self.exitGame)
        self.ra1.clicked.connect(self.radioClicked)
        self.ra2.clicked.connect(self.radioClicked)
        self.ra3.clicked.connect(self.radioClicked)

    def radioClicked(self):
        self.radio_value=self.sender().text()

        if self.radio_value =='상':  # 난이도에 맞는 데이터 지정
            self.dbfilename='High.dat'
        elif self.radio_value=='중':
            self.dbfilename='Middle.dat'
        else:
            self.dbfilename='Low.dat'

        self.readRankDB() # dbfilename에 난이도에 맞는 데이터 넣음
        self.showRankDB()

    def startGame(self):
        if self.tf1.text()=='':
            QMessageBox.warning(self, 'Error', "ID를 입력하세요.")
        else:
            #게임 시작
            self.addRankDB()
            self.writeRankDB()
        self.showRankDB()

    def exitGame(self):
        # self.writeRankDB()  # 나갈 때 저장.
        self.close()
        # self.show() --> 다시 새로운 창 켜짐

    def readRankDB(self): # 데이터 읽어오기
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

    def writeRankDB(self): # 데이터 쓰기
        fh = open(self.dbfilename,'wb')
        pickle.dump(self.db, fh)
        fh.close()

    def showRankDB(self): # 데이터 table에 띄우기
        self.table.setText('')
        self.readRankDB()
        for p in sorted(self.db, key=lambda person: person['Score'] , reverse=True):
            self.table.append('{}={}\t{}={}'.format('ID',p['ID'],'Score',int(p['Score'])))
        self.table.setFont(QFont('Arial', 11))

    def addRankDB(self):  #-------------- 랭킹 갱신
        score = 20 # 임시로 점수 지정.
        check=0 # 중복체크
        record=[]

        for p in self.db:
            if p['ID'] == self.tf1.text():
                check=1

        if check ==1:
            buttonReply = QMessageBox.question(self, '경고!', '동일한 ID가 존재합니다. \n해당 ID의 Score를 갱신하시겠습니까?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes: # 중복되어도 실행하는 경우
                # 게임시작!
                for p in self.db: # 게임이 끝나고 , Score가 기존의 기록보다 클 경우 점수 갱신.
                    if p['ID'] == self.tf1.text():
                        if p['Score'] < score:
                            p['Score']=score
            else:
                self.tf1.setText('')

        else: # ID가 중복되지 않았을 때 (게임 끝나고 데이터 기록)
            record = {'ID': self.tf1.text(), 'Score': score}
            self.db += [record]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = main()
    ma.show()
    sys.exit(app.exec_())