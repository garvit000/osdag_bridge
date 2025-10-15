import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QComboBox, QScrollArea, QLabel, QFormLayout, QLineEdit, QGroupBox, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QPixmap, QDoubleValidator, QRegularExpressionValidator

from common import *


class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()


def right_aligned_widget(widget):
    """Right-align widget horizontally within its container"""
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addStretch()
    layout.addWidget(widget)
    layout.setAlignment(widget, Qt.AlignRight | Qt.AlignVCenter)
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
    widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    widget.setMaximumWidth(180)
    widget.setMinimumHeight(24)
    
    if isinstance(widget, QComboBox):
        style = """
        QComboBox {
            padding: 3px 5px;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            background-color: white;
            color: black;
            min-height: 20px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #c0c0c0;
            background-color: #4a7ba7;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid white;
            margin-right: 5px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #c0c0c0;
            outline: none;
            selection-background-color: #e8f4ff;
        }
        QComboBox QAbstractItemView::item {
            color: black;
            background-color: white;
            padding: 4px;
            min-height: 20px;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #e8f4ff;
            color: black;
        }
        """
        widget.setStyleSheet(style)
    elif isinstance(widget, QLineEdit):
        widget.setStyleSheet("""
        QLineEdit {
            padding: 3px 5px;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            background-color: white;
            color: black;
            min-height: 20px;
        }
        QLineEdit:focus {
            border: 1px solid #4a7ba7;
        }
        """)


def style_main_buttons():
    return """
        QPushButton {
            background-color: #90AF13;
            color: white;
            font-weight: bold;
            border: 1px solid #7a9611;
            border-radius: 3px;
            padding: 6px 16px;
            min-height: 28px;
        }
        QPushButton:hover {
            background-color: #7a9a12;
        }
        QPushButton:pressed {
            background-color: #6a8a10;
        }
    """


class InputDock(QWidget):
    def __init__(self, backend, parent):
        super().__init__()
        self.parent = parent
        self.backend = backend
        self.input_widget = None
        self.structure_type_combo = None  # Store reference to structure type combo box

        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.left_container = QWidget()

        # Get input fields from backend
        input_field_list = self.backend.input_values()

        self.build_left_panel(input_field_list)
        self.main_layout.addWidget(self.left_container)

        # Toggle strip
        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #90AF13;")
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
                background-color: #7a9a12;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #6a8a10;
            }
        """)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        self.main_layout.addWidget(self.toggle_strip)

    def get_validator(self, validator):
        if validator == 'Int Validator':
            return QRegularExpressionValidator(QRegularExpression("^(0|[1-9]\\d*)(\\.\\d+)?$"))
        elif validator == 'Double Validator':
            return QDoubleValidator()
        else:
            return None
    
    def on_structure_type_changed(self, text):
        """Handle structure type combo box changes"""
        if text == "Other":
            # Show warning message when "Other" is selected
            QMessageBox.warning(
                self,
                "Structure Type Not Supported",
                "The selected structure type is not included currently.\n\n"
                "This application currently only covers Highway Bridge design.",
                QMessageBox.Ok
            )
        
    def build_left_panel(self, field_list):
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("background-color: white;")
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(8, 8, 8, 8)
        panel_layout.setSpacing(0)

        # Top Bar with buttons
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        top_bar.setContentsMargins(0, 0, 0, 10)
        
        input_dock_btn = QPushButton("Basic Inputs")
        input_dock_btn.setStyleSheet(style_main_buttons())
        input_dock_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(input_dock_btn)
        
        additional_inputs_btn = QPushButton("Additional Inputs")
        additional_inputs_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                font-weight: normal;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 6px 16px;
                min-height: 28px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #a0a0a0;
            }
        """)
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
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
                border-radius: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 0px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        group_container = QWidget()
        self.input_widget = group_container
        group_container_layout = QVBoxLayout(group_container)
        group_container_layout.setContentsMargins(0, 0, 0, 0)
        group_container_layout.setSpacing(12)

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
                        border: 1px solid #d0d0d0;
                        border-radius: 4px;
                        margin-top: 8px;
                        font-weight: bold;
                        font-size: 11px;
                        padding-top: 8px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top left;
                        left: 8px;
                        padding: 0 4px;
                        background-color: white;
                        color: #333;
                    }
                """)
                cur_box_form = QFormLayout()
                cur_box_form.setHorizontalSpacing(8)
                cur_box_form.setVerticalSpacing(12)
                cur_box_form.setContentsMargins(12, 16, 12, 12)
                cur_box_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                cur_box_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

            elif type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setStyleSheet("font-weight: normal; color: #333; font-size: 10px;")

                right = NoScrollComboBox()
                right.setObjectName(field[0])
                apply_field_style(right)
                option_list = field[3]
                right.addItems(option_list)

                # Connect signal for Structure Type combo box
                if field[0] == KEY_STRUCTURE_TYPE:
                    self.structure_type_combo = right
                    right.currentTextChanged.connect(self.on_structure_type_changed)

                cur_box_form.addRow(left, right_aligned_widget(right))
            
            elif type == TYPE_IMAGE:
                left = ""
                right = QLabel()
                right.setFixedWidth(90)
                right.setFixedHeight(90)
                right.setObjectName(field[0])
                right.setScaledContents(True)
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
                left.setStyleSheet("font-weight: normal; color: #333; font-size: 10px;")
                
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
        btn_button_layout.setContentsMargins(0, 15, 0, 0)
        btn_button_layout.setSpacing(10)

        save_input_btn = QPushButton("Save Input")
        save_input_btn.setStyleSheet(style_main_buttons())
        save_input_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_button_layout.addWidget(save_input_btn)

        design_btn = QPushButton("Design")
        design_btn.setStyleSheet(style_main_buttons())
        design_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_button_layout.addWidget(design_btn)

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
                background: #f0f0f0;
                height: 10px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 30px;
            }
        """)
        h_scroll_area.setWidget(self.left_panel)

        left_layout.addWidget(h_scroll_area)