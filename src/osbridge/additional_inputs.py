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
    
    def __init__(self, footpath_value="None", carriageway_width=7.5, parent=None):
        super().__init__(parent)
        self.footpath_value = footpath_value
        self.carriageway_width = carriageway_width
        self.updating_fields = False  # Flag to prevent circular updates
        self.init_ui()
    
    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        field.setMinimumHeight(28)
        if isinstance(field, QComboBox):
            field.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    padding-right: 30px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
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
        self.girder_spacing.setValidator(QDoubleValidator(0.01, 50.0, 3))
        self.girder_spacing.setText(str(DEFAULT_GIRDER_SPACING))
        self.girder_spacing.setPlaceholderText(f"Default: {DEFAULT_GIRDER_SPACING} m")
        self.style_input_field(self.girder_spacing)
        self.girder_spacing.textChanged.connect(self.on_girder_spacing_changed)
        girder_layout.addRow("Girder Spacing (m):", self.girder_spacing)
        
        self.no_of_girders = QLineEdit()
        self.no_of_girders.setValidator(QIntValidator(2, 100))
        self.no_of_girders.setPlaceholderText("Auto-calculated integer")
        self.style_input_field(self.no_of_girders)
        self.no_of_girders.textChanged.connect(self.on_no_of_girders_changed)
        girder_layout.addRow("No. of Girders:", self.no_of_girders)
        
        self.deck_overhang = QLineEdit()
        self.deck_overhang.setValidator(QDoubleValidator(0.0, 10.0, 3))
        self.deck_overhang.setText(str(DEFAULT_DECK_OVERHANG))
        self.deck_overhang.setPlaceholderText(f"Default: {DEFAULT_DECK_OVERHANG} m")
        self.style_input_field(self.deck_overhang)
        self.deck_overhang.textChanged.connect(self.on_deck_overhang_changed)
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
        self.footpath_width.setValidator(QDoubleValidator(MIN_FOOTPATH_WIDTH, 5.0, 3))
        self.footpath_width.setPlaceholderText(f"Min: {MIN_FOOTPATH_WIDTH} m (IRC 5 Clause 104.3.6)")
        self.style_input_field(self.footpath_width)
        self.footpath_width.textChanged.connect(self.on_footpath_width_changed)
        self.footpath_width.editingFinished.connect(self.validate_footpath_width)
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
        self.crash_barrier_width.setText(str(DEFAULT_CRASH_BARRIER_WIDTH))
        self.crash_barrier_width.setPlaceholderText(f"Default: {DEFAULT_CRASH_BARRIER_WIDTH} m")
        self.crash_barrier_width.setValidator(QDoubleValidator(0.0, 2.0, 3))
        self.crash_barrier_width.textChanged.connect(self.recalculate_girders)
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
        self.railing_width.setValidator(QDoubleValidator(0.0, 1.0, 3))
        self.railing_width.setText(str(DEFAULT_RAILING_WIDTH))
        self.railing_width.setPlaceholderText(f"Default: {DEFAULT_RAILING_WIDTH} m")
        self.style_input_field(self.railing_width)
        self.railing_width.textChanged.connect(self.recalculate_girders)
        railing_form.addRow("Width (m):", self.railing_width)
        
        self.railing_height = QLineEdit()
        self.railing_height.setValidator(QDoubleValidator(MIN_RAILING_HEIGHT, 3.0, 3))
        self.railing_height.setPlaceholderText(f"Min: {MIN_RAILING_HEIGHT} m (IRC 5 Clauses 109.7.2.3 & 109.7.2.4)")
        self.style_input_field(self.railing_height)
        self.railing_height.editingFinished.connect(self.validate_railing_height)
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
        self.safety_kerb_width.setValidator(QDoubleValidator(MIN_SAFETY_KERB_WIDTH, 2.0, 3))
        self.safety_kerb_width.setPlaceholderText(f"Min: {MIN_SAFETY_KERB_WIDTH} m (IRC 5 Clause 101.41)")
        self.safety_kerb_width.editingFinished.connect(self.validate_safety_kerb_width)
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
        
        # Connect deck thickness to footpath thickness
        self.deck_thickness.textChanged.connect(self.update_footpath_thickness)
        
        # Initialize calculations with default values
        self.recalculate_girders()
    
    def update_footpath_value(self, footpath_value):
        """Update visibility based on footpath selection"""
        self.footpath_value = footpath_value
        self.footpath_group.setVisible(footpath_value != "None")
        self.safety_kerb_container.setVisible(footpath_value == "None")
        self.recalculate_girders()  # Recalculate when footpath changes
        self.footpath_changed.emit(footpath_value)
    
    def get_overall_bridge_width(self):
        """Calculate Overall Bridge Width = Carriageway + Footpath + Crash Barrier/Railing"""
        try:
            overall_width = self.carriageway_width
            
            # Add footpath width
            if self.footpath_value != "None":
                footpath_width = float(self.footpath_width.text()) if self.footpath_width.text() else 0
                # Count footpaths: "Single Sided" = 1, "Both" = 2
                num_footpaths = 2 if self.footpath_value == "Both" else (1 if self.footpath_value == "Single Sided" else 0)
                overall_width += footpath_width * num_footpaths
            
            # Add crash barrier width
            crash_barrier_width = float(self.crash_barrier_width.text()) if self.crash_barrier_width.text() else DEFAULT_CRASH_BARRIER_WIDTH
            # Assuming crash barriers on both edges
            overall_width += crash_barrier_width * 2
            
            # Add railing width (if footpath present)
            if self.footpath_value != "None":
                railing_width = float(self.railing_width.text()) if self.railing_width.text() else DEFAULT_RAILING_WIDTH
                # Railings on both sides if footpath exists
                overall_width += railing_width * 2
            
            return overall_width
        except:
            return self.carriageway_width
    
    def recalculate_girders(self):
        """Recalculate based on the formula: (Overall Bridge Width - Deck Overhang) / Girder Spacing = No. of Girders"""
        if self.updating_fields:
            return
        
        try:
            overall_width = self.get_overall_bridge_width()
            spacing = float(self.girder_spacing.text()) if self.girder_spacing.text() else DEFAULT_GIRDER_SPACING
            overhang = float(self.deck_overhang.text()) if self.deck_overhang.text() else DEFAULT_DECK_OVERHANG
            
            # Validate: spacing and overhang should be less than overall bridge width
            if spacing >= overall_width or overhang >= overall_width:
                self.no_of_girders.setText("")
                return
            
            # Calculate: No. of Girders = (Overall Width - 2*Overhang) / Spacing + 1
            if spacing > 0:
                no_girders = int(round((overall_width - 2 * overhang) / spacing)) + 1
                if no_girders >= 2:
                    self.updating_fields = True
                    self.no_of_girders.setText(str(no_girders))
                    self.updating_fields = False
        except:
            pass
    
    def on_girder_spacing_changed(self):
        """When user changes girder spacing, recalculate number of girders"""
        if not self.updating_fields:
            try:
                overall_width = self.get_overall_bridge_width()
                spacing_text = self.girder_spacing.text()
                if spacing_text:
                    spacing = float(spacing_text)
                    if spacing >= overall_width:
                        QMessageBox.warning(self, "Invalid Girder Spacing", 
                            f"Girder spacing ({spacing:.2f} m) must be less than overall bridge width ({overall_width:.2f} m).")
                        return
                self.recalculate_girders()
            except:
                pass
    
    def on_deck_overhang_changed(self):
        """When user changes deck overhang, recalculate number of girders"""
        if not self.updating_fields:
            try:
                overall_width = self.get_overall_bridge_width()
                overhang_text = self.deck_overhang.text()
                if overhang_text:
                    overhang = float(overhang_text)
                    if overhang >= overall_width:
                        QMessageBox.warning(self, "Invalid Deck Overhang", 
                            f"Deck overhang ({overhang:.2f} m) must be less than overall bridge width ({overall_width:.2f} m).")
                        return
                self.recalculate_girders()
            except:
                pass
    
    def on_no_of_girders_changed(self):
        """When user changes number of girders, recalculate girder spacing"""
        if not self.updating_fields:
            try:
                no_girders_text = self.no_of_girders.text()
                if no_girders_text:
                    no_girders = int(no_girders_text)
                    if no_girders < 2:
                        QMessageBox.warning(self, "Invalid Number of Girders", 
                            "Number of girders must be at least 2.")
                        return
                    
                    overall_width = self.get_overall_bridge_width()
                    overhang = float(self.deck_overhang.text()) if self.deck_overhang.text() else DEFAULT_DECK_OVERHANG
                    
                    # Calculate spacing: Spacing = (Overall Width - 2*Overhang) / (No. of Girders - 1)
                    if no_girders > 1:
                        new_spacing = (overall_width - 2 * overhang) / (no_girders - 1)
                        self.updating_fields = True
                        self.girder_spacing.setText(f"{new_spacing:.3f}")
                        self.updating_fields = False
            except:
                pass
    
    def on_footpath_width_changed(self):
        """When footpath width changes, recalculate girders"""
        if not self.updating_fields:
            self.recalculate_girders()
    
    def validate_footpath_width(self):
        """Validate footpath width meets minimum IRC 5 requirements"""
        try:
            if self.footpath_width.text():
                width = float(self.footpath_width.text())
                if width < MIN_FOOTPATH_WIDTH:
                    QMessageBox.critical(self, "Footpath Width Error", 
                        f"Footpath width must be at least {MIN_FOOTPATH_WIDTH} m as per IRC 5 Clause 104.3.6.")
        except:
            pass
    
    def validate_railing_height(self):
        """Validate railing height meets minimum IRC 5 requirements"""
        try:
            if self.railing_height.text():
                height = float(self.railing_height.text())
                if height < MIN_RAILING_HEIGHT:
                    QMessageBox.critical(self, "Railing Height Error", 
                        f"Railing height must be at least {MIN_RAILING_HEIGHT} m as per IRC 5 Clauses 109.7.2.3 and 109.7.2.4.")
        except:
            pass
    
    def validate_safety_kerb_width(self):
        """Validate safety kerb width meets minimum IRC 5 requirements"""
        try:
            if self.safety_kerb_width.text():
                width = float(self.safety_kerb_width.text())
                if width < MIN_SAFETY_KERB_WIDTH:
                    QMessageBox.critical(self, "Safety Kerb Width Error", 
                        f"Safety kerb width must be at least {MIN_SAFETY_KERB_WIDTH} m (750 mm) as per IRC 5 Clause 101.41.")
        except:
            pass
    
    def update_footpath_thickness(self):
        """Pre-fill footpath thickness with deck thickness"""
        if self.deck_thickness.text() and not self.footpath_thickness.text():
            self.footpath_thickness.setText(self.deck_thickness.text())
    
    def on_crash_barrier_type_changed(self, barrier_type):
        """Warn if flexible/semi-rigid barrier without footpath"""
        if (barrier_type in ["Flexible", "Semi-Rigid"]) and (self.footpath_value == "None"):
            QMessageBox.critical(self, "Crash Barrier Type Not Permitted", 
                f"{barrier_type} crash barriers are not permitted on bridges without an outer footpath per IRC 5 Clause 109.6.4.")


