from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MessageGroupBox(QGroupBox):
    def __init__(self, nick, chat, parent):
        QGroupBox.__init__(self)
        self.main_window = parent
        self.chat = chat
        self.nick = nick

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        delete = menu.addAction("Delete chat " + self.chat + " from " + self.nick)
        ban = menu.addAction("ban " + self.nick)
        quitaction = menu.addAction("QUIT")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitaction:
            qApp.quit()

    def mousePressEvent(self, event):
        self.main_window.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.main_window.offset.x()
        y_w = self.main_window.offset.y()
        self.main_window.move(x - x_w, y - y_w)


class MainGroupBox(QGroupBox):
    def __init__(self, parent):
        QGroupBox.__init__(self)
        self.main_window = parent

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        self.main_window.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.main_window.offset.x()
        y_w = self.main_window.offset.y()
        self.main_window.move(x - x_w, y - y_w)


class ChatWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.maingroupbox = MainGroupBox(self)
        self.VBoxLayout = QGridLayout()
        self.pixmaplist = []
        self.row = 0

        self.maingroupbox.setAttribute(Qt.WA_TranslucentBackground)

        self.maingroupbox.setLayout(self.VBoxLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.maingroupbox)
        self.scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)
        self.btn = QPushButton('Button', self)
        self.btn.clicked.connect(self.add)

        layout.addWidget(self.btn)

    def autoScroll(self):
        scrl = self.scroll.verticalScrollBar()
        scrl.setValue(scrl.maximum())

    def add(self):
        mygroupbox = MessageGroupBox('nick' + str(self.row), 'GG' + str(self.row), self)
        grid = QGridLayout()

        self.pixmaplist.append(getpixmap(":TWITCH:"))

        label_ = QLabel()
        label_.setPixmap(self.pixmaplist[self.row])
        grid.addWidget(label_, self.row, 0)
        grid.addWidget(QLabel('NAME'), self.row, 1)
        msg_label = QLabel('This is some test user message; and it so very long and long and long and long')
        msg_label.setWordWrap(True)
        grid.addWidget(msg_label, self.row, 2)
        grid.setColumnStretch(2, 5)
        mygroupbox.setLayout(grid)
        self.VBoxLayout.addWidget(mygroupbox, self.row, 1)
        self.row = self.row + 1
        QTimer.singleShot(100, self.autoScroll)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)


def getpixmap(chat):
    if chat == ":GG:":
        return QPixmap("./img/goodgame.png").scaledToWidth(20).scaledToWidth(20)
    elif chat == ":TWITCH:":
        return QPixmap("./img/twitch.png").scaledToWidth(20).scaledToWidth(20)
    else:
        return QPixmap().scaledToWidth(20).scaledToWidth(20)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = ChatWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_NoSystemBackground, True)
    window.setAttribute(Qt.WA_TranslucentBackground, True)
    window.setGeometry(500, 300, 300, 400)
    window.show()
    sys.exit(app.exec_())
