"""
Additional Inputs Widget for Highway Bridge Design
Provides detailed input fields for manual bridge parameter definition
"""
import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTabBar, QLabel, QLineEdit,
    QComboBox, QGroupBox, QFormLayout, QPushButton, QScrollArea,
    QCheckBox, QMessageBox, QSizePolicy, QSpacerItem, QStackedWidget,
    QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QDialog
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QDoubleValidator, QIntValidator

from osbridge.backend.common import *


def get_combobox_style():
    """Return the common stylesheet for dropdowns with the SVG icon from resources."""
    return """
        QComboBox {
            padding: 2px 28px 2px 8px;
            border: 1px solid #000000;
            border-radius: 5px;
            background-color: #ffffff;
            color: #000000;
            font-size: 12px;
            min-height: 28px;
        }
        QComboBox:hover {
            border: 1px solid #5d5d5d;
        }
        QComboBox:focus {
            border: 1px solid #90AF13;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border: none;
            margin-right: 4px;
        }
        QComboBox::down-arrow {
            image: url(:/vectors/arrow_down_light.svg);
            width: 16px;
            height: 16px;
        }
        QComboBox::down-arrow:on {
            image: url(:/vectors/arrow_up_light.svg);
            width: 16px;
            height: 16px;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #000000;
            outline: none;
        }
        QComboBox QAbstractItemView::item {
            color: #000000;
            padding: 4px 8px;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #90AF13;
            color: #000000;
        }
    """


def get_lineedit_style():
    """Return the shared stylesheet for line edits in the section inputs."""
    return """
        QLineEdit {
            padding: 1px 7px;
            border: 1px solid #070707;
            border-radius: 6px;
            background-color: #ffffff;
            color: #000000;
            font-size: 12px;
            min-height: 28px;
        }
        QLineEdit:hover {
            border: 1px solid #5d5d5d;
        }
        QLineEdit:focus {
            border: 1px solid #90AF13;
        }
        QLineEdit:disabled {
            background-color: #f5f5f5;
            color: #9b9b9b;
        }
    """


def apply_field_style(widget):
    """Apply the appropriate style to combo boxes and line edits."""
    widget.setMinimumHeight(28)
    if isinstance(widget, QComboBox):
        widget.setStyleSheet(get_combobox_style())
    elif isinstance(widget, QLineEdit):
        widget.setStyleSheet(get_lineedit_style())


def create_action_button_bar(parent=None):
    """Create a standardized Defaults/Save bar with gray backing."""
    frame = QFrame(parent)
    frame.setObjectName("actionButtonBar")
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    frame.setStyleSheet(
        "QFrame#actionButtonBar {"
        "    background-color: #ededed;"
        "    border: 1px solid #c8c8c8;"
        "    border-radius: 6px;"
        "}"
        "QFrame#actionButtonBar QPushButton {"
        "    background-color: #ffffff;"
        "    color: #2f2f2f;"
        "    font-weight: 600;"
        "    border: 1px solid #8c8c8c;"
        "    border-radius: 4px;"
        "    padding: 6px 24px;"
        "    min-width: 120px;"
        "}"
        "QFrame#actionButtonBar QPushButton:hover {"
        "    background-color: #f6f6f6;"
        "}"
        "QFrame#actionButtonBar QPushButton:pressed {"
        "    background-color: #e0e0e0;"
        "}"
    )

    layout = QHBoxLayout(frame)
    layout.setContentsMargins(22, 10, 22, 10)
    layout.setSpacing(12)
    layout.addStretch()

    defaults_button = QPushButton("Defaults", frame)
    save_button = QPushButton("Save", frame)
    layout.addWidget(defaults_button)
    layout.addWidget(save_button)
    layout.addStretch()

    return frame, defaults_button, save_button


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

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(VALUES_OPTIMIZATION_MODE)
        self.mode_combo.setMinimumWidth(140)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.input_field = QLineEdit()
        self.input_field.setEnabled(False)
        self.input_field.setVisible(False)
        self.input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.mode_combo)
        self.layout.addWidget(self.input_field)

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


