import sys
from playsound import playsound
from PyQt5.QtWidgets import QApplication,QWidget,QTextEdit,QVBoxLayout,QPushButton,QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import time
import os
import numpy as np

# 全局变量,获取当前单词
global NUM
NUM = 0

class Word(QThread):
    '''
        用于显示单词及词义的子线程
    '''
    word = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        '''
            通过全局变量NUM获取到当前的单词，查找字典中的词义，组合到一起
        '''
        # 路径
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        path = '.\\Speech_US' + '\\' + date
        # 路径下所有音频名
        wordnames = os.listdir(path)
        print(wordnames)
        dictionary = np.load(date+'.npy',allow_pickle=True).item()
        global NUM
        self.word.emit(wordnames[NUM][:-4]+': '+ dictionary[wordnames[NUM][:-4]])
        print(wordnames[NUM][:-4]+': '+ dictionary[wordnames[NUM][:-4]])
        NUM += 1
        print(NUM)

class Recite(QThread):
    #信号量
    word = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        # 路径
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        path = '.\\Speech_US' + '\\' + date
        wordnames = os.listdir(path)
        print(wordnames[NUM][:-4])
        self.word.emit(wordnames[NUM][:-4])

class GUI(QWidget):
    def __init__(self):
        '''

        :return:
        '''
        super().__init__() #继承父类的属性和方法
        self.InitUI()

    def InitUI(self):
        '''

        :return:
        '''
        self.KnowButton = QPushButton("Know")
        self.NotKowButton = QPushButton("NotKnow")
        self.ReciteButton = QPushButton("Recite")
        self.textEdit = QTextEdit()

        # 横向布局
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.KnowButton)
        self.hbox.addWidget(self.NotKowButton)
        self.hbox.addStretch(1)

        # 竖向布局
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.textEdit)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.ReciteButton)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.KnowButton.clicked.connect(self.wordEmit)
        self.NotKowButton.clicked.connect(self.wordEmit)
        self.ReciteButton.clicked.connect(self.reciteWord)
        self.setGeometry(500,500,500,250)
        self.setWindowTitle("单词听写器")
        self.show()

    def wordEmit(self):
        '''
            创建线程，发射信号，用于槽函数显示
        :return: word+": "+meaning
        '''
        self.thread = Word()
        self.thread.word.connect(self.showWord)
        self.thread.start()


    def showWord(self,word):
        '''
        Show the word and meanings
        :return:
        '''
        # print(word)
        self.textEdit.setText(word)

    def playSound(self,word):
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        path = '.\\Speech_US' + '\\' + date + '\\'
        playsound(path+word+'.mp3')


    def reciteWord(self,word):
        '''
        Just play the mp3 of the word
        :param word: Dictation of words
        :return: nothing
        '''
        self.thread2 = Recite()
        self.thread2.word.connect(self.playSound)
        self.thread2.start()



if __name__=='__main__':
    # GUI
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())

