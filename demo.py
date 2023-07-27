from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow,QTextBrowser
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt
import sys
from new_widget import Set_question
from untitled import Ui_MainWindow

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.sum=0                                                  #气泡数量
        self.widgetlist = []                                        #记录气泡
        self.text = ""                                              # 存储信息
        self.icon = QtGui.QPixmap("1.jpg")                          # 头像
        #设置聊天窗口样式 隐藏滚动条
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 信号与槽
        self.pushButton.clicked.connect(self.create_widget)         #创建气泡
        self.pushButton.clicked.connect(self.set_widget)            #修改气泡长宽
        self.plainTextEdit.undoAvailable.connect(self.Event)        #监听输入框状态
        scrollbar = self.scrollArea.verticalScrollBar()
        scrollbar.rangeChanged.connect(self.adjustScrollToMaxValue) #监听窗口滚动条范围


    # 回车绑定发送
    def Event(self):
        if not self.plainTextEdit.isEnabled():  #这里通过文本框的是否可输入
            self.plainTextEdit.setEnabled(True)
            self.pushButton.click()
            self.plainTextEdit.setFocus()

    #创建气泡
    def create_widget(self):
        self.text=self.plainTextEdit.toPlainText()
        self.plainTextEdit.setPlainText("")
        self.sum += 1
        if self.sum % 2:   # 根据判断创建左右气泡
            Set_question.set_return(self, self.icon, self.text,QtCore.Qt.LeftToRight)    # 调用new_widget.py中方法生成左气泡
            QApplication.processEvents()                                # 等待并处理主循环事件队列
        else:
            Set_question.set_return(self, self.icon, self.text,QtCore.Qt.RightToLeft)   # 调用new_widget.py中方法生成右气泡
            QApplication.processEvents()                                # 等待并处理主循环事件队列


        # 你可以通过这个下面代码中的数组单独控制每一条气泡
        # self.widgetlist.append(self.widget)
        # print(self.widgetlist)
        # for i in range(self.sum):
        #     f=self.widgetlist[i].findChild(QTextBrowser)    #气泡内QTextBrowser对象
        #     print("第{0}条气泡".format(i),f.toPlainText())

    # 修改气泡长宽
    def set_widget(self):
        font = QFont()
        font.setPointSize(16)
        fm = QFontMetrics(font)
        text_width = fm.width(self.text)+115    #根据字体大小生成适合的气泡宽度
        if self.sum != 0:
            if text_width>632:                  #宽度上限
                text_width=int(self.textBrowser.document().size().width())+100  #固定宽度
            self.widget.setMinimumSize(text_width,int(self.textBrowser.document().size().height())+ 40) #规定气泡大小
            self.widget.setMaximumSize(text_width,int(self.textBrowser.document().size().height())+ 40) #规定气泡大小
            self.scrollArea.verticalScrollBar().setValue(10)


    # 窗口滚动到最底部
    def adjustScrollToMaxValue(self):
        scrollbar = self.scrollArea.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())