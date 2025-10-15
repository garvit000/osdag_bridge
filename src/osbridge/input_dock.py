import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QComboBox, QScrollArea, QLabel, QFormLayout, QLineEdit, QGroupBox, QSizePolicy
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QPixmap, QDoubleValidator, QRegularExpressionValidator

# Import constants from Common
from common import *


class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()


def right_aligned_widget(widget):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    layout.setAlignment(widget, Qt.AlignVCenter)
    return container


def left_aligned_widget(widget):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    layout.addStretch()
    layout.setAlignment(widget, Qt.AlignVCenter)
    return container


def apply_field_style(widget):
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    if isinstance(widget, QComboBox):
        style = """
        QComboBox {
            padding: 2px;
            border: 1px solid black;
            border-radius: 5px;
            background-color: white;
            color: black;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            border-left: 0px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid black;
            outline: none;
        }
        QComboBox QAbstractItemView::item {
            color: black;
            background-color: white;
            padding: 2px;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #90AF13;
            color: black;
        }
        """
        widget.setStyleSheet(style)
    elif isinstance(widget, QLineEdit):
        widget.setStyleSheet("""
        QLineEdit {
            padding: 1px 7px;
            border: 1px solid #070707;
            border-radius: 6px;
            background-color: white;
            color: #000000;
        }
        """)


def style_main_buttons():
    return """
        QPushButton {
            background-color: #94b816;
            color: white;
            font-weight: bold;
            border-radius: 4px;
            padding: 6px 18px;
        }
        QPushButton:hover {
            background-color: #7a9a12;
        }
    """


