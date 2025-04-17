import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QTextEdit, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import json

api_key = "YOUR_OPENAI_API_KEY"  # 여기에 OpenAI API 키를 입력하세요.

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_path = None
        # OpenAI API 키를 환경 변수에서 가져오거나 직접 설정
        self.api_key = api_key

    def initUI(self):
        # 메인 위젯 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(main_widget)
        
        # 이미지 선택 버튼
        self.select_button = QPushButton('이미지 선택')
        self.select_button.clicked.connect(self.select_image)
        main_layout.addWidget(self.select_button)
        
        # 이미지 표시 레이블
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid #ddd;")
        main_layout.addWidget(self.image_label)
        
        # 분석 버튼
        self.analyze_button = QPushButton('이미지 분석')
        self.analyze_button.clicked.connect(self.analyze_image)
        self.analyze_button.setEnabled(False)  # 이미지 선택 전까지 비활성화
        main_layout.addWidget(self.analyze_button)
        
        # 결과 텍스트 영역
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(150)
        main_layout.addWidget(self.result_text)
        
        # 창 설정
        self.setWindowTitle('이미지 설명 애플리케이션')
        self.setGeometry(300, 300, 600, 600)
        self.show()
        
    def select_image(self):
        # 파일 다이얼로그로 이미지 선택
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, '이미지 선택', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        
        if file_path:
            self.image_path = file_path
            # 이미지 표시
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            # 분석 버튼 활성화
            self.analyze_button.setEnabled(True)
            # 결과 초기화
            self.result_text.clear()
            
    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    def analyze_image(self):
        if not self.image_path:
            self.result_text.setText("이미지를 먼저 선택해주세요.")
            return
            
        if not self.api_key:
            self.result_text.setText("OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 설정하세요.")
            return
            
        self.result_text.setText("이미지 분석 중...")
        
        try:
            # 이미지를 base64로 인코딩
            base64_image = self.encode_image_to_base64(self.image_path)
            
            # OpenAI API 요청
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "이 이미지에 대한 자세한 설명을 해주세요."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                    headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                description = result["choices"][0]["message"]["content"]
                self.result_text.setText(description)
            else:
                self.result_text.setText(f"API 요청 오류: {response.status_code}\n{response.text}")
                
        except Exception as e:
            self.result_text.setText(f"오류 발생: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoForm()
    sys.exit(app.exec_())