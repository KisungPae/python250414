import random
from openpyxl import Workbook

# 제품 데이터 생성
product_names = [
    "스마트폰", "노트북", "태블릿", "스마트워치", "이어폰", 
    "헤드폰", "모니터", "키보드", "마우스", "프린터"
]

# Excel 파일 생성
wb = Workbook()
ws = wb.active
ws.title = "제품리스트"

# 헤더 추가
ws.append(["제품 ID", "제품명", "수량", "가격"])

# 데이터 생성 및 추가
for i in range(1, 101):  # 100개의 데이터 생성
    product_id = f"P{i:03}"  # 제품 ID (예: P001, P002, ...)
    product_name = random.choice(product_names)  # 랜덤 제품명
    quantity = random.randint(1, 100)  # 수량 (1~100)
    price = random.randint(10000, 1000000)  # 가격 (10,000원 ~ 1,000,000원)
    ws.append([product_id, product_name, quantity, price])

# 파일 저장
output_file = "products.xlsx"
wb.save(output_file)
print(f"'{output_file}' 파일이 생성되었습니다.")