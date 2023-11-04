import sys
from PyQt5.QtWidgets import QApplication,QStyleFactory,QMessageBox,QWidget,QDialog,QLCDNumber
from PyQt5.QtCore import QThread, pyqtSignal,QTimer
from Ui_pausepass import Ui_PausePass

from key_generate_lib import generate_key,encrypt_password,task
from key_display_lib import read_from_file,decrypt_password

class PausePass(QWidget,Ui_PausePass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.key=''
        self.encrypted_key = None
        self.countdowndlg = None
        self.duration=7*24*60*60
    def initUI(self):
        self.changeStyle('Fusion')
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.pushButton.clicked.connect(self.on_generate)
        self.pushButton_2.clicked.connect(self.on_display)
        self.setFixedSize(self.width(), self.height()); 
        self.show()
        
    def on_generate(self):
        key = generate_key()
        #QMessageBox.warning(self, '提示',f'生成的密码:{self.key}')
        result = QMessageBox().question(self, "提示", f'生成的密码:{key},保存吗', QMessageBox.Yes|QMessageBox.Cancel, QMessageBox.Cancel)
        if(result == QMessageBox.Yes):
            self.key=key
            self.encrypted_key = encrypt_password('pwd123', self.key)
            self.thread = TaskThread(duration= self.duration,encrypted_key=self.encrypted_key)
            # 连接信号到槽函数
            self.thread.finished.connect(self.on_task_finished)
            QMessageBox.warning(self, '提示','请等待一段时间之后保存')
            self.thread.start()
            self.countdowndlg = CountDownDlg(self.duration)

    def on_task_finished(self):
        QMessageBox.information(self, "提示", "密码已经保存到文件.")

    def on_display(self):
        encrypted_key = read_from_file('key.pkl')
        if encrypted_key==None:
            QMessageBox.warning(self, '提示','读取\'key.pkl\'文件失败')
            return
        decrypted_key = decrypt_password('pwd123', encrypted_key)
        QMessageBox.warning(self, '提示',f'上次保存的密码是: {decrypted_key}')

    def changeStyle(self, styleName):
        #改变Style
        QApplication.setStyle(QStyleFactory.create(styleName))

    def closeEvent(self,event):
        if self.countdowndlg!=None:
            self.countdowndlg.close()
        if self.encrypted_key!=None:
            task(0,self.encrypted_key)

class TaskThread(QThread):

    finished = pyqtSignal()
    def __init__(self, duration, encrypted_key):
        super().__init__()
        self.duration = duration
        self.encrypted_key = encrypted_key
        

    def run(self):
        # 这里执行你的任务
        task(self.duration,self.encrypted_key)
        # 当任务完成时发出信号
        self.finished.emit()

class CountDownDlg(QDialog):
    def __init__(self,duration):
        super().__init__()
        self.initUI()
        self.duration=duration

    def initUI(self):
        self.lcd = QLCDNumber(self)  # 设置数字类
        self.lcd.setDigitCount(11)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setStyleSheet(
            "border: 1px solid green; color: green; background: silver;"
        )
        self.resize(250, 90)
        self.lcd.setGeometry(0, 0, 250, 90)
        self.setWindowTitle('预计需要时间')
        self.show()
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.flush)  # 使用了计时器

    def flush(self):
        # 将秒数转换为小时、分钟和秒
        days = self.duration // 86400
        hours = (self.duration % 86400) // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        # 显示的内容
        self.lcd.display(f'{days}:{hours}:{minutes}:{seconds}')
        if self.duration<1:
            self.close()
        self.duration-=1
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw=PausePass()
    
    sys.exit(app.exec_())