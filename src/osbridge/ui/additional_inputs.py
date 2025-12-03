"""
Additional Inputs Widget for Highway Bridge Design
Provides detailed input fields for manual bridge parameter definition
"""
import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit,
    QComboBox, QGroupBox, QFormLayout, QPushButton, QScrollArea,
    QCheckBox, QMessageBox, QSizePolicy, QSpacerItem, QStackedWidget,
    QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator

from osbridge.backend.common import *


def get_combobox_style():
    """Return the common stylesheet for dropdowns with the SVG icon from resources."""
    return """
        QComboBox {
            padding: 6px 42px 6px 14px;
            border: 1px solid #b8b8b8;
            border-radius: 8px;
            background-color: #ffffff;
            color: #2b2b2b;
            font-size: 12px;
            min-height: 34px;
        }
        QComboBox:hover {
            border: 1px solid #909090;
        }
        QComboBox:focus {
            border: 1px solid #4a7ba7;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 26px;
            height: 26px;
            border: 1px solid #606060;
            border-radius: 13px;
            background: transparent;
            right: 8px;
        }
        QComboBox::down-arrow {
            image: url(:/vectors/arrow_down_light.svg);
            width: 16px;
            height: 16px;
        }
        /* when popup is open show the up arrow */
        QComboBox::down-arrow:on {
            image: url(:/vectors/arrow_up_light.svg);
            width: 16px;
            height: 16px;
        }
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
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 20)
        card_layout.setSpacing(16)

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
        diagram_layout.addWidget(diagram_label, 0, Qt.AlignCenter)

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
        main_layout.addWidget(input_container, 1)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 10, 0, 0)
        button_row.setSpacing(12)
        button_row.addStretch()

        self.defaults_button = QPushButton("Defaults")
        self.defaults_button.setFixedWidth(120)
        self.defaults_button.setStyleSheet("QPushButton { background-color: #e0e0e0; border: 1px solid #c6c6c6; padding: 8px 18px; }")
        self.defaults_button.clicked.connect(lambda: self._show_placeholder_message("Defaults"))
        button_row.addWidget(self.defaults_button)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(120)
        self.save_button.setStyleSheet("QPushButton { background-color: #dadada; border: 1px solid #c6c6c6; padding: 8px 18px; }")
        self.save_button.clicked.connect(lambda: self._show_placeholder_message("Save"))
        button_row.addWidget(self.save_button)

        button_row.addStretch()
        main_layout.addLayout(button_row)

        self.deck_thickness.textChanged.connect(self.update_footpath_thickness)
        self.recalculate_girders()

    def create_layout_tab(self):
        layout_widget = QWidget()
        layout_widget.setStyleSheet("background-color: #f5f5f5;")
        layout_layout = QVBoxLayout(layout_widget)
        layout_layout.setContentsMargins(25, 25, 25, 25)
        layout_layout.setSpacing(20)

        title_label = QLabel("Inputs:")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #000;")
        layout_layout.addWidget(title_label)

        grid = QGridLayout()
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(18)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

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
        grid.addWidget(values_adjusted_label, 1, 2, 1, 2, Qt.AlignLeft)

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
        grid.addWidget(_label("Footpath Thickness (mm):"), 3, 2, Qt.AlignLeft)
        grid.addWidget(self.footpath_thickness, 3, 3)

        self.footpath_width = QLineEdit()
        self.footpath_width.setValidator(QDoubleValidator(MIN_FOOTPATH_WIDTH, 5.0, 3))
        self.footpath_width.textChanged.connect(self.on_footpath_width_changed)
        self.style_input_field(self.footpath_width)
        self.footpath_width.setText(f"{MIN_FOOTPATH_WIDTH:.2f}")

        grid.addWidget(_label("Footpath Width (m):"), 4, 0, Qt.AlignLeft)
        grid.addWidget(self.footpath_width, 4, 1)

        layout_layout.addLayout(grid)
        layout_layout.addStretch()
        self.input_tabs.addTab(layout_widget, "Layout")

    def create_crash_barrier_tab(self):
        crash_widget = QWidget()
        crash_widget.setStyleSheet("background-color: #f5f5f5;")
        crash_layout = QVBoxLayout(crash_widget)
        crash_layout.setContentsMargins(25, 20, 25, 25)
        crash_layout.setSpacing(20)

        card, card_layout = self._create_section_card("Crash Barrier Inputs:")
        grid = QGridLayout()
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(18)
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
        median_layout.setContentsMargins(25, 20, 25, 25)
        median_layout.setSpacing(20)

        card, card_layout = self._create_section_card("Median Inputs:")
        grid = QGridLayout()
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(18)
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
        railing_layout.setContentsMargins(25, 20, 25, 25)
        railing_layout.setSpacing(20)

        card, card_layout = self._create_section_card("Railing Inputs:")
        grid = QGridLayout()
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(18)
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
        wearing_layout.setContentsMargins(25, 20, 25, 25)
        wearing_layout.setSpacing(20)

        card, card_layout = self._create_section_card("Wearing Course Inputs:")
        grid = QGridLayout()
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(18)
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
        lane_layout.setContentsMargins(25, 20, 25, 25)
        lane_layout.setSpacing(20)

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
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.lane_table.verticalHeader().setVisible(False)
        self.lane_table.setAlternatingRowColors(True)
        self.lane_table.setStyleSheet("QTableWidget { background-color: #ffffff; }")

        card_layout.addWidget(self.lane_table)
        lane_layout.addWidget(card)
        lane_layout.addStretch()

        self.input_tabs.addTab(lane_widget, "Lane Details")
        self._update_lane_details_rows(self.lane_count_combo.currentText())

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
        nav_bar.setStyleSheet("background-color: transparent;")
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
                    padding: 10px 20px;
                    text-align: center;
                    font-size: 11px;
                    font-weight: normal;
                    min-height: 30px;
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
        
        # Sub-Tab 1: Typical Section Details
        self.typical_section_tab = TypicalSectionDetailsTab(self.footpath_value, self.carriageway_width)
        self.tabs.addTab(self.typical_section_tab, "Typical Section Details")
        
        # Sub-Tab 2: Member Properties
        self.section_properties_tab = SectionPropertiesTab()
        self.tabs.addTab(self.section_properties_tab, "Member Properties")
        
        # Sub-Tab 3: Loading
        loading_tab = self.create_placeholder_tab(
            "Loading",
            "This tab will contain:\n\n" +
            "• Dead Load (Self Weight, Wearing Coat, etc.)\n" +
            "• Live Load (IRC Vehicles, Custom Loads)\n" +
            "• Lateral Load (Wind, Seismic)\n\n" +
            "Implementation in progress..."
        )
        self.tabs.addTab(loading_tab, "Loading")
        
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
        self.typical_section_tab.update_footpath_value(footpath_value)
