import re

# 이메일 주소를 검사할 정규표현식
email_pattern = re.compile(
    r'^'                     # ^ : 문자열의 시작
    r'[a-zA-Z0-9._%+-]+'     # 이름 부분: 알파벳(대소문자), 숫자, ., _, %, +, - 중 하나 이상
    r'@'                     # @ : 반드시 골뱅이(@) 기호가 들어가야 함
    r'[a-zA-Z0-9.-]+'        # 도메인 부분: 알파벳, 숫자, 점(.), 하이픈(-) 중 하나 이상
    r'\.'                    # \. : 점(.)은 특수문자라서 역슬래시(\)로 이스케이프 처리
    r'[a-zA-Z]{2,}'          # 마지막 부분: 알파벳 2개 이상 (예: com, net, org 등)
    r'$'                     # $ : 문자열의 끝
)

# 샘플 이메일 주소 리스트
sample_emails = [
    "user@example.com",             # 유효
    "john.doe@company.co.uk",       # 유효
    "hello_world123@gmail.com",     # 유효
    "invalid-email@",               # 유효하지 않음 (도메인 없음)
    "missingatsign.com",            # 유효하지 않음 (@ 없음)
    "user@.com",                    # 유효하지 않음 (도메인 없음)
    "name@domain.c",                # 유효하지 않음 (끝이 한 글자)
    "user@domain..com",             # 유효하지 않음 (.. 연속 점)
    "user@@domain.com",             # 유효하지 않음 (@ 두 개)
    "valid.email+alias@sub.domain.org"  # 유효
]

# 이메일 검사 함수
def check_email(email):
    return bool(email_pattern.match(email))

# 검사 실행
for email in sample_emails:
    result = "Valid" if check_email(email) else "Invalid"
    print(f"{email}: {result}")
