"""
Additional Inputs Widget for Highway Bridge Design
Provides detailed input fields for manual bridge parameter definition
"""
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit,
    QComboBox, QGroupBox, QFormLayout, QPushButton, QScrollArea,
    QCheckBox, QMessageBox, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator

from common import *


class OptimizableField(QWidget):
    """Widget that allows selection between Optimized/Customized/All modes with input field"""
    
    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Mode selector
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(VALUES_OPTIMIZATION_MODE)
        self.mode_combo.setMaximumWidth(120)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setEnabled(False)  # Disabled by default for "Optimized"
        
        self.layout.addWidget(self.mode_combo)
        self.layout.addWidget(self.input_field)
        
        # Connect signal
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
    
    def on_mode_changed(self, text):
        """Enable/disable input field based on selection"""
        if text == "Optimized":
            self.input_field.setEnabled(False)
            self.input_field.clear()
        else:
            self.input_field.setEnabled(True)
    
    def get_value(self):
        """Returns tuple of (mode, value)"""
        return (self.mode_combo.currentText(), self.input_field.text())


class BridgeGeometryTab(QWidget):
    """Sub-tab for Bridge Geometry inputs"""
    
    footpath_changed = Signal(str)  # Signal when footpath status changes
    
    def __init__(self, footpath_value="None", parent=None):
        super().__init__(parent)
        self.footpath_value = footpath_value
        self.init_ui()
    
    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        field.setMinimumHeight(28)
        if isinstance(field, QComboBox):
            field.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 20px;
                    border-left: 1px solid #c0c0c0;
                    background-color: #e8e8e8;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid #606060;
                    margin-right: 5px;
                }
                QComboBox:focus {
                    border: 1px solid #4a7ba7;
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
            """)
        else:
            field.setStyleSheet("""
                QLineEdit {
                    padding: 4px 8px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
                }
                QLineEdit:focus {
                    border: 1px solid #4a7ba7;
                }
                QLineEdit:disabled {
                    background-color: #f0f0f0;
                    color: #999;
                }
            """)
    
    def style_group_box(self, group_box):
        """Apply consistent styling to group boxes"""
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #d0d0d0;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: #f9f9f9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                background-color: white;
                color: #4a7ba7;
            }
        """)
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Main horizontal split: Diagram (left) and Inputs (right)
        content_layout = QHBoxLayout()
        
        # LEFT SIDE: Diagram
        diagram_widget = QWidget()
        diagram_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #d0d0d0;
                border-radius: 4px;
            }
        """)
        diagram_widget.setMinimumWidth(450)
        diagram_widget.setMaximumWidth(500)
        diagram_layout = QVBoxLayout(diagram_widget)
        diagram_layout.setContentsMargins(10, 10, 10, 10)
        
        # Diagram image placeholder
        diagram_label = QLabel()
        diagram_label.setText("Bridge Geometry Diagram\n(Placeholder)")
        diagram_label.setAlignment(Qt.AlignCenter)
        diagram_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                border: 1px dashed #999;
                padding: 20px;
                font-size: 12px;
                color: #666;
                min-height: 300px;
            }
        """)
        diagram_layout.addWidget(diagram_label)
        
        content_layout.addWidget(diagram_widget)
        
        # RIGHT SIDE: Input Fields with Scroll
        input_scroll = QScrollArea()
        input_scroll.setWidgetResizable(True)
        input_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        input_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)
        
        input_container = QWidget()
        input_container.setStyleSheet("background-color: white; color: #000000;")
        inputs_layout = QVBoxLayout(input_container)
        inputs_layout.setContentsMargins(15, 10, 15, 10)
        inputs_layout.setSpacing(12)
        
        # GROUP 1: Girder Spacing, No. of Girders, Deck Overhang Width
        girder_group = QGroupBox("")
        self.style_group_box(girder_group)
        girder_layout = QFormLayout(girder_group)
        girder_layout.setSpacing(8)
        girder_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.girder_spacing = QLineEdit()
        self.girder_spacing.setValidator(QDoubleValidator(0.0, 10.0, 2))
        self.girder_spacing.setPlaceholderText("Enter spacing in meters")
        self.style_input_field(self.girder_spacing)
        girder_layout.addRow("Girder Spacing (m):", self.girder_spacing)
        
        self.no_of_girders = QLineEdit()
        self.no_of_girders.setEnabled(False)
        self.no_of_girders.setPlaceholderText("Auto-calculated")
        self.style_input_field(self.no_of_girders)
        girder_layout.addRow("No. of Girders:", self.no_of_girders)
        
        self.deck_overhang = QLineEdit()
        self.deck_overhang.setValidator(QDoubleValidator(0.0, 5.0, 2))
        self.deck_overhang.setPlaceholderText("Enter overhang width")
        self.style_input_field(self.deck_overhang)
        girder_layout.addRow("Deck Overhang Width (m):", self.deck_overhang)
        
        inputs_layout.addWidget(girder_group)
        
        # GROUP 2: Deck Thickness
        deck_group = QGroupBox("")
        self.style_group_box(deck_group)
        deck_layout = QFormLayout(deck_group)
        deck_layout.setSpacing(8)
        deck_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.deck_thickness = QLineEdit()
        self.deck_thickness.setValidator(QDoubleValidator(0.0, 500.0, 0))
        self.deck_thickness.setPlaceholderText("Enter thickness in mm")
        self.style_input_field(self.deck_thickness)
        deck_layout.addRow("Deck Thickness (mm):", self.deck_thickness)
        
        inputs_layout.addWidget(deck_group)
        
        # GROUP 3: Footpath Width and Thickness
        self.footpath_group = QGroupBox("")
        self.style_group_box(self.footpath_group)
        self.footpath_group.setVisible(self.footpath_value != "None")
        footpath_layout = QFormLayout(self.footpath_group)
        footpath_layout.setSpacing(8)
        footpath_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.footpath_width = QLineEdit()
        self.footpath_width.setValidator(QDoubleValidator(0.0, 5.0, 2))
        self.footpath_width.setPlaceholderText("Enter width in meters")
        self.style_input_field(self.footpath_width)
        footpath_layout.addRow("Footpath Width (m):", self.footpath_width)
        
        self.footpath_thickness = QLineEdit()
        self.footpath_thickness.setValidator(QDoubleValidator(0.0, 500.0, 0))
        self.footpath_thickness.setPlaceholderText("Auto-fills from deck thickness")
        self.style_input_field(self.footpath_thickness)
        footpath_layout.addRow("Footpath Thickness (mm):", self.footpath_thickness)
        
        inputs_layout.addWidget(self.footpath_group)
        
        # GROUP 4: Crash Barrier Details, Railing Details, Safety Kerb (Combined)
        combined_group = QGroupBox("")
        self.style_group_box(combined_group)
        combined_layout = QVBoxLayout(combined_group)
        combined_layout.setSpacing(10)
        
        # Crash Barrier Details Section
        crash_barrier_label = QLabel("Crash Barrier Details:")
        crash_barrier_label.setStyleSheet("font-weight: bold; font-size: 11px; margin-bottom: 5px; color: #4a7ba7;")
        combined_layout.addWidget(crash_barrier_label)
        
        crash_form = QFormLayout()
        crash_form.setSpacing(8)
        crash_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.crash_barrier_type = QComboBox()
        self.style_input_field(self.crash_barrier_type)
        self.crash_barrier_type.addItems(VALUES_CRASH_BARRIER_TYPE)
        self.crash_barrier_type.currentTextChanged.connect(self.on_crash_barrier_type_changed)
        crash_form.addRow("Type:", self.crash_barrier_type)
        
        self.crash_barrier_density = QLineEdit()
        self.style_input_field(self.crash_barrier_density)
        self.crash_barrier_density.setPlaceholderText("Material density")
        self.crash_barrier_density.setValidator(QDoubleValidator(0.0, 100.0, 2))
        crash_form.addRow("Material Density (MPa):", self.crash_barrier_density)
        
        self.crash_barrier_width = QLineEdit()
        self.style_input_field(self.crash_barrier_width)
        self.crash_barrier_width.setPlaceholderText("Barrier width")
        self.crash_barrier_width.setValidator(QDoubleValidator(0.0, 2.0, 3))
        crash_form.addRow("Width (m):", self.crash_barrier_width)
        
        self.crash_barrier_area = QLineEdit()
        self.style_input_field(self.crash_barrier_area)
        self.crash_barrier_area.setPlaceholderText("Cross-sectional area")
        self.crash_barrier_area.setValidator(QDoubleValidator(0.0, 10.0, 4))
        crash_form.addRow("Area (m²):", self.crash_barrier_area)
        
        combined_layout.addLayout(crash_form)
        
        # Railing Details Section
        railing_label = QLabel("Railing Details:")
        railing_label.setStyleSheet("font-weight: bold; font-size: 11px; margin-top: 10px; margin-bottom: 5px; color: #4a7ba7;")
        combined_layout.addWidget(railing_label)
        
        railing_form = QFormLayout()
        railing_form.setSpacing(8)
        railing_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.railing_width = QLineEdit()
        self.railing_width.setValidator(QDoubleValidator(0.0, 1000.0, 0))
        self.railing_width.setPlaceholderText("Enter width in mm")
        self.style_input_field(self.railing_width)
        railing_form.addRow("Width (m):", self.railing_width)
        
        self.railing_height = QLineEdit()
        self.railing_height.setValidator(QDoubleValidator(0.0, 3000.0, 0))
        self.railing_height.setPlaceholderText("Enter height in mm")
        self.style_input_field(self.railing_height)
        railing_form.addRow("Height (m):", self.railing_height)
        
        combined_layout.addLayout(railing_form)
        
        # Safety Kerb Section (conditional)
        self.safety_kerb_container = QWidget()
        self.safety_kerb_container.setVisible(self.footpath_value == "None")
        safety_kerb_layout = QVBoxLayout(self.safety_kerb_container)
        safety_kerb_layout.setContentsMargins(0, 0, 0, 0)
        safety_kerb_layout.setSpacing(5)
        
        safety_kerb_label = QLabel("Safety Kerb:")
        safety_kerb_label.setStyleSheet("font-weight: bold; font-size: 11px; margin-top: 10px; margin-bottom: 5px; color: #4a7ba7;")
        safety_kerb_layout.addWidget(safety_kerb_label)
        
        safety_kerb_form = QFormLayout()
        safety_kerb_form.setSpacing(8)
        safety_kerb_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.safety_kerb_width = QLineEdit()
        self.style_input_field(self.safety_kerb_width)
        self.safety_kerb_width.setPlaceholderText("Min 750mm if no footpath")
        self.safety_kerb_width.setValidator(QDoubleValidator(0.0, 2.0, 3))
        safety_kerb_form.addRow("Width (m):", self.safety_kerb_width)
        
        self.safety_kerb_thickness = QLineEdit()
        self.style_input_field(self.safety_kerb_thickness)
        self.safety_kerb_thickness.setPlaceholderText("Enter thickness in mm")
        self.safety_kerb_thickness.setValidator(QDoubleValidator(0.0, 500.0, 0))
        safety_kerb_form.addRow("Thickness (mm):", self.safety_kerb_thickness)
        
        safety_kerb_layout.addLayout(safety_kerb_form)
        combined_layout.addWidget(self.safety_kerb_container)
        
        inputs_layout.addWidget(combined_group)
        
        inputs_layout.addStretch()
        
        input_scroll.setWidget(input_container)
        content_layout.addWidget(input_scroll, 1)
        
        main_layout.addLayout(content_layout)
        
        # Connect calculation signals
        self.girder_spacing.textChanged.connect(self.calculate_no_of_girders)
        self.deck_overhang.textChanged.connect(self.calculate_no_of_girders)
        self.deck_thickness.textChanged.connect(self.update_footpath_thickness)
    
    def update_footpath_value(self, footpath_value):
        """Update visibility based on footpath selection"""
        self.footpath_value = footpath_value
        self.footpath_group.setVisible(footpath_value != "None")
        self.safety_kerb_container.setVisible(footpath_value == "None")
        self.footpath_changed.emit(footpath_value)
    
    def calculate_no_of_girders(self):
        """Calculate number of girders based on spacing and overhang"""
        # This would need bridge width from main inputs
        # Placeholder calculation
        try:
            spacing = float(self.girder_spacing.text()) if self.girder_spacing.text() else 0
            overhang = float(self.deck_overhang.text()) if self.deck_overhang.text() else 0
            if spacing > 0:
                # Placeholder: assume bridge width of 10m for demo
                bridge_width = 10.0
                no_girders = int((bridge_width - 2 * overhang) / spacing) + 1
                self.no_of_girders.setText(str(no_girders))
        except:
            pass
    
    def update_footpath_thickness(self):
        """Pre-fill footpath thickness with deck thickness"""
        if self.deck_thickness.text() and not self.footpath_thickness.text():
            self.footpath_thickness.setText(self.deck_thickness.text())
    
    def on_crash_barrier_type_changed(self, barrier_type):
        """Warn if flexible/semi-rigid barrier without footpath"""
        if (barrier_type in ["Flexible", "Semi-Rigid"]) and (self.footpath_value == "None"):
            QMessageBox.warning(
                self,
                "Crash Barrier Type Not Permitted",
                f"{barrier_type} crash barriers are not permitted on bridges without an outer footpath per IRC 5 Clause 109.6.4.",
                QMessageBox.Ok
            )


