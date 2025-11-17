import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenuBar,
    QSplitter,
    QSizePolicy,
    QPushButton,
    QGroupBox,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from input_dock import InputDock
from backend import BackendOsBridge
from common import *


class DummyCADWidget(QWidget):
    """Placeholder for CAD widget"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("CAD Window\n(Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            """
            QLabel {
                background-color: #f0f0f0;
                border: 2px dashed #999;
                padding: 40px;
                font-size: 18px;
                color: #666;
            }
            """
        )
        layout.addWidget(label)


class OutputDock(QWidget):
    """Output dock with collapsible design controls and scrollable layout."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget {
                background-color: white;
            }
            """
        )
        self.init_ui()

    def init_ui(self):
        from input_dock import NoScrollComboBox, apply_field_style

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(10)

        title_bar = QWidget()
        title_bar.setStyleSheet(
            """
            QWidget {
                background-color: #90AF13;
                border-radius: 4px;
            }
            """
        )
        title_bar.setFixedHeight(35)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(12, 0, 12, 0)

        title_label = QLabel("Output Dock")
        title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            """
        )
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addWidget(title_bar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        results_group = QGroupBox("Analysis Results")
        results_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #333;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 8px;
                padding: 0 4px;
                background-color: white;
            }
            """
        )
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(10, 8, 10, 10)
        results_layout.setSpacing(8)

        member_row = QHBoxLayout()
        member_label = QLabel("Member:")
        member_label.setStyleSheet("font-size: 10px; color: #333; font-weight: normal;")
        member_label.setMinimumWidth(100)
        self.member_combo = NoScrollComboBox()
        self.member_combo.addItems(["All"])
        apply_field_style(self.member_combo)
        member_row.addWidget(member_label)
        member_row.addWidget(self.member_combo)
        results_layout.addLayout(member_row)

        load_combo_row = QHBoxLayout()
        load_combo_label = QLabel("Load Combination:")
        load_combo_label.setStyleSheet("font-size: 10px; color: #333; font-weight: normal;")
        load_combo_label.setMinimumWidth(100)
        self.load_combo = NoScrollComboBox()
        self.load_combo.addItems(["Envelope"])
        apply_field_style(self.load_combo)
        load_combo_row.addWidget(load_combo_label)
        load_combo_row.addWidget(self.load_combo)
        results_layout.addLayout(load_combo_row)

        forces_grid = QHBoxLayout()
        forces_grid.setSpacing(8)

        col1 = QVBoxLayout()
        for text in ["Fx", "Mx", "Dx"]:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-size: 10px; color: #333;")
            col1.addWidget(cb)
        col2 = QVBoxLayout()
        for text in ["Fy", "My", "Dy"]:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-size: 10px; color: #333;")
            col2.addWidget(cb)
        col3 = QVBoxLayout()
        for text in ["Fz", "Mz", "Dz"]:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-size: 10px; color: #333;")
            col3.addWidget(cb)
        forces_grid.addLayout(col1)
        forces_grid.addLayout(col2)
        forces_grid.addLayout(col3)
        results_layout.addLayout(forces_grid)

        display_label = QLabel("Display Options:")
        display_label.setStyleSheet("font-size: 10px; color: #333; font-weight: normal; margin-top: 4px;")
        results_layout.addWidget(display_label)

        display_row = QHBoxLayout()
        display_row.setSpacing(12)
        for text in ["Max", "Min"]:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-size: 10px; color: #333;")
            display_row.addWidget(cb)
        display_row.addStretch()
        results_layout.addLayout(display_row)

        utilization_check = QCheckBox("Controlling Utilization Ratio")
        utilization_check.setStyleSheet("font-size: 10px; color: #333;")
        results_layout.addWidget(utilization_check)

        scroll_layout.addWidget(results_group)

        design_group = QGroupBox("Design")
        design_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #333;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 8px;
                padding: 0 4px;
                background-color: white;
            }
            """
        )
        design_layout = QVBoxLayout(design_group)
        design_layout.setContentsMargins(10, 8, 10, 10)
        design_layout.setSpacing(8)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        svg_down = os.path.join(base_dir, "dropdown_down.svg").replace("\\", "/")
        svg_up = os.path.join(base_dir, "dropdown_up.svg").replace("\\", "/")

        super_frame = QFrame()
        super_frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background: white;
            }
            """
        )
        super_layout = QVBoxLayout(super_frame)
        super_layout.setContentsMargins(8, 6, 8, 6)
        super_layout.setSpacing(6)

        super_header = QHBoxLayout()
        super_title = QLabel("Superstructure")
        super_title.setStyleSheet("font-size: 10px; font-weight: bold; color: #333;")
        super_header.addWidget(super_title)
        super_header.addStretch()

        super_toggle = QPushButton()
        super_toggle.setCheckable(True)
        super_toggle.setChecked(True)
        super_toggle.setIcon(QIcon(svg_up))
        super_toggle.setIconSize(QSize(14, 14))
        super_toggle.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 2px;
            }
            """
        )
        super_header.addWidget(super_toggle)
        super_layout.addLayout(super_header)

        super_body = QWidget()
        super_body_layout = QVBoxLayout(super_body)
        super_body_layout.setContentsMargins(0, 0, 0, 0)
        super_body_layout.setSpacing(6)

        for text in ["Steel Design", "Deck Design"]:
            btn = QPushButton(text)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: white;
                    color: #333;
                    border: 1px solid #b0b0b0;
                    border-radius: 3px;
                    padding: 8px;
                    font-size: 10px;
                    font-weight: normal;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
                """
            )
            super_body_layout.addWidget(btn)

        super_layout.addWidget(super_body)

        def toggle_super(checked: bool):
            super_body.setVisible(checked)
            super_toggle.setIcon(QIcon(svg_up if checked else svg_down))

        super_toggle.toggled.connect(toggle_super)
        design_layout.addWidget(super_frame)

        sub_frame = QFrame()
        sub_frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background: white;
            }
            """
        )
        sub_layout = QVBoxLayout(sub_frame)
        sub_layout.setContentsMargins(8, 6, 8, 6)
        sub_layout.setSpacing(6)

        sub_header = QHBoxLayout()
        sub_title = QLabel("Substructure")
        sub_title.setStyleSheet("font-size: 10px; font-weight: bold; color: #333;")
        sub_header.addWidget(sub_title)
        sub_header.addStretch()

        sub_toggle = QPushButton()
        sub_toggle.setCheckable(True)
        sub_toggle.setChecked(True)
        sub_toggle.setIcon(QIcon(svg_up))
        sub_toggle.setIconSize(QSize(14, 14))
        sub_toggle.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 2px;
            }
            """
        )
        sub_header.addWidget(sub_toggle)
        sub_layout.addLayout(sub_header)

        sub_body = QWidget()
        sub_body_layout = QVBoxLayout(sub_body)
        sub_body_layout.setContentsMargins(0, 0, 0, 0)
        sub_body_layout.setSpacing(0)
        sub_layout.addWidget(sub_body)

        def toggle_sub(checked: bool):
            sub_body.setVisible(checked)
            sub_toggle.setIcon(QIcon(svg_up if checked else svg_down))

        sub_toggle.toggled.connect(toggle_sub)
        design_layout.addWidget(sub_frame)

        scroll_layout.addWidget(design_group)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        results_btn = QPushButton("Generate Results Table")
        results_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #90AF13;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a9a12;
            }
            """
        )
        main_layout.addWidget(results_btn)

        report_btn = QPushButton("Generate Report")
        report_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #90AF13;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a9a12;
            }
            """
        )
        main_layout.addWidget(report_btn)


class DummyLogDock(QWidget):
    """Placeholder for log dock."""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Log Window\n(Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            """
            QLabel {
                background-color: #fff3e0;
                border: 2px dashed #ff9800;
                padding: 20px;
                font-size: 14px;
                color: #e65100;
            }
            """
        )
        layout.addWidget(label)
        self.hide()


class CustomWindow(QWidget):
    def __init__(self, title: str, backend: object, parent=None):
        super().__init__()
        self.parent = parent
        self.backend = backend()

        self.setWindowTitle(title)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #ffffff;
                margin: 0px;
                padding: 0px;
            }
            QMenuBar {
                background-color: #F4F4F4;
                color: #000000;
                padding: 0px;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #FFFFFF;
            }
            """
        )

        self.init_ui()

    def init_ui(self):
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)

        self.menu_bar = QMenuBar(self)
        self.menu_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.menu_bar.setFixedHeight(28)
        self.menu_bar.setContentsMargins(0, 0, 0, 0)
        self.menu_bar.addMenu("File")
        self.menu_bar.addMenu("Edit")
        self.menu_bar.addMenu("Graphics")
        self.menu_bar.addMenu("Help")
        main_v_layout.addWidget(self.menu_bar)

        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal, body_widget)

        input_dock = InputDock(backend=self.backend, parent=self)
        input_dock.setMinimumWidth(300)
        input_dock.setMaximumWidth(450)
        splitter.addWidget(input_dock)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        cad_widget = DummyCADWidget()
        central_layout.addWidget(cad_widget, 3)

        logs_dock = DummyLogDock()
        central_layout.addWidget(logs_dock, 1)
        splitter.addWidget(central_widget)

        output_dock = OutputDock()
        output_dock.setMinimumWidth(250)
        output_dock.setMaximumWidth(350)
        splitter.addWidget(output_dock)

        body_layout.addWidget(splitter)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        input_dock_width = 240
        output_dock_width = 270
        total_width = self.width() if self.width() > 0 else 1200
        central_width = max(500, total_width - input_dock_width - output_dock_width)
        splitter.setSizes([input_dock_width, central_width, output_dock_width])

        main_v_layout.addWidget(body_widget)

        self.splitter = splitter
        self.input_dock = input_dock
        self.output_dock = output_dock
        self.cad_widget = cad_widget
        self.logs_dock = logs_dock


def main():
    app = QApplication(sys.argv)
    window = CustomWindow("Fin Plate Connection - Test", BackendOsBridge)
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
