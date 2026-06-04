import streamlit as st

st.title("测试应用")
st.write("这是一个简单的测试应用")

# 测试照片展示
photos = [
    {"url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200", "caption": "测试照片"},
]

if photos:
    cols = st.columns(4)
    for i, photo in enumerate(photos):
        with cols[i % 4]:
            st.image(photo['url'], use_column_width=True)

st.button("测试按钮")
