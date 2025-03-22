import streamlit as st
import os
import shutil

def merge_images_and_delete_subfolders(root_path):
    messages = []
    # root_path 내의 각 항목(하위 폴더)을 확인합니다.
    for item in os.listdir(root_path):
        subfolder = os.path.join(root_path, item)
        if os.path.isdir(subfolder):
            # 하위 폴더 내의 jpg, jpeg 파일들을 처리합니다.
            for file_name in os.listdir(subfolder):
                if file_name.lower().endswith(('.jpg', '.jpeg')):
                    src_file = os.path.join(subfolder, file_name)
                    new_name = f"{item}-{file_name}"
                    dest_file = os.path.join(root_path, new_name)
                    
                    if os.path.exists(dest_file):
                        messages.append(f"경고: {dest_file} 가 이미 존재합니다. 건너뜁니다.")
                    else:
                        shutil.move(src_file, dest_file)
                        messages.append(f"이동: {src_file} -> {dest_file}")
            # 하위 폴더 삭제 (내부에 남은 파일이나 폴더가 있어도 전체 삭제)
            try:
                shutil.rmtree(subfolder)
                messages.append(f"삭제: {subfolder} 폴더 삭제됨")
            except Exception as e:
                messages.append(f"오류: {subfolder} 폴더 삭제 실패: {str(e)}")
    return messages

st.title("폴더 내 jpg 파일 병합 및 하위 폴더 삭제 도구")

# 폴더 경로를 직접 입력받음
folder_path = st.text_input("병합할 폴더의 전체 경로를 입력하세요:")

if st.button("실행"):
    if os.path.isdir(folder_path):
        with st.spinner("작업 중..."):
            log_messages = merge_images_and_delete_subfolders(folder_path)
        st.success("작업이 완료되었습니다.")
        for msg in log_messages:
            st.write(msg)
    else:
        st.error("올바른 폴더가 선택되지 않았습니다.")