class InputDock(QWidget):
    def __init__(self, backend, parent):
        super().__init__()
        self.parent = parent
        self.backend = backend
        self.input_widget = None

        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.left_container = QWidget()

        # Get input fields from backend
        input_field_list = self.backend.input_values()
        input_field_list = self.equalize_label_length(input_field_list)

        self.build_left_panel(input_field_list)
        self.main_layout.addWidget(self.left_container)

        # Toggle strip
        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #94b816;")
        self.toggle_strip.setFixedWidth(6)
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("<")
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setToolTip("Hide panel")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c8408;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #5e7407;
            }
        """)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        self.main_layout.addWidget(self.toggle_strip)

    def equalize_label_length(self, list):
        max_len = 0
        for t in list:
            if t[2] not in [TYPE_TITLE, TYPE_IMAGE]:
                if len(t[1]) > max_len:
                    max_len = len(t[1])
        
        return_list = [] 
        for t in list:
            if t[2] not in [TYPE_TITLE, TYPE_IMAGE]:
                new_tupple = (t[0], t[1].ljust(max_len)) + t[2:]
            else:
                new_tupple = t
            return_list.append(new_tupple)

        return return_list

    def get_validator(self, validator):
        if validator == 'Int Validator':
            return QRegularExpressionValidator(QRegularExpression("^(0|[1-9]\\d*)(\\.\\d+)?$"))
        elif validator == 'Double Validator':
            return QDoubleValidator()
        else:
            return None
        
    def build_left_panel(self, field_list):
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("background-color: white;")
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(5, 5, 5, 5)
        panel_layout.setSpacing(0)

        # Top Bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)
        input_dock_btn = QPushButton("Basic Inputs")
        input_dock_btn.setStyleSheet(style_main_buttons())
        input_dock_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(input_dock_btn)
        
        additional_inputs_btn = QPushButton("Additional Inputs")
        additional_inputs_btn.setStyleSheet(style_main_buttons())
        additional_inputs_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(additional_inputs_btn)
        panel_layout.addLayout(top_bar)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #EFEFEC;
                background-color: transparent;
                padding: 3px;
            }
            QScrollBar:vertical {
                background: #E0E0E0;
                width: 8px;
                margin: 0px 0px 0px 3px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #A0A0A0;
                min-height: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #707070;
            }
        """)

        group_container = QWidget()
        self.input_widget = group_container
        group_container_layout = QVBoxLayout(group_container)

        # Build form
        track_group = False
        index = 0
        for field in field_list:
            index += 1
            label = field[1]
            type = field[2]
            
            if type == TYPE_MODULE:
                continue
            elif type == TYPE_TITLE:
                if track_group:
                    current_group.setLayout(cur_box_form)
                    group_container_layout.addWidget(current_group)
                    track_group = False
                
                current_group = QGroupBox(label)
                current_group.setObjectName(label + "_group")
                track_group = True
                current_group.setStyleSheet("""
                    QGroupBox {
                        border: 1px solid #90AF13;
                        border-radius: 4px;
                        margin-top: 0.8em;
                        font-weight: bold;
                    }
                    QGroupBox::title {
                        subcontrol-origin: content;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 4px;
                        margin-top: -15px;
                        background-color: white;
                    }
                """)
                cur_box_form = QFormLayout()
                cur_box_form.setHorizontalSpacing(5)
                cur_box_form.setVerticalSpacing(10)
                cur_box_form.setContentsMargins(10, 10, 10, 10)
                cur_box_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
                cur_box_form.setAlignment(Qt.AlignmentFlag.AlignRight)

            elif type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")

                right = NoScrollComboBox()
                right.setObjectName(field[0])
                apply_field_style(right)
                option_list = field[3]
                right.addItems(option_list)

                cur_box_form.addRow(left, right_aligned_widget(right))
            
            elif type == TYPE_IMAGE:
                left = ""
                right = QLabel()
                right.setFixedWidth(90)
                right.setFixedHeight(90)
                right.setObjectName(field[0])
                right.setScaledContents(True)
                # Try to load image if path exists
                try:
                    pixmap = QPixmap(field[3])
                    if not pixmap.isNull():
                        right.setPixmap(pixmap)
                except:
                    right.setText("Image")
                right.setAlignment(Qt.AlignmentFlag.AlignLeft)
                cur_box_form.addRow(left, left_aligned_widget(right))
            
            elif type == TYPE_TEXTBOX:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                
                right = QLineEdit()
                apply_field_style(right)
                right.setObjectName(field[0])
                right.setEnabled(True if field[4] else False)
                if field[5] != 'No Validator':
                    right.setValidator(self.get_validator(field[5]))
                cur_box_form.addRow(left, right_aligned_widget(right))
            
            if index == len(field_list):
                current_group.setLayout(cur_box_form)
                group_container_layout.addWidget(current_group)

        group_container_layout.addStretch()
        scroll_area.setWidget(group_container)

        self.data = {}
        panel_layout.addWidget(scroll_area)

        # Bottom buttons
        btn_button_layout = QHBoxLayout()
        btn_button_layout.setContentsMargins(0, 20, 0, 0)
        btn_button_layout.addStretch(2)

        save_input_btn = QPushButton("Save Input")
        save_input_btn.setStyleSheet(style_main_buttons())
        btn_button_layout.addWidget(save_input_btn)
        btn_button_layout.addStretch(1)

        design_btn = QPushButton("Design")
        design_btn.setStyleSheet(style_main_buttons())
        btn_button_layout.addWidget(design_btn)
        btn_button_layout.addStretch(2)

        panel_layout.addLayout(btn_button_layout)

        # Horizontal scroll area
        h_scroll_area = QScrollArea()
        h_scroll_area.setWidgetResizable(True)
        h_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        h_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        h_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                background: #E0E0E0;
                height: 8px;
                margin: 3px 0px 0px 0px;
                border-radius: 2px;
            }
            QScrollBar::handle:horizontal {
                background: #A0A0A0;
                min-width: 30px;
                border-radius: 2px;
            }
        """)
        h_scroll_area.setWidget(self.left_panel)

        left_layout.addWidget(h_scroll_area)