class SectionPropertiesTab(QWidget):
    """Sub-tab for Section Properties with nested tabs for Girder, Stiffener, Cross-Bracing, and End Diaphragm"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create nested tab widget for different section types
        self.section_tabs = QTabWidget()
        self.section_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                color: black;
                border: 1px solid #d0d0d0;
                padding: 6px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #A2EBB6;
                color: black;
                font-weight: bold;
            }
        """)
        
        # Add nested tabs
        self.girder_tab = GirderDetailsTab()
        self.section_tabs.addTab(self.girder_tab, "Girder Details")
        
        self.stiffener_tab = StiffenerDetailsTab()
        self.section_tabs.addTab(self.stiffener_tab, "Stiffener Details")
        
        self.cross_bracing_tab = CrossBracingDetailsTab()
        self.section_tabs.addTab(self.cross_bracing_tab, "Cross-Bracing Details")
        
        self.end_diaphragm_tab = EndDiaphragmDetailsTab()
        self.section_tabs.addTab(self.end_diaphragm_tab, "End Diaphragm Details")
        
        main_layout.addWidget(self.section_tabs)


class GirderDetailsTab(QWidget):
    """Tab for Girder Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Girder Type Selection
        type_group = QGroupBox("Girder Type")
        type_group.setStyleSheet(self.get_group_style())
        type_layout = QVBoxLayout()
        
        type_row = QHBoxLayout()
        type_label = QLabel("Girder Type:")
        type_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.girder_type_combo = QComboBox()
        self.girder_type_combo.addItems(VALUES_GIRDER_TYPE)
        self.style_input_field(self.girder_type_combo)
        type_row.addWidget(type_label)
        type_row.addWidget(self.girder_type_combo)
        type_row.addStretch()
        type_layout.addLayout(type_row)
        
        type_group.setLayout(type_layout)
        scroll_layout.addWidget(type_group)
        
        # IS Rolled Beam Section (visible when IS Standard Rolled Beam is selected)
        self.is_beam_group = QGroupBox("IS Standard Rolled Beam Section")
        self.is_beam_group.setStyleSheet(self.get_group_style())
        is_beam_layout = QVBoxLayout()
        
        is_beam_row = QHBoxLayout()
        is_beam_label = QLabel("Select IS Beam Section:")
        is_beam_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.is_beam_combo = QComboBox()
        # Add sample IS sections - you can expand this list
        self.is_beam_combo.addItems([
            "Select Section",
            "ISMB 100", "ISMB 125", "ISMB 150", "ISMB 175", "ISMB 200",
            "ISMB 225", "ISMB 250", "ISMB 300", "ISMB 350", "ISMB 400",
            "ISMB 450", "ISMB 500", "ISMB 550", "ISMB 600",
            "ISWB 150", "ISWB 175", "ISWB 200", "ISWB 225", "ISWB 250",
            "ISWB 300", "ISWB 350", "ISWB 400", "ISWB 450", "ISWB 500", "ISWB 550", "ISWB 600"
        ])
        self.style_input_field(self.is_beam_combo)
        is_beam_row.addWidget(is_beam_label)
        is_beam_row.addWidget(self.is_beam_combo)
        is_beam_row.addStretch()
        is_beam_layout.addLayout(is_beam_row)
        
        self.is_beam_group.setLayout(is_beam_layout)
        scroll_layout.addWidget(self.is_beam_group)
        
        # Plate Girder Section (visible when Plate Girder is selected)
        self.plate_girder_group = QGroupBox("Plate Girder Details")
        self.plate_girder_group.setStyleSheet(self.get_group_style())
        plate_layout = QVBoxLayout()
        
        # Girder Symmetry
        symmetry_row = QHBoxLayout()
        symmetry_label = QLabel("Girder Symmetry:")
        symmetry_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.symmetry_combo = QComboBox()
        self.symmetry_combo.addItems(VALUES_GIRDER_SYMMETRY)
        self.style_input_field(self.symmetry_combo)
        symmetry_row.addWidget(symmetry_label)
        symmetry_row.addWidget(self.symmetry_combo)
        symmetry_row.addStretch()
        plate_layout.addLayout(symmetry_row)
        
        # Top Flange Width
        top_width_row = QHBoxLayout()
        top_width_label = QLabel("Top Flange Width (mm):")
        top_width_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.top_width_field = OptimizableField("Top Flange Width")
        self.style_input_field(self.top_width_field.mode_combo)
        self.style_input_field(self.top_width_field.input_field)
        top_width_row.addWidget(top_width_label)
        top_width_row.addWidget(self.top_width_field)
        top_width_row.addStretch()
        plate_layout.addLayout(top_width_row)
        
        # Top Flange Thickness
        top_thick_row = QHBoxLayout()
        top_thick_label = QLabel("Top Flange Thickness (mm):")
        top_thick_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.top_thick_field = OptimizableField("Top Flange Thickness")
        self.style_input_field(self.top_thick_field.mode_combo)
        self.style_input_field(self.top_thick_field.input_field)
        top_thick_row.addWidget(top_thick_label)
        top_thick_row.addWidget(self.top_thick_field)
        top_thick_row.addStretch()
        plate_layout.addLayout(top_thick_row)
        
        # Bottom Flange Width
        bottom_width_row = QHBoxLayout()
        bottom_width_label = QLabel("Bottom Flange Width (mm):")
        bottom_width_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.bottom_width_field = OptimizableField("Bottom Flange Width")
        self.style_input_field(self.bottom_width_field.mode_combo)
        self.style_input_field(self.bottom_width_field.input_field)
        bottom_width_row.addWidget(bottom_width_label)
        bottom_width_row.addWidget(self.bottom_width_field)
        bottom_width_row.addStretch()
        plate_layout.addLayout(bottom_width_row)
        
        # Bottom Flange Thickness
        bottom_thick_row = QHBoxLayout()
        bottom_thick_label = QLabel("Bottom Flange Thickness (mm):")
        bottom_thick_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.bottom_thick_field = OptimizableField("Bottom Flange Thickness")
        self.style_input_field(self.bottom_thick_field.mode_combo)
        self.style_input_field(self.bottom_thick_field.input_field)
        bottom_thick_row.addWidget(bottom_thick_label)
        bottom_thick_row.addWidget(self.bottom_thick_field)
        bottom_thick_row.addStretch()
        plate_layout.addLayout(bottom_thick_row)
        
        # Depth of Section
        depth_row = QHBoxLayout()
        depth_label = QLabel("Depth of Section (mm):")
        depth_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.depth_field = OptimizableField("Depth of Section")
        self.style_input_field(self.depth_field.mode_combo)
        self.style_input_field(self.depth_field.input_field)
        depth_row.addWidget(depth_label)
        depth_row.addWidget(self.depth_field)
        depth_row.addStretch()
        plate_layout.addLayout(depth_row)
        
        # Web Thickness
        web_thick_row = QHBoxLayout()
        web_thick_label = QLabel("Web Thickness (mm):")
        web_thick_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.web_thick_field = OptimizableField("Web Thickness")
        self.style_input_field(self.web_thick_field.mode_combo)
        self.style_input_field(self.web_thick_field.input_field)
        web_thick_row.addWidget(web_thick_label)
        web_thick_row.addWidget(self.web_thick_field)
        web_thick_row.addStretch()
        plate_layout.addLayout(web_thick_row)
        
        # Torsional Restraint
        torsion_row = QHBoxLayout()
        torsion_label = QLabel("Torsional Restraint:")
        torsion_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.torsion_combo = QComboBox()
        self.torsion_combo.addItems(VALUES_TORSIONAL_RESTRAINT)
        self.style_input_field(self.torsion_combo)
        torsion_row.addWidget(torsion_label)
        torsion_row.addWidget(self.torsion_combo)
        torsion_row.addStretch()
        plate_layout.addLayout(torsion_row)
        
        # Warping Restraint
        warp_row = QHBoxLayout()
        warp_label = QLabel("Warping Restraint:")
        warp_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.warp_combo = QComboBox()
        self.warp_combo.addItems(VALUES_WARPING_RESTRAINT)
        self.style_input_field(self.warp_combo)
        warp_row.addWidget(warp_label)
        warp_row.addWidget(self.warp_combo)
        warp_row.addStretch()
        plate_layout.addLayout(warp_row)
        
        # Web Type
        web_type_row = QHBoxLayout()
        web_type_label = QLabel("Web Type:")
        web_type_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.web_type_combo = QComboBox()
        self.web_type_combo.addItems(VALUES_WEB_TYPE)
        self.style_input_field(self.web_type_combo)
        web_type_row.addWidget(web_type_label)
        web_type_row.addWidget(self.web_type_combo)
        web_type_row.addStretch()
        plate_layout.addLayout(web_type_row)
        
        self.plate_girder_group.setLayout(plate_layout)
        scroll_layout.addWidget(self.plate_girder_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Connect signals
        self.girder_type_combo.currentTextChanged.connect(self.on_girder_type_changed)
        
        # Initialize visibility
        self.on_girder_type_changed(self.girder_type_combo.currentText())
    
    def on_girder_type_changed(self, text):
        """Show/hide sections based on girder type"""
        if text == "IS Standard Rolled Beam":
            self.is_beam_group.setVisible(True)
            self.plate_girder_group.setVisible(False)
        else:  # Plate Girder
            self.is_beam_group.setVisible(False)
            self.plate_girder_group.setVisible(True)
    
    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        field.setMinimumHeight(28)
        if isinstance(field, QComboBox):
            field.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    padding-right: 30px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
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
                QComboBox:focus {
                    border: 1px solid #4a7ba7;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    border: 1px solid #c0c0c0;
                    selection-background-color: #e8f4ff;
                }
            """)
        elif isinstance(field, QLineEdit):
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
                    background-color: #f5f5f5;
                    color: #999;
                }
            """)
    
    def get_group_style(self):
        """Return consistent group box styling"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: white;
            }
        """


class StiffenerDetailsTab(QWidget):
    """Tab for Stiffener Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Stiffener Details Group
        stiff_group = QGroupBox("Stiffener Configuration")
        stiff_group.setStyleSheet(self.get_group_style())
        stiff_layout = QVBoxLayout()
        
        # Design Method
        method_row = QHBoxLayout()
        method_label = QLabel("Stiffener Design Method:")
        method_label.setStyleSheet("font-size: 11px; min-width: 220px;")
        self.method_combo = QComboBox()
        self.method_combo.addItems(VALUES_STIFFENER_DESIGN)
        self.style_input_field(self.method_combo)
        method_row.addWidget(method_label)
        method_row.addWidget(self.method_combo)
        method_row.addStretch()
        stiff_layout.addLayout(method_row)
        
        # Stiffener Plate Thickness
        thick_row = QHBoxLayout()
        thick_label = QLabel("Stiffener Plate Thickness (mm):")
        thick_label.setStyleSheet("font-size: 11px; min-width: 220px;")
        self.thick_combo = QComboBox()
        self.thick_combo.addItems(["Optimized", "All"])
        self.style_input_field(self.thick_combo)
        thick_row.addWidget(thick_label)
        thick_row.addWidget(self.thick_combo)
        thick_row.addStretch()
        stiff_layout.addLayout(thick_row)
        
        # Stiffener Spacing
        spacing_row = QHBoxLayout()
        spacing_label = QLabel("Stiffener Spacing (mm):")
        spacing_label.setStyleSheet("font-size: 11px; min-width: 220px;")
        self.spacing_field = OptimizableField("Stiffener Spacing")
        self.spacing_field.mode_combo.clear()
        self.spacing_field.mode_combo.addItems(["Optimized", "Customized"])
        self.style_input_field(self.spacing_field.mode_combo)
        self.style_input_field(self.spacing_field.input_field)
        spacing_row.addWidget(spacing_label)
        spacing_row.addWidget(self.spacing_field)
        spacing_row.addStretch()
        stiff_layout.addLayout(spacing_row)
        
        # Longitudinal Stiffener Requirement
        long_req_row = QHBoxLayout()
        long_req_label = QLabel("Longitudinal Stiffener Requirement:")
        long_req_label.setStyleSheet("font-size: 11px; min-width: 220px;")
        self.long_req_combo = QComboBox()
        self.long_req_combo.addItems(VALUES_YES_NO)
        self.style_input_field(self.long_req_combo)
        long_req_row.addWidget(long_req_label)
        long_req_row.addWidget(self.long_req_combo)
        long_req_row.addStretch()
        stiff_layout.addLayout(long_req_row)
        
        # Longitudinal Stiffener Thickness
        long_thick_row = QHBoxLayout()
        long_thick_label = QLabel("Longitudinal Stiffener Thickness (mm):")
        long_thick_label.setStyleSheet("font-size: 11px; min-width: 220px;")
        self.long_thick_combo = QComboBox()
        self.long_thick_combo.addItems(["Optimized", "All"])
        self.long_thick_combo.setEnabled(False)  # Disabled by default
        self.style_input_field(self.long_thick_combo)
        long_thick_row.addWidget(long_thick_label)
        long_thick_row.addWidget(self.long_thick_combo)
        long_thick_row.addStretch()
        stiff_layout.addLayout(long_thick_row)
        
        stiff_group.setLayout(stiff_layout)
        scroll_layout.addWidget(stiff_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Connect signals
        self.long_req_combo.currentTextChanged.connect(self.on_long_req_changed)
    
    def on_long_req_changed(self, text):
        """Enable/disable longitudinal stiffener thickness based on requirement"""
        self.long_thick_combo.setEnabled(text == "Yes")
    
    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        field.setMinimumHeight(28)
        if isinstance(field, QComboBox):
            field.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    padding-right: 30px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
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
                QComboBox:focus {
                    border: 1px solid #4a7ba7;
                }
                QComboBox:disabled {
                    background-color: #f5f5f5;
                    color: #999;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    border: 1px solid #c0c0c0;
                    selection-background-color: #e8f4ff;
                }
            """)
        elif isinstance(field, QLineEdit):
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
                    background-color: #f5f5f5;
                    color: #999;
                }
            """)
    
    def get_group_style(self):
        """Return consistent group box styling"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: white;
            }
        """


