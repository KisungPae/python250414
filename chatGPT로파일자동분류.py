import os
import shutil

# 다운로드 폴더 경로
download_dir = r"C:\Users\student\Downloads"

# 이동할 폴더 경로 설정
folders = {
    'images': ['.jpg', '.jpeg'],
    'data': ['.csv', '.xlsx'],
    'docs': ['.txt', '.doc', '.pdf'],
    'archive': ['.zip']
}

# 각 폴더 생성 (없으면)
for folder in folders.keys():
    folder_path = os.path.join(download_dir, folder)
    os.makedirs(folder_path, exist_ok=True)  # 이미 있으면 그냥 넘어감

# 파일 이동 함수
def move_files():
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)

        # 파일인지 확인
        if os.path.isfile(file_path):
            # 확장자 추출 (소문자로 변환)
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            # 확장자에 맞는 폴더 찾아 이동
            for folder, extensions in folders.items():
                if ext in extensions:
                    dest_path = os.path.join(download_dir, folder, filename)
                    print(f"이동: {filename} -> {folder}/")
                    shutil.move(file_path, dest_path)
                    break

# 실행
if __name__ == "__main__":
    move_files()
