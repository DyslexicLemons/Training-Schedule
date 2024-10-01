from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class RichTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = QWebEngineView()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Rich Text Editor with CKEditor")

        # Load CKEditor
        ckeditor_html = '''
        <html>
        <head>
            <script src="https://cdn.ckeditor.com/4.16.1/standard/ckeditor.js"></script>
        </head>
        <body>
            <textarea name="editor1"></textarea>
            <script>
                CKEDITOR.replace( 'editor1' );
            </script>
        </body>
        </html>
        '''
        self.editor.setHtml(ckeditor_html)

        layout = QVBoxLayout()
        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = RichTextEditor()
    editor.show()
    sys.exit(app.exec_())
