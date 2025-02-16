from XStudio.utils import *
from XStudio.custom_widget import CollapsibleContainer


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CollapsibleContainer Test")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # 创建 CollapsibleContainer 实例
        collapsible_container = CollapsibleContainer("Test Container")


        layout.addWidget(collapsible_container)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())