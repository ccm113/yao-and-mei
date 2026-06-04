import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import math
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
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
                {"url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200", "caption": "相识的那天"},
                {"url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200", "caption": "第一次约会"},
                {"url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=200", "caption": "一起看日落"},
                {"url": "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=200", "caption": "海边漫步"}
            ], f)
    
    if not os.path.exists(WISHLIST_FILE):
        with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# 读取数据
def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# 保存数据
def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 登录检查
def check_login():
    return st.session_state.get('logged_in', False)

# 爱心绽放动画
def show_heart_animation():
    st.markdown("""
    <style>
    .heart {
        animation: heartbeat 1s ease-in-out infinite;
        color: #ff6b9d;
        font-size: 40px;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .splash-text {
        font-family: 'Microsoft YaHei', sans-serif;
        font-size: 36px;
        color: #ff6b9d;
        animation: fadeIn 2s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center; padding-top: 100px;">', unsafe_allow_html=True)
    
    # 爱心粒子
    hearts = []
    for i in range(20):
        size = random.randint(20, 60)
        left = random.randint(10, 90)
        delay = random.uniform(0, 2)
        hearts.append(f'<span class="heart" style="position: absolute; left: {left}%; animation-delay: {delay}s;">💕</span>')
    
    st.markdown(''.join(hearts), unsafe_allow_html=True)
    
    # 文字显示
    st.markdown('<div class="splash-text" style="margin-top: 150px;">李昕垚 and 陈昌梅</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ff9800; font-size: 20px; margin-top: 20px;">💖 垚＆槑 的精神小世界 💖</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(3)

# 登录页面
def login_page():
    st.title("💖 欢迎来到闺蜜小世界")
    
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("登录"):
            users = load_data(USERS_FILE)
            user = next((u for u in users if u['username'] == username and u['password'] == password), None)
            
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("登录成功！")
                time.sleep(1)
                st.rerun()
            else:
                st.error("用户名或密码错误")
    
    with col2:
        if st.button("注册"):
            st.session_state['page'] = 'register'
            st.rerun()

# 注册页面
def register_page():
    st.title("🎀 注册新账户")
    
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    confirm_password = st.text_input("确认密码", type="password")
    
    if st.button("注册"):
        if not username or not password:
            st.error("请填写所有字段")
        elif password != confirm_password:
            st.error("两次密码不一致")
        else:
            users = load_data(USERS_FILE)
            if any(u['username'] == username for u in users):
                st.error("用户名已存在")
            else:
                users.append({'username': username, 'password': password})
                save_data(USERS_FILE, users)
                st.success("注册成功！")
                time.sleep(1)
                st.session_state['page'] = 'login'
                st.rerun()
    
    if st.button("返回登录"):
        st.session_state['page'] = 'login'
        st.rerun()

# 首页
def home_page():
    # 开屏动画
    if 'splash_shown' not in st.session_state:
        st.session_state['splash_shown'] = True
        show_heart_animation()
    

    
    # 照片展示
    st.markdown("---")
    st.header("📷 感谢相机")
    photos = load_data(PHOTOS_FILE)
    
    # 生成椭圆轮播HTML
    carousel_html = """
    <style>
    .carousel-container {
        width: 100%;
        height: 400px;
        position: relative;
        overflow: hidden;
    }
    
    .carousel-item {
        position: absolute;
        width: 100px;
        height: 100px;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        object-fit: cover;
        z-index: 5;
    }
    
    .carousel-item:hover {
        transform: scale(1.15);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        z-index: 10;
    }
    
    .add-btn {
        position: absolute;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6b9d, #ff8e53);
        border: none;
        color: white;
        font-size: 28px;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(255,107,157,0.5);
        transition: transform 0.3s;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 20;
    }
    
    .add-btn:hover {
        transform: translate(-50%, -50%) scale(1.1);
    }
    
    .modal {
        display: none;
        position: fixed;
        z-index: 100;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0,0,0,0.7);
    }
    
    .modal-content {
        background-color: #fefefe;
        margin: 10% auto;
        padding: 20px;
        border-radius: 15px;
        width: 80%;
        max-width: 500px;
        text-align: center;
    }
    
    .modal-content img {
        max-width: 100%;
        max-height: 400px;
        border-radius: 10px;
    }
    
    .modal-buttons {
        margin-top: 20px;
        display: flex;
        justify-content: center;
        gap: 15px;
    }
    
    .modal-btn {
        padding: 10px 25px;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        font-size: 15px;
    }
    
    .delete-btn {
        background-color: #ff4444;
        color: white;
    }
    
    .replace-btn {
        background-color: #4488ff;
        color: white;
    }
    
    .close-btn {
        color: #aaa;
        float: right;
        font-size: 25px;
        font-weight: bold;
        cursor: pointer;
    }
    </style>
    
    <div class="carousel-container" id="carouselContainer">
        <button class="add-btn" onclick="window.location.href='?add_photo=true'">+</button>
    </div>
    
    <div id="photoModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <img id="modalImage" src="" />
            <div class="modal-buttons">
                <button class="modal-btn delete-btn" onclick="deletePhoto()">删除</button>
                <button class="modal-btn replace-btn" onclick="replacePhoto()">替换</button>
            </div>
        </div>
    </div>
    
    <script>
    let currentIndex = -1;
    let photos = %s;
    let angle = 0;
    let animationId;
    
    function initCarousel() {
        const container = document.getElementById('carouselContainer');
        
        photos.forEach((photo, index) => {
            const img = document.createElement('img');
            img.src = photo.url;
            img.className = 'carousel-item';
            img.onclick = () => showModal(photo.url, index);
            container.appendChild(img);
        });
        
        animate();
    }
    
    function animate() {
        const items = document.querySelectorAll('.carousel-item');
        const centerX = 50;
        const centerY = 50;
        const radiusX = 35;
        const radiusY = 20;
        
        items.forEach((item, index) => {
            const itemAngle = angle + (index * 72 * Math.PI / 180);
            const x = centerX + radiusX * Math.cos(itemAngle);
            const y = centerY + radiusY * Math.sin(itemAngle);
            
            item.style.left = x + '%';
            item.style.top = y + '%';
            item.style.transform = 'translate(-50%, -50%)';
        });
        
        angle += 0.01;
        animationId = requestAnimationFrame(animate);
    }
    
    function showModal(src, index) {
        currentIndex = index;
        document.getElementById('modalImage').src = src;
        document.getElementById('photoModal').style.display = 'block';
    }
    
    function closeModal() {
        document.getElementById('photoModal').style.display = 'none';
        currentIndex = -1;
    }
    
    function deletePhoto() {
        if (currentIndex >= 0) {
            window.location.href = '?delete=' + currentIndex;
        }
    }
    
    function replacePhoto() {
        if (currentIndex >= 0) {
            window.location.href = '?replace=' + currentIndex;
        }
    }
    
    window.onclick = function(event) {
        const modal = document.getElementById('photoModal');
        if (event.target == modal) {
            closeModal();
        }
    };
    
    // 初始化
    initCarousel();
    </script>
    """ % photos
    
    st.markdown(carousel_html, unsafe_allow_html=True)
    
    # 处理照片操作
    query_params = st.experimental_get_query_params()
    
    if 'delete' in query_params:
        idx = int(query_params['delete'][0])
        if idx < len(photos):
            photos.pop(idx)
            save_data(PHOTOS_FILE, photos)
            st.experimental_set_query_params()
            st.rerun()
    
    if 'replace' in query_params:
        idx = int(query_params['replace'][0])
        if idx < len(photos):
            photos[idx]['url'] = f"https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200&random={random.randint(1, 1000)}"
            save_data(PHOTOS_FILE, photos)
            st.experimental_set_query_params()
            st.rerun()
    
    if 'add_photo' in query_params:
        photos.append({
            "url": f"https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200&random={random.randint(1, 1000)}",
            "caption": f"照片 {len(photos) + 1}"
        })
        save_data(PHOTOS_FILE, photos)
        st.experimental_set_query_params()
        st.rerun()
    
    # 词云图
    st.markdown("---")
    st.header("💬 我俩关键词")
    
    word_freq = {
        "李昕垚": 20, "梅": 20, "垚": 20, "闺蜜": 16, "幸福": 16,
        "快乐": 13, "美好": 13, "温暖": 12, "开心": 12, "欢笑": 11,
        "永远": 11, "友情": 11, "温柔": 10, "勇敢": 10, "吃货": 9,
        "最可爱": 9, "最爱": 9, "最善良": 9, "美丽动人": 8, "温馨": 8,
        "闪闪发光": 7, "独一无二": 7, "姐妹情深": 7, "友谊万岁": 7,
        "心心相印": 6, "形影不离": 6, "携手同行": 6, "梦想成真": 6
    }
    
    colors = [
        '#E91E63', '#FF4081', '#F06292', '#9C27B0', '#BA68C8',
        '#673AB7', '#5C6BC0', '#3F51B5', '#42A5F5', '#2196F3',
        '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#8BC34A',
        '#FF9800', '#FFA726', '#FF5722', '#FF7043'
    ]
    
    wc = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',
        width=800, height=400,
        background_color='white',
        colormap='plasma',
        random_state=42,
        prefer_horizontal=0.9,
        relative_scaling=0.5,
        scale=2,
        collocations=False,
        contour_width=1,
        contour_color='lightgray'
    ).generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# 故事回顾
def story_page():
    st.title("📖 故事回顾")
    
    st.markdown("""
    ## 🌸 相识相知

    那是一个阳光明媚的午后，在大学的图书馆里，李昕垚和陈昌梅第一次相遇。
    
    **那一刻，命运的齿轮开始转动...**
    
    昕垚正在寻找一本很难找的书，而这本书正好在昌梅的手中。她们就这样开始了第一次交谈，发现彼此有很多共同爱好——都喜欢美食、旅行，还有看浪漫的电影。
    
    ## 🌼 相知相伴
    
    从那以后，她们成了最好的朋友。一起上课、一起吃饭、一起在校园里散步聊天。
    
    记得有一次，昕垚因为考试失利而心情低落，昌梅陪着她在操场上走了一圈又一圈，听她倾诉，给她鼓励。那一刻，她们知道，这份友谊会持续很久很久。
    
    ## 🌷 闺蜜情深
    
    毕业之后，她们虽然工作在不同的城市，但依然保持着密切的联系。每个周末都会视频通话，分享彼此的生活点滴。
    
    她们约定，每年都要一起去一个新的地方旅行，创造更多美好的回忆。
    
    **愿这份友谊，天长地久，直到永远...** 💖
    """)
    
    st.image("https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600", caption="闺蜜情深", use_column_width=True)

# 小游戏
def game_page():
    st.title("🎮 闺蜜小游戏")
    
    game_type = st.selectbox("选择游戏", ["猜猜我是谁", "成语接龙", "真心话大冒险"])
    
    if game_type == "猜猜我是谁":
        st.subheader("🤔 猜猜我是谁")
        st.write("根据描述猜出是哪位闺蜜！")
        
        questions = [
            {"desc": "喜欢吃甜食，特别是草莓蛋糕", "answer": "李昕垚"},
            {"desc": "最喜欢的颜色是粉色", "answer": "陈昌梅"},
            {"desc": "总是充满正能量，给人温暖", "answer": "李昕垚"},
            {"desc": "梦想是环游世界", "answer": "陈昌梅"},
            {"desc": "最擅长做的菜是红烧肉", "answer": "李昕垚"}
        ]
        
        if 'current_q' not in st.session_state:
            st.session_state['current_q'] = 0
            st.session_state['score'] = 0
        
        q = questions[st.session_state['current_q']]
        st.write(f"**题目 {st.session_state['current_q'] + 1}：** {q['desc']}")
        
        answer = st.text_input("你的答案")
        
        if st.button("提交"):
            if answer.strip() == q['answer']:
                st.success("🎉 答对了！")
                st.session_state['score'] += 1
            else:
                st.error(f"😢 答错了，正确答案是：{q['answer']}")
            
            if st.session_state['current_q'] < len(questions) - 1:
                st.session_state['current_q'] += 1
                st.rerun()
            else:
                st.markdown(f"---")
                st.write(f"🎉 游戏结束！你的得分：{st.session_state['score']}/{len(questions)}")
                if st.button("再玩一次"):
                    st.session_state['current_q'] = 0
                    st.session_state['score'] = 0
                    st.rerun()
    
    elif game_type == "成语接龙":
        st.subheader("📝 成语接龙")
        st.write("以下一个成语的首字开头，接出新的成语！")
        
        if 'current_idiom' not in st.session_state:
            st.session_state['current_idiom'] = "一心一意"
        
        st.write(f"当前成语：**{st.session_state['current_idiom']}**")
        next_idiom = st.text_input("接下一个成语")
        
        if st.button("接龙"):
            last_char = st.session_state['current_idiom'][-1]
            first_char = next_idiom[0] if next_idiom else ''
            
            if first_char == last_char:
                st.success("✅ 接龙成功！")
                st.session_state['current_idiom'] = next_idiom
                st.rerun()
            else:
                st.error(f"❌ 开头字不对！应该以 '{last_char}' 开头")
    
    else:
        st.subheader("🎲 真心话大冒险")
        
        truths = [
            "你最想和闺蜜一起做的一件事是什么？",
            "你觉得闺蜜最大的优点是什么？",
            "你们之间最难忘的回忆是什么？",
            "如果可以穿越时空，你想回到和闺蜜相识的那一天吗？",
            "你想对闺蜜说但一直没说出口的话是？"
        ]
        
        dares = [
            "给闺蜜发一条甜蜜的微信",
            "学一个可爱的表情发给闺蜜",
            "唱一首闺蜜最喜欢的歌",
            "说出三个闺蜜的优点",
            "做一个搞笑的鬼脸"
        ]
        
        if st.button("🎯 真心话"):
            st.session_state['truth_question'] = random.choice(truths)
        
        if 'truth_question' in st.session_state:
            st.write(f"**真心话问题：** {st.session_state['truth_question']}")
            answer = st.text_area("写下你的答案：", height=100)
            if st.button("保存答案"):
                if answer:
                    st.success("答案已保存！")
                    st.session_state['truth_answer'] = answer
        
        if st.button("🎲 大冒险"):
            st.write(f"**大冒险任务：** {random.choice(dares)}")

# 真心话问答
def qna_page():
    st.title("💬 相互了解")
    st.subheader("让我们更了解彼此")
    
    questions = [
        {"q": "你最喜欢的颜色是什么？", "options": ["粉色", "蓝色", "紫色", "绿色"]},
        {"q": "你最喜欢的食物是什么？", "options": ["火锅", "甜品", "烧烤", "寿司"]},
        {"q": "你最喜欢的季节是？", "options": ["春天", "夏天", "秋天", "冬天"]},
        {"q": "你最大的梦想是？", "options": ["环游世界", "成为富豪", "拥有自己的小店", "家庭幸福"]},
        {"q": "如果有超能力，你想要什么？", "options": ["会飞", "读心术", "时间旅行", "隐身"]}
    ]
    
    if 'answers' not in st.session_state:
        st.session_state['answers'] = {}
    
    for i, q in enumerate(questions):
        st.write(f"**{i + 1}. {q['q']}**")
        answer = st.radio(f"问题 {i + 1}", q['options'], key=f"q{i}", horizontal=True)
        st.session_state['answers'][i] = answer
    
    if st.button("查看我的选择"):
        st.markdown("---")
        st.subheader("📋 我的答案")
        for i, q in enumerate(questions):
            st.write(f"{i + 1}. {q['q']} → **{st.session_state['answers'].get(i, '未选择')}**")

# 心愿清单
def wishlist_page():
    st.title("🌍 心愿清单")
    st.subheader("想和你一起去的地方")
    
    destinations = [
        {"name": "巴黎", "emoji": "🗼", "desc": "浪漫之都，埃菲尔铁塔"},
        {"name": "东京", "emoji": "🏯", "desc": "繁华都市，樱花季"},
        {"name": "巴厘岛", "emoji": "🌴", "desc": "热带天堂，海滩度假"},
        {"name": "威尼斯", "emoji": "🚤", "desc": "水城风情，浪漫之旅"},
        {"name": "悉尼", "emoji": "🌉", "desc": "海港城市，歌剧院"},
        {"name": "马尔代夫", "emoji": "🏝️", "desc": "海岛度假，水上别墅"},
        {"name": "瑞士", "emoji": "⛰️", "desc": "雪山风光，滑雪胜地"},
        {"name": "京都", "emoji": "🏮", "desc": "古色古香，红叶季节"}
    ]
    
    # 选择目的地
    selected = st.selectbox("选择想去的地方", [d['name'] for d in destinations])
    dest = next(d for d in destinations if d['name'] == selected)
    
    st.markdown(f"## {dest['emoji']} {dest['name']}")
    st.write(dest['desc'])
    
    st.image(f"https://source.unsplash.com/random/600x300?{selected}", caption=selected, use_column_width=True)
    
    # 心愿清单列表
    st.markdown("---")
    wishlist = load_data(WISHLIST_FILE)
    
    if st.button(f"➕ 添加 {selected} 到心愿清单"):
        if not any(w['name'] == selected for w in wishlist):
            wishlist.append({"name": selected, "emoji": dest['emoji'], "added_at": time.strftime("%Y-%m-%d")})
            save_data(WISHLIST_FILE, wishlist)
            st.success("添加成功！")
            st.rerun()
        else:
            st.warning("已经在心愿清单中了")
    
    if wishlist:
        st.subheader("❤️ 我的心愿清单")
        for item in wishlist:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"{item['emoji']} {item['name']}")
            with col2:
                st.write(f"添加于：{item['added_at']}")
            with col3:
                if st.button(f"删除", key=f"del_{item['name']}"):
                    wishlist = [w for w in wishlist if w['name'] != item['name']]
                    save_data(WISHLIST_FILE, wishlist)
                    st.rerun()

# 主函数
def main():
    init_files()
    
    st.set_page_config(page_title="闺蜜小世界", page_icon="💖", layout="wide")
    
    # 检查登录状态
    if not check_login():
        if st.session_state.get('page', 'login') == 'register':
            register_page()
        else:
            login_page()
        return
    
    # 已登录状态
    st.sidebar.title(f"👋 欢迎, {st.session_state['username']}")
    
    menu = st.sidebar.radio("导航", ["首页", "故事回顾", "小游戏", "相互了解", "心愿清单"])
    
    if st.sidebar.button("退出登录"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.session_state['splash_shown'] = False
        st.rerun()
    
    if menu == "首页":
        home_page()
    elif menu == "故事回顾":
        story_page()
    elif menu == "小游戏":
        game_page()
    elif menu == "相互了解":
        qna_page()
    elif menu == "心愿清单":
        wishlist_page()

if __name__ == "__main__":
    main()