class TypicalSectionDetailsTab(QWidget):
    """Sub-tab for Typical Section Details inputs"""

    footpath_changed = Signal(str)

    def __init__(self, footpath_value="None", carriageway_width=7.5, parent=None):
        super().__init__(parent)
        self.footpath_value = footpath_value
        self.carriageway_width = carriageway_width
        self.updating_fields = False
        self.init_ui()

    def style_input_field(self, field):
        apply_field_style(field)

    def style_group_box(self, group_box):
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

    def _create_section_card(self, title):
        card = QFrame()
        card.setObjectName("sectionCard")
        card.setStyleSheet("""
            QFrame#sectionCard {
                background-color: #f5f5f5;
                border: none;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #000;")
        card_layout.addWidget(title_label)

        return card, card_layout

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        diagram_widget = QWidget()
        diagram_widget.setStyleSheet("""
            QWidget {
                background-color: #d9d9d9;
                border: 1px solid #b0b0b0;
                border-radius: 8px;
            }
        """)
        diagram_widget.setMinimumHeight(150)
        diagram_widget.setMaximumHeight(200)
        diagram_layout = QVBoxLayout(diagram_widget)
        diagram_layout.setContentsMargins(20, 20, 20, 20)
        diagram_layout.setAlignment(Qt.AlignCenter)

        diagram_label = QLabel("Typical Section Details\nDiagram")
        diagram_label.setAlignment(Qt.AlignCenter)
        diagram_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                padding: 20px;
                font-size: 13px;
                color: #333;
            }
        """)
        diagram_layout.addWidget(diagram_label)

        main_layout.addWidget(diagram_widget)
        main_layout.addSpacing(10)

        input_container = QWidget()
        input_container.setStyleSheet("QWidget { background-color: white; }")
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(0)

        self.input_tabs = QTabWidget()
        self.input_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #b0b0b0;
                border-top: none;
                background-color: #f5f5f5;
                border-radius: 0px 0px 8px 8px;
            }
            QTabBar::tab {
                background-color: #e8e8e8;
                color: #555;
                padding: 10px 20px;
                border: 1px solid #b0b0b0;
                border-bottom: none;
                border-right: none;
                font-size: 11px;
                min-width: 80px;
            }
            QTabBar::tab:last {
                border-right: 1px solid #b0b0b0;
            }
            QTabBar::tab:selected {
                background-color: #90AF13;
                color: white;
                font-weight: bold;
                border: 1px solid #90AF13;
                border-bottom: none;
            }
            QTabBar::tab:hover:!selected {
                background-color: #d0d0d0;
            }
        """)

        self.create_layout_tab()
        self.create_crash_barrier_tab()
        self.create_median_tab()
        self.create_railing_tab()
        self.create_wearing_course_tab()
        self.create_lane_details_tab()

        input_layout.addWidget(self.input_tabs)
        main_layout.addWidget(input_container)

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        self.defaults_button.clicked.connect(lambda: self._show_placeholder_message("Defaults"))
        self.save_button.clicked.connect(lambda: self._show_placeholder_message("Save"))
        main_layout.addSpacing(8)
        main_layout.addWidget(action_bar)

        self.deck_thickness.textChanged.connect(self.update_footpath_thickness)
        self.recalculate_girders()

    def create_layout_tab(self):
        layout_widget = QWidget()
        layout_widget.setStyleSheet("background-color: #f5f5f5;")
        layout_layout = QVBoxLayout(layout_widget)
        # CHANGED: Reduced all margins significantly
        layout_layout.setContentsMargins(18, 6, 18, 12)
        # CHANGED: Set spacing to 0 to remove gap between title and grid
        layout_layout.setSpacing(0)

        title_label = QLabel("Inputs:")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #000;")
        layout_layout.addWidget(title_label)
        layout_layout.addSpacing(8)

        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        grid.setContentsMargins(0, 0, 0, 0)

        def _label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size: 11px; color: #000;")
            lbl.setMinimumWidth(180)
            return lbl

        self.girder_spacing = QLineEdit()
        self.girder_spacing.setValidator(QDoubleValidator(0.01, 50.0, 3))
        self.girder_spacing.setText(str(DEFAULT_GIRDER_SPACING))
        self.style_input_field(self.girder_spacing)
        self.girder_spacing.textChanged.connect(self.on_girder_spacing_changed)

        self.no_of_girders = QLineEdit()
        self.no_of_girders.setValidator(QIntValidator(2, 100))
        self.style_input_field(self.no_of_girders)
        self.no_of_girders.textChanged.connect(self.on_no_of_girders_changed)

        grid.addWidget(_label("Girder Spacing (m):"), 0, 0, Qt.AlignLeft)
        grid.addWidget(self.girder_spacing, 0, 1)
        grid.addWidget(_label("No. of Girders:"), 0, 2, Qt.AlignLeft)
        grid.addWidget(self.no_of_girders, 0, 3)

        self.deck_overhang = QLineEdit()
        self.deck_overhang.setValidator(QDoubleValidator(0.0, 10.0, 3))
        self.deck_overhang.setText(str(DEFAULT_DECK_OVERHANG))
        self.style_input_field(self.deck_overhang)
        self.deck_overhang.textChanged.connect(self.on_deck_overhang_changed)

        values_adjusted_label = QLabel("Values adjusted for:")
        values_adjusted_label.setStyleSheet("font-size: 11px; color: #5b5b5b; font-style: italic;")

        grid.addWidget(_label("Deck Overhang Width (m):"), 1, 0, Qt.AlignLeft)
        grid.addWidget(self.deck_overhang, 1, 1)
        #grid.addWidget(values_adjusted_label, 1, 2, 1, 2, Qt.AlignLeft)

        self.overall_bridge_width_display = QLineEdit()
        self.style_input_field(self.overall_bridge_width_display)
        self.overall_bridge_width_display.setReadOnly(True)
        self.overall_bridge_width_display.setEnabled(False)

        grid.addWidget(_label("Overall Bridge Width (m):"), 2, 0, Qt.AlignLeft)
        grid.addWidget(self.overall_bridge_width_display, 2, 1)

        self.deck_thickness = QLineEdit()
        self.deck_thickness.setValidator(QDoubleValidator(0.0, 500.0, 0))
        self.style_input_field(self.deck_thickness)

        self.footpath_thickness = QLineEdit()
        self.footpath_thickness.setValidator(QDoubleValidator(0.0, 500.0, 0))
        self.style_input_field(self.footpath_thickness)

        grid.addWidget(_label("Deck Thickness (mm):"), 3, 0, Qt.AlignLeft)
        grid.addWidget(self.deck_thickness, 3, 1)
        grid.addWidget(_label("Footpath Thickness (mm):"), 4, 2, Qt.AlignLeft)
        grid.addWidget(self.footpath_thickness, 4, 3)

        self.footpath_width = QLineEdit()
        self.footpath_width.setValidator(QDoubleValidator(MIN_FOOTPATH_WIDTH, 5.0, 3))
        self.footpath_width.textChanged.connect(self.on_footpath_width_changed)
        self.style_input_field(self.footpath_width)
        self.footpath_width.setText(f"{MIN_FOOTPATH_WIDTH:.2f}")

        grid.addWidget(_label("Footpath Width (m):"), 4, 0, Qt.AlignLeft)
        grid.addWidget(self.footpath_width, 4, 1)

        layout_layout.addLayout(grid)
        # CHANGED: Add stretch at bottom to push content up
        layout_layout.addStretch()
        
        self.input_tabs.addTab(layout_widget, "Layout")
    def create_crash_barrier_tab(self):
        crash_widget = QWidget()
        crash_widget.setStyleSheet("background-color: #f5f5f5;")
        crash_layout = QVBoxLayout(crash_widget)
        crash_layout.setContentsMargins(18, 6, 18, 12)
        crash_layout.setSpacing(0)

        card, card_layout = self._create_section_card("Crash Barrier Inputs:")
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        def add_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 11px; color: #000;")
            label.setMinimumWidth(210)
            grid.addWidget(label, row, 0, Qt.AlignLeft)
            grid.addWidget(widget, row, 1)

        self.crash_barrier_type = QComboBox()
        self.crash_barrier_type.addItems(VALUES_CRASH_BARRIER_TYPE)
        self.style_input_field(self.crash_barrier_type)
        self.crash_barrier_type.currentTextChanged.connect(self.on_crash_barrier_type_changed)
        add_row(0, "Type:", self.crash_barrier_type)

        self.crash_barrier_density = QLineEdit()
        self.crash_barrier_density.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.style_input_field(self.crash_barrier_density)
        add_row(1, "Material Density (kN/m^3):", self.crash_barrier_density)

        self.crash_barrier_width = QLineEdit()
        self.crash_barrier_width.setValidator(QDoubleValidator(0.0, 2.0, 3))
        self.crash_barrier_width.setText(str(DEFAULT_CRASH_BARRIER_WIDTH))
        self.style_input_field(self.crash_barrier_width)
        self.crash_barrier_width.textChanged.connect(self.recalculate_girders)
        add_row(2, "Width (m):", self.crash_barrier_width)

        self.crash_barrier_height = QLineEdit()
        self.crash_barrier_height.setValidator(QDoubleValidator(0.0, 3.0, 3))
        self.style_input_field(self.crash_barrier_height)
        add_row(3, "Height (m):", self.crash_barrier_height)

        self.crash_barrier_area = QLineEdit()
        self.crash_barrier_area.setValidator(QDoubleValidator(0.0, 10.0, 4))
        self.style_input_field(self.crash_barrier_area)
        add_row(4, "Area (m^2):", self.crash_barrier_area)

        card_layout.addLayout(grid)
        crash_layout.addWidget(card)
        crash_layout.addStretch()
        self.input_tabs.addTab(crash_widget, "Crash Barrier")

    def create_median_tab(self):
        median_widget = QWidget()
        median_widget.setStyleSheet("background-color: #f5f5f5;")
        median_layout = QVBoxLayout(median_widget)
        median_layout.setContentsMargins(18, 6, 18, 12)
        median_layout.setSpacing(0)

        card, card_layout = self._create_section_card("Median Inputs:")
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        def add_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 11px; color: #000;")
            label.setMinimumWidth(210)
            grid.addWidget(label, row, 0, Qt.AlignLeft)
            grid.addWidget(widget, row, 1)

        self.median_type = QComboBox()
        self.median_type.addItems(VALUES_MEDIAN_TYPE)
        self.style_input_field(self.median_type)
        add_row(0, "Type:", self.median_type)

        self.median_density = QLineEdit()
        self.median_density.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.style_input_field(self.median_density)
        add_row(1, "Material Density (kN/m^3):", self.median_density)

        self.median_width = QLineEdit()
        self.median_width.setValidator(QDoubleValidator(0.0, 3.0, 3))
        self.style_input_field(self.median_width)
        add_row(2, "Width (m):", self.median_width)

        self.median_height = QLineEdit()
        self.median_height.setValidator(QDoubleValidator(0.0, 3.0, 3))
        self.style_input_field(self.median_height)
        add_row(3, "Height (m):", self.median_height)

        self.median_area = QLineEdit()
        self.median_area.setValidator(QDoubleValidator(0.0, 10.0, 4))
        self.style_input_field(self.median_area)
        add_row(4, "Area (m^2):", self.median_area)

        card_layout.addLayout(grid)
        median_layout.addWidget(card)
        median_layout.addStretch()
        self.input_tabs.addTab(median_widget, "Median")

    def create_railing_tab(self):
        railing_widget = QWidget()
        railing_widget.setStyleSheet("background-color: #f5f5f5;")
        railing_layout = QVBoxLayout(railing_widget)
        railing_layout.setContentsMargins(18, 6, 18, 12)
        railing_layout.setSpacing(0)

        card, card_layout = self._create_section_card("Railing Inputs:")
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        def add_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 11px; color: #000;")
            label.setMinimumWidth(180)
            grid.addWidget(label, row, 0, Qt.AlignLeft)
            grid.addWidget(widget, row, 1)

        self.railing_type = QComboBox()
        self.railing_type.addItems(VALUES_RAILING_TYPE)
        self.style_input_field(self.railing_type)
        add_row(0, "Type:", self.railing_type)

        self.railing_width = QLineEdit()
        self.railing_width.setValidator(QDoubleValidator(0.0, 2000.0, 1))
        self.railing_width.setText(f"{DEFAULT_RAILING_WIDTH * 1000:.0f}")
        self.style_input_field(self.railing_width)
        self.railing_width.textChanged.connect(self.recalculate_girders)
        add_row(1, "Width (mm):", self.railing_width)

        self.railing_height = QLineEdit()
        self.railing_height.setValidator(QDoubleValidator(MIN_RAILING_HEIGHT, 3.0, 3))
        self.style_input_field(self.railing_height)
        self.railing_height.editingFinished.connect(self.validate_railing_height)
        add_row(2, "Height (m):", self.railing_height)

        load_row = QHBoxLayout()
        load_row.setContentsMargins(0, 0, 0, 0)
        load_row.setSpacing(12)

        self.railing_load_mode = QComboBox()
        self.railing_load_mode.addItems(["Automatic (IRC 6)", "User-defined"])
        self.style_input_field(self.railing_load_mode)
        self.railing_load_mode.currentTextChanged.connect(self.on_railing_load_mode_changed)
        load_row.addWidget(self.railing_load_mode)

        self.railing_load_value = QLineEdit()
        self.railing_load_value.setValidator(QDoubleValidator(0.0, 50.0, 2))
        self.railing_load_value.setPlaceholderText("Value")
        self.railing_load_value.setEnabled(False)
        self.style_input_field(self.railing_load_value)
        load_row.addWidget(self.railing_load_value)

        load_container = QWidget()
        load_container.setLayout(load_row)
        add_row(3, "Load (kN/m):", load_container)

        card_layout.addLayout(grid)
        railing_layout.addWidget(card)
        railing_layout.addStretch()
        self.input_tabs.addTab(railing_widget, "Railing")

    def create_wearing_course_tab(self):
        wearing_widget = QWidget()
        wearing_widget.setStyleSheet("background-color: #f5f5f5;")
        wearing_layout = QVBoxLayout(wearing_widget)
        wearing_layout.setContentsMargins(18, 6, 18, 12)
        wearing_layout.setSpacing(0)

        card, card_layout = self._create_section_card("Wearing Course Inputs:")
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        def add_row(row, label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 11px; color: #000;")
            label.setMinimumWidth(200)
            grid.addWidget(label, row, 0, Qt.AlignLeft)
            grid.addWidget(widget, row, 1)

        self.wearing_material = QComboBox()
        self.wearing_material.addItems(VALUES_WEARING_COAT_MATERIAL)
        self.style_input_field(self.wearing_material)
        add_row(0, "Material:", self.wearing_material)

        self.wearing_density = QLineEdit()
        self.wearing_density.setValidator(QDoubleValidator(0.0, 40.0, 2))
        self.style_input_field(self.wearing_density)
        add_row(1, "Density (kN/m^3):", self.wearing_density)

        self.wearing_thickness = QLineEdit()
        self.wearing_thickness.setValidator(QDoubleValidator(0.0, 200.0, 1))
        self.style_input_field(self.wearing_thickness)
        add_row(2, "Thickness (mm):", self.wearing_thickness)

        card_layout.addLayout(grid)
        wearing_layout.addWidget(card)
        wearing_layout.addStretch()
        self.input_tabs.addTab(wearing_widget, "Wearing Course")

    def create_lane_details_tab(self):
        lane_widget = QWidget()
        lane_widget.setStyleSheet("background-color: #f5f5f5;")
        lane_layout = QVBoxLayout(lane_widget)
        lane_layout.setContentsMargins(18, 6, 18, 12)
        lane_layout.setSpacing(0)

        card, card_layout = self._create_section_card("Inputs:")

        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(12)

        lanes_label = QLabel("No. of Traffic Lanes:")
        lanes_label.setStyleSheet("font-size: 11px; color: #000;")
        selector_layout.addWidget(lanes_label)

        self.lane_count_combo = QComboBox()
        self.lane_count_combo.addItems([str(i) for i in range(1, 7)])
        self.style_input_field(self.lane_count_combo)
        self.lane_count_combo.currentTextChanged.connect(self.on_lane_count_changed)
        selector_layout.addWidget(self.lane_count_combo)
        selector_layout.addStretch()

        card_layout.addLayout(selector_layout)

        self.lane_table = QTableWidget()
        self.lane_table.setColumnCount(3)
        self.lane_table.setHorizontalHeaderLabels([
            "Traffic Lane Number",
            "Distance from inner edge of crash barrier to left edge of lane (m)",
            "Lane Width (m)"
        ])
        header = self.lane_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.lane_table.verticalHeader().setVisible(False)
        self.lane_table.setAlternatingRowColors(True)
        self.lane_table.setStyleSheet("""
            QTableWidget { 
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
                gridline-color: #e0e0e0;
                border: 1px solid #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:hover {
                background-color: #e8f4f8;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #333;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
                font-size: 11px;
            }
        """)

        card_layout.addWidget(self.lane_table)
        lane_layout.addWidget(card)
        lane_layout.addStretch()

        self.input_tabs.addTab(lane_widget, "Lane Details")
        self._update_lane_details_rows(self.lane_count_combo.currentText())
    
    def _update_lane_details_rows(self, count):
        try:
            num_lanes = int(count)
            self.lane_table.setRowCount(num_lanes)
            
            for i in range(num_lanes):
                # Lane number (non-editable)
                lane_num_item = QTableWidgetItem(str(i + 1))
                lane_num_item.setFlags(lane_num_item.flags() & ~Qt.ItemIsEditable)
                lane_num_item.setTextAlignment(Qt.AlignCenter)
                self.lane_table.setItem(i, 0, lane_num_item)
                
                # Distance field (editable)
                if not self.lane_table.item(i, 1):
                    self.lane_table.setItem(i, 1, QTableWidgetItem(""))
                
                # Width field (editable)
                if not self.lane_table.item(i, 2):
                    self.lane_table.setItem(i, 2, QTableWidgetItem(""))
        except ValueError:
            pass

    def update_footpath_value(self, footpath_value):
        self.footpath_value = footpath_value
        if hasattr(self, "footpath_width"):
            self.footpath_width.setEnabled(footpath_value != "None")
            self.footpath_thickness.setEnabled(footpath_value != "None")
        self.recalculate_girders()
        self.footpath_changed.emit(footpath_value)

    def get_overall_bridge_width(self):
        try:
            overall_width = self.carriageway_width
            if self.footpath_value != "None":
                footpath_width = float(self.footpath_width.text()) if self.footpath_width.text() else 0
                num_footpaths = 2 if self.footpath_value == "Both" else (1 if self.footpath_value == "Single Sided" else 0)
                overall_width += footpath_width * num_footpaths

            crash_barrier_width = float(self.crash_barrier_width.text()) if self.crash_barrier_width.text() else DEFAULT_CRASH_BARRIER_WIDTH
            overall_width += crash_barrier_width * 2

            if self.footpath_value != "None":
                railing_width_text = self.railing_width.text() if hasattr(self, "railing_width") else ""
                if railing_width_text:
                    railing_width = float(railing_width_text) / 1000.0
                else:
                    railing_width = DEFAULT_RAILING_WIDTH
                overall_width += railing_width * 2

            return overall_width
        except:
            return self.carriageway_width

    def _update_overall_bridge_width_display(self):
        if hasattr(self, "overall_bridge_width_display"):
            try:
                overall_width = self.get_overall_bridge_width()
                self.overall_bridge_width_display.setText(f"{overall_width:.3f}")
            except:
                self.overall_bridge_width_display.clear()

    def recalculate_girders(self):
        if self.updating_fields:
            return
        try:
            self._update_overall_bridge_width_display()
            overall_width = self.get_overall_bridge_width()
            spacing = float(self.girder_spacing.text()) if self.girder_spacing.text() else DEFAULT_GIRDER_SPACING
            overhang = float(self.deck_overhang.text()) if self.deck_overhang.text() else DEFAULT_DECK_OVERHANG
            if spacing >= overall_width or overhang >= overall_width:
                self.no_of_girders.setText("")
                return
            if spacing > 0:
                no_girders = int(round((overall_width - 2 * overhang) / spacing)) + 1
                if no_girders >= 2:
                    self.updating_fields = True
                    self.no_of_girders.setText(str(no_girders))
                    self.updating_fields = False
        except:
            pass

    def on_girder_spacing_changed(self):
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
                    if no_girders > 1:
                        new_spacing = (overall_width - 2 * overhang) / (no_girders - 1)
                        self.updating_fields = True
                        self.girder_spacing.setText(f"{new_spacing:.3f}")
                        self.updating_fields = False
            except:
                pass

    def on_footpath_width_changed(self):
        if not self.updating_fields:
            self.recalculate_girders()

    def validate_footpath_width(self):
        try:
            if self.footpath_width.text():
                width = float(self.footpath_width.text())
                if width < MIN_FOOTPATH_WIDTH:
                    QMessageBox.critical(self, "Footpath Width Error",
                                         f"Footpath width must be at least {MIN_FOOTPATH_WIDTH} m as per IRC 5 Clause 104.3.6.")
        except:
            pass

    def validate_railing_height(self):
        try:
            if self.railing_height.text():
                height = float(self.railing_height.text())
                if height < MIN_RAILING_HEIGHT:
                    QMessageBox.critical(self, "Railing Height Error",
                                         f"Railing height must be at least {MIN_RAILING_HEIGHT} m as per IRC 5 Clauses 109.7.2.3 and 109.7.2.4.")
        except:
            pass

    def update_footpath_thickness(self):
        if self.deck_thickness.text() and not self.footpath_thickness.text():
            self.footpath_thickness.setText(self.deck_thickness.text())

    def on_crash_barrier_type_changed(self, barrier_type):
        if (barrier_type in ["Flexible", "Semi-Rigid"]) and (self.footpath_value == "None"):
            QMessageBox.critical(self, "Crash Barrier Type Not Permitted",
                                 f"{barrier_type} crash barriers are not permitted on bridges without an outer footpath per IRC 5 Clause 109.6.4.")

    def on_railing_load_mode_changed(self, mode):
        if not hasattr(self, "railing_load_value"):
            return
        is_auto = mode.startswith("Automatic")
        self.railing_load_value.setEnabled(not is_auto)
        if is_auto:
            self.railing_load_value.clear()

    def on_lane_count_changed(self, text):
        self._update_lane_details_rows(text)

    def _update_lane_details_rows(self, count):
        try:
            total_rows = int(count)
        except (TypeError, ValueError):
            total_rows = 1
        if not hasattr(self, "lane_table"):
            return
        self.lane_table.setRowCount(total_rows)
        for row in range(total_rows):
            lane_item = QTableWidgetItem(str(row + 1))
            lane_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.lane_table.setItem(row, 0, lane_item)
            for col in range(1, self.lane_table.columnCount()):
                existing_item = self.lane_table.item(row, col)
                if existing_item is None:
                    self.lane_table.setItem(row, col, QTableWidgetItem(""))

    def _show_placeholder_message(self, action_name):
        QMessageBox.information(self, action_name, "This action will be available in an upcoming update.")

class SectionPropertiesTab(QWidget):
    """Sub-tab for Section Properties with custom navigation layout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_buttons = []
        self.init_ui()

    def init_ui(self):
        """Initialize styled navigation and content panels."""
        self.setStyleSheet("background-color: #f0f0f0;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Top navigation bar (horizontal)
        nav_bar = QWidget()
        nav_bar.setStyleSheet("background-color: white;")
        nav_bar_layout = QHBoxLayout(nav_bar)
        nav_bar_layout.setContentsMargins(0, 0, 0, 0)
        nav_bar_layout.setSpacing(0)
        
        main_layout.addWidget(nav_bar)

        # Content frame
        content_frame = QFrame()
        content_frame.setObjectName("sectionContentFrame")
        content_frame.setStyleSheet("""
            QFrame#sectionContentFrame {
                background-color: #f0f0f0;
                border: none;
            }
        """)
        content_inner_layout = QVBoxLayout(content_frame)
        content_inner_layout.setContentsMargins(0, 0, 0, 0)
        content_inner_layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setObjectName("sectionStack")
        self.stack.setStyleSheet("QStackedWidget#sectionStack { background-color: transparent; }")
        content_inner_layout.addWidget(self.stack)

        main_layout.addWidget(content_frame, 1)

        sections = [
            ("Girder Details:", GirderDetailsTab),
            ("Stiffener Details:", StiffenerDetailsTab),
            ("Cross-Bracing Details:", CrossBracingDetailsTab),
            ("End Diaphragm Details:", EndDiaphragmDetailsTab),
        ]

        for i, (label, widget_class) in enumerate(sections):
            btn = QPushButton(label)
            btn.setObjectName("sectionNavBtn")
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton#sectionNavBtn {
                    background-color: white;
                    color: #333;
                    border: 1px solid #b0b0b0;
                    border-right: none;
                    padding: 6px 14px;
                    text-align: center;
                    font-size: 10px;
                    font-weight: normal;
                    min-height: 26px;
                }
                QPushButton#sectionNavBtn:first {
                    border-top-left-radius: 5px;
                    border-bottom-left-radius: 5px;
                }
                QPushButton#sectionNavBtn:last {
                    border-right: 1px solid #b0b0b0;
                    border-top-right-radius: 5px;
                    border-bottom-right-radius: 5px;
                }
                QPushButton#sectionNavBtn:checked {
                    background-color: #90AF13;
                    color: white;
                    font-weight: bold;
                    border: 1px solid #90AF13;
                }
                QPushButton#sectionNavBtn:hover:!checked {
                    background-color: #f5f5f5;
                }
            """)
            btn.clicked.connect(lambda checked, idx=i: self.switch_section(idx))
            self.nav_buttons.append(btn)
            nav_bar_layout.addWidget(btn)

            section_widget = widget_class()
            self.stack.addWidget(section_widget)

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
            self.stack.setCurrentIndex(0)

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        main_layout.addSpacing(6)
        main_layout.addWidget(action_bar)

    def switch_section(self, index):
        """Switch the stacked widget page and update navigation states."""
        self.stack.setCurrentIndex(index)
        for btn_index, button in enumerate(self.nav_buttons):
            button.setChecked(btn_index == index)


class GirderDetailsTab(QWidget):
    """Tab for Girder Details styled to match the provided reference."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.welded_rows = []
        self.rolled_rows = []
        self.section_property_inputs = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        main_layout.addWidget(scroll)

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        main_layout.addSpacing(6)
        main_layout.addWidget(action_bar)

        content = QWidget()
        scroll.setWidget(content)
        content.setStyleSheet("background-color: white;")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 0, 10, 10)
        content_layout.setSpacing(12)

        content_layout.addWidget(self._build_overview_card())
        content_layout.addWidget(self._build_section_card())
        content_layout.addStretch()

    def _build_overview_card(self):
        card = self._create_card_frame()
        layout = QGridLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(12)

        self.select_girder_combo = QComboBox()
        self.select_girder_combo.addItems(["Girder 1", "Girder 2", "Girder 3", "Girder 4", "Girder 5", "All"])
        apply_field_style(self.select_girder_combo)
        self._set_field_width(self.select_girder_combo)

        self.span_combo = QComboBox()
        self.span_combo.addItems(["Custom", "Full Length"])
        apply_field_style(self.span_combo)
        self._set_field_width(self.span_combo)

        self.member_id_input = QLineEdit("G1-1")
        apply_field_style(self.member_id_input)
        self._set_field_width(self.member_id_input)

        self.member_select_combo = QComboBox()
        self.member_select_combo.addItems(["Girder 1", "Girder 2", "Girder 3", "Girder 4", "Girder 5"])
        apply_field_style(self.member_select_combo)
        self._set_field_width(self.member_select_combo)

        self.distance_start_input = QLineEdit("0")
        self.distance_end_input = QLineEdit("30")
        apply_field_style(self.distance_start_input)
        apply_field_style(self.distance_end_input)
        self._set_field_width(self.distance_start_input, 80)
        self._set_field_width(self.distance_end_input, 80)

        self.length_input = QLineEdit("30")
        apply_field_style(self.length_input)
        self._set_field_width(self.length_input)

        layout.addWidget(self._create_label("Select Girder:"), 0, 0)
        layout.addWidget(self.select_girder_combo, 0, 1)
        layout.addWidget(self._create_label("Span:"), 0, 2)
        layout.addWidget(self.span_combo, 0, 3)

        layout.addWidget(self._create_label("Member ID:"), 1, 0)
        layout.addWidget(self.member_id_input, 1, 1)
        layout.addWidget(self._create_label("Length (m):"), 1, 2)
        layout.addWidget(self.length_input, 1, 3)

        layout.addWidget(self._create_label("Distance from left edge (m):"), 2, 0)
        layout.addLayout(self._build_distance_row(), 2, 1)

        layout.addWidget(self._create_label("Member:"), 2, 2)
        layout.addWidget(self.member_select_combo, 2, 3)

        return card

    def _build_distance_row(self):
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(self._create_small_label("Start"))
        row.addWidget(self.distance_start_input)
        row.addWidget(self._create_small_label("End"))
        row.addWidget(self.distance_end_input)
        return row

    def _build_section_card(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)

        # Left side - two bordered boxes stacked vertically
        left_column = QWidget()
        left_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        left_column_layout = QVBoxLayout(left_column)
        left_column_layout.setContentsMargins(0, 0, 0, 0)
        left_column_layout.setSpacing(12)

        # Section Inputs box (single frame containing all fields)
        section_inputs_box = self._create_inner_box()
        section_inputs_layout = QVBoxLayout(section_inputs_box)
        section_inputs_layout.setContentsMargins(12, 10, 12, 10)
        section_inputs_layout.setSpacing(10)

        section_inputs_title = self._create_label("Section Inputs:")
        section_inputs_layout.addWidget(section_inputs_title)

        inputs_grid = QGridLayout()
        inputs_grid.setContentsMargins(0, 0, 0, 0)
        inputs_grid.setHorizontalSpacing(16)
        inputs_grid.setVerticalSpacing(12)
        inputs_grid.setColumnMinimumWidth(0, 150)
        inputs_grid.setColumnStretch(0, 0)
        inputs_grid.setColumnStretch(1, 1)

        self.design_combo = QComboBox()
        self.design_combo.addItems(["Customized", "Optimized"])
        apply_field_style(self.design_combo)
        row = self._add_box_row(inputs_grid, 0, "Design:", self.design_combo)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Welded", "Rolled"])
        apply_field_style(self.type_combo)
        row = self._add_box_row(inputs_grid, row, "Type:", self.type_combo)

        self.symmetry_combo = QComboBox()
        self.symmetry_combo.addItems(["Girder Symmetric", "Girder Unsymmetric"])
        apply_field_style(self.symmetry_combo)
        row = self._add_box_row(inputs_grid, row, "Symmetry:", self.symmetry_combo)

        self.total_depth_input = self._create_line_edit()
        row = self._add_box_row(inputs_grid, row, "Total Depth (mm):", self.total_depth_input, self.welded_rows)

        self.web_thickness_combo = QComboBox()
        self.web_thickness_combo.addItems(["All", "Custom"])
        apply_field_style(self.web_thickness_combo)
        row = self._add_box_row(inputs_grid, row, "Web Thickness (mm):", self.web_thickness_combo, self.welded_rows)

        self.top_width_input = self._create_line_edit()
        row = self._add_box_row(inputs_grid, row, "Width of Top Flange (mm):", self.top_width_input, self.welded_rows)

        self.top_thickness_combo = QComboBox()
        self.top_thickness_combo.addItems(["All", "Custom"])
        apply_field_style(self.top_thickness_combo)
        row = self._add_box_row(inputs_grid, row, "Top Flange Thickness (mm):", self.top_thickness_combo, self.welded_rows)

        self.bottom_width_input = self._create_line_edit()
        row = self._add_box_row(inputs_grid, row, "Width of Bottom Flange (mm):", self.bottom_width_input, self.welded_rows)

        self.bottom_thickness_combo = QComboBox()
        self.bottom_thickness_combo.addItems(["All", "Custom"])
        apply_field_style(self.bottom_thickness_combo)
        row = self._add_box_row(inputs_grid, row, "Bottom Flange Thickness (mm):", self.bottom_thickness_combo, self.welded_rows)

        self.is_section_combo = QComboBox()
        self.is_section_combo.addItems([
            "ISMB 500", "ISMB 550", "ISMB 600",
            "ISWB 500", "ISWB 550", "ISWB 600"
        ])
        apply_field_style(self.is_section_combo)
        self._add_box_row(inputs_grid, row, "IS Section:", self.is_section_combo, self.rolled_rows)

        # Torsional restraint group heading (only shown for welded)
        torsion_heading = self._create_label("Torsional & Web Details:")
        torsion_heading.setProperty("category", "torsion")
        torsion_heading.setStyleSheet("font-size: 11px; font-weight: 600; color: #4b4b4b; border: none;")
        inputs_grid.addWidget(torsion_heading, row, 0, 1, 2)
        self.torsion_heading = torsion_heading
        row += 1

        self.torsion_combo = QComboBox()
        self.torsion_combo.addItems(VALUES_TORSIONAL_RESTRAINT)
        apply_field_style(self.torsion_combo)
        row = self._add_box_row(inputs_grid, row, "Torsional Restraint:", self.torsion_combo, self.welded_rows)

        self.warping_combo = QComboBox()
        self.warping_combo.addItems(VALUES_WARPING_RESTRAINT)
        apply_field_style(self.warping_combo)
        row = self._add_box_row(inputs_grid, row, "Warping Restraint:", self.warping_combo, self.welded_rows)

        self.web_type_combo = QComboBox()
        self.web_type_combo.addItems(["Thin Web with ITS", "Thick Web"])
        apply_field_style(self.web_type_combo)
        self._add_box_row(inputs_grid, row, "Web Type*:", self.web_type_combo, self.welded_rows)

        section_inputs_layout.addLayout(inputs_grid)
        left_column_layout.addWidget(section_inputs_box)

        main_layout.addWidget(left_column)

        # Right side - image + section properties box
        right_column = QWidget()
        right_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_column_layout = QVBoxLayout(right_column)
        right_column_layout.setContentsMargins(0, 0, 0, 0)
        right_column_layout.setSpacing(12)

        # Dynamic image box
        image_box = self._create_inner_box()
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(10, 10, 10, 10)
        image_layout.setSpacing(5)

        self.dynamic_image_label = QLabel("Welded Girder")
        self.dynamic_image_label.setAlignment(Qt.AlignCenter)
        self.dynamic_image_label.setMinimumSize(240, 140)
        self.dynamic_image_label.setStyleSheet("QLabel { border: 1px solid #d0d0d0; border-radius: 4px; background-color: #fafafa; font-weight: bold; color: #5b5b5b; }")
        image_layout.addWidget(self.dynamic_image_label)

        right_column_layout.addWidget(image_box)

        # Section Properties box
        props_box = self._create_inner_box()
        props_layout = QVBoxLayout(props_box)
        props_layout.setContentsMargins(12, 10, 12, 10)
        props_layout.setSpacing(10)

        props_title = self._create_label("Section Properties:")
        props_layout.addWidget(props_title)

        properties_grid = QGridLayout()
        properties_grid.setContentsMargins(0, 0, 0, 0)
        properties_grid.setHorizontalSpacing(12)
        properties_grid.setVerticalSpacing(10)
        properties_grid.setColumnMinimumWidth(0, 140)
        properties_grid.setColumnStretch(0, 0)
        properties_grid.setColumnStretch(1, 1)

        property_fields = [
            "Mass, M (Kg/m)",
            "Sectional Area, a (cm2)",
            "2nd Moment of Area, Iz (cm4)",
            "2nd Moment of Area, Iy (cm4)",
            "Radius of Gyration, rz (cm)",
            "Radius of Gyration, ry (cm)",
            "Elastic Modulus, Zz (cm3)",
            "Elastic Modulus, Zy (cm3)",
            "Plastic Modulus, Zuz (cm3)",
            "Plastic Modulus, Zuy (cm3)",
            "Torsion Constant, It (cm4)",
            "Warping Constant, Iw (cm6)"
        ]

        for index, text in enumerate(property_fields):
            label = self._create_small_label(text)
            line_edit = self._create_line_edit()
            line_edit.setPlaceholderText("")
            properties_grid.addWidget(label, index, 0)
            properties_grid.addWidget(line_edit, index, 1)
            self.section_property_inputs[text] = line_edit

        props_layout.addLayout(properties_grid)
        right_column_layout.addWidget(props_box)

        main_layout.addWidget(right_column)

        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        self._on_type_changed(self.type_combo.currentText())

        return container

    def _create_card_frame(self):
        frame = QFrame()
        frame.setObjectName("girderCard")
        frame.setStyleSheet("QFrame#girderCard { background-color: white; border: 1px solid #cfcfcf; border-radius: 10px; }")
        return frame

    def _create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 12px; color: #2f2f2f; font-weight: 600; background: transparent;")
        label.setAutoFillBackground(False)
        return label

    def _create_small_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 10px; color: #5a5a5a; background: transparent;")
        label.setAutoFillBackground(False)
        return label

    def _create_line_edit(self):
        line_edit = QLineEdit()
        apply_field_style(line_edit)
        return line_edit

    def _add_section_row(self, layout, row, text, widget, tracker=None):
        label = self._create_label(text)
        widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._set_field_width(widget)
        layout.addWidget(label, row, 0)
        layout.addWidget(widget, row, 1)
        if tracker is not None:
            tracker.append((label, widget))
        return row + 1

    def _set_field_width(self, widget, width=230):
        widget.setMaximumWidth(width)
        widget.setMinimumWidth(min(width, 160))

    def _on_type_changed(self, text):
        is_welded = text.lower() == "welded"
        self._set_row_visibility(self.welded_rows, is_welded)
        self._set_row_visibility(self.rolled_rows, not is_welded)
        if hasattr(self, "torsion_heading"):
            self.torsion_heading.setVisible(is_welded)
        if is_welded:
            self.dynamic_image_label.setText("Welded Girder")
        else:
            self.dynamic_image_label.setText("Rolled Section")

    def _set_row_visibility(self, rows, visible):
        for label, widget in rows:
            label.setVisible(visible)
            widget.setVisible(visible)

    def _create_inner_box(self):
        """Create a bordered box for grouped controls"""
        box = QFrame()
        box.setStyleSheet(
            "QFrame {"
            "   border: 1px solid #b0b0b0;"
            "   border-radius: 6px;"
            "   background-color: #ffffff;"
            "}"
            "QFrame QComboBox, QFrame QLineEdit {"
            "   border: none;"
            "   border-bottom: 1px solid #d0d0d0;"
            "   border-radius: 0px;"
            "   min-height: 28px;"
            "   padding: 4px 8px;"
            "   background-color: #ffffff;"
            "}"
            "QFrame QComboBox:hover, QFrame QLineEdit:hover {"
            "   border-bottom: 1px solid #5d5d5d;"
            "}"
            "QFrame QComboBox:focus, QFrame QLineEdit:focus {"
            "   border-bottom: 1px solid #90AF13;"
            "}"
            "QFrame QLabel {"
            "   border: none;"
            "   padding: 0px;"
            "   margin: 0px;"
            "}"
        )
        return box

    def _create_small_label(self, text):
        """Create a smaller label for compact layouts"""
        label = QLabel(text)
        label.setStyleSheet(
            "QLabel {"
            "   color: #2b2b2b;"
            "   font-size: 11px;"
            "   font-weight: 500;"
            "   background: transparent;"
            "   border: none;"
            "   padding: 0px;"
            "   margin: 0px;"
            "}"
        )
        label.setAutoFillBackground(False)
        return label

    def _add_box_row(self, layout, row, label_text, widget, visibility_list=None):
        """Add a row to a box grid layout"""
        label = self._create_small_label(label_text)
        layout.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(widget, row, 1)
        if visibility_list is not None:
            visibility_list.append((label, widget))
        return row + 1


