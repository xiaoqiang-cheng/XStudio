from XStudio.utils import *
from .custom_widget import CollapsibleContainer
import os

class View(QMainWindow):
    def __init__(self, meta_path = "./toolbox.json") -> None:
        super().__init__()
        self.setWindowTitle("Xiaoqiang Studio")
        # 创建一个中心小部件并设置布局

        self.content_area = QWidget()
        self.content_layout = QGridLayout(self.content_area)  # 使用 QGridLayout
        self.content_area.setLayout(self.content_layout)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.content_area)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setWidgetResizable(True)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.central_layout.addWidget(self.scroll_area)

        self.tool_list = parse_json(meta_path)
        self.toolnum_rows = self.tool_list['meta']['cols']

        self.toolbox_widget = {}
        self.toolbox_config = {}
        for index, tool in enumerate(self.tool_list['tools']):
            curr_tool_path = os.path.join("plugin", tool + ".json")
            if os.path.exists(curr_tool_path):
                self.toolbox_config[tool] = parse_json(curr_tool_path)
            else:
                print('test tool')
                self.toolbox_config[tool] = {
                    "cmd": "echo %s"%tool,
                    "params": []
                }
            self.toolbox_widget[index] = CollapsibleContainer(tool, self.toolbox_config[tool]['params'])

            # 计算行和列的位置
            row = index // self.toolnum_rows  # 每行放两个小部件
            col = index % self.toolnum_rows
            self.content_layout.addWidget(self.toolbox_widget[index], row, col)