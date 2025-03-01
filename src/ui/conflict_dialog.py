from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox


class ConflictDialog(QDialog):
    def __init__(self, conflicts, parent=None):
        super(ConflictDialog, self).__init__(parent)
        self.setWindowTitle("Resolve Conflicts")
        self.conflicts = conflicts
        self.selected_action = None

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Conflicting Map Entries:")
        self.layout.addWidget(self.label)

        self.conflict_list = QListWidget(self)
        self.populate_conflict_list()
        self.layout.addWidget(self.conflict_list)

        self.keep_button = QPushButton("Keep as Main", self)
        self.keep_button.clicked.connect(self.keep_as_main)
        self.layout.addWidget(self.keep_button)

        self.new_entry_button = QPushButton("Set as New Entry", self)
        self.new_entry_button.clicked.connect(self.set_as_new_entry)
        self.layout.addWidget(self.new_entry_button)

        self.delete_button = QPushButton("Delete Entry", self)
        self.delete_button.clicked.connect(self.delete_entry)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

    def populate_conflict_list(self):
        for conflict in self.conflicts:
            item = QListWidgetItem(conflict)
            self.conflict_list.addItem(item)

    def keep_as_main(self):
        selected_items = self.conflict_list.selectedItems()
        if selected_items:
            self.selected_action = "keep"
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select an entry to keep as main.")

    def set_as_new_entry(self):
        selected_items = self.conflict_list.selectedItems()
        if selected_items:
            self.selected_action = "new_entry"
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select an entry to set as new.")

    def delete_entry(self):
        selected_items = self.conflict_list.selectedItems()
        if selected_items:
            self.selected_action = "delete"
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select an entry to delete.")

    def get_selected_action(self):
        return self.selected_action