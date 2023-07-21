import sys
from PyQt5.QtWidgets import QApplication
from CODE.SCREEN.MainWidget import MainWindow

def main():
    app = QApplication(sys.argv)
    # 위젯 스타일
    app.setStyle("Plastique")

    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
