import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from CODE.SCREEN.MainWidget import MainWindow

def main():
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")

    # 글꼴 설정
    fontDB = QFontDatabase()
    # fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
    # fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
    # fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
    # fontDB.addApplicationFont("../../FONT/NanumSquareRoundR.ttf")

    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()

