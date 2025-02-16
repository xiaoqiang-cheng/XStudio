from XStudio.utils import *



class LineTextWithLabelWidget(QWidget):
    textChanged = Signal(str)
    def __init__(self, parent=None, widget_titie="", default_value = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(widget_titie)
        self.linetxt = QLineEdit(str(default_value))
        layout.addWidget(self.label)
        layout.addWidget(self.linetxt)
        self.setLayout(layout)

    def text(self):
        return self.linetxt.text()

    def setText(self, cstr):
        self.linetxt.setText(cstr)



class CollapsibleContainer(QFrame):
    beCliced = Signal(str, dict)
    def __init__(self, title="", params_list = [], parent=None):
        super(CollapsibleContainer, self).__init__(parent)
        self.lay = QVBoxLayout(self)
        self.title = title
        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=True
        )
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.DownArrow)
        self.toggle_button.clicked.connect(self.on_pressed)
        self.toggle_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toggle_button.customContextMenuRequested.connect(self.show_context_menu)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QWidget()
        self.content_area.setLayout(QVBoxLayout())
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.content_area)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")


        self.lay.addWidget(self.toggle_button, 0, Qt.AlignTop)
        self.lay.addWidget(self.scroll_area, 1, Qt.AlignTop)

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)
        self.init_widget(params_list)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        change_color_action = menu.addAction("Change Color")
        change_color_action.triggered.connect(self.change_color)
        menu.exec_(self.toggle_button.mapToGlobal(pos))

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color = color.name()
            self.update_stylesheet(color)

    def update_stylesheet(self, color):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = "#000000" if brightness > 128 else "#FFFFFF"

        self.setStyleSheet(
            f"background-color: {color}; color: {text_color};"
            )
        #  font-size: 14px; font-family: Arial, sans-serif;
    @Slot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            Qt.RightArrow   if not checked else Qt.DownArrow
        )
        if checked:
            self.scroll_area.show()
        else:
            self.scroll_area.hide()

    def init_widget(self, widget_cfg_list):
        self.params_widgets = {}
        for curr_widget in widget_cfg_list:
            widget_key = curr_widget['key']
            widget_type = curr_widget['type']
            widget_value = curr_widget['value']

            if widget_type == 'string':
                widget = LineTextWithLabelWidget(self, widget_key, widget_value)
            elif widget_type == 'number':
                widget = LineTextWithLabelWidget(self, widget_key, widget_value)
            elif widget_type == 'bool':
                widget = QCheckBox(widget_key)
                widget.setChecked(widget_value)
            self.params_widgets[widget_key] = widget
            self.add_widget(widget)
        self.add_final_run_button()

    def add_widget(self, widget):
        self.content_area.layout().addWidget(widget)

    def add_final_run_button(self):
        self.run_button = QPushButton("Run")
        self.content_area.layout().addWidget(self.run_button, -1, Qt.AlignBottom)
        self.run_button.clicked.connect(self.run_button_clicked)

    def run_button_clicked(self):
        params = {}
        for key, widget in self.params_widgets.items():
            if isinstance(widget, QCheckBox):
                params[key] = int(widget.isChecked())
            else:
                params[key] = widget.text()
        self.beCliced.emit(self.title, params)

