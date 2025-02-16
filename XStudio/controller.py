from XStudio.utils import *
from XStudio.view import View
from XStudio.model import Model
import signal

class Controller():
    def __init__(self) -> None:
        self.app = QApplication([])
        self.view = View()
        self.model = Model()
        signal.signal(signal.SIGINT, self.sigint_handler)

        # 使用 QTimer 定期检查信号
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)

        self.singal_init()

    def singal_init(self):
        for widget in self.view.toolbox_widget.values():
            widget.beCliced.connect(self.on_toolbox_widget_clicked)

    def on_toolbox_widget_clicked(self, title, params):
        self.model.exec_tool(title, self.view.toolbox_config[title], params)

    def run(self):
        self.view.show()
        self.app.exec_()
        sys.exit(0)

    def sigint_handler(self, signum = None, frame = None):
        print("Ctrl + C 退出程序")
        sys.exit(0)