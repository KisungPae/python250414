import sys
import base64
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import openai
from pathlib import Path

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        
        # OpenAI API 키 설정
        openai.api_key = "YOUR_OPENAI_API_KEY"  # 여기에 OpenAI API 키를 입력하세요.
        # OpenAI API 엔드포인트 설정
        openai.api_base = "https://api.openai.com/v1"

    def setupUI(self):
        # 윈도우 설정
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("이미지 설명 프로그램")

        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 이미지 표시 레이블
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 400)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid black")
        layout.addWidget(self.image_label)

        # 이미지 선택 버튼
        self.select_button = QPushButton("이미지 선택")
        self.select_button.clicked.connect(self.select_image)
        layout.addWidget(self.select_button)

        # 설명 분석 버튼
        self.analyze_button = QPushButton("이미지 설명 분석")
        self.analyze_button.clicked.connect(self.analyze_image)
        layout.addWidget(self.analyze_button)

        # 결과 표시 텍스트 영역
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.image_path = None

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def analyze_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "경고", "이미지를 먼저 선택해주세요.")
            return

        try:
            # 이미지를 base64로 인코딩
            with open(self.image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # OpenAI API 호출
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "이 이미지에 대해 설명해주세요."},
                            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_image}"}
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post(
                f"{openai.api_base}/chat/completions",
                headers=headers,
                json=payload
            )
            
            # 응답 확인 및 결과 표시
            if response.status_code == 200:
                result = response.json()
                description = result['choices'][0]['message']['content']
                self.result_text.setText(description)
            else:
                raise Exception(f"API 오류: {response.status_code} - {response.text}")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"분석 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    sys.exit(app.exec_())