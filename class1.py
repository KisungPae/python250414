# class1.py
# 1)클래스 정의
class Person:
    # 초기화 메서드
    def __init__(self):
        self.name = "default name"
    def print(self):
        print("My name is {0}".format(self.name))

# 2) 인스턴스 생성
p1 = Person()
p2 = Person()
p2.name = "전우치"

# 3) 메서드
p1.print()
p2.print()

# 전역변수
strName = "전역변수의 값"
class DemoString:
    def __init__(self):
        self.strName = ""
    def set(self, msg):
        self.strName = msg
    def print(self):
        print(strName)
        print(self.strName)

g = DemoString()
g.set("멤버변수에 셋팅")
g.print()