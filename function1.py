# function1.py

# 함수를 정의
def setValue(newValue):
    # 지역변수 초기화
    x = newValue
    print("지역변수:", x)

# 함수 호출
retValue = setValue(5)
print(retValue)

# 여러개 리턴
def swap(x,y):
    return y,x

# 호출
retValue = swap(3,4)
print(retValue)

print(dir())
print(globals())

# 기본값 몇시
def times(a=10, b=20):
    return a*b

# 호출
print(times())
print(times(5))
print(times(5, 6))

# 키워드 인자
def connectURI(server, port):
    strURL = "http://" + server + ":" + port
    return strURL

print(connectURI("multi.com", "80"))
print(connectURI(port="80", server="multi.com"))

# 가변인자 함수
def union(*ar):
    # 지역변수
    result = []
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result

# 호출
print(union("HAM", "EGG"))
print(union("HAM", "EGG", "SPAM"))

# 람다함수
g = lambda x,y:x*y
print( g(3,4) )
print( g(5,6) )
print( (lambda x:x*x)(3) )
print( globals() )

