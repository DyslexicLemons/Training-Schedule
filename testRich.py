import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QToolBar, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QIcon
import os

class RichTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file = None  # Track the current file

        self.init_ui()

    def init_ui(self):
        # Main text edit widget (QTextEdit)
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Create a toolbar for formatting options
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add Bold action
        bold_action = QAction("Bold", self)
        bold_action.triggered.connect(self.make_bold)
        toolbar.addAction(bold_action)

        # Add Italic action
        italic_action = QAction("Italic", self)
        italic_action.triggered.connect(self.make_italic)
        toolbar.addAction(italic_action)

        # Add Underline action
        underline_action = QAction("Underline", self)
        underline_action.triggered.connect(self.make_underline)
        toolbar.addAction(underline_action)

        # Add "Open" action
        open_action = QAction(QIcon(), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        # Add "Save" action
        save_action = QAction(QIcon(), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        # Add "Save As" action
        save_as_action = QAction(QIcon(), 'Save As', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_file_as)
        toolbar.addAction(save_as_action)

        # Window properties
        self.setWindowTitle("Rich Text Editor")
        self.setGeometry(100, 100, 800, 600)

    def make_bold(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontWeight(75 if fmt.fontWeight() != 75 else 50)  # 75 = bold, 50 = normal
        self.text_edit.setCurrentCharFormat(fmt)

    def make_italic(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.text_edit.setCurrentCharFormat(fmt)

    def make_underline(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.text_edit.setCurrentCharFormat(fmt)

    def open_file(self):
        """ Open a file to edit """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;HTML Files (*.html);;All Files (*)", options=options)

        if filename:
            self.current_file = filename
            with open(filename, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

            self.setWindowTitle(f"Rich Text Editor - {os.path.basename(filename)}")

    def save_file(self):
        """ Save the current content to the current file """
        if self.current_file:
            content = self.text_edit.toPlainText()
            try:
                with open(self.current_file, 'w') as file:
                    file.write(content)
                QMessageBox.information(self, "File Saved", f"File saved successfully: {self.current_file}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file: {str(e)}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """ Save the current content as a new file """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;HTML Files (*.html);;All Files (*)", options=options)

        if filename:
            self.current_file = filename
            content = self.text_edit.toPlainText()
            try:
                with open(filename, 'w') as file:
                    file.write(content)
                self.setWindowTitle(f"Rich Text Editor - {os.path.basename(filename)}")
                QMessageBox.information(self, "File Saved", f"File saved successfully: {self.current_file}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = RichTextEditor()
    editor.show()
    sys.exit(app.exec_())