class StiffenerDetailsTab(QWidget):
    """Tab for Stiffener Details with card layout"""

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

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        main_layout.addSpacing(6)
        main_layout.addWidget(action_bar)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(16)

        # Primary card containing inputs + description
        primary_card = self._create_card_frame()
        card_layout = QHBoxLayout(primary_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(16)

        left_column = QWidget()
        left_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)

        # Girder selection
        self.girder_member_combo = QComboBox()
        self.girder_member_combo.addItems(["G1-1", "G1-2", "G1-3", "All"])
        apply_field_style(self.girder_member_combo)

        selection_box = self._create_inner_box()
        selection_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        selection_layout = QVBoxLayout(selection_box)
        selection_layout.setContentsMargins(12, 10, 12, 10)
        selection_layout.setSpacing(8)
        selection_layout.addWidget(self._create_heading_label("Select Girder Member"))
        self.girder_member_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        selection_layout.addWidget(self.girder_member_combo)
        left_layout.addWidget(selection_box)

        # Stiffener inputs box
        inputs_box = self._create_inner_box()
        inputs_layout = QVBoxLayout(inputs_box)
        inputs_layout.setContentsMargins(12, 10, 12, 10)
        inputs_layout.setSpacing(10)
        inputs_layout.addWidget(self._create_heading_label("Stiffener Inputs"))

        inputs_grid = QGridLayout()
        inputs_grid.setContentsMargins(0, 0, 0, 0)
        inputs_grid.setHorizontalSpacing(16)
        inputs_grid.setVerticalSpacing(12)
        inputs_grid.setColumnMinimumWidth(0, 150)
        inputs_grid.setColumnStretch(0, 0)
        inputs_grid.setColumnStretch(1, 1)

        self.intermediate_combo = QComboBox()
        self.intermediate_combo.addItems(["No", "Yes - At Supports", "Yes - Spaced"])
        apply_field_style(self.intermediate_combo)
        row = self._add_form_row(inputs_grid, 0, "Intermediate Stiffener:", self.intermediate_combo)

        self.spacing_field = OptimizableField("Intermediate Stiffener Spacing")
        self.spacing_field.mode_combo.clear()
        self.spacing_field.mode_combo.addItems(["NA", "Optimized", "Customized"])
        self.spacing_field.on_mode_changed(self.spacing_field.mode_combo.currentText())
        self._prepare_optimizable_field(self.spacing_field)
        row = self._add_form_row(inputs_grid, row, "Intermediate Stiffener Spacing:", self.spacing_field)

        self.longitudinal_combo = QComboBox()
        self.longitudinal_combo.addItems(["None", "Yes and 1 stiffener", "Yes and 2 stiffeners"])
        apply_field_style(self.longitudinal_combo)
        row = self._add_form_row(inputs_grid, row, "Longitudinal Stiffener:", self.longitudinal_combo)

        self.intermediate_thick_combo = QComboBox()
        self.intermediate_thick_combo.addItems(["All", "Custom"])
        apply_field_style(self.intermediate_thick_combo)
        row = self._add_form_row(inputs_grid, row, "Intermediate Stiffener Thickness:", self.intermediate_thick_combo)

        self.long_thick_combo = QComboBox()
        self.long_thick_combo.addItems(["All", "Custom"])
        self.long_thick_combo.setEnabled(False)
        apply_field_style(self.long_thick_combo)
        row = self._add_form_row(inputs_grid, row, "Longitudinal Stiffener Thickness:", self.long_thick_combo)

        inputs_layout.addLayout(inputs_grid)

        # Web buckling section
        inputs_layout.addWidget(self._create_heading_label("Web Buckling Details"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(VALUES_STIFFENER_DESIGN)
        apply_field_style(self.method_combo)
        inputs_layout.addLayout(self._form_row(self._create_label("Shear Buckling Design Method:"), self.method_combo))

        left_layout.addWidget(inputs_box)

        card_layout.addWidget(left_column)

        # Description box on right
        right_column = QWidget()
        right_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)

        description_box = self._create_inner_box()
        desc_layout = QVBoxLayout(description_box)
        desc_layout.setContentsMargins(12, 10, 12, 10)
        desc_layout.setSpacing(8)
        desc_layout.addWidget(self._create_heading_label("Description"))
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setPlaceholderText("Describe stiffener assumptions or notes here.")
        self.description_text.setStyleSheet("QTextEdit { border: none; background: transparent; color: #3a3a3a; }")
        desc_layout.addWidget(self.description_text)
        right_layout.addWidget(description_box)

        card_layout.addWidget(right_column)
        container_layout.addWidget(primary_card)

        # Dynamic image box spanning width
        image_box = self._create_inner_box()
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(20, 16, 20, 16)
        image_layout.setSpacing(8)
        self.dynamic_image_label = QLabel("Dynamic Image")
        self.dynamic_image_label.setAlignment(Qt.AlignCenter)
        self.dynamic_image_label.setMinimumHeight(180)
        self.dynamic_image_label.setStyleSheet("QLabel { border: 1px solid #d0d0d0; border-radius: 8px; background-color: #fafafa; font-weight: bold; color: #5b5b5b; }")
        image_layout.addWidget(self.dynamic_image_label)
        container_layout.addWidget(image_box)
        container_layout.addStretch()

        # Signals
        self.longitudinal_combo.currentTextChanged.connect(self.on_longitudinal_changed)

    def _create_card_frame(self):
        card = QFrame()
        card.setStyleSheet("QFrame { border: 1px solid #d0d0d0; border-radius: 12px; background-color: #ffffff; }")
        return card

    def _create_inner_box(self):
        box = QFrame()
        box.setStyleSheet(
            "QFrame { border: 1px solid #cfcfcf; border-radius: 8px; background-color: #ffffff; }"
            "QFrame QComboBox, QFrame QLineEdit { border: none; border-bottom: 1px solid #d0d0d0; border-radius: 0px; padding: 4px 8px; background-color: #ffffff; min-height: 28px; }"
            "QFrame QComboBox:hover, QFrame QLineEdit:hover { border-bottom: 1px solid #5d5d5d; }"
            "QFrame QComboBox:focus, QFrame QLineEdit:focus { border-bottom: 1px solid #90AF13; }"
            "QFrame QLabel { border: none; }"
        )
        return box

    def _create_heading_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 12px; font-weight: 600; color: #4b4b4b; border: none;")
        return label

    def _create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 11px; color: #4b4b4b; border: none;")
        return label

    def _form_row(self, label, widget):
        row_widget = QHBoxLayout()
        row_widget.setContentsMargins(0, 0, 0, 0)
        row_widget.setSpacing(10)
        label.setMinimumWidth(150)
        row_widget.addWidget(label)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row_widget.addWidget(widget)
        return row_widget

    def _add_form_row(self, layout, row, text, widget):
        label = self._create_label(text)
        layout.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignVCenter)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(widget, row, 1)
        return row + 1

    def _prepare_optimizable_field(self, field):
        field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        apply_field_style(field.mode_combo)
        apply_field_style(field.input_field)

    def on_longitudinal_changed(self, text):
        has_longitudinal = text.lower().startswith("yes")
        self.long_thick_combo.setEnabled(has_longitudinal)


