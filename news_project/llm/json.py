import json

data = {
    "chu_the": [
        "xăng RON 95-III",
        "E5 RON 92",
        "dầu mazut",
        "xăng dầu"
    ],
    "tinh_chat": [
        "tăng",
        "tăng",
        "giảm",
        "tăng"
    ],
    "gia": [
        "23.400 đồng một lít",
        "22.170 đồng một lít",
        "20.540 - 20.370 đồng một lít"
    ],
    "nguyen_nhan": [
        "căng thẳng leo thang tại Trung Đông",
        "nguồn cung xăng dầu tại Mỹ thắt chặt",
        "thời tiết lạnh gây gián đoạn sản xuất"
    ]
}

# Tạo danh sách câu hoàn chỉnh
sentences = []
for i in range(len(data["chu_the"])):
    if i < len(data["tinh_chat"]) and i < len(data["gia"]):
        chu_the = data["chu_the"][i]
        tinh_chat = data["tinh_chat"][i]
        gia = data["gia"][i]
        
        sentence = f"{chu_the} {tinh_chat} {gia}."
        sentences.append(sentence)

# In ra các câu hoàn chỉnh
for sentence in sentences:
    print(sentence)

# In ra nguyên nhân
print("\nNguyên nhân:")
for nguyen_nhan in data["nguyen_nhan"]:
    print(f'    "{nguyen_nhan}",')
