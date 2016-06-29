import sys

sys.path.append('UI/MainUI')
sys.path.append('Classes')

from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap
import MainUI
from EEG_reader import EEGReader
from PyQt4.QtCore import QTimer

class App(QtGui.QMainWindow, MainUI.Ui_BCARM):
    labelsList = []
    reader = None
    timer = QTimer()
    breakTime = 20

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.labelsList = [[self.A, self.B, self.C],
                           [self.D, self.E, self.F],
                           [self.G, self.H, self.I]]
        self.reader = EEGReader();
        # connect signals with their corresponding slots
        self.reader.flashOn.connect(self.flashOn)
        self.reader.flashOff.connect(self.flashOff)
        self.reader.markAsNormal.connect(self.markAsNormal)
        self.reader.markAsTarget.connect(self.markAsTarget)
        self.reader.brk.connect(self.brk)
        
        self.timer.timeout.connect(self.tick)

    def showFullScreen(self):
        super(self.__class__, self).showFullScreen()
        self.reader.start()

    def getRow(self, c):
        ''' given a character c, returns the row including the character in the screen '''
        code = c - ord('A')
        return code / 3

    def getCol(self, c):
        ''' given a character c, returns the column including the character in the screen '''
        code = c - ord('A')
        return code % 3

    def markAsNormal(self, c):
	x = self.getRow(c)
	y = self.getCol(c)
	self.labelsList[x][y].setStyleSheet("color: rgb(61, 61, 61)")
        font = QtGui.QFont()
        font.setPointSize(48)
        self.labelsList[x][y].setFont(font)

    def markAsTarget(self, c):
        x = self.getRow(c)
        y = self.getCol(c)
        self.labelsList[x][y].setStyleSheet("color: rgb(255, 0, 0)")
        font = QtGui.QFont()
        font.setPointSize(64)
        self.labelsList[x][y].setFont(font)

    def flashOn(self, rc):
        dx, dy = 0, 1
        x, y = rc, 0
        if (rc > 2): 
            dx, dy = 1, 0
            x, y = 0, rc - 3 
        for i in range(3):
            self.labelsList[x][y].setStyleSheet("color: rgb(255, 255, 255)")
            font = QtGui.QFont()
            font.setPointSize(64)
            self.labelsList[x][y].setFont(font)
            x = x + dx
            y = y + dy

    def flashOff(self, rc):
        dx, dy = 0, 1
        x, y = rc, 0
        if (rc > 2): 
            dx, dy = 1, 0
            x, y = 0, rc - 3 
        for i in range(3):
            self.labelsList[x][y].setStyleSheet("color: rgb(61, 61, 61)")
            font = QtGui.QFont()
            font.setPointSize(48)
            self.labelsList[x][y].setFont(font)
            x = x + dx
            y = y + dy
    
    def brk(self):
        self.timer.start(1000)

    def tick(self):
        print self.breakTime
        self.breakTime -= 1
        if (self.breakTime == 0):
            self.timer.stop()
            self.breakTime = 120
            self.reader.startEpoch()

def main():
	app = QtGui.QApplication(sys.argv)
	form = App();
	form.showFullScreen();
	app.exec_();

if __name__ == '__main__':
    main()