class CrossBracingDetailsTab(QWidget):
    """Tab for Cross-Bracing Details with visual previews"""

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

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        main_layout.addSpacing(6)
        main_layout.addWidget(action_bar)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(16)

        primary_card = self._create_card_frame()
        card_layout = QHBoxLayout(primary_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(16)

        # Left column (inputs)
        left_column = QWidget()
        left_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)

        selection_box = self._create_inner_box()
        selection_layout = QGridLayout(selection_box)
        selection_layout.setContentsMargins(12, 10, 12, 10)
        selection_layout.setHorizontalSpacing(16)
        selection_layout.setVerticalSpacing(10)
        selection_layout.setColumnMinimumWidth(0, 130)
        selection_layout.setColumnStretch(1, 1)

        selection_layout.addWidget(self._create_heading_label("Select Girders"), 0, 0, 1, 2)

        self.select_girders_combo = QComboBox()
        self.select_girders_combo.addItems(["G1 to G2", "G3 to G4", "All"])
        apply_field_style(self.select_girders_combo)
        selection_layout.addWidget(self._create_label("Select Girders:"), 1, 0)
        selection_layout.addWidget(self.select_girders_combo, 1, 1)

        self.member_id_combo = QComboBox()
        self.member_id_combo.addItems(["B1-1 to B1-15", "B2-1 to B2-10", "Custom"])
        apply_field_style(self.member_id_combo)
        selection_layout.addWidget(self._create_label("Member ID:"), 2, 0)
        selection_layout.addWidget(self.member_id_combo, 2, 1)

        left_layout.addWidget(selection_box)

        inputs_box = self._create_inner_box()
        inputs_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        inputs_layout = QVBoxLayout(inputs_box)
        inputs_layout.setContentsMargins(12, 10, 12, 10)
        inputs_layout.setSpacing(10)
        inputs_layout.addWidget(self._create_heading_label("Section Inputs:"))

        inputs_grid = QGridLayout()
        inputs_grid.setContentsMargins(0, 0, 0, 0)
        inputs_grid.setHorizontalSpacing(16)
        inputs_grid.setVerticalSpacing(12)
        inputs_grid.setColumnMinimumWidth(0, 130)
        inputs_grid.setColumnStretch(0, 0)
        inputs_grid.setColumnStretch(1, 1)

        self.design_combo = QComboBox()
        self.design_combo.addItems(["Customized", "Optimized"])
        apply_field_style(self.design_combo)
        row = self._add_grid_row(inputs_grid, 0, "Design:", self.design_combo)

        self.bracing_type_combo = QComboBox()
        self.bracing_type_combo.addItems(["K-Bracing", "X-Bracing", "Diagonal", "Horizontal"])
        apply_field_style(self.bracing_type_combo)
        row = self._add_grid_row(inputs_grid, row, "Type of Bracing:", self.bracing_type_combo)

        section_options = [
            "ISA 50 x 50 x 6", "ISA 65 x 65 x 6", "ISA 75 x 75 x 6",
            "ISA 90 x 90 x 8", "ISA 100 x 100 x 8", "ISA 110 x 110 x 10",
            "ISA 130 x 130 x 10", "ISMC 75", "ISMC 100", "ISMC 125",
            "ISMC 150", "2-ISA 65 x 65 x 6", "2-ISA 75 x 75 x 6"
        ]

        self.bracing_section_combo = QComboBox()
        self.bracing_section_combo.addItems(section_options)
        apply_field_style(self.bracing_section_combo)
        row = self._add_grid_row(inputs_grid, row, "Bracing Section:", self.bracing_section_combo)

        self.top_bracket_type_combo = QComboBox()
        self.top_bracket_type_combo.addItems(["Double Angles", "Single Angle", "Channel"])
        apply_field_style(self.top_bracket_type_combo)
        row = self._add_grid_row(inputs_grid, row, "Top Bracket Section:", self.top_bracket_type_combo)

        self.top_bracket_size_combo = QComboBox()
        self.top_bracket_size_combo.addItems(section_options)
        apply_field_style(self.top_bracket_size_combo)
        row = self._add_grid_row(inputs_grid, row, "Top Bracket Size:", self.top_bracket_size_combo)

        self.bottom_bracket_type_combo = QComboBox()
        self.bottom_bracket_type_combo.addItems(["Double Angles", "Single Angle", "Channel"])
        apply_field_style(self.bottom_bracket_type_combo)
        row = self._add_grid_row(inputs_grid, row, "Bottom Bracket Section:", self.bottom_bracket_type_combo)

        self.bottom_bracket_size_combo = QComboBox()
        self.bottom_bracket_size_combo.addItems(section_options)
        apply_field_style(self.bottom_bracket_size_combo)
        row = self._add_grid_row(inputs_grid, row, "Bottom Bracket Size:", self.bottom_bracket_size_combo)

        self.spacing_input = QLineEdit()
        self.spacing_input.setPlaceholderText("Spacing (mm)")
        self.spacing_input.setValidator(QDoubleValidator(0, 100000, 2))
        apply_field_style(self.spacing_input)
        self._add_grid_row(inputs_grid, row, "Spacing:", self.spacing_input)

        inputs_layout.addLayout(inputs_grid)
        left_layout.addWidget(inputs_box)

        card_layout.addWidget(left_column)

        # Right column (previews)
        right_column = QWidget()
        right_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)

        type_box = self._create_inner_box()
        type_layout = QVBoxLayout(type_box)
        type_layout.setContentsMargins(12, 10, 12, 10)
        type_layout.setSpacing(10)
        type_layout.addWidget(self._create_heading_label("Type of Bracing"))
        self.bracing_image_label = self._create_image_placeholder(210)
        type_layout.addWidget(self.bracing_image_label)
        right_layout.addWidget(type_box)

        self.bracing_preview_box, self.bracing_preview_label = self._create_preview_box("Bracing")
        right_layout.addWidget(self.bracing_preview_box)

        self.top_bracket_preview_box, self.top_bracket_preview_label = self._create_preview_box("Top Bracket")
        right_layout.addWidget(self.top_bracket_preview_box)

        self.bottom_bracket_preview_box, self.bottom_bracket_preview_label = self._create_preview_box("Bottom Bracket")
        right_layout.addWidget(self.bottom_bracket_preview_box)

        card_layout.addWidget(right_column)
        card_layout.setStretch(0, 3)
        card_layout.setStretch(1, 2)
        container_layout.addWidget(primary_card)
        container_layout.addStretch()

        self.bracing_type_combo.currentTextChanged.connect(self._update_previews)
        self.bracing_section_combo.currentTextChanged.connect(self._update_previews)
        self.top_bracket_size_combo.currentTextChanged.connect(self._update_previews)
        self.bottom_bracket_size_combo.currentTextChanged.connect(self._update_previews)
        self._update_previews()

    def _create_card_frame(self):
        card = QFrame()
        card.setStyleSheet("QFrame { border: 1px solid #d0d0d0; border-radius: 12px; background-color: #ffffff; }")
        return card

    def _create_inner_box(self):
        box = QFrame()
        box.setStyleSheet(
            "QFrame { border: 1px solid #cfcfcf; border-radius: 8px; background-color: #ffffff; }"
            "QFrame QComboBox, QFrame QLineEdit { border: none; border-bottom: 1px solid #d0d0d0; border-radius: 0px; min-height: 28px; padding: 4px 8px; background-color: #ffffff; }"
            "QFrame QComboBox:hover, QFrame QLineEdit:hover { border-bottom: 1px solid #5d5d5d; }"
            "QFrame QComboBox:focus, QFrame QLineEdit:focus { border-bottom: 1px solid #90AF13; }"
            "QFrame QLabel { border: none; }"
        )
        return box

    def _create_heading_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 12px; font-weight: 600; color: #4b4b4b; border: none;")
        return label

    def _create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 11px; color: #4b4b4b; border: none;")
        return label

    def _add_grid_row(self, layout, row, text, widget):
        label = self._create_label(text)
        layout.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignVCenter)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(widget, row, 1)
        return row + 1

    def _create_image_placeholder(self, height):
        label = QLabel("Bracing Preview")
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumHeight(height)
        label.setStyleSheet("QLabel { border: 1px solid #d0d0d0; border-radius: 10px; background-color: #f7f7f7; font-weight: bold; color: #5b5b5b; }")
        return label

    def _create_preview_box(self, title):
        box = self._create_inner_box()
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        layout.addWidget(self._create_heading_label(title))
        image = self._create_image_placeholder(120)
        layout.addWidget(image)
        return box, image

    def _update_previews(self):
        self.bracing_image_label.setText(self.bracing_type_combo.currentText())
        self.bracing_preview_label.setText(self.bracing_section_combo.currentText())
        self.top_bracket_preview_label.setText(self.top_bracket_size_combo.currentText())
        self.bottom_bracket_preview_label.setText(self.bottom_bracket_size_combo.currentText())


