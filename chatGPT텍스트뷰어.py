import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QVBoxLayout, QWidget


class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("텍스트 뷰어")
        self.setGeometry(100, 100, 800, 600)

        # 텍스트 편집기 위젯
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # 읽기 전용으로 설정

        # 중앙 위젯 설정
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.text_edit)
        self.setCentralWidget(central_widget)

        # 메뉴바 설정
        self.create_menu()

    def create_menu(self):
        # 메뉴바 생성
        menu_bar = self.menuBar()

        # 파일 메뉴 생성
        file_menu = menu_bar.addMenu("파일")

        # 열기 액션 생성
        open_action = QAction("열기", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # 종료 액션 생성
        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        # 파일 열기 대화상자
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "텍스트 파일 열기", "", "텍스트 파일 (*.txt);;모든 파일 (*)", options=options)

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_edit.setText(content)
            except Exception as e:
                self.text_edit.setText(f"파일을 열 수 없습니다: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TextViewer()
    viewer.show()
    sys.exit(app.exec_())