import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QComboBox, QScrollArea, QLabel, QFormLayout, QLineEdit, QGroupBox, QSizePolicy, QMessageBox, QInputDialog, QDialog, QCheckBox, QFrame
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QPixmap, QDoubleValidator, QRegularExpressionValidator

from common import *
from additional_inputs import AdditionalInputsWidget


class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()


def apply_field_style(widget):
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    widget.setMinimumHeight(28)
    
    if isinstance(widget, QComboBox):
        style = """
        QComboBox {
            padding: 4px 8px;
            padding-right: 30px;
            border: 1px solid #b0b0b0;
            border-radius: 3px;
            background-color: white;
            color: black;
            min-height: 24px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 18px;
            height: 18px;
            border: 1px solid #606060;
            border-radius: 9px;
            background-color: transparent;
            right: 5px;
        }
        QComboBox::drop-down:hover {
            background-color: #e0e0e0;
        }
        QComboBox::down-arrow {
            image: none;
            width: 0;
            height: 0;
            border-left: 3px solid transparent;
            border-right: 3px solid transparent;
            border-top: 4px solid #606060;
        }
        QComboBox:hover {
            border: 1px solid #909090;
        }
        QComboBox:focus {
            border: 1px solid #4a7ba7;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            border: 1px solid #b0b0b0;
            outline: none;
            selection-background-color: #e8f4ff;
        }
        QComboBox QAbstractItemView::item {
            color: black;
            background-color: white;
            padding: 5px;
            min-height: 24px;
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
            padding: 4px 8px;
            border: 1px solid #b0b0b0;
            border-radius: 3px;
            background-color: white;
            color: black;
            min-height: 24px;
        }
        QLineEdit:hover {
            border: 1px solid #909090;
        }
        QLineEdit:focus {
            border: 1px solid #4a7ba7;
        }
        QLineEdit:disabled {
            background-color: #f5f5f5;
            color: #999;
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


def create_group_box(title):
    """Create a styled group box"""
    group_box = QGroupBox(title)
    group_box.setStyleSheet("""
        QGroupBox {
            font-weight: bold;
            font-size: 11px;
            color: #333;
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
    return group_box


def create_form_row(label_text, widget, tooltip=None):
    """Create a horizontal layout with label and widget side by side"""
    row = QHBoxLayout()
    row.setSpacing(10)
    
    label = QLabel(label_text)
    label.setStyleSheet("font-size: 10px; color: #555; font-weight: normal;")
    label.setMinimumWidth(140)
    label.setMaximumWidth(140)
    
    if tooltip:
        widget.setToolTip(tooltip)
    
    row.addWidget(label)
    row.addWidget(widget, 1)
    
    return row


class InputDock(QWidget):
    def __init__(self, backend, parent):
        super().__init__()
        self.parent = parent
        self.backend = backend
        self.input_widget = None
        self.structure_type_combo = None
        self.project_location_combo = None
        self.custom_location_input = None
        self.footpath_combo = None
        self.additional_inputs_window = None

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
            if hasattr(self, 'structure_note'):
                self.structure_note.setVisible(True)
        else:
            if hasattr(self, 'structure_note'):
                self.structure_note.setVisible(False)
    
    def on_project_location_changed(self, text):
        """Handle project location combo box changes"""
        if text == "Custom":
            custom_location, ok = QInputDialog.getText(
                self,
                "Custom Location",
                "Enter city name for load calculations:",
                QLineEdit.Normal,
                ""
            )
            if ok and custom_location.strip():
                self.custom_location_input = custom_location.strip()
                QMessageBox.information(
                    self,
                    "Custom Location Set",
                    f"Custom location '{custom_location.strip()}' has been set.\n\n"
                    f"Note: Please ensure load calculation data is available for this location.",
                    QMessageBox.Ok
                )
                self.project_location_combo.addItem(custom_location.strip())
            elif ok:
                QMessageBox.warning(
                    self,
                    "No Location Entered",
                    "Please enter a valid city name or select from the dropdown.",
                    QMessageBox.Ok
                )
                if self.project_location_combo:
                    self.project_location_combo.setCurrentIndex(0)
        
    def show_project_location_dialog(self):
        """Show Project Location selection dialog"""
        state_districts = {
            "Select State": ["Select District"],
            "Delhi": ["Central Delhi", "East Delhi", "New Delhi", "North Delhi", "North East Delhi", 
                      "North West Delhi", "South Delhi", "South East Delhi", "South West Delhi", "West Delhi"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", 
                           "Amravati", "Kolhapur", "Raigad", "Satara", "Sangli"],
            "Karnataka": ["Bangalore", "Mysore", "Hubli", "Belgaum", "Mangalore", "Gulbarga", 
                         "Bellary", "Bijapur", "Shimoga", "Tumkur", "Davangere"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", 
                          "Tiruppur", "Erode", "Vellore", "Thoothukudi", "Dindigul"],
            "West Bengal": ["Kolkata", "Howrah", "Darjeeling", "Siliguri", "Asansol", "Durgapur", 
                           "Bardhaman", "Malda", "Jalpaiguri", "Murshidabad", "Nadia"]
        }
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Project Location")
        dialog.setMinimumWidth(850)
        dialog.setMinimumHeight(650)
        
        # Set white background for the entire dialog
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QCheckBox {
                color: black;
            }
            QLabel {
                color: black;
            }
        """)
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # === Enter Coordinates Row ===
        coords_row = QHBoxLayout()
        coords_row.setSpacing(15)
        
        self.coords_checkbox = QCheckBox("Enter Coordinates")
        self.coords_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px; 
                font-weight: normal;
                color: black;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #90AF13;
                border-color: #90AF13;
            }
            QCheckBox::indicator:hover {
                border-color: #7a9a12;
            }
        """)
        coords_row.addWidget(self.coords_checkbox)
        
        coords_row.addStretch()
        
        lat_label = QLabel("Latitude (°):")
        lat_label.setStyleSheet("font-size: 11px;")
        coords_row.addWidget(lat_label)
        
        self.latitude_input = QLineEdit()
        self.latitude_input.setMaximumWidth(120)
        self.latitude_input.setEnabled(False)
        apply_field_style(self.latitude_input)
        coords_row.addWidget(self.latitude_input)
        
        lng_label = QLabel("Longitude (°):")
        lng_label.setStyleSheet("font-size: 11px;")
        coords_row.addWidget(lng_label)
        
        self.longitude_input = QLineEdit()
        self.longitude_input.setMaximumWidth(120)
        self.longitude_input.setEnabled(False)
        apply_field_style(self.longitude_input)
        coords_row.addWidget(self.longitude_input)
        
        main_layout.addLayout(coords_row)
        
        # Separator line
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line1.setStyleSheet("background-color: #d0d0d0;")
        main_layout.addWidget(line1)
        
        # === Enter Location Name Row ===
        location_row = QHBoxLayout()
        location_row.setSpacing(15)
        
        self.location_checkbox = QCheckBox("Enter Location Name")
        self.location_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px; 
                font-weight: normal;
                color: black;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #90AF13;
                border-color: #90AF13;
            }
            QCheckBox::indicator:hover {
                border-color: #7a9a12;
            }
        """)
        location_row.addWidget(self.location_checkbox)
        
        location_row.addStretch()
        
        state_label = QLabel("State")
        state_label.setStyleSheet("font-size: 11px;")
        location_row.addWidget(state_label)
        
        self.state_combo = NoScrollComboBox()
        self.state_combo.setMaximumWidth(150)
        self.state_combo.setEnabled(False)
        self.state_combo.addItems(list(state_districts.keys()))
        apply_field_style(self.state_combo)
        location_row.addWidget(self.state_combo)
        
        district_label = QLabel("District")
        district_label.setStyleSheet("font-size: 11px;")
        location_row.addWidget(district_label)
        
        self.district_combo = NoScrollComboBox()
        self.district_combo.setMaximumWidth(150)
        self.district_combo.setEnabled(False)
        self.district_combo.addItems(["Select District"])
        apply_field_style(self.district_combo)
        location_row.addWidget(self.district_combo)
        
        main_layout.addLayout(location_row)
        
        # Separator line
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setStyleSheet("background-color: #d0d0d0;")
        main_layout.addWidget(line2)
        
        # === Select on Map Section ===
        map_section = QVBoxLayout()
        map_section.setSpacing(8)
        
        self.map_checkbox = QCheckBox("Select on Map")
        self.map_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px; 
                font-weight: normal;
                color: black;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #90AF13;
                border-color: #90AF13;
            }
            QCheckBox::indicator:hover {
                border-color: #7a9a12;
            }
        """)
        map_section.addWidget(self.map_checkbox)
        
        # Map placeholder
        self.map_placeholder = QLabel()
        self.map_placeholder.setStyleSheet("""
            QLabel {
                border: 1px solid #e0e0e0;
                background-color: white;
                padding: 20px;
                color: #999999;
            }
        """)
        self.map_placeholder.setAlignment(Qt.AlignCenter)
        self.map_placeholder.setMinimumHeight(200)
        self.map_placeholder.setText("Map Placeholder\n(Will be added later)")
        self.map_placeholder.setEnabled(False)  # Disabled by default
        map_section.addWidget(self.map_placeholder)
        
        main_layout.addLayout(map_section)
        
        # Separator line
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setFrameShadow(QFrame.Sunken)
        line3.setStyleSheet("background-color: #d0d0d0;")
        main_layout.addWidget(line3)
        
        # === IRC 6 (2017) Values Section ===
        results_section = QVBoxLayout()
        results_section.setSpacing(8)
        
        results_title = QLabel("IRC 6 (2017) Values:")
        results_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #4CAF50;")
        results_section.addWidget(results_title)
        
        self.wind_speed_label = QLabel("Basic Wind Speed (m/sec)")
        self.wind_speed_label.setStyleSheet("font-size: 11px; color: #4CAF50;")
        results_section.addWidget(self.wind_speed_label)
        
        self.seismic_zone_label = QLabel("Seismic Zone and Zone Factor")
        self.seismic_zone_label.setStyleSheet("font-size: 11px; color: #4CAF50;")
        results_section.addWidget(self.seismic_zone_label)
        
        self.temp_label = QLabel("Shade Air Temperature (°C)")
        self.temp_label.setStyleSheet("font-size: 11px; color: #4CAF50;")
        results_section.addWidget(self.temp_label)
        
        main_layout.addLayout(results_section)
        
        # Separator line
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setFrameShadow(QFrame.Sunken)
        line4.setStyleSheet("background-color: #d0d0d0;")
        main_layout.addWidget(line4)
        
        # === Custom Loading Parameters Checkbox ===
        self.custom_params_checkbox = QCheckBox("Tabulate Custom Loading Parameters")
        self.custom_params_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 11px;
                color: black;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #b0b0b0;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #90AF13;
                border-color: #90AF13;
            }
            QCheckBox::indicator:hover {
                border-color: #7a9a12;
            }
        """)
        main_layout.addWidget(self.custom_params_checkbox)
        
        main_layout.addStretch()
        
        # === Bottom Buttons ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(style_main_buttons())
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 6px 16px;
                min-height: 28px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(btn_layout)
        
        # Function to update districts based on selected state
        def on_state_changed(state_name):
            districts = state_districts.get(state_name, ["Select District"])
            self.district_combo.clear()
            self.district_combo.addItems(districts)
        
        # Function to handle map checkbox
        def on_map_checkbox_changed(state):
            enabled = (state == 2)
            self.map_placeholder.setEnabled(enabled)
            if enabled:
                self.map_placeholder.setStyleSheet("""
                    QLabel {
                        border: 2px solid #90AF13;
                        background-color: white;
                        padding: 20px;
                        color: #666666;
                    }
                """)
                self.map_placeholder.setText("Map Placeholder\n(Click to select location)\n(Will be implemented later)")
            else:
                self.map_placeholder.setStyleSheet("""
                    QLabel {
                        border: 1px solid #e0e0e0;
                        background-color: #f5f5f5;
                        padding: 20px;
                        color: #999999;
                    }
                """)
                self.map_placeholder.setText("Map Placeholder\n(Will be added later)")
        
        # Connect checkbox signals to enable/disable fields
        self.coords_checkbox.stateChanged.connect(lambda state: self.latitude_input.setEnabled(state == 2) or self.longitude_input.setEnabled(state == 2))
        self.location_checkbox.stateChanged.connect(lambda state: self.state_combo.setEnabled(state == 2) or self.district_combo.setEnabled(state == 2))
        self.map_checkbox.stateChanged.connect(on_map_checkbox_changed)
        
        # Connect state combo to update districts
        self.state_combo.currentTextChanged.connect(on_state_changed)
        
        if dialog.exec() == QDialog.Accepted:
            pass
    
    def build_left_panel(self, field_list):
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("background-color: white;")
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(15, 10, 15, 10)
        panel_layout.setSpacing(0)

        # Top Bar with buttons
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        top_bar.setContentsMargins(0, 0, 0, 15)
        
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
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 6px 16px;
                min-height: 28px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #909090;
            }
        """)
        additional_inputs_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        additional_inputs_btn.clicked.connect(self.show_additional_inputs)
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
        
        # === Type of Structure Section ===
        structure_group = create_group_box("Type of Structure")
        structure_layout = QVBoxLayout()
        structure_layout.setContentsMargins(10, 15, 10, 10)
        structure_layout.setSpacing(8)
        
        self.structure_type_combo = NoScrollComboBox()
        self.structure_type_combo.setObjectName(KEY_STRUCTURE_TYPE)
        apply_field_style(self.structure_type_combo)
        self.structure_type_combo.addItems(VALUES_STRUCTURE_TYPE)
        self.structure_type_combo.setToolTip("Defines the application of the steel girder bridge.\nCurrently only Highway Bridge is supported.")
        
        structure_row = create_form_row("Type of structure", self.structure_type_combo)
        structure_layout.addLayout(structure_row)
        
        self.structure_note = QLabel("*Other structures not included")
        self.structure_note.setStyleSheet("font-size: 9px; color: #d32f2f; font-style: italic; margin-left: 150px;")
        self.structure_note.setVisible(False)
        structure_layout.addWidget(self.structure_note)
        
        self.structure_type_combo.currentTextChanged.connect(self.on_structure_type_changed)
        
        structure_group.setLayout(structure_layout)
        group_container_layout.addWidget(structure_group)
        
        # === Project Location Section ===
        location_group = QGroupBox()
        location_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 0px;
                padding-top: 10px;
                background-color: #fafafa;
            }
        """)
        location_layout = QVBoxLayout()
        location_layout.setContentsMargins(10, 10, 10, 10)
        location_layout.setSpacing(0)
        
        self.project_location_combo = NoScrollComboBox()
        self.project_location_combo.setObjectName(KEY_PROJECT_LOCATION)
        self.project_location_combo.addItems(VALUES_PROJECT_LOCATION)
        self.project_location_combo.currentTextChanged.connect(self.on_project_location_changed)
        self.project_location_combo.hide()
        
        location_btn = QPushButton("Project Location")
        location_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px 12px;
                text-align: left;
                min-height: 28px;
                padding-right: 30px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #909090;
            }
            QPushButton::menu-indicator {
                image: none;
                width: 0px;
            }
        """)
        
        # Add dropdown arrow indicator
        location_btn_container = QWidget()
        location_btn_layout = QHBoxLayout(location_btn_container)
        location_btn_layout.setContentsMargins(0, 0, 0, 0)
        location_btn_layout.setSpacing(0)
        
        location_btn.clicked.connect(self.show_project_location_dialog)
        location_btn_layout.addWidget(location_btn)
        
        # Create arrow overlay
        arrow_label = QLabel("▼")
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setStyleSheet("""
            QLabel {
                color: #606060;
                font-size: 8px;
                background-color: transparent;
                border: 1px solid #606060;
                border-radius: 10px;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                margin-right: 8px;
            }
            QLabel:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # We don't need arrow_label.setFixedWidth(20) anymore
        location_btn_layout.addWidget(arrow_label)
        location_btn_layout.setAlignment(arrow_label, Qt.AlignRight | Qt.AlignVCenter)
        
        # Position arrow on top of button
        arrow_label.raise_()
        arrow_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        location_layout.addWidget(location_btn)
        
        location_group.setLayout(location_layout)
        group_container_layout.addWidget(location_group)
        
        # === Geometric Details Section ===
        geometric_group = create_group_box("Geometric Details")
        geometric_layout = QVBoxLayout()
        geometric_layout.setContentsMargins(10, 15, 10, 10)
        geometric_layout.setSpacing(8)
        
        # Span
        self.span_input = QLineEdit()
        self.span_input.setObjectName(KEY_SPAN)
        apply_field_style(self.span_input)
        self.span_input.setValidator(QDoubleValidator(SPAN_MIN, SPAN_MAX, 2))
        self.span_input.setPlaceholderText(f"{SPAN_MIN}-{SPAN_MAX} m")
        span_row = create_form_row("Span (m):", self.span_input, 
                                   f"Total length of the steel girder bridge.\nMust be between {SPAN_MIN} m and {SPAN_MAX} m")
        geometric_layout.addLayout(span_row)
        
        # Carriageway Width
        self.carriageway_input = QLineEdit()
        self.carriageway_input.setObjectName(KEY_CARRIAGEWAY_WIDTH)
        apply_field_style(self.carriageway_input)
        self.carriageway_input.setValidator(QDoubleValidator(CARRIAGEWAY_WIDTH_MIN, 100.0, 2))
        self.carriageway_input.setPlaceholderText(f"Min {CARRIAGEWAY_WIDTH_MIN} m")
        carriageway_row = create_form_row("Carriageway (m):", self.carriageway_input,
                                         f"Width of bridge deck surface from curb to curb.\nIRC 5 Clause 104.3.1 requires minimum {CARRIAGEWAY_WIDTH_MIN} m")
        geometric_layout.addLayout(carriageway_row)
        
        # Footpath
        self.footpath_combo = NoScrollComboBox()
        self.footpath_combo.setObjectName(KEY_FOOTPATH)
        apply_field_style(self.footpath_combo)
        self.footpath_combo.addItems(VALUES_FOOTPATH)
        self.footpath_combo.setCurrentIndex(0)
        footpath_row = create_form_row("Footpath:", self.footpath_combo,
                                      "Select footpath configuration.\nIRC 5 Clause 101.41: Safety kerb required when footpath is not present.")
        self.footpath_combo.currentTextChanged.connect(self.on_footpath_changed)
        geometric_layout.addLayout(footpath_row)
        
        # Skew Angle
        self.skew_input = QLineEdit()
        self.skew_input.setObjectName(KEY_SKEW_ANGLE)
        apply_field_style(self.skew_input)
        self.skew_input.setValidator(QDoubleValidator(SKEW_ANGLE_MIN, SKEW_ANGLE_MAX, 1))
        self.skew_input.setText(str(SKEW_ANGLE_DEFAULT))
        self.skew_input.setPlaceholderText(f"Default: {SKEW_ANGLE_DEFAULT}°")
        skew_row = create_form_row("Skew Angle (°):", self.skew_input,
                                  f"Skew angle of rolled beams or plate girders.\nIRC 24 (2010) requires detailed analysis when skew angle exceeds ±15°.\nRange: {SKEW_ANGLE_MIN}° to {SKEW_ANGLE_MAX}°")
        geometric_layout.addLayout(skew_row)
        
        geometric_group.setLayout(geometric_layout)
        group_container_layout.addWidget(geometric_group)
        
        # === Material Inputs Section ===
        material_group = create_group_box("Material Inputs")
        material_layout = QVBoxLayout()
        material_layout.setContentsMargins(10, 15, 10, 10)
        material_layout.setSpacing(8)
        
        # Girder
        self.girder_combo = NoScrollComboBox()
        self.girder_combo.setObjectName(KEY_GIRDER)
        apply_field_style(self.girder_combo)
        self.girder_combo.addItems(VALUES_MATERIAL)
        girder_row = create_form_row("Girder:", self.girder_combo)
        material_layout.addLayout(girder_row)
        
        # Cross Bracing
        self.cross_bracing_combo = NoScrollComboBox()
        self.cross_bracing_combo.setObjectName(KEY_CROSS_BRACING)
        apply_field_style(self.cross_bracing_combo)
        self.cross_bracing_combo.addItems(VALUES_MATERIAL)
        cross_bracing_row = create_form_row("Cross Bracing:", self.cross_bracing_combo)
        material_layout.addLayout(cross_bracing_row)
        
        # Deck
        self.deck_combo = NoScrollComboBox()
        self.deck_combo.setObjectName(KEY_DECK_CONCRETE_GRADE_BASIC)
        apply_field_style(self.deck_combo)
        self.deck_combo.addItems(VALUES_DECK_CONCRETE_GRADE)
        self.deck_combo.setCurrentText("M25")
        deck_row = create_form_row("Deck:", self.deck_combo,
                                  "Select concrete grade for bridge deck.\nMinimum M25 grade required for bridge deck construction.")
        material_layout.addLayout(deck_row)
        
        material_group.setLayout(material_layout)
        group_container_layout.addWidget(material_group)
        
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
    
    def show_additional_inputs(self):
        """Show Additional Inputs dialog"""
        footpath_value = self.footpath_combo.currentText() if self.footpath_combo else "None"
        
        carriageway_width = 7.5
        if self.input_widget:
            carriageway_field = self.input_widget.findChild(QLineEdit, KEY_CARRIAGEWAY_WIDTH)
            if carriageway_field and carriageway_field.text():
                try:
                    carriageway_width = float(carriageway_field.text())
                except ValueError:
                    carriageway_width = 7.5
        
        if self.additional_inputs_window is None or not self.additional_inputs_window.isVisible():
            self.additional_inputs_window = QDialog(self)
            self.additional_inputs_window.setWindowTitle("Additional Inputs - Manual Bridge Parameter Definition")
            self.additional_inputs_window.resize(900, 700)
            
            layout = QVBoxLayout(self.additional_inputs_window)
            layout.setContentsMargins(0, 0, 0, 0)
            
            self.additional_inputs_widget = AdditionalInputsWidget(footpath_value, carriageway_width, self.additional_inputs_window)
            layout.addWidget(self.additional_inputs_widget)
            
            self.additional_inputs_window.show()
        else:
            self.additional_inputs_window.raise_()
            self.additional_inputs_window.activateWindow()
    
    def on_footpath_changed(self, footpath_value):
        """Update additional inputs when footpath changes"""
        if self.additional_inputs_window and self.additional_inputs_window.isVisible():
            if hasattr(self, 'additional_inputs_widget'):
                self.additional_inputs_widget.update_footpath_value(footpath_value)