class EndDiaphragmDetailsTab(QWidget):
    """Tab for End Diaphragm Details with type-specific layouts"""

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

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        main_layout.addSpacing(6)
        main_layout.addWidget(action_bar)

        container = QWidget()
        scroll.setWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(16)

        self.type_stack = QStackedWidget()
        container_layout.addWidget(self.type_stack)
        container_layout.addStretch()

        self.views = {}
        self.view_order = []
        self.type_selector_map = {}
        self.type_selectors = []
        self.current_type = None
        self.block_type_sync = False

        cross_view, cross_selector = self._build_cross_bracing_view()
        self._add_type_view("Cross Bracing", cross_view, cross_selector)
        rolled_view, rolled_selector = self._build_rolled_view()
        self._add_type_view("Rolled Beam", rolled_view, rolled_selector)
        welded_view, welded_selector = self._build_welded_view()
        self._add_type_view("Welded Beam", welded_view, welded_selector)

        self._set_current_type("Cross Bracing")

    def _add_type_view(self, key, widget, type_selector):
        self.views[key] = widget
        self.view_order.append(key)
        self.type_stack.addWidget(widget)
        self.type_selector_map[key] = type_selector
        self.type_selectors.append(type_selector)
        type_selector.currentTextChanged.connect(self._handle_type_selection)

    # ---- Shared helpers ----
    def _create_card_frame(self):
        card = QFrame()
        card.setStyleSheet("QFrame { border: 1px solid #d0d0d0; border-radius: 12px; background-color: #ffffff; }")
        return card

    def _create_inner_box(self):
        box = QFrame()
        box.setStyleSheet(
            "QFrame { border: 1px solid #cfcfcf; border-radius: 8px; background-color: #ffffff; }"
            "QFrame QComboBox, QFrame QLineEdit { border: none; border-bottom: 1px solid #d0d0d0; border-radius: 0px; min-height: 28px; padding: 4px 8px; background-color: #ffffff; }"
            "QFrame QComboBox:hover, QFrame QLineEdit:hover { border-bottom: 1px solid #5d5d5d; }"
            "QFrame QComboBox:focus, QFrame QLineEdit:focus { border-bottom: 1px solid #90AF13; }"
            "QFrame QLabel { border: none; }"
        )
        return box

    def _create_heading_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 12px; font-weight: 600; color: #4b4b4b; border: none;")
        return label

    def _create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 11px; color: #4b4b4b; border: none;")
        return label

    def _add_grid_row(self, layout, row, text, widget):
        label = self._create_label(text)
        layout.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignVCenter)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(widget, row, 1)
        return row + 1

    def _create_image_placeholder(self, text, min_height=140):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumHeight(min_height)
        label.setStyleSheet("QLabel { border: 1px solid #d0d0d0; border-radius: 10px; background-color: #f7f7f7; font-weight: bold; color: #5b5b5b; }")
        return label

    def _create_line_edit(self, placeholder=""):
        line_edit = QLineEdit()
        if placeholder:
            line_edit.setPlaceholderText(placeholder)
        apply_field_style(line_edit)
        return line_edit

    def _create_selection_box(self):
        box = self._create_inner_box()
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QGridLayout(box)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(10)
        layout.setColumnMinimumWidth(0, 120)
        layout.setColumnStretch(1, 1)
        layout.addWidget(self._create_heading_label("Select Girders"), 0, 0, 1, 2)

        girders_combo = QComboBox()
        girders_combo.addItems(["G1 to G2", "G3 to G4", "All"])
        apply_field_style(girders_combo)
        layout.addWidget(self._create_label("Select Girders:"), 1, 0)
        layout.addWidget(girders_combo, 1, 1)

        member_combo = QComboBox()
        member_combo.addItems(["E1-1, E1-2", "E2-1, E2-2", "Custom"])
        apply_field_style(member_combo)
        layout.addWidget(self._create_label("Member ID:"), 2, 0)
        layout.addWidget(member_combo, 2, 1)

        return box

    def _create_section_properties_box(self, title):
        box = self._create_inner_box()
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)
        layout.addWidget(self._create_heading_label(title))

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)
        grid.setColumnMinimumWidth(0, 150)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        properties = [
            "Mass, M (Kg/m)",
            "Sectional Area, a (cm2)",
            "2nd Moment of Area, Iz (cm4)",
            "2nd Moment of Area, Iy (cm4)",
            "Radius of Gyration, rz (cm)",
            "Radius of Gyration, ry (cm)",
            "Elastic Modulus, Zz (cm3)",
            "Elastic Modulus, Zy (cm3)",
            "Plastic Modulus, Zuz (cm3)",
            "Plastic Modulus, Zuy (cm3)",
            "Torsion Constant, It (cm4)",
            "Warping Constant, Iw (cm6)"
        ]

        inputs = {}
        for row, name in enumerate(properties):
            label = self._create_label(name)
            field = self._create_line_edit()
            grid.addWidget(label, row, 0)
            grid.addWidget(field, row, 1)
            inputs[name] = field

        layout.addLayout(grid)
        return box, inputs

    # ---- View builders ----
    def _build_cross_bracing_view(self):
        view = self._create_card_frame()
        layout = QHBoxLayout(view)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)
        left_layout.addWidget(self._create_selection_box())

        inputs_box = self._create_inner_box()
        inputs_layout = QVBoxLayout(inputs_box)
        inputs_layout.setContentsMargins(12, 10, 12, 10)
        inputs_layout.setSpacing(10)
        inputs_layout.addWidget(self._create_heading_label("Section Inputs:"))

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setColumnMinimumWidth(0, 130)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        design_combo = QComboBox()
        design_combo.addItems(["Customized", "Optimized"])
        apply_field_style(design_combo)
        row = self._add_grid_row(grid, 0, "Design:", design_combo)

        type_selector = QComboBox()
        type_selector.addItems(VALUES_END_DIAPHRAGM_TYPE)
        type_selector.setCurrentText("Cross Bracing")
        apply_field_style(type_selector)
        row = self._add_grid_row(grid, row, "Type:", type_selector)

        bracing_combo = QComboBox()
        bracing_combo.addItems(["K-Bracing", "X-Bracing", "Diagonal", "Horizontal"])
        apply_field_style(bracing_combo)
        row = self._add_grid_row(grid, row, "Type of Bracing:", bracing_combo)

        section_options = [
            "Double Angles", "Single Angle", "Channel",
            "ISA 100 x 100 x 8", "ISA 110 x 110 x 10"
        ]

        bracing_section = QComboBox()
        bracing_section.addItems(section_options)
        apply_field_style(bracing_section)
        row = self._add_grid_row(grid, row, "Bracing Section:", bracing_section)

        top_bracket = QComboBox()
        top_bracket.addItems(section_options)
        apply_field_style(top_bracket)
        row = self._add_grid_row(grid, row, "Top Bracket Section:", top_bracket)

        bottom_bracket = QComboBox()
        bottom_bracket.addItems(section_options)
        apply_field_style(bottom_bracket)
        row = self._add_grid_row(grid, row, "Bottom Bracket Section:", bottom_bracket)

        spacing_input = self._create_line_edit("Spacing (mm)")
        spacing_input.setValidator(QDoubleValidator(0, 100000, 2))
        self._add_grid_row(grid, row, "Spacing:", spacing_input)

        inputs_layout.addLayout(grid)
        left_layout.addWidget(inputs_box)

        layout.addWidget(left_column)

        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)

        type_box = self._create_inner_box()
        type_layout = QVBoxLayout(type_box)
        type_layout.setContentsMargins(12, 10, 12, 10)
        type_layout.setSpacing(8)
        type_layout.addWidget(self._create_heading_label("Type of Bracing"))
        type_layout.addWidget(self._create_image_placeholder("Bracing Layout", 200))
        right_layout.addWidget(type_box)

        for title in ["Bracing", "Top Bracket", "Bottom Bracket"]:
            preview_box = self._create_inner_box()
            preview_layout = QVBoxLayout(preview_box)
            preview_layout.setContentsMargins(12, 10, 12, 10)
            preview_layout.setSpacing(6)
            preview_layout.addWidget(self._create_heading_label(title))
            preview_layout.addWidget(self._create_image_placeholder("Preview", 110))
            right_layout.addWidget(preview_box)

        layout.addWidget(right_column)
        return view, type_selector

    def _build_rolled_view(self):
        view = self._create_card_frame()
        layout = QHBoxLayout(view)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)
        left_layout.addWidget(self._create_selection_box())

        inputs_box = self._create_inner_box()
        inputs_layout = QVBoxLayout(inputs_box)
        inputs_layout.setContentsMargins(12, 10, 12, 10)
        inputs_layout.setSpacing(10)
        inputs_layout.addWidget(self._create_heading_label("Section Inputs"))

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setColumnMinimumWidth(0, 130)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        design_combo = QComboBox()
        design_combo.addItems(["Customized", "Optimized"])
        apply_field_style(design_combo)
        row = self._add_grid_row(grid, 0, "Design:", design_combo)

        type_selector = QComboBox()
        type_selector.addItems(VALUES_END_DIAPHRAGM_TYPE)
        type_selector.setCurrentText("Rolled Beam")
        apply_field_style(type_selector)
        row = self._add_grid_row(grid, row, "Type:", type_selector)

        is_section_combo = QComboBox()
        is_section_combo.addItems([
            "ISMB 500", "ISMB 550", "ISMB 600",
            "ISWB 500", "ISWB 550", "ISWB 600"
        ])
        apply_field_style(is_section_combo)
        self._add_grid_row(grid, row, "IS Section:", is_section_combo)

        inputs_layout.addLayout(grid)
        left_layout.addWidget(inputs_box)
        layout.addWidget(left_column)

        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)

        image_box = self._create_inner_box()
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(12, 10, 12, 10)
        image_layout.setSpacing(8)
        image_layout.addWidget(self._create_heading_label("Dynamic Image"))
        image_layout.addWidget(self._create_image_placeholder("Rolled Section", 180))
        right_layout.addWidget(image_box)

        props_box, _ = self._create_section_properties_box("Section Properties:")
        right_layout.addWidget(props_box)

        layout.addWidget(right_column)
        return view, type_selector

    def _build_welded_view(self):
        view = self._create_card_frame()
        layout = QHBoxLayout(view)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)
        left_layout.addWidget(self._create_selection_box())

        inputs_box = self._create_inner_box()
        inputs_layout = QVBoxLayout(inputs_box)
        inputs_layout.setContentsMargins(12, 10, 12, 10)
        inputs_layout.setSpacing(10)
        inputs_layout.addWidget(self._create_heading_label("Section Inputs:"))

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setColumnMinimumWidth(0, 150)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        design_combo = QComboBox()
        design_combo.addItems(["Customized", "Optimized"])
        apply_field_style(design_combo)
        row = self._add_grid_row(grid, 0, "Design:", design_combo)

        type_selector = QComboBox()
        type_selector.addItems(VALUES_END_DIAPHRAGM_TYPE)
        type_selector.setCurrentText("Welded Beam")
        apply_field_style(type_selector)
        row = self._add_grid_row(grid, row, "Type:", type_selector)

        symmetry_combo = QComboBox()
        symmetry_combo.addItems(["Girder Symmetric", "Girder Unsymmetric"])
        apply_field_style(symmetry_combo)
        row = self._add_grid_row(grid, row, "Symmetry:", symmetry_combo)

        total_depth = self._create_line_edit()
        row = self._add_grid_row(grid, row, "Total Depth (mm):", total_depth)

        web_thick_combo = QComboBox()
        web_thick_combo.addItems(["All", "Custom"])
        apply_field_style(web_thick_combo)
        row = self._add_grid_row(grid, row, "Web Thickness (mm):", web_thick_combo)

        top_width = self._create_line_edit()
        row = self._add_grid_row(grid, row, "Width of Top Flange (mm):", top_width)

        top_thickness_combo = QComboBox()
        top_thickness_combo.addItems(["All", "Custom"])
        apply_field_style(top_thickness_combo)
        row = self._add_grid_row(grid, row, "Top Flange Thickness (mm):", top_thickness_combo)

        bottom_width = self._create_line_edit()
        row = self._add_grid_row(grid, row, "Width of Bottom Flange (mm):", bottom_width)

        bottom_thickness_combo = QComboBox()
        bottom_thickness_combo.addItems(["All", "Custom"])
        apply_field_style(bottom_thickness_combo)
        row = self._add_grid_row(grid, row, "Bottom Flange Thickness (mm):", bottom_thickness_combo)

        bearing_thickness = self._create_line_edit()
        self._add_grid_row(grid, row, "Bearing Stiffener Thickness (mm):", bearing_thickness)

        inputs_layout.addLayout(grid)
        left_layout.addWidget(inputs_box)
        layout.addWidget(left_column)

        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)

        image_box = self._create_inner_box()
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(12, 10, 12, 10)
        image_layout.setSpacing(8)
        image_layout.addWidget(self._create_heading_label("Dynamic Image"))
        image_layout.addWidget(self._create_image_placeholder("Welded Section", 180))
        right_layout.addWidget(image_box)

        props_box, _ = self._create_section_properties_box("Section Properties:")
        right_layout.addWidget(props_box)

        layout.addWidget(right_column)
        return view, type_selector

    def _handle_type_selection(self, value):
        if self.block_type_sync:
            return
        if value in self.view_order:
            self._set_current_type(value)

    def _set_current_type(self, target):
        if target not in self.view_order:
            return
        if self.current_type == target:
            return
        self.current_type = target
        index = self.view_order.index(target)
        self.type_stack.setCurrentIndex(index)
        self.block_type_sync = True
        for selector in self.type_selectors:
            selector.setCurrentText(target)
        self.block_type_sync = False


