# import sys,time
# from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout
#
# class WinForm(QWidget):
#     def __init__(self,parent=None):
#         super(WinForm, self).__init__(parent)
#         #设置标题与布局方式
#         self.setWindowTitle('实时刷新界面的例子')
#         layout=QGridLayout()
#
#         #实例化列表控件与按钮控件
#         self.listFile=QListWidget()
#         self.btnStart=QPushButton('开始')
#
#         #添加到布局中指定位置
#         layout.addWidget(self.listFile,0,0,1,2)
#         layout.addWidget(self.btnStart,1,1)
#
#         #按钮的点击信号触发自定义的函数
#         self.btnStart.clicked.connect(self.slotAdd)
#         self.setLayout(layout)
#     def slotAdd(self):
#         for n in range(10):
#             #获取条目文本
#             str_n='File index{0}'.format(n)
#             #添加文本到列表控件中
#             self.listFile.addItem(str_n)
#             #实时刷新界面
#             QApplication.processEvents()
#             #睡眠一秒
#             time.sleep(1)
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     win=WinForm()
#     win.show()
#     sys.exit(app.exec_())

# 通过线程
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QLabel
import time
import sys


class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currTime))
            time.sleep(1)


class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(400, 100)
        self.input = QLabel(self)
        self.input.resize(400, 100)
        self.initUI()

    def initUI(self):
        # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(self.handleDisplay)
        self.thread = QThread()
        self.backend.moveToThread(self.thread)
        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        self.input.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
