"""
Configuration selector dialog for choosing simulation presets.

Displays available presets organized by category and allows users
to select a configuration to run.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, 
    QTreeWidgetItem, QLabel, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from components import config_presets


class ConfigSelectorDialog(QDialog):
    """Dialog for selecting simulation configuration presets."""
    
    def __init__(self, current_config=None, parent=None):
        """
        Initialize the config selector dialog.
        
        Args:
            current_config: dict with current sim_type, scenario, solution
            parent: parent widget
        """
        super().__init__(parent)
        self.current_config = current_config or {}
        self.selected_preset = None
        
        self.setWindowTitle("Select Simulation Configuration")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Available Simulation Presets")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Main content layout: tree on left, details on right
        content_layout = QHBoxLayout()
        
        # Left: Preset tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Preset"])
        self.tree.itemSelectionChanged.connect(self._on_preset_selected)
        self._populate_tree()
        content_layout.addWidget(self.tree, 1)
        
        # Right: Details
        details_layout = QVBoxLayout()
        
        details_title = QLabel("Description")
        details_font = details_title.font()
        details_font.setBold(True)
        details_title.setFont(details_font)
        details_layout.addWidget(details_title)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text, 1)
        
        # Config display
        config_title = QLabel("Configuration")
        config_font = config_title.font()
        config_font.setBold(True)
        config_title.setFont(config_font)
        details_layout.addWidget(config_title)
        
        self.config_text = QTextEdit()
        self.config_text.setReadOnly(True)
        self.config_text.setMaximumHeight(100)
        details_layout.addWidget(self.config_text)
        
        content_layout.addLayout(details_layout, 1)
        
        layout.addLayout(content_layout, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        button_layout.addStretch()
        
        self.select_btn = QPushButton("Select & Restart")
        self.select_btn.clicked.connect(self._on_select_clicked)
        self.select_btn.setEnabled(False)
        button_layout.addWidget(self.select_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _populate_tree(self):
        """Populate the preset tree with categories and presets."""
        for category in config_presets.get_all_categories():
            category_item = QTreeWidgetItem(self.tree)
            category_item.setText(0, category)
            category_item.setExpanded(True)
            
            for preset in config_presets.get_presets_by_category(category):
                if preset.get("working", False):
                    preset_item = QTreeWidgetItem(category_item)
                    preset_item.setText(0, preset["name"])
                    preset_item.setData(0, Qt.UserRole, preset["id"])
    
    def _on_preset_selected(self):
        """Handle preset selection from tree."""
        selected_items = self.tree.selectedItems()
        if not selected_items:
            self.details_text.clear()
            self.config_text.clear()
            self.select_btn.setEnabled(False)
            return
        
        item = selected_items[0]
        preset_id = item.data(0, Qt.UserRole)
        
        if preset_id is None:
            # Category selected, not a preset
            self.details_text.clear()
            self.config_text.clear()
            self.select_btn.setEnabled(False)
            return
        
        preset = config_presets.get_preset_by_id(preset_id)
        if preset:
            self.selected_preset = preset
            self.details_text.setText(preset.get("description", ""))
            
            config_str = (
                f"Sim Type: {preset['sim_type']}\n"
                f"Scenario: {preset['scenario']}\n"
                f"Solution: {preset['solution']}"
            )
            
            # Add current config indicator if different
            if self._is_different_from_current(preset):
                config_str += "\n\n✓ Different from current"
            else:
                config_str += "\n\n(Current configuration)"
            
            self.config_text.setText(config_str)
            self.select_btn.setEnabled(True)
    
    def _is_different_from_current(self, preset):
        """Check if preset differs from current config."""
        return (
            preset["sim_type"] != self.current_config.get("sim_type") or
            preset["scenario"] != self.current_config.get("scenario") or
            preset["solution"] != self.current_config.get("solution")
        )
    
    def _on_select_clicked(self):
        """Handle select button click."""
        if not self.selected_preset:
            QMessageBox.warning(self, "Selection Required", "Please select a preset first.")
            return
        
        if not self._is_different_from_current(self.selected_preset):
            QMessageBox.information(
                self, 
                "Same Configuration", 
                "Selected configuration is already active."
            )
            return
        
        self.accept()
    
    def get_selected_preset(self):
        """Return the selected preset or None if cancelled."""
        return self.selected_preset
