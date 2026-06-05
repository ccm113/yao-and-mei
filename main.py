import streamlit as st
import json
import os
import base64

# 数据文件路径
USERS_FILE = "users.json"
PHOTOS_FILE = "photos.json"
WISHLIST_FILE = "wishlist.json"

# 将本地图片转换为 Base64
def image_to_base64(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# 初始化数据文件
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    if not os.path.exists(PHOTOS_FILE):
        # 使用本地图片
        local_photos = []
        image_dir = "image"
        if os.path.exists(image_dir):
            for i in range(1, 12):
                img_path = os.path.join(image_dir, f"tupian ({i}).jpg")
                if os.path.exists(img_path):
                    local_photos.append({"url": img_path, "caption": f"照片 {i}"})
        
        # 如果没有本地图片，使用网络图片作为备用
        if not local_photos:
            local_photos = [
                {"url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200", "caption": "相识的那天"},
                {"url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200", "caption": "第一次约会"},
                {"url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=200", "caption": "一起看日落"},
                {"url": "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=200", "caption": "海边漫步"},
                {"url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200", "caption": "闺蜜时光"},
                {"url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200", "caption": "快乐时刻"},
                {"url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200", "caption": "美好回忆"},
                {"url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=200", "caption": "温馨瞬间"}
            ]
        
        with open(PHOTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(local_photos, f, ensure_ascii=False)
    
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
    
    # 使用 Streamlit 原生组件展示照片网格
    cols = st.columns(4)
    for i, photo in enumerate(photos):
        col = cols[i % 4]
        # 处理图片路径
        url = photo["url"]
        if os.path.exists(url):
            base64_str = image_to_base64(url)
            if base64_str:
                url = f"data:image/jpeg;base64,{base64_str}"
        with col:
            st.image(url, caption=photo["caption"], width=150)
    
    # 添加照片按钮
    if st.button("➕ 添加新照片"):
        photos.append({
            "url": f"https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200&random={os.urandom(4).hex()}",
            "caption": f"新照片 {len(photos) + 1}"
        })
        save_data(PHOTOS_FILE, photos)
        st.rerun()
    
    # 词云图 - 使用简单的关键词展示
    st.markdown("---")
    st.header("💬 我俩关键词")
    
    keywords = [
        {"text": "李昕垚", "size": 48, "color": "#FF6B9D"},
        {"text": "梅", "size": 48, "color": "#FF8E53"},
        {"text": "闺蜜", "size": 32, "color": "#A855F7"},
        {"text": "幸福", "size": 28, "color": "#EC4899"},
        {"text": "快乐", "size": 28, "color": "#F43F5E"},
        {"text": "美好", "size": 24, "color": "#FB7185"},
        {"text": "温暖", "size": 24, "color": "#FEF3C7"},
        {"text": "友情", "size": 22, "color": "#A78BFA"},
        {"text": "永远", "size": 22, "color": "#60A5FA"},
        {"text": "温柔", "size": 20, "color": "#34D399"},
        {"text": "勇敢", "size": 20, "color": "#FBBF24"},
        {"text": "吃货", "size": 18, "color": "#FB923C"},
        {"text": "最可爱", "size": 18, "color": "#F472B6"},
        {"text": "最善良", "size": 16, "color": "#C084FC"},
        {"text": "美丽动人", "size": 16, "color": "#60A5FA"},
        {"text": "心心相印", "size": 14, "color": "#34D399"},
        {"text": "姐妹情深", "size": 14, "color": "#FB7185"},
        {"text": "友谊万岁", "size": 12, "color": "#FBBF24"},
    ]
    
    # 生成关键词展示 HTML
    keywords_html = '<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; padding: 20px; background: linear-gradient(135deg, #fff5f5 0%, #fdf2f8 100%); border-radius: 16px;">'
    for kw in keywords:
        keywords_html += f'<span style="font-size: {kw["size"]}px; color: {kw["color"]}; font-weight: bold; padding: 8px 16px; border-radius: 20px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">{kw["text"]}</span>'
    keywords_html += '</div>'
    
    st.markdown(keywords_html, unsafe_allow_html=True)

# 运行主页面
home_page()