class CustomVehicleDialog(QDialog):
    """Dialog for adding or editing custom live load vehicles"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Live Load Custom Vehicle Add/Edit")
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setStyleSheet("background-color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        name_row = QHBoxLayout()
        name_row.setSpacing(10)
        name_label = QLabel("Vehicle Name:")
        name_label.setMinimumWidth(120)
        self.vehicle_name_input = QLineEdit()
        apply_field_style(self.vehicle_name_input)
        name_row.addWidget(name_label)
        name_row.addWidget(self.vehicle_name_input)
        layout.addLayout(name_row)

        pd_row = QHBoxLayout()
        pd_row.setSpacing(12)
        self.P_input = QLineEdit()
        self.D_input = QLineEdit()
        for label_text, field in (("P#", self.P_input), ("D#", self.D_input)):
            sub_layout = QHBoxLayout()
            sub_layout.setSpacing(6)
            lbl = QLabel(label_text)
            field.setMaximumWidth(90)
            apply_field_style(field)
            sub_layout.addWidget(lbl)
            sub_layout.addWidget(field)
            pd_row.addLayout(sub_layout)
        pd_row.addStretch()
        layout.addLayout(pd_row)

        table_row = QHBoxLayout()
        table_row.setSpacing(12)

        self.axle_table = QTableWidget()
        self.axle_table.setColumnCount(3)
        self.axle_table.setHorizontalHeaderLabels(["No.", "Load (kN)", "Spacing (m)"])
        self.axle_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.axle_table.verticalHeader().setVisible(False)
        self.axle_table.setMinimumHeight(160)
        table_row.addWidget(self.axle_table, 3)

        diagram = QLabel("Axle Layout")
        diagram.setAlignment(Qt.AlignCenter)
        diagram.setMinimumWidth(150)
        diagram.setStyleSheet("QLabel { border: 1px solid #cfcfcf; border-radius: 8px; background: #f7f7f7; }")
        table_row.addWidget(diagram, 2)

        layout.addLayout(table_row)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        self.add_axle_button = QPushButton("Add")
        self.modify_axle_button = QPushButton("Modify")
        self.delete_axle_button = QPushButton("Delete")
        for btn in (self.add_axle_button, self.modify_axle_button, self.delete_axle_button):
            btn.setFixedWidth(90)
            button_row.addWidget(btn)
        button_row.addStretch()
        layout.addLayout(button_row)

        fields_grid = QGridLayout()
        fields_grid.setContentsMargins(0, 0, 0, 0)
        fields_grid.setHorizontalSpacing(14)
        fields_grid.setVerticalSpacing(10)
        fields_grid.setColumnMinimumWidth(0, 260)
        fields_grid.setColumnStretch(1, 1)

        field_labels = [
            "Minimum nose to tail distance (m):",
            "Width of Wheel, w (mm):",
            "Minimum Clearance from Carriageway Edge, f (mm):",
            "Minimum Clearance from Crossing Vehicles, g (mm):",
            "Wheel Spacing in Transverse Direction (m):",
            "Impact Factor:",
        ]

        self.custom_fields = {}
        for row, text in enumerate(field_labels):
            lbl = QLabel(text)
            field = QLineEdit()
            if "Impact" in text:
                field.setText("0.25")
            apply_field_style(field)
            fields_grid.addWidget(lbl, row, 0)
            fields_grid.addWidget(field, row, 1)
            self.custom_fields[text] = field

        layout.addLayout(fields_grid)

        diagram_bottom = QLabel("Clear Carriageway Width Diagram")
        diagram_bottom.setAlignment(Qt.AlignCenter)
        diagram_bottom.setMinimumHeight(140)
        diagram_bottom.setStyleSheet("QLabel { border: 1px solid #cfcfcf; border-radius: 8px; background: #fafafa; }")
        layout.addWidget(diagram_bottom)

        layout.addStretch()


class LoadingTab(QWidget):
    """Loading tab with permanent load layout and load-type subtabs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_vehicle_dialog = CustomVehicleDialog(self)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.load_tabs = QTabWidget()
        self.load_tabs.setDocumentMode(True)
        self.load_tabs.setStyleSheet(
            "QTabWidget::pane { border: none; background: #f5f5f5; }"
            "QTabBar::tab { background: #e8e8e8; color: #4b4b4b; border: 1px solid #cfcfcf;"
            " border-bottom: none; padding: 8px 20px; margin-right: 2px; min-width: 120px;"
            " font-size: 11px; border-top-left-radius: 6px; border-top-right-radius: 6px; }"
            "QTabBar::tab:selected { background: #9ecb3d; color: #ffffff; font-weight: bold; }"
            "QTabBar::tab:!selected { margin-top: 2px; }"
        )

        self.load_tabs.addTab(self._build_permanent_load_tab(), "Permanent Load")
        self.load_tabs.addTab(self._build_live_load_tab(), "Live Load")
        self.load_tabs.addTab(self._create_placeholder_page("Seismic Load"), "Seismic Load")
        self.load_tabs.addTab(self._create_placeholder_page("Wind Load"), "Wind Load")
        self.load_tabs.addTab(self._create_placeholder_page("Temperature Load"), "Temperature Load")
        self.load_tabs.addTab(self._create_placeholder_page("Custom Load"), "Custom Load")
        self.load_tabs.addTab(self._create_placeholder_page("Load Combination"), "Load Combination")
        main_layout.addWidget(self.load_tabs)

        action_bar, self.defaults_button, self.save_button = create_action_button_bar()
        main_layout.addSpacing(6)
        main_layout.addWidget(action_bar)

    def _build_permanent_load_tab(self):
        page = QWidget()
        page.setStyleSheet("background-color: #f5f5f5;")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(12, 12, 12, 12)
        page_layout.setSpacing(12)

        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(18)

        left_card = self._create_card()
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(18)

        self._add_load_section(left_layout, "Dead Load (DL):", [
            ("Include Member Self Weight:", self._create_yes_no_combo()),
            ("Self-weight factor:", self._create_line_edit()),
            ("Include Concrete Deck Weight:", self._create_yes_no_combo()),
        ])

        self._add_load_section(left_layout, "Dead Load for Surfacing (DW):", [
            ("Include Load from Wearing Course:", self._create_yes_no_combo()),
        ])

        self._add_load_section(left_layout, "Super-Imposed Dead Load (SIDL):", [
            ("Include Load from Crash Barrier:", self._create_yes_no_combo()),
            ("Include Load from Median:", self._create_yes_no_combo()),
            ("Include Load from Railing:", self._create_yes_no_combo()),
        ])

        left_layout.addStretch()

        right_card = self._create_card()
        right_card.setMinimumWidth(260)
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(12)
        description_label = QLabel("Description Box")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-size: 14px; color: #6a6a6a;")
        description_label.setMinimumHeight(260)
        right_layout.addWidget(description_label)

        content_row.addWidget(left_card, 3)
        content_row.addWidget(right_card, 2)

        page_layout.addLayout(content_row)
        page_layout.addStretch()
        return page

    def _build_live_load_tab(self):
        page = QWidget()
        page.setStyleSheet("background-color: #f5f5f5;")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(12, 12, 12, 12)
        page_layout.setSpacing(12)

        content_row = QHBoxLayout()
        content_row.setSpacing(18)

        left_card = self._create_card()
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(16)

        title = QLabel("Live Load (LL) Inputs:")
        title.setStyleSheet("font-size: 13px; font-weight: 600; color: #3a3a3a;")
        left_layout.addWidget(title)

        irc_vehicles = [
            "Class A", "Class 70R Wheeled", "Class 70R Tracked",
            "Class AA Wheeled", "Class AA Tracked", "Class SV", "Fatigue Truck"
        ]
        self._add_checkbox_section(left_layout, "Vehicles from IRC 6:", irc_vehicles)

        custom_header = QHBoxLayout()
        custom_header.setSpacing(10)
        custom_label = QLabel("Custom Vehicle:")
        custom_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #3a3a3a;")
        custom_header.addWidget(custom_label)
        custom_header.addStretch()
        self.custom_vehicle_add_button = QPushButton("Add")
        self.custom_vehicle_edit_button = QPushButton("Edit")
        for btn in (self.custom_vehicle_add_button, self.custom_vehicle_edit_button):
            btn.setFixedWidth(70)
            custom_header.addWidget(btn)
        left_layout.addLayout(custom_header)

        custom_grid = QGridLayout()
        custom_grid.setContentsMargins(0, 0, 0, 0)
        custom_grid.setHorizontalSpacing(12)
        custom_grid.setVerticalSpacing(10)
        custom_grid.setColumnStretch(1, 1)

        self.custom_vehicle_name_inputs = []
        for index in range(2):
            label = QLabel(f"Vehicle Name {index + 1}")
            line_edit = QLineEdit()
            apply_field_style(line_edit)
            checkbox = QCheckBox()
            custom_grid.addWidget(label, index, 0)
            custom_grid.addWidget(line_edit, index, 1)
            custom_grid.addWidget(checkbox, index, 2, Qt.AlignCenter)
            self.custom_vehicle_name_inputs.append((line_edit, checkbox))

        left_layout.addLayout(custom_grid)

        self._add_checkbox_section(left_layout, "Braking Load from Vehicles:", irc_vehicles)

        ecc_row = QHBoxLayout()
        ecc_row.setSpacing(12)
        ecc_label = QLabel("Eccentricity from top of Deck (m):")
        self.eccentricity_input = QLineEdit()
        apply_field_style(self.eccentricity_input)
        ecc_row.addWidget(ecc_label)
        ecc_row.addWidget(self.eccentricity_input)
        left_layout.addLayout(ecc_row)

        footpath_row = QHBoxLayout()
        footpath_row.setSpacing(12)
        footpath_label = QLabel("Footpath Pressure (kN/mm^2):")
        self.footpath_mode_combo = QComboBox()
        self.footpath_mode_combo.addItems(["Automatic", "User-defined"])
        apply_field_style(self.footpath_mode_combo)
        self.footpath_value_input = QLineEdit()
        self.footpath_value_input.setPlaceholderText("Value")
        apply_field_style(self.footpath_value_input)
        footpath_row.addWidget(footpath_label)
        footpath_row.addWidget(self.footpath_mode_combo)
        footpath_row.addWidget(self.footpath_value_input)
        left_layout.addLayout(footpath_row)

        left_layout.addStretch()

        right_card = self._create_card()
        right_card.setMinimumWidth(280)
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(10)
        desc_label = QLabel("Description Box")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #3a3a3a;")
        right_layout.addWidget(desc_label)

        description_text = (
            "211.2 The braking effect on a simply supported span or a continuous unit of spans "
            "or on any other type of bridge unit shall be assumed to have the following value:\n\n"
            "a) In the case of a single lane or a two lane bridge: twenty percent of the first train "
            "load plus ten percent of the load of the succeeding trains or part thereof, the train "
            "loads in one lane only being considered for the purpose of this subclause. Where the "
            "entire first train is not on the full span, the braking force shall be taken as equal to "
            "twenty percent of the loads actually on the span or continuous unit of spans.\n"
            "b) In the case of bridges having more than two lanes: as in (a) above for the first two "
            "lanes plus five percent of the loads on the lanes in excess of two."
        )
        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 11px; color: #4b4b4b;")
        right_layout.addWidget(description_label)
        right_layout.addStretch()

        content_row.addWidget(left_card, 3)
        content_row.addWidget(right_card, 2)
        page_layout.addLayout(content_row)
        page_layout.addStretch()

        self.custom_vehicle_add_button.clicked.connect(self.show_custom_vehicle_dialog)
        self.custom_vehicle_edit_button.clicked.connect(self.show_custom_vehicle_dialog)
        self.footpath_mode_combo.currentTextChanged.connect(self._on_footpath_mode_changed)
        self._on_footpath_mode_changed(self.footpath_mode_combo.currentText())

        return page

    def _add_load_section(self, parent_layout, title, rows):
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #3e3e3e;")
        parent_layout.addWidget(title_label)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(10)
        grid.setColumnMinimumWidth(0, 200)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)

        for row_index, (label_text, widget) in enumerate(rows):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 11px; color: #4b4b4b;")
            grid.addWidget(label, row_index, 0, Qt.AlignLeft | Qt.AlignVCenter)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            grid.addWidget(widget, row_index, 1)

        parent_layout.addLayout(grid)

    def _add_checkbox_section(self, parent_layout, title, items):
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #3e3e3e;")
        parent_layout.addWidget(title_label)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)
        grid.setColumnStretch(0, 1)

        for row, name in enumerate(items):
            label = QLabel(name)
            label.setStyleSheet("font-size: 11px; color: #4b4b4b;")
            checkbox = QCheckBox()
            grid.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignVCenter)
            grid.addWidget(checkbox, row, 1, Qt.AlignRight | Qt.AlignVCenter)

        parent_layout.addLayout(grid)

    def _on_footpath_mode_changed(self, mode):
        is_custom = mode == "User-defined"
        self.footpath_value_input.setEnabled(is_custom)
        if not is_custom:
            self.footpath_value_input.clear()

    def show_custom_vehicle_dialog(self):
        self.custom_vehicle_dialog.show()
        self.custom_vehicle_dialog.raise_()
        self.custom_vehicle_dialog.activateWindow()

    def _create_yes_no_combo(self):
        combo = QComboBox()
        combo.addItems(VALUES_YES_NO)
        combo.setCurrentText("Yes")
        apply_field_style(combo)
        return combo

    def _create_line_edit(self):
        line_edit = QLineEdit()
        apply_field_style(line_edit)
        return line_edit

    def _create_card(self):
        card = QFrame()
        card.setStyleSheet("QFrame { border: 1px solid #cfcfcf; border-radius: 12px; background-color: #ffffff; }")
        return card

    def _create_placeholder_page(self, title):
        page = QWidget()
        page.setStyleSheet("background-color: #f5f5f5;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(f"{title} inputs will be added soon.")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 12px; color: #6a6a6a;")
        layout.addWidget(label)
        return page


