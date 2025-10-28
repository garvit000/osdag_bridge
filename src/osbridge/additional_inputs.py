"""
Additional Inputs Widget for Highway Bridge Design
Provides detailed input fields for manual bridge parameter definition
"""
import sys
import base64
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit,
    QComboBox, QGroupBox, QFormLayout, QPushButton, QScrollArea,
    QCheckBox, QMessageBox, QSizePolicy, QSpacerItem, QStackedWidget,
    QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator

from common import *


def get_dropdown_svg_icon():
    """Return the SVG markup for styled dropdown arrows."""
    return (
        "<svg width=\"30\" height=\"28\" viewBox=\"0 0 30 28\" fill=\"none\" "
        "xmlns=\"http://www.w3.org/2000/svg\">"
        "<path d=\"M14.5833 17.875L20.4167 12.375H8.75L14.5833 17.875Z\" fill=\"black\"/>"
        "<path d=\"M14.5833 27.5C12.566 27.5 10.6701 27.1391 8.89583 26.4172C7.12153 25.6953 "
        "5.57812 24.7156 4.26562 23.4781C2.95312 22.2406 1.91406 20.7854 1.14844 19.1125C0.382812 "
        "17.4396 0 15.6521 0 13.75C0 11.8479 0.382812 10.0604 1.14844 8.3875C1.91406 6.71458 2.95312 "
        "5.25938 4.26562 4.02187C5.57812 2.78437 7.12153 1.80469 8.89583 1.08281C10.6701 0.360938 12.566 "
        "0 14.5833 0C16.6007 0 18.4965 0.360938 20.2708 1.08281C22.0451 1.80469 23.5885 2.78437 24.901 4.02187C26.2135 "
        "5.25938 27.2526 6.71458 28.0182 8.3875C28.7839 10.0604 29.1667 11.8479 29.1667 13.75C29.1667 15.6521 28.7839 17.4396 "
        "28.0182 19.1125C27.2526 20.7854 26.2135 22.2406 24.901 23.4781C23.5885 24.7156 22.0451 25.6953 20.2708 26.4172C18.4965 "
        "27.1391 16.6007 27.5 14.5833 27.5ZM14.5833 24.75C17.8403 24.75 20.599 23.6844 22.8594 21.5531C25.1198 19.4219 26.25 "
        "16.8208 26.25 13.75C26.25 10.6792 25.1198 8.07812 22.8594 5.94688C20.599 3.81563 17.8403 2.75 14.5833 2.75C11.3264 2.75 "
        "8.56771 3.81563 6.30729 5.94688C4.04688 8.07812 2.91667 10.6792 2.91667 13.75C2.91667 16.8208 4.04688 19.4219 6.30729 "
        "21.5531C8.56771 23.6844 11.3264 24.75 14.5833 24.75Z\" fill=\"black\"/>"
        "</svg>"
    )


def get_combobox_style():
    """Return the common stylesheet for dropdowns with the SVG icon."""
    svg_data = get_dropdown_svg_icon().encode("utf-8")
    svg_base64 = base64.b64encode(svg_data).decode("utf-8")
    return f"""
        QComboBox {{
            padding: 6px 42px 6px 14px;
            border: 1px solid #b8b8b8;
            border-radius: 8px;
            background-color: #ffffff;
            color: #2b2b2b;
            font-size: 12px;
            min-height: 34px;
        }}
        QComboBox:hover {{
            border: 1px solid #909090;
        }}
        QComboBox:focus {{
            border: 1px solid #4a7ba7;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 30px;
            border: none;
            background: transparent;
            right: 8px;
        }}
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,{svg_base64});
            width: 26px;
            height: 26px;
        }}
        QComboBox QAbstractItemView {{
            border: 1px solid #b8b8b8;
            background: #ffffff;
            selection-background-color: #e7f2ff;
            selection-color: #1f1f1f;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 6px 10px;
            font-size: 12px;
        }}
    """


def get_lineedit_style():
    """Return the shared stylesheet for line edits in the section inputs."""
    return """
        QLineEdit {
            padding: 6px 12px;
            border: 1px solid #b8b8b8;
            border-radius: 8px;
            background-color: #ffffff;
            color: #2b2b2b;
            font-size: 12px;
            min-height: 34px;
        }
        QLineEdit:hover {
            border: 1px solid #909090;
        }
        QLineEdit:focus {
            border: 1px solid #4a7ba7;
        }
        QLineEdit:disabled {
            background-color: #f0f0f0;
            color: #9b9b9b;
        }
    """


