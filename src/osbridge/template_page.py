import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QMenuBar, QSplitter, QSizePolicy
)
from PySide6.QtCore import Qt

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
        label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 2px dashed #999;
                padding: 40px;
                font-size: 18px;
                color: #666;
            }
        """)
        layout.addWidget(label)


class OutputDock(QWidget):
    """Output dock with design buttons and result fields"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        self.init_ui()
    
    def init_ui(self):
        from PySide6.QtWidgets import QPushButton, QGroupBox, QLineEdit, QComboBox
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #90AF13;
                border-radius: 5px;
            }
        """)
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        title_label = QLabel("Output Dock")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        main_layout.addWidget(title_bar)
        
        # Design buttons group
        design_group = QGroupBox()
        design_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 5px;
                padding-top: 10px;
                background-color: #fafafa;
            }
        """)
        design_layout = QVBoxLayout(design_group)
        design_layout.setSpacing(10)
        design_layout.setContentsMargins(10, 10, 10, 10)
        
        # Girder Design button
        girder_btn = QPushButton("Girder Design")
        girder_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px;
                text-align: center;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #909090;
            }
        """)
        design_layout.addWidget(girder_btn)
        
        # Deck Design button
        deck_btn = QPushButton("Deck Design")
        deck_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px;
                text-align: center;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #909090;
            }
        """)
        design_layout.addWidget(deck_btn)
        
        main_layout.addWidget(design_group)
        
        # Plot section
        plot_group = QGroupBox("Plot:")
        plot_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: white;
            }
        """)
        plot_layout = QVBoxLayout(plot_group)
        plot_layout.setSpacing(10)
        plot_layout.setContentsMargins(10, 15, 10, 10)
        
        # Load Combination row
        load_row = QHBoxLayout()
        load_label = QLabel("Load Combination:")
        load_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        load_combo = QComboBox()
        load_combo.addItems(["Envelope"])
        load_combo.setStyleSheet("""
            QComboBox {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        load_row.addWidget(load_label)
        load_row.addWidget(load_combo)
        plot_layout.addLayout(load_row)
        
        # Force type buttons
        force_row = QHBoxLayout()
        force_row.setSpacing(5)
        
        shear_btn = QPushButton("Shear\nForce")
        shear_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px 5px;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        bending_btn = QPushButton("Bending\nMoment")
        bending_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px 5px;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        deflection_btn = QPushButton("Deflection")
        deflection_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px 5px;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        force_row.addWidget(shear_btn)
        force_row.addWidget(bending_btn)
        force_row.addWidget(deflection_btn)
        plot_layout.addLayout(force_row)
        
        # Maximum Value
        max_row = QHBoxLayout()
        max_label = QLabel("Maximum Value:")
        max_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        max_input = QLineEdit()
        max_input.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        max_row.addWidget(max_label)
        max_row.addWidget(max_input)
        plot_layout.addLayout(max_row)
        
        # Minimum Value
        min_row = QHBoxLayout()
        min_label = QLabel("Minimum Value:")
        min_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        min_input = QLineEdit()
        min_input.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        min_row.addWidget(min_label)
        min_row.addWidget(min_input)
        plot_layout.addLayout(min_row)
        
        main_layout.addWidget(plot_group)
        
        # Controlling Utilization Ratios
        ratio_group = QGroupBox("Controlling Utilization Ratios:")
        ratio_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: white;
            }
        """)
        ratio_layout = QVBoxLayout(ratio_group)
        ratio_layout.setSpacing(8)
        ratio_layout.setContentsMargins(10, 15, 10, 10)
        
        # Ratio field
        ratio_row = QHBoxLayout()
        ratio_label = QLabel("Ratio:")
        ratio_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        ratio_label.setMinimumWidth(80)
        ratio_input = QLineEdit()
        ratio_input.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        ratio_row.addWidget(ratio_label)
        ratio_row.addWidget(ratio_input)
        ratio_layout.addLayout(ratio_row)
        
        # Member No.
        member_row = QHBoxLayout()
        member_label = QLabel("Member No.:")
        member_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        member_label.setMinimumWidth(80)
        member_input = QLineEdit()
        member_input.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        member_row.addWidget(member_label)
        member_row.addWidget(member_input)
        ratio_layout.addLayout(member_row)
        
        # Criteria
        criteria_row = QHBoxLayout()
        criteria_label = QLabel("Criteria:")
        criteria_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        criteria_label.setMinimumWidth(80)
        criteria_input = QLineEdit()
        criteria_input.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        criteria_row.addWidget(criteria_label)
        criteria_row.addWidget(criteria_input)
        ratio_layout.addLayout(criteria_row)
        
        # Load Case
        load_case_row = QHBoxLayout()
        load_case_label = QLabel("Load Case:")
        load_case_label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
        load_case_label.setMinimumWidth(80)
        load_case_input = QLineEdit()
        load_case_input.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
                font-size: 10px;
            }
        """)
        load_case_row.addWidget(load_case_label)
        load_case_row.addWidget(load_case_input)
        ratio_layout.addLayout(load_case_row)
        
        main_layout.addWidget(ratio_group)
        
        # Bottom buttons
        results_btn = QPushButton("Generate Results Table")
        results_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        main_layout.addWidget(results_btn)
        
        report_btn = QPushButton("Generate Report")
        report_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        main_layout.addWidget(report_btn)
        
        main_layout.addStretch()


