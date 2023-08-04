import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QFormLayout, QLineEdit, QWidget, QApplication,
                             QCompleter, QPushButton, QLabel, QVBoxLayout)
from Movies import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(300, 300)
        self.setMinimumSize(QSize(300, 300))
        self.setMaximumSize(QSize(500, 500))
        layout = QFormLayout()

        # 发送账号
        self.input_from = QLineEdit(self)
        self.input_from.setAlignment(Qt.AlignCenter)
        layout.addRow('发送邮箱:', self.input_from)
        from_data = account
        from_completer = QCompleter(from_data)  # 自动填充
        self.input_from.setCompleter(from_completer)

        # 发送账号密码
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setAlignment(Qt.AlignCenter)
        layout.addRow('密码:', self.input_password)

        # 接受邮箱
        self.input_to = QLineEdit(self)
        self.input_to.setAlignment(Qt.AlignCenter)
        layout.addRow('接受邮箱:', self.input_to)
        to_data = account
        to_completer = QCompleter(to_data)
        self.input_to.setCompleter(to_completer)

        # 按钮
        confirmBtn = QPushButton('确认', self)
        confirmBtn.clicked.connect(self.run)
        exitBtn = QPushButton('退出', self)
        exitBtn.clicked.connect(self.exitsys)
        layout.addRow(confirmBtn, exitBtn)

        accountBtn = QPushButton('账号管理', self)
        accountBtn.clicked.connect(self.show_account)
        layout.addRow(accountBtn)
        confirmBtn.resize(50, 50)
        exitBtn.resize(50, 50)

        self.setLayout(layout)
        self.setWindowTitle("爬取豆瓣新片网")

    def show_account(self):
        self.child_windows = AccountWin()
        self.child_windows.show()

    def exitsys(self):
        exit_accounts = codecs.open('accounts.txt', 'w', 'utf-8')
        print(account)
        for acc in account:
            exit_accounts.write(acc + '\n')
        sys.exit()

    def run(self):
        douban(url, headers, infofile)
        infofile.write("\r\n")
        infofile.close()
        to_163(
            self.input_from.text(), self.input_to.text(), self.input_password.text()
        )
        if self.input_from.text() in account:
            pass
        else:
            account.append(self.input_from.text())
        if self.input_to.text() in account:
            pass
        else:
            account.append(self.input_to.text())
        print(account)


class AccountWin(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(150, 100)
        account_layout = QVBoxLayout()
        lable1 = QLabel(self)
        lable1.setText(account[0])
        account_layout.addWidget(lable1)


def mainwindows():
    app = QApplication(sys.argv)
    new_windows = MainWindow()
    new_windows.show()
    sys.exit(app.exec_())


if __name__ == "__main__":

    directory = 'new_movie//' + strftime("%Y_%m_%d") + '//'
    os.makedirs(directory, exist_ok=True)

    # 存储文件
    infofile = codecs.open('new_movie' + '//' + strftime("%Y_%m_%d") + '//' +
                           'new_movie' + strftime("%Y_%m_%d") + '.txt', 'w', 'utf-8')
    # 消息头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36'}
    # 网址
    url = 'https://movie.douban.com/chart'
    # 账号
    if os.path.exists('accounts.txt'):
        accounts = codecs.open('accounts.txt', 'r', 'utf-8')
        account = []
        for line in accounts.readlines():
            account.append(line.strip())
            print(account)
        accounts.close()
    else:
        accounts = codecs.open('accounts.txt', 'w', 'utf-8')
        account = {}
        accounts.close()

    mainwindows()
