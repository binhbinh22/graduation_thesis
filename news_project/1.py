import os
import re

# Thư mục chứa các file .docx
folder_path = 'path/to/your/folder'  # Thay đổi đường dẫn tới thư mục của bạn

# Định dạng regex để bắt ngày, tháng, năm từ tiêu đề file
pattern = re.compile(r'^(\d{1,2})\.(\d{1,2})\.(\d{2,4})-(.*\.docx)$')

for filename in os.listdir(folder_path):
    if filename.endswith(".docx"):
        match = pattern.match(filename)
        if match:
            day, month, year, rest = match.groups()
            new_name = f"33.2024.{month.zfill(2)}.{day.zfill(2)}-{rest}"
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_name)
            os.rename(old_file, new_file)
            print(f"Đã đổi tên: {filename} thành {new_name}")

print("Hoàn thành!")