class DummyLogDock(QWidget):
    """Placeholder for log dock"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Log Window\n(Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: #fff3e0;
                border: 2px dashed #ff9800;
                padding: 20px;
                font-size: 14px;
                color: #e65100;
            }
        """)
        layout.addWidget(label)
        self.hide()  # Hidden initially


class CustomWindow(QWidget):
    def __init__(self, title: str, backend: object, parent=None):
        super().__init__()
        self.parent = parent
        self.backend = backend()

        self.setWindowTitle(title)
        self.setStyleSheet("""
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
        """)

        self.init_ui(title)

    def init_ui(self, title: str):
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.menu_bar.setFixedHeight(28)
        self.menu_bar.setContentsMargins(0, 0, 0, 0)
        
        # Add simple menus
        file_menu = self.menu_bar.addMenu("File")
        edit_menu = self.menu_bar.addMenu("Edit")
        graphics_menu = self.menu_bar.addMenu("Graphics")
        help_menu = self.menu_bar.addMenu("Help")
        
        main_v_layout.addWidget(self.menu_bar)

        # Body widget
        self.body_widget = QWidget()
        self.layout = QHBoxLayout(self.body_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Splitter for docks
        self.splitter = QSplitter(Qt.Horizontal, self.body_widget)
        
        # Input dock
        self.input_dock = InputDock(backend=self.backend, parent=self)
        # Set reasonable size constraints for the input dock
        # Minimum width should accommodate labels + controls + margins
        self.input_dock.setMinimumWidth(300)
        self.input_dock.setMaximumWidth(450)
        self.splitter.addWidget(self.input_dock)

        # Central widget with CAD and log
        central_widget = QWidget()
        central_V_layout = QVBoxLayout(central_widget)
        central_V_layout.setContentsMargins(0, 0, 0, 0)
        central_V_layout.setSpacing(0)

        # CAD widget
        self.cad_widget = DummyCADWidget()
        central_V_layout.addWidget(self.cad_widget, 3)

        # Log dock
        self.logs_dock = DummyLogDock()
        central_V_layout.addWidget(self.logs_dock, 1)

        self.splitter.addWidget(central_widget)

        # Output dock
        self.output_dock = OutputDock()
        self.output_dock.setMinimumWidth(250)
        self.output_dock.setMaximumWidth(350)
        self.splitter.addWidget(self.output_dock)

        self.layout.addWidget(self.splitter)

        # Set stretch factors: give central widget most space
        self.splitter.setStretchFactor(0, 0)  # input dock: no stretch
        self.splitter.setStretchFactor(1, 1)  # central widget: stretches
        self.splitter.setStretchFactor(2, 0)  # output dock: no stretch

        # Set initial sizes - with visible output dock
        input_dock_width = 240
        output_dock_width = 270
        total_width = self.width() if self.width() > 0 else 1200
        central_width = max(500, total_width - input_dock_width - output_dock_width)
        
        self.splitter.setSizes([input_dock_width, central_width, output_dock_width])
        
        main_v_layout.addWidget(self.body_widget)


def main():
    app = QApplication(sys.argv)
    
    # Create and show window
    window = CustomWindow("Fin Plate Connection - Test", BackendOsBridge, None)
    window.resize(1200, 800)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()