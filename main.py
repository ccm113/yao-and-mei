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
    
    # 将本地图片转换为 Base64
    processed_photos = []
    for photo in photos:
        url = photo["url"]
        # 如果是本地路径，转换为 Base64
        if os.path.exists(url):
            base64_str = image_to_base64(url)
            if base64_str:
                url = f"data:image/jpeg;base64,{base64_str}"
        processed_photos.append({"url": url, "caption": photo["caption"]})
    
    # 生成椭圆轮播HTML
    import json as json_module
    photos_json = json_module.dumps(processed_photos).replace('"', '\\"')
    
    carousel_html = f'''
    <style>
    .carousel-container {{
        width: 100%;
        height: 450px;
        position: relative;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(135deg, #fff5f5 0%, #fdf2f8 50%, #fce7f3 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(255, 107, 157, 0.1);
    }}

    .carousel-item {{
        position: absolute;
        width: 140px;
        height: 140px;
        border-radius: 16px;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        object-fit: cover;
        z-index: 5;
        border: 4px solid white;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }}

    .carousel-item:hover {{
        transform: scale(1.15);
        box-shadow: 0 15px 40px rgba(255, 107, 157, 0.4);
        z-index: 100;
    }}

    .add-btn {{
        position: absolute;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6b9d, #ff8e53);
        border: 4px solid white;
        color: white;
        font-size: 36px;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(255, 107, 157, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        z-index: 200;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .add-btn:hover {{
        transform: scale(1.15);
        box-shadow: 0 15px 40px rgba(255, 107, 157, 0.7);
    }}
    </style>

    <div class="carousel-container" id="carouselContainer">
        <button class="add-btn" onclick="window.location.href='?add_photo=true'">+</button>
    </div>

    <script>
    let photos = JSON.parse('{photos_json}');
    let angle = 0;
    let animationId;
    const speed = 0.012;  // 滚动速度

    function initCarousel() {{
        const container = document.getElementById('carouselContainer');
        
        photos.forEach(function(photo, index) {{
            const img = document.createElement('img');
            img.src = photo.url;
            img.className = 'carousel-item';
            img.title = photo.caption;
            img.alt = photo.caption;
            container.appendChild(img);
        }});
        
        animate();
    }}

    function animate() {{
        const items = document.querySelectorAll('.carousel-item');
        const container = document.getElementById('carouselContainer');
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        
        // 椭圆参数
        const centerX = containerWidth / 2;
        const centerY = containerHeight / 2;
        const radiusX = containerWidth * 0.35;  // 水平半径
        const radiusY = containerHeight * 0.25;  // 垂直半径
        
        items.forEach(function(item, index) {{
            // 每个图片有不同的起始角度，形成椭圆分布
            const itemAngle = angle + (index * (360 / items.length) * Math.PI / 180);
            const x = centerX - 70 + radiusX * Math.cos(itemAngle);
            const y = centerY - 70 + radiusY * Math.sin(itemAngle);
            
            item.style.left = x + 'px';
            item.style.top = y + 'px';
            
            // 根据位置调整大小和透明度（模拟3D效果）
            const visibility = (Math.cos(itemAngle) + 1) / 2;
            const scale = 0.7 + visibility * 0.3;
            item.style.transform = 'scale(' + scale + ')';
            item.style.opacity = 0.55 + visibility * 0.45;
            item.style.zIndex = Math.floor(visibility * 20) + 5;
        }});
        
        // 持续旋转（从右向左滑动效果）
        angle += speed;
        animationId = requestAnimationFrame(animate);
    }}

    // 初始化
    initCarousel();

    // 响应窗口大小变化
    window.addEventListener('resize', function() {{
        // 重新计算位置
    }});
    </script>
    '''
    
    st.markdown(carousel_html, unsafe_allow_html=True)
    
    # 添加照片
    if 'add_photo' in st.query_params:
        photos.append({
            "url": f"https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200&random={os.urandom(4).hex()}",
            "caption": f"新照片 {len(photos) + 1}"
        })
        save_data(PHOTOS_FILE, photos)
        del st.query_params['add_photo']
        st.rerun()
    
    # 词云图
    st.markdown("---")
    st.header("💬 我俩关键词")
    
    try:
        from wordcloud import WordCloud, STOPWORDS
        import matplotlib.pyplot as plt
        
        # 词频字典
        word_freq = {
            "李昕垚": 20, "梅": 20, "垚": 18, "闺蜜": 16, "幸福": 16,
            "快乐": 13, "美好": 13, "温暖": 12, "开心": 12, "欢笑": 11,
            "永远": 11, "友情": 11, "温柔": 10, "勇敢": 10, "吃货": 9,
            "最可爱": 9, "最爱": 9, "最善良": 9, "美丽动人": 8, "温馨": 8,
            "心中": 8, "最": 8, "美": 7, "闪闪发光": 7, "独一无二": 7,
            "姐妹情深": 7, "友谊万岁": 7, "心心相印": 6, "形影不离": 6,
            "携手同行": 6, "梦想成真": 6
        }
        
        # 尝试多个平台的字体路径
        font_path = None
        font_candidates = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/arphic/uming.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/Songti.ttc",
        ]
        
        for candidate in font_candidates:
            if os.path.exists(candidate):
                font_path = candidate
                break
        
        # 创建词云图
        wc_params = {
            "width": 800,
            "height": 400,
            "background_color": "white",
            "max_words": 200,
            "colormap": "plasma",
            "random_state": 42,
            "prefer_horizontal": 0.9,
            "relative_scaling": 0.5,
            "scale": 2,
            "collocations": False,
            "stopwords": set(STOPWORDS),
            "contour_width": 1,
            "contour_color": "lightgray"
        }
        
        if font_path:
            wc_params["font_path"] = font_path
        
        wc = WordCloud(**wc_params)
        wordcloud = wc.generate_from_frequencies(word_freq)
        
        # 显示词云图
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(plt)
    
    except Exception as e:
        st.error(f"词云图生成失败: {str(e)}")
        st.markdown("### 我俩关键词")
        keywords = ["李昕垚", "梅", "闺蜜", "幸福", "快乐", "美好", "温暖", "友情", "永远", "温柔"]
        st.write(" ".join([f"**{kw}**" for kw in keywords]))

# 运行主页面
home_page()
