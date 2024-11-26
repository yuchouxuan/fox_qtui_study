from u001 import Ui_MainWindow
''' 懒，就写了两个，回头随学随加吧，反正就是自己学东西玩
u001 Oillescope 
u002 傅里叶
'''
from PyQt5 import   QtWidgets
import qdarktheme

if __name__ == '__main__':
    palette = qdarktheme.load_palette()
    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarktheme.load_stylesheet())
    mw = Ui_MainWindow()
    mw.setupUi(mw)
    mw.show()
    app.exec()
