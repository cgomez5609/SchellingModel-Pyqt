import sys

from PyQt5.QtWidgets import QApplication

from pyqt_main import MainWindow


# Global Variables
DIFF_AGENT_TYPES = 3
AGENTS_PER_TYPE = 200
THRESHOLD = 3

# Schelling Model
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Grid is 45 x 45
    demo = MainWindow(num_of_agent_classes=DIFF_AGENT_TYPES,
                      num_agents_per_class=AGENTS_PER_TYPE,
                      satisfaction_threshold=THRESHOLD)
    demo.count_the_wealthy()
    demo.show()

    sys.exit(app.exec_())