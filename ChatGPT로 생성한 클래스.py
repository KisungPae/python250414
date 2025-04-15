# Person 클래스 정의
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        # f-string문법으로 변수명 바로 넘김
        print(f"ID: {self.id}, Name: {self.name}")

# Manager 클래스 정의 (Person 상속)
class Manager(Person):
    def __init__(self, id, name, title):
        # 부모를 지칭하는 함수
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")

# Employee 클래스 정의 (Person 상속)
class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")

# 테스트 코드 10개
def run_tests():
    print("1. Person 인스턴스 테스트")
    p1 = Person(1, "Alice")
    p1.printInfo()

    print("\n2. Manager 인스턴스 테스트")
    m1 = Manager(2, "Bob", "Team Lead")
    m1.printInfo()

    print("\n3. Employee 인스턴스 테스트")
    e1 = Employee(3, "Charlie", "Python")
    e1.printInfo()

    print("\n4. Manager의 title 확인")
    print(f"Title: {m1.title}")

    print("\n5. Employee의 skill 확인")
    print(f"Skill: {e1.skill}")

    print("\n6. Person의 id 변경 테스트")
    p1.id = 10
    p1.printInfo()

    print("\n7. Manager 이름 변경 테스트")
    m1.name = "Robert"
    m1.printInfo()

    print("\n8. Employee skill 변경 테스트")
    e1.skill = "Java"
    e1.printInfo()

    print("\n9. Manager 상속 확인")
    print(isinstance(m1, Person))  # True

    print("\n10. Employee 상속 확인")
    print(isinstance(e1, Person))  # True

# 테스트 실행
if __name__ == "__main__":
    run_tests()