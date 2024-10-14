import os
import shutil

def copy_c_file(source_file, destination_folder):
    # 목적지 폴더가 없으면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # 소스 파일이 .c 확장자인지 확인
    if source_file.endswith('.c'):
        # 파일 이름 추출
        filename = os.path.basename(source_file)
        destination_path = os.path.join(destination_folder, filename)
        
        # 파일 복사
        shutil.copy2(source_file, destination_path)
        print(f"파일 '{filename}'이(가) '{destination_folder}'로 복사되었습니다.")
    else:
        print("오류: 지정된 파일이 .c 확장자가 아닙니다.")

# copy_c_file('/path/to/source/file.c', '/path/to/