class StretchingTabBar(QTabBar):
    """Tab bar that distributes tab widths across available space."""

    def tabSizeHint(self, index):
        hint = super().tabSizeHint(index)
        count = max(1, self.count())
        available_width = max(self.width(), hint.width() * count)
        stretched_width = max(hint.width(), available_width // count)
        return QSize(stretched_width, hint.height())

    def minimumTabSizeHint(self, index):
        return self.tabSizeHint(index)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGeometry()


class AdditionalInputsWidget(QWidget):
    """Main widget for Additional Inputs with tabbed interface"""
    
    def __init__(self, footpath_value="None", carriageway_width=7.5, parent=None):
        super().__init__(parent)
        self.setObjectName("additionalInputsWidget")
        self.footpath_value = footpath_value
        self.carriageway_width = carriageway_width
        self.setStyleSheet(
            "QWidget#additionalInputsWidget { background-color: #ffffff; }"
        )
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Main tab widget
        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stretching_tab_bar = StretchingTabBar()
        self.stretching_tab_bar.setElideMode(Qt.ElideRight)
        self.tabs.setTabBar(self.stretching_tab_bar)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d1d1d1;
                background-color: #ffffff;
                border-radius: 6px;
            }
            QTabBar::tab {
                font-weight: bold;
                font-size: 12px;
                background: #ffffff;
                color: #3a3a3a;
                border: 1px solid #d1d1d1;
                padding: 10px 22px;
            }
            QTabBar::tab:selected {
                background: #90AF13;
                color: #ffffff;
                border: 1px solid #90AF13;
            }
            QTabBar::tab:hover {
                background: #90AF13;
                color: #ffffff;
            }
        """)
        
        # Sub-Tab 1: Typical Section Details
        self.typical_section_tab = TypicalSectionDetailsTab(self.footpath_value, self.carriageway_width)
        self.tabs.addTab(self.typical_section_tab, "Typical Section Details")
        
        # Sub-Tab 2: Member Properties
        self.section_properties_tab = SectionPropertiesTab()
        self.tabs.addTab(self.section_properties_tab, "Member Properties")
        
        # Sub-Tab 3: Loading
        self.loading_tab = LoadingTab()
        self.tabs.addTab(self.loading_tab, "Loading")
        
        # Sub-Tab 4: Support Conditions
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
        
        # Sub-Tab 5: Design Options
        shear_connection_tab = self.create_placeholder_tab(
            "Design Options",
            "This tab will contain:\n\n" +
            "• Shear Connector Type\n" +
            "• Connector Size and Spacing\n" +
            "• Connection Details\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(shear_connection_tab, "Design Options")
        
        # Sub-Tab 6: Design Options (Cont.)
        analysis_design_tab = self.create_placeholder_tab(
            "Design Options (Cont.)",
            "This tab will contain:\n\n" +
            "• Analysis Method\n" +
            "• Design Code Options\n" +
            "• Safety Factors\n" +
            "• Other Design Parameters\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(analysis_design_tab, "Design Options (Cont.)")
        
        main_layout.addWidget(self.tabs)
        
    
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
        layout.addSpacing(10)
        action_bar, _, _ = create_action_button_bar(widget)
        layout.addWidget(action_bar)
        
        return widget
    
    def update_footpath_value(self, footpath_value):
        """Update footpath value across all tabs"""
        self.footpath_value = footpath_value
        self.typical_section_tab.update_footpath_value(footpath_value)