def apply_field_style(widget):
    """Apply the appropriate style to combo boxes and line edits."""
    widget.setMinimumHeight(34)
    if isinstance(widget, QComboBox):
        widget.setStyleSheet(get_combobox_style())
    elif isinstance(widget, QLineEdit):
        widget.setStyleSheet(get_lineedit_style())


SECTION_NAV_BUTTON_STYLE = """
    QPushButton {
        background-color: #f4f4f4;
        border: 2px solid #d2d2d2;
        border-radius: 12px;
        padding: 20px 16px;
        text-align: left;
        font-weight: bold;
        font-size: 12px;
        color: #333333;
    }
    QPushButton:hover {
        border-color: #b5b5b5;
    }
    QPushButton:checked {
        background-color: #9ecb3d;
        border-color: #7da523;
        color: #ffffff;
    }
"""


class OptimizableField(QWidget):
    """Widget that allows selection between Optimized/Customized/All modes with input field"""
    
    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
        
        # Mode selector
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(VALUES_OPTIMIZATION_MODE)
        self.mode_combo.setMinimumWidth(140)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setEnabled(False)  # Disabled by default for "Optimized"
        self.input_field.setVisible(False)
        self.input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.layout.addWidget(self.mode_combo)
        self.layout.addWidget(self.input_field)
        
        # Connect signal
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        self.on_mode_changed(self.mode_combo.currentText())
    
    def on_mode_changed(self, text):
        """Enable/disable input field based on selection"""
        if text in ("Optimized", "All"):
            self.input_field.setEnabled(False)
            self.input_field.clear()
            self.input_field.setVisible(False)
        else:
            self.input_field.setEnabled(True)
            self.input_field.setVisible(True)
    
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
        apply_field_style(field)
    
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
    """Sub-tab for Section Properties with custom navigation layout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_buttons = []
        self.init_ui()

    def init_ui(self):
        """Initialize styled navigation and content panels."""
        self.setStyleSheet("background-color: #f7f7f7;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(22)
        main_layout.addLayout(content_layout)

        nav_frame = QFrame()
        nav_frame.setObjectName("sectionNavFrame")
        nav_frame.setFixedWidth(190)
        nav_frame.setStyleSheet(
            "QFrame#sectionNavFrame {"
            " background-color: #f2f2f2;"
            " border: 1px solid #d1d1d1;"
            " border-radius: 16px;"
            "}"
        )
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(14, 20, 14, 20)
        nav_layout.setSpacing(14)
        content_layout.addWidget(nav_frame)

        content_frame = QFrame()
        content_frame.setObjectName("sectionContentFrame")
        content_frame.setStyleSheet(
            "QFrame#sectionContentFrame {"
            " background-color: #ffffff;"
            " border: 1px solid #c7c7c7;"
            " border-radius: 18px;"
            "}"
        )
        content_inner_layout = QVBoxLayout(content_frame)
        content_inner_layout.setContentsMargins(30, 24, 30, 24)
        content_inner_layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setObjectName("sectionStack")
        self.stack.setStyleSheet("QStackedWidget#sectionStack { background-color: transparent; }")
        content_inner_layout.addWidget(self.stack)

        content_layout.addWidget(content_frame, 1)
        content_layout.setStretch(0, 0)
        content_layout.setStretch(1, 1)

        sections = [
            ("Girder Details", GirderDetailsTab),
            ("Stiffener Details", StiffenerDetailsTab),
            ("Cross-Bracing Details", CrossBracingDetailsTab),
            ("End Diaphragm Details", EndDiaphragmDetailsTab),
        ]

        for index, (title, widget_cls) in enumerate(sections):
            button = QPushButton(f"{title}:")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(SECTION_NAV_BUTTON_STYLE)
            button.setMinimumHeight(86)
            button.clicked.connect(lambda _checked, idx=index: self.switch_section(idx))
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)

            section_widget = widget_cls()
            self.stack.addWidget(section_widget)

        nav_layout.addStretch()

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
            self.stack.setCurrentIndex(0)

    def switch_section(self, index):
        """Switch the stacked widget page and update navigation states."""
        self.stack.setCurrentIndex(index)
        for btn_index, button in enumerate(self.nav_buttons):
            button.setChecked(btn_index == index)


class GirderDetailsTab(QWidget):
    """Tab for Girder Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plate_rows = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background: transparent; }")
        self.form_layout = QGridLayout(form_frame)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setHorizontalSpacing(28)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setColumnMinimumWidth(0, 220)
        self.form_layout.setColumnStretch(1, 1)
        container_layout.addWidget(form_frame)
        container_layout.addStretch()

        row = 0
        self.girder_type_label = self.create_label("Girder Type:")
        self.girder_type_combo = QComboBox()
        self.girder_type_combo.addItems(VALUES_GIRDER_TYPE)
        apply_field_style(self.girder_type_combo)
        self.form_layout.addWidget(self.girder_type_label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(self.girder_type_combo, row, 1)
        row += 1

        self.is_section_label = self.create_label("Select IS Beam Section:")
        self.is_beam_combo = QComboBox()
        self.is_beam_combo.addItems([
            "Select Section",
            "ISMB 100", "ISMB 125", "ISMB 150", "ISMB 175", "ISMB 200",
            "ISMB 225", "ISMB 250", "ISMB 300", "ISMB 350", "ISMB 400",
            "ISMB 450", "ISMB 500", "ISMB 550", "ISMB 600",
            "ISWB 150", "ISWB 175", "ISWB 200", "ISWB 225", "ISWB 250",
            "ISWB 300", "ISWB 350", "ISWB 400", "ISWB 450", "ISWB 500", "ISWB 550", "ISWB 600"
        ])
        apply_field_style(self.is_beam_combo)
        self.form_layout.addWidget(self.is_section_label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(self.is_beam_combo, row, 1)
        row += 1

        self.symmetry_combo = QComboBox()
        self.symmetry_combo.addItems(VALUES_GIRDER_SYMMETRY)
        apply_field_style(self.symmetry_combo)
        row = self.add_plate_row(row, "Girder Symmetry", self.symmetry_combo)

        self.top_width_field = OptimizableField("Top Flange Width")
        self.prepare_optimizable_field(self.top_width_field)
        row = self.add_plate_row(row, "Top Flange Width (mm):", self.top_width_field)

        self.top_thick_field = OptimizableField("Top Flange Thickness")
        self.prepare_optimizable_field(self.top_thick_field)
        row = self.add_plate_row(row, "Top Flange Thickness (mm):", self.top_thick_field)

        self.bottom_width_field = OptimizableField("Bottom Flange Width")
        self.prepare_optimizable_field(self.bottom_width_field)
        row = self.add_plate_row(row, "Bottom Flange Width (mm):", self.bottom_width_field)

        self.bottom_thick_field = OptimizableField("Bottom Flange Thickness")
        self.prepare_optimizable_field(self.bottom_thick_field)
        row = self.add_plate_row(row, "Bottom Flange Thickness (mm):", self.bottom_thick_field)

        self.depth_field = OptimizableField("Depth of Section")
        self.prepare_optimizable_field(self.depth_field)
        row = self.add_plate_row(row, "Depth of Section (mm):", self.depth_field)

        self.web_thick_field = OptimizableField("Web Thickness")
        self.prepare_optimizable_field(self.web_thick_field)
        row = self.add_plate_row(row, "Web Thickness (mm):", self.web_thick_field)

        self.torsion_combo = QComboBox()
        self.torsion_combo.addItems(VALUES_TORSIONAL_RESTRAINT)
        apply_field_style(self.torsion_combo)
        row = self.add_plate_row(row, "Torsional Restraint:", self.torsion_combo)

        self.warp_combo = QComboBox()
        self.warp_combo.addItems(VALUES_WARPING_RESTRAINT)
        apply_field_style(self.warp_combo)
        row = self.add_plate_row(row, "Warping Restraint:", self.warp_combo)

        self.web_type_combo = QComboBox()
        self.web_type_combo.addItems(VALUES_WEB_TYPE)
        apply_field_style(self.web_type_combo)
        row = self.add_plate_row(row, "Web Type* :", self.web_type_combo)

        self.girder_type_combo.currentTextChanged.connect(self.on_girder_type_changed)
        self.on_girder_type_changed(self.girder_type_combo.currentText())

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 13px; color: #2f2f2f; font-weight: 600;")
        return label

    def prepare_optimizable_field(self, field):
        field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        apply_field_style(field.mode_combo)
        apply_field_style(field.input_field)

    def add_plate_row(self, row, text, widget):
        label = self.create_label(text)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.form_layout.addWidget(label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(widget, row, 1)
        self.plate_rows.append((label, widget))
        return row + 1

    def on_girder_type_changed(self, text):
        is_standard = text == "IS Standard Rolled Beam"
        self.is_section_label.setVisible(is_standard)
        self.is_beam_combo.setVisible(is_standard)
        for label, widget in self.plate_rows:
            label.setVisible(not is_standard)
            widget.setVisible(not is_standard)


class StiffenerDetailsTab(QWidget):
    """Tab for Stiffener Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background: transparent; }")
        self.form_layout = QGridLayout(form_frame)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setHorizontalSpacing(28)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setColumnMinimumWidth(0, 240)
        self.form_layout.setColumnStretch(1, 1)
        container_layout.addWidget(form_frame)
        container_layout.addStretch()

        row = 0
        self.method_combo = QComboBox()
        self.method_combo.addItems(VALUES_STIFFENER_DESIGN)
        apply_field_style(self.method_combo)
        row = self.add_row(row, "Stiffener design method:", self.method_combo)

        self.thick_combo = QComboBox()
        self.thick_combo.addItems(["Optimized", "All"])
        apply_field_style(self.thick_combo)
        row = self.add_row(row, "Stiffener Plate Thickness (mm):", self.thick_combo)

        self.spacing_field = OptimizableField("Stiffener Spacing")
        self.spacing_field.mode_combo.clear()
        self.spacing_field.mode_combo.addItems(["Optimized", "Customized"])
        self.spacing_field.on_mode_changed(self.spacing_field.mode_combo.currentText())
        self.prepare_optimizable_field(self.spacing_field)
        row = self.add_row(row, "Stiffener Spacing (mm):", self.spacing_field)

        self.long_req_combo = QComboBox()
        self.long_req_combo.addItems(VALUES_YES_NO)
        apply_field_style(self.long_req_combo)
        row = self.add_row(row, "Longitudinal stiffener requirement:", self.long_req_combo)

        self.long_thick_combo = QComboBox()
        self.long_thick_combo.addItems(["Optimized", "All"])
        self.long_thick_combo.setEnabled(False)
        apply_field_style(self.long_thick_combo)
        self.add_row(row, "Longitudinal stiffener thickness:", self.long_thick_combo)

        self.long_req_combo.currentTextChanged.connect(self.on_long_req_changed)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 13px; color: #2f2f2f; font-weight: 600;")
        return label

    def add_row(self, row, text, widget):
        label = self.create_label(text)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.form_layout.addWidget(label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(widget, row, 1)
        return row + 1

    def prepare_optimizable_field(self, field):
        field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        apply_field_style(field.mode_combo)
        apply_field_style(field.input_field)

    def on_long_req_changed(self, text):
        """Enable/disable longitudinal stiffener thickness based on requirement"""
        self.long_thick_combo.setEnabled(text == "Yes")


class CrossBracingDetailsTab(QWidget):
    """Tab for Cross-Bracing Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background: transparent; }")
        self.form_layout = QGridLayout(form_frame)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setHorizontalSpacing(28)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setColumnMinimumWidth(0, 210)
        self.form_layout.setColumnStretch(1, 1)
        container_layout.addWidget(form_frame)
        container_layout.addStretch()

        row = 0
        self.type_combo = QComboBox()
        self.type_combo.addItems(VALUES_CROSS_BRACING_TYPE)
        apply_field_style(self.type_combo)
        row = self.add_row(row, "Type of Bracing:", self.type_combo)

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
        apply_field_style(self.section_combo)
        row = self.add_row(row, "Bracing Section:", self.section_combo)

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
        self.bracket_combo.setEnabled(False)
        apply_field_style(self.bracket_combo)
        row = self.add_row(row, "Bracket Section:", self.bracket_combo)

        self.spacing_input = QLineEdit()
        self.spacing_input.setPlaceholderText("Enter spacing in mm")
        self.spacing_input.setValidator(QDoubleValidator(0, 100000, 2))
        apply_field_style(self.spacing_input)
        self.add_row(row, "Spacing (mm):", self.spacing_input)

        self.type_combo.currentTextChanged.connect(self.on_bracing_type_changed)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 13px; color: #2f2f2f; font-weight: 600;")
        return label

    def add_row(self, row, text, widget):
        label = self.create_label(text)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.form_layout.addWidget(label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(widget, row, 1)
        return row + 1

    def on_bracing_type_changed(self, text):
        """Enable/disable bracket section based on bracing type"""
        has_bracket = "bracket" in text.lower()
        self.bracket_combo.setEnabled(has_bracket)


class EndDiaphragmDetailsTab(QWidget):
    """Tab for End Diaphragm Details"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plate_rows = []
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        form_frame = QFrame()
        form_frame.setStyleSheet("QFrame { background: transparent; }")
        self.form_layout = QGridLayout(form_frame)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setHorizontalSpacing(28)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setColumnMinimumWidth(0, 230)
        self.form_layout.setColumnStretch(1, 1)
        container_layout.addWidget(form_frame)
        container_layout.addStretch()

        row = 0
        self.type_combo = QComboBox()
        self.type_combo.addItems(VALUES_END_DIAPHRAGM_TYPE)
        apply_field_style(self.type_combo)
        self.form_layout.addWidget(self.create_label("Type of Section:"), row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(self.type_combo, row, 1)
        row += 1

        self.is_section_label = self.create_label("Select IS Beam Section:")
        self.is_beam_combo = QComboBox()
        self.is_beam_combo.addItems([
            "Select Section",
            "ISMB 100", "ISMB 125", "ISMB 150", "ISMB 175", "ISMB 200",
            "ISMB 225", "ISMB 250", "ISMB 300", "ISMB 350", "ISMB 400",
            "ISWB 150", "ISWB 175", "ISWB 200", "ISWB 225", "ISWB 250",
            "ISWB 300", "ISWB 350", "ISWB 400"
        ])
        apply_field_style(self.is_beam_combo)
        self.form_layout.addWidget(self.is_section_label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(self.is_beam_combo, row, 1)
        row += 1

        self.top_width_field = OptimizableField("Top Flange Width")
        self.prepare_optimizable_field(self.top_width_field)
        row = self.add_plate_row(row, "Top Flange Width (mm):", self.top_width_field)

        self.top_thick_field = OptimizableField("Top Flange Thickness")
        self.prepare_optimizable_field(self.top_thick_field)
        row = self.add_plate_row(row, "Top Flange Thickness (mm):", self.top_thick_field)

        self.bottom_width_field = OptimizableField("Bottom Flange Width")
        self.prepare_optimizable_field(self.bottom_width_field)
        row = self.add_plate_row(row, "Bottom Flange Width (mm):", self.bottom_width_field)

        self.bottom_thick_field = OptimizableField("Bottom Flange Thickness")
        self.prepare_optimizable_field(self.bottom_thick_field)
        row = self.add_plate_row(row, "Bottom Flange Thickness (mm):", self.bottom_thick_field)

        self.depth_field = OptimizableField("Depth of Section")
        self.prepare_optimizable_field(self.depth_field)
        row = self.add_plate_row(row, "Depth of Section (mm):", self.depth_field)

        self.web_thick_field = OptimizableField("Web Thickness")
        self.prepare_optimizable_field(self.web_thick_field)
        row = self.add_plate_row(row, "Web Thickness (mm):", self.web_thick_field)

        self.spacing_input = QLineEdit()
        self.spacing_input.setPlaceholderText("Enter spacing in mm")
        self.spacing_input.setValidator(QDoubleValidator(0, 100000, 2))
        apply_field_style(self.spacing_input)
        self.spacing_label = self.create_label("Spacing (mm):")
        self.form_layout.addWidget(self.spacing_label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(self.spacing_input, row, 1)

        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.on_type_changed(self.type_combo.currentText())

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 13px; color: #2f2f2f; font-weight: 600;")
        return label

    def prepare_optimizable_field(self, field):
        field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        apply_field_style(field.mode_combo)
        apply_field_style(field.input_field)

    def add_plate_row(self, row, text, widget):
        label = self.create_label(text)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.form_layout.addWidget(label, row, 0, Qt.AlignVCenter)
        self.form_layout.addWidget(widget, row, 1)
        self.plate_rows.append((label, widget))
        return row + 1

    def on_type_changed(self, text):
        """Show/hide sections based on diaphragm type"""
        is_same = text == "Same as cross-bracing"
        is_rolled = text == "Rolled Beam Section"

        self.is_section_label.setVisible(is_rolled)
        self.is_beam_combo.setVisible(is_rolled)

        show_plate = text == "Plate Girder Section"
        for label, widget in self.plate_rows:
            label.setVisible(show_plate)
            widget.setVisible(show_plate)

        if is_same:
            self.spacing_input.setEnabled(False)
            self.spacing_label.setEnabled(False)
            self.spacing_input.clear()
        else:
            self.spacing_input.setEnabled(True)
            self.spacing_label.setEnabled(True)


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
                border: 1px solid #d1d1d1;
                background: #ffffff;
            }
            QTabBar::tab {
                background: #e9e9e9;
                color: #3a3a3a;
                border: 1px solid #d1d1d1;
                border-bottom-color: #d1d1d1;
                padding: 10px 22px;
                margin-right: 4px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:selected {
                background: #9ecb3d;
                color: #ffffff;
                border: 1px solid #7ea82d;
            }
            QTabBar::tab:hover {
                background: #f5f5f5;
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