class CrossBracingDetailsTab(QWidget):
    """Tab for Cross-Bracing Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Cross-Bracing Group
        bracing_group = QGroupBox("Cross-Bracing Configuration")
        bracing_group.setStyleSheet(self.get_group_style())
        bracing_layout = QVBoxLayout()
        
        # Type of Bracing
        type_row = QHBoxLayout()
        type_label = QLabel("Type of Bracing:")
        type_label.setStyleSheet("font-size: 11px; min-width: 180px;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(VALUES_CROSS_BRACING_TYPE)
        self.style_input_field(self.type_combo)
        type_row.addWidget(type_label)
        type_row.addWidget(self.type_combo)
        type_row.addStretch()
        bracing_layout.addLayout(type_row)
        
        # Bracing Section
        section_row = QHBoxLayout()
        section_label = QLabel("Bracing Section:")
        section_label.setStyleSheet("font-size: 11px; min-width: 180px;")
        self.section_combo = QComboBox()
        self.section_combo.addItems([
            "Select Section",
            "ISA 50x50x6", "ISA 65x65x6", "ISA 75x75x6", "ISA 90x90x8",
            "ISA 100x100x8", "ISA 110x110x10", "ISA 130x130x10",
            "2-ISA 50x50x6 (LL)", "2-ISA 65x65x6 (LL)", "2-ISA 75x75x6 (LL)",
            "2-ISA 50x50x6 (SL)", "2-ISA 65x65x6 (SL)", "2-ISA 75x75x6 (SL)",
            "ISMC 75", "ISMC 100", "ISMC 125", "ISMC 150",
            "2-ISMC 75", "2-ISMC 100", "2-ISMC 125"
        ])
        self.style_input_field(self.section_combo)
        section_row.addWidget(section_label)
        section_row.addWidget(self.section_combo)
        section_row.addStretch()
        bracing_layout.addLayout(section_row)
        
        # Bracket Section
        self.bracket_row = QHBoxLayout()
        bracket_label = QLabel("Bracket Section:")
        bracket_label.setStyleSheet("font-size: 11px; min-width: 180px;")
        self.bracket_combo = QComboBox()
        self.bracket_combo.addItems([
            "Select Section",
            "ISA 50x50x6", "ISA 65x65x6", "ISA 75x75x6", "ISA 90x90x8",
            "ISA 100x100x8", "ISA 110x110x10",
            "2-ISA 50x50x6 (LL)", "2-ISA 65x65x6 (LL)", "2-ISA 75x75x6 (LL)",
            "2-ISA 50x50x6 (SL)", "2-ISA 65x65x6 (SL)", "2-ISA 75x75x6 (SL)",
            "ISMC 75", "ISMC 100", "ISMC 125",
            "2-ISMC 75", "2-ISMC 100"
        ])
        self.bracket_combo.setEnabled(False)  # Disabled by default
        self.style_input_field(self.bracket_combo)
        self.bracket_row.addWidget(bracket_label)
        self.bracket_row.addWidget(self.bracket_combo)
        self.bracket_row.addStretch()
        bracing_layout.addLayout(self.bracket_row)
        
        # Spacing
        spacing_row = QHBoxLayout()
        spacing_label = QLabel("Spacing (mm):")
        spacing_label.setStyleSheet("font-size: 11px; min-width: 180px;")
        self.spacing_input = QLineEdit()
        self.spacing_input.setPlaceholderText("Enter spacing in mm")
        self.spacing_input.setValidator(QDoubleValidator(0, 100000, 2))
        self.style_input_field(self.spacing_input)
        spacing_row.addWidget(spacing_label)
        spacing_row.addWidget(self.spacing_input)
        spacing_row.addStretch()
        bracing_layout.addLayout(spacing_row)
        
        bracing_group.setLayout(bracing_layout)
        scroll_layout.addWidget(bracing_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Connect signals
        self.type_combo.currentTextChanged.connect(self.on_bracing_type_changed)
    
    def on_bracing_type_changed(self, text):
        """Enable/disable bracket section based on bracing type"""
        has_bracket = "bracket" in text.lower()
        self.bracket_combo.setEnabled(has_bracket)
    
    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        field.setMinimumHeight(28)
        if isinstance(field, QComboBox):
            field.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    padding-right: 30px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
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
                QComboBox:focus {
                    border: 1px solid #4a7ba7;
                }
                QComboBox:disabled {
                    background-color: #f5f5f5;
                    color: #999;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    border: 1px solid #c0c0c0;
                    selection-background-color: #e8f4ff;
                }
            """)
        elif isinstance(field, QLineEdit):
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
                    background-color: #f5f5f5;
                    color: #999;
                }
            """)
    
    def get_group_style(self):
        """Return consistent group box styling"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: white;
            }
        """


class EndDiaphragmDetailsTab(QWidget):
    """Tab for End Diaphragm Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # End Diaphragm Group
        diaphragm_group = QGroupBox("End Diaphragm Configuration")
        diaphragm_group.setStyleSheet(self.get_group_style())
        diaphragm_layout = QVBoxLayout()
        
        # Type of Section
        type_row = QHBoxLayout()
        type_label = QLabel("Type of Section:")
        type_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(VALUES_END_DIAPHRAGM_TYPE)
        self.style_input_field(self.type_combo)
        type_row.addWidget(type_label)
        type_row.addWidget(self.type_combo)
        type_row.addStretch()
        diaphragm_layout.addLayout(type_row)
        
        diaphragm_group.setLayout(diaphragm_layout)
        scroll_layout.addWidget(diaphragm_group)
        
        # IS Rolled Beam Section
        self.is_beam_group = QGroupBox("IS Standard Rolled Beam Section")
        self.is_beam_group.setStyleSheet(self.get_group_style())
        is_beam_layout = QVBoxLayout()
        
        is_beam_row = QHBoxLayout()
        is_beam_label = QLabel("Select IS Beam Section:")
        is_beam_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.is_beam_combo = QComboBox()
        self.is_beam_combo.addItems([
            "Select Section",
            "ISMB 100", "ISMB 125", "ISMB 150", "ISMB 175", "ISMB 200",
            "ISMB 225", "ISMB 250", "ISMB 300", "ISMB 350", "ISMB 400",
            "ISWB 150", "ISWB 175", "ISWB 200", "ISWB 225", "ISWB 250",
            "ISWB 300", "ISWB 350", "ISWB 400"
        ])
        self.style_input_field(self.is_beam_combo)
        is_beam_row.addWidget(is_beam_label)
        is_beam_row.addWidget(self.is_beam_combo)
        is_beam_row.addStretch()
        is_beam_layout.addLayout(is_beam_row)
        
        self.is_beam_group.setLayout(is_beam_layout)
        scroll_layout.addWidget(self.is_beam_group)
        
        # Plate Girder Section
        self.plate_girder_group = QGroupBox("Plate Girder Details")
        self.plate_girder_group.setStyleSheet(self.get_group_style())
        plate_layout = QVBoxLayout()
        
        # Top Flange Width
        top_width_row = QHBoxLayout()
        top_width_label = QLabel("Top Flange Width (mm):")
        top_width_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.top_width_field = OptimizableField("Top Flange Width")
        self.style_input_field(self.top_width_field.mode_combo)
        self.style_input_field(self.top_width_field.input_field)
        top_width_row.addWidget(top_width_label)
        top_width_row.addWidget(self.top_width_field)
        top_width_row.addStretch()
        plate_layout.addLayout(top_width_row)
        
        # Top Flange Thickness
        top_thick_row = QHBoxLayout()
        top_thick_label = QLabel("Top Flange Thickness (mm):")
        top_thick_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.top_thick_field = OptimizableField("Top Flange Thickness")
        self.style_input_field(self.top_thick_field.mode_combo)
        self.style_input_field(self.top_thick_field.input_field)
        top_thick_row.addWidget(top_thick_label)
        top_thick_row.addWidget(self.top_thick_field)
        top_thick_row.addStretch()
        plate_layout.addLayout(top_thick_row)
        
        # Bottom Flange Width
        bottom_width_row = QHBoxLayout()
        bottom_width_label = QLabel("Bottom Flange Width (mm):")
        bottom_width_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.bottom_width_field = OptimizableField("Bottom Flange Width")
        self.style_input_field(self.bottom_width_field.mode_combo)
        self.style_input_field(self.bottom_width_field.input_field)
        bottom_width_row.addWidget(bottom_width_label)
        bottom_width_row.addWidget(self.bottom_width_field)
        bottom_width_row.addStretch()
        plate_layout.addLayout(bottom_width_row)
        
        # Bottom Flange Thickness
        bottom_thick_row = QHBoxLayout()
        bottom_thick_label = QLabel("Bottom Flange Thickness (mm):")
        bottom_thick_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.bottom_thick_field = OptimizableField("Bottom Flange Thickness")
        self.style_input_field(self.bottom_thick_field.mode_combo)
        self.style_input_field(self.bottom_thick_field.input_field)
        bottom_thick_row.addWidget(bottom_thick_label)
        bottom_thick_row.addWidget(self.bottom_thick_field)
        bottom_thick_row.addStretch()
        plate_layout.addLayout(bottom_thick_row)
        
        # Depth of Section
        depth_row = QHBoxLayout()
        depth_label = QLabel("Depth of Section (mm):")
        depth_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.depth_field = OptimizableField("Depth of Section")
        self.style_input_field(self.depth_field.mode_combo)
        self.style_input_field(self.depth_field.input_field)
        depth_row.addWidget(depth_label)
        depth_row.addWidget(self.depth_field)
        depth_row.addStretch()
        plate_layout.addLayout(depth_row)
        
        # Web Thickness
        web_thick_row = QHBoxLayout()
        web_thick_label = QLabel("Web Thickness (mm):")
        web_thick_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.web_thick_field = OptimizableField("Web Thickness")
        self.style_input_field(self.web_thick_field.mode_combo)
        self.style_input_field(self.web_thick_field.input_field)
        web_thick_row.addWidget(web_thick_label)
        web_thick_row.addWidget(self.web_thick_field)
        web_thick_row.addStretch()
        plate_layout.addLayout(web_thick_row)
        
        self.plate_girder_group.setLayout(plate_layout)
        scroll_layout.addWidget(self.plate_girder_group)
        
        # Spacing
        spacing_group = QGroupBox("Spacing")
        spacing_group.setStyleSheet(self.get_group_style())
        spacing_layout = QVBoxLayout()
        
        spacing_row = QHBoxLayout()
        spacing_label = QLabel("Spacing (mm):")
        spacing_label.setStyleSheet("font-size: 11px; min-width: 200px;")
        self.spacing_input = QLineEdit()
        self.spacing_input.setPlaceholderText("Enter spacing in mm")
        self.spacing_input.setValidator(QDoubleValidator(0, 100000, 2))
        self.style_input_field(self.spacing_input)
        spacing_row.addWidget(spacing_label)
        spacing_row.addWidget(self.spacing_input)
        spacing_row.addStretch()
        spacing_layout.addLayout(spacing_row)
        
        spacing_group.setLayout(spacing_layout)
        scroll_layout.addWidget(spacing_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Connect signals
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        
        # Initialize visibility
        self.on_type_changed(self.type_combo.currentText())
    
    def on_type_changed(self, text):
        """Show/hide sections based on diaphragm type"""
        if text == "Same as cross-bracing":
            self.is_beam_group.setVisible(False)
            self.plate_girder_group.setVisible(False)
        elif text == "Rolled Beam Section":
            self.is_beam_group.setVisible(True)
            self.plate_girder_group.setVisible(False)
        else:  # Plate Girder Section
            self.is_beam_group.setVisible(False)
            self.plate_girder_group.setVisible(True)
    
    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        field.setMinimumHeight(28)
        if isinstance(field, QComboBox):
            field.setStyleSheet("""
                QComboBox {
                    padding: 4px 8px;
                    padding-right: 30px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                    color: #333;
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
                QComboBox:focus {
                    border: 1px solid #4a7ba7;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    border: 1px solid #c0c0c0;
                    selection-background-color: #e8f4ff;
                }
            """)
        elif isinstance(field, QLineEdit):
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
                    background-color: #f5f5f5;
                    color: #999;
                }
            """)
    
    def get_group_style(self):
        """Return consistent group box styling"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #fafafa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                background-color: white;
            }
        """


class AdditionalInputsWidget(QWidget):
    """Main widget for Additional Inputs with tabbed interface"""
    
    def __init__(self, footpath_value="None", carriageway_width=7.5, parent=None):
        super().__init__(parent)
        self.footpath_value = footpath_value
        self.carriageway_width = carriageway_width
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
        self.bridge_geometry_tab = BridgeGeometryTab(self.footpath_value, self.carriageway_width)
        self.tabs.addTab(self.bridge_geometry_tab, "Bridge Geometry")
        
        # Sub-Tab 2: Section Properties
        self.section_properties_tab = SectionPropertiesTab()
        self.tabs.addTab(self.section_properties_tab, "Section Properties")
        
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
