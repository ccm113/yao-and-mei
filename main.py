import streamlit as st
import json
import os

# 数据文件路径
USERS_FILE = "users.json"
PHOTOS_FILE = "photos.json"
WISHLIST_FILE = "wishlist.json"

# 初始化数据文件
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    if not os.path.exists(PHOTOS_FILE):
        with open(PHOTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump([
                {"url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200", "caption": "相识的那天", "rotation": 0},
                {"url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200", "caption": "第一次约会", "rotation": 0},
                {"url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=200", "caption": "一起看日落", "rotation": 0},
                {"url": "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=200", "caption": "海边漫步", "rotation": 0}
            ], f)
    
    if not os.path.exists(WISHLIST_FILE):
        with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化
init_files()

# 页面配置
st.set_page_config(
    page_title="垚＆槑",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主页面
def home_page():
    # 欢迎信息
    st.title("💕 垚＆槑")
    st.markdown("### 欢迎来到我们的精神小世界")
    
    # 照片展示
    st.markdown("---")
    st.header("📷 感谢相机")
    photos = load_data(PHOTOS_FILE)
    
    # 使用简单的网格布局
    if photos:
        cols = st.columns(4)
        for i, photo in enumerate(photos):
            with cols[i % 4]:
                rotation = photo.get('rotation', 0)
                st.markdown(f"""
                <div style="transform: rotate({rotation}deg); margin: 10px;">
                    <img src="{photo['url']}" style="width: 100%; border-radius: 10px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);" />
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"↻ 左旋", key=f"left_{i}"):
                        photos[i]['rotation'] = (rotation - 90) % 360
                        save_data(PHOTOS_FILE, photos)
                        st.rerun()
                with col2:
                    if st.button(f"↺ 右旋", key=f"right_{i}"):
                        photos[i]['rotation'] = (rotation + 90) % 360
                        save_data(PHOTOS_FILE, photos)
                        st.rerun()
    
    # 添加照片按钮
    if st.button("➕ 添加新照片"):
        photos.append({
            "url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200",
            "caption": "新照片",
            "rotation": 0
        })
        save_data(PHOTOS_FILE, photos)
        st.rerun()

# 运行主页面
home_page()
