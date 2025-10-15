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


class DummyOutputDock(QWidget):
    """Placeholder for output dock"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Output Dock\n(Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: #e8f5e9;
                border: 2px dashed #4caf50;
                padding: 20px;
                font-size: 16px;
                color: #2e7d32;
            }
        """)
        layout.addWidget(label)
        self.hide()  # Hidden initially


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
        # Constrain the input dock width to avoid it taking too much space at startup
        self.input_dock.setMinimumWidth(220)
        self.input_dock.setMaximumWidth(420)
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
        self.output_dock = DummyOutputDock()
        self.splitter.addWidget(self.output_dock)

        self.layout.addWidget(self.splitter)

        # Set initial sizes and stretch factors so the input dock is narrower by default
        # Give the central widget most of the available space
        self.splitter.setStretchFactor(0, 0)  # input dock: low stretch
        self.splitter.setStretchFactor(1, 1)  # central widget: high stretch
        self.splitter.setStretchFactor(2, 0)  # output dock: low stretch

        # Try to set reasonable default sizes (input small, central large, output hidden)
        input_dock_width = 300
        total_width = self.width() if self.width() > 0 else 1200
        central_width = max(600, total_width - input_dock_width)
        output_dock_width = 0
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