class AdditionalInputsWidget(QWidget):
    """Main widget for Additional Inputs with tabbed interface"""
    
    def __init__(self, footpath_value="None", parent=None):
        super().__init__(parent)
        self.footpath_value = footpath_value
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("Additional Inputs")
        title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(title)
        
        # Main tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                color: black;
                border: 1px solid #d0d0d0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #A2EBB6;
                color: black;
                border-bottom-color: white;
            }
        """)
        
        # Sub-Tab 1: Bridge Geometry
        self.bridge_geometry_tab = BridgeGeometryTab(self.footpath_value)
        self.tabs.addTab(self.bridge_geometry_tab, "Bridge Geometry")
        
        # Sub-Tab 2: Section Properties
        section_props_tab = self.create_placeholder_tab(
            "Section Properties",
            "This tab will contain:\n\n" +
            "• Girder Details (IS Standard Rolled Beam / Plate Girder)\n" +
            "• Stiffener Details\n" +
            "• Cross-Bracing Details\n" +
            "• End Diaphragm Details\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(section_props_tab, "Section Properties")
        
        # Sub-Tab 3: Dead Load Inputs
        dead_load_tab = self.create_placeholder_tab(
            "Dead Load Inputs",
            "This tab will contain:\n\n" +
            "• Self Weight (with factor)\n" +
            "• Superimposed Load (Wearing Coat)\n" +
            "• Load from Railing\n" +
            "• Load from Crash Barrier\n" +
            "• Additional Superimposed Load (Pressure/Line/Point)\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(dead_load_tab, "Dead Load Inputs")
        
        # Sub-Tab 4: Live Load Inputs
        live_load_tab = self.create_placeholder_tab(
            "Live Load Inputs",
            "This tab will contain:\n\n" +
            "• Standard IRC Vehicles (Class A, 70R, AA, SV)\n" +
            "• Custom Vehicle Configuration\n" +
            "• Footpath Pressure (Automatic/User-defined)\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(live_load_tab, "Live Load Inputs")
        
        # Sub-Tab 5: Lateral Load
        lateral_load_tab = self.create_placeholder_tab(
            "Lateral Load",
            "Lateral load definition is under development.\n\n" +
            "This will include wind loads, seismic loads, and other\n" +
            "lateral forces acting on the bridge structure."
        )
        self.tabs.addTab(lateral_load_tab, "Lateral Load")
        
        # Sub-Tab 6: Support Conditions
        support_tab = self.create_placeholder_tab(
            "Support Conditions",
            "This tab will contain:\n\n" +
            "• Left Support (Fixed/Pinned)\n" +
            "• Right Support (Fixed/Pinned)\n" +
            "• Bearing Length (mm)\n\n" +
            "Note: If bearing length is 0, the end bearing\n" +
            "stiffener will not be designed.\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(support_tab, "Support Conditions")
        
        main_layout.addWidget(self.tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setMaximumWidth(100)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        main_layout.addLayout(btn_layout)
    
    def create_placeholder_tab(self, title, description):
        """Create a styled placeholder tab with title and description"""
        widget = QWidget()
        widget.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Icon or visual indicator
        icon_label = QLabel("🚧")
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Status
        status_label = QLabel("Under Development")
        status_label.setStyleSheet("""
            font-size: 14px;
            color: #f39c12;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-size: 12px;
            color: #666;
            line-height: 1.6;
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setMaximumWidth(600)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        return widget
    
    def update_footpath_value(self, footpath_value):
        """Update footpath value across all tabs"""
        self.footpath_value = footpath_value
        self.bridge_geometry_tab.update_footpath_value(footpath_value)
