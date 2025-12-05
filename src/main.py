# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui import UserInterface
from player import VideoPlayer

def main():
    app = QApplication(sys.argv)
    player = VideoPlayer()
    ui = UserInterface(player)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()