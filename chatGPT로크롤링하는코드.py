import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 크롤링할 URL
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%B0%98%EB%8F%84%EC%B2%B4"

# HTTP 요청
response = requests.get(url)
response.raise_for_status()  # 요청 실패 시 예외 발생

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, "html.parser")

# 기사 제목 크롤링
titles = []
for title in soup.find_all("a", class_="news_tit"):  # 네이버 뉴스 제목의 클래스 이름
    titles.append(title.get_text())

# 결과 출력
print("크롤링된 기사 제목:")
for idx, title in enumerate(titles, start=1):
    print(f"{idx}. {title}")

# Excel 파일 생성 및 저장
wb = Workbook()
ws = wb.active
ws.title = "뉴스 제목"

# 헤더 추가
ws.append(["번호", "기사 제목"])

# 데이터 추가
for idx, title in enumerate(titles, start=1):
    ws.append([idx, title])

# 파일 저장
output_file = "results.xlsx"
wb.save(output_file)
print(f"크롤링 결과가 '{output_file}' 파일에 저장되었습니다.")