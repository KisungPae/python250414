# demoForm2.py
# demoForm2.ui(화면단) + demoForm2.py(로직단)
# QyQt5 선언
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# 디자인한 파일을 로딩
form_class = uic.loadUiType("demoForm2.ui")[0]

# 폼클래스를 정의(QMainWindow클래스를 상속)
class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 설정
    # 슬롯메서드를 정의
    def firstClick(self):
        self.label.setText("첫 번째 버튼 클릭")
    def secondClick(self):
        self.label.setText("두 번째 버튼 클릭했습니다")
    def thirdClick(self):
        self.label.setText("세 번째 버튼 클릭~~")

# 직접 모듈을 실행했는지 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demoForm = DemoForm()  # DemoForm 객체 생성
    demoForm.show()  # 폼을 화면에 출력
    app.exec_()  # 이벤트 루프 시작