import streamlit as st
import json
import os
import base64
import random

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

# 侧边栏菜单
def sidebar():
    with st.sidebar:
        st.title("💕 导航")
        menu = st.radio("选择页面", ["首页", "故事回顾", "小游戏", "真心话问答", "心愿清单", "个人画像"])
        return menu

# 首页
def home_page():
    st.title("💕 垚＆槑")
    st.markdown("### 欢迎来到我们的精神小世界")
    
    # 照片展示
    st.markdown("---")
    st.header("📷 时光照相机")
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
    
    # 关键词展示
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
    
    keywords_html = '<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; padding: 20px; background: linear-gradient(135deg, #fff5f5 0%, #fdf2f8 100%); border-radius: 16px;">'
    for kw in keywords:
        keywords_html += f'<span style="font-size: {kw["size"]}px; color: {kw["color"]}; font-weight: bold; padding: 8px 16px; border-radius: 20px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">{kw["text"]}</span>'
    keywords_html += '</div>'
    
    st.markdown(keywords_html, unsafe_allow_html=True)

# 故事回顾
def story_page():
    st.title("📖 故事回顾")
    st.markdown("### 相识相知的美好时光")
    
    story = """
    在一个阳光明媚的午后，李昕垚和陈昌梅在大学图书馆相遇了。
    
    那天，昕垚正在找一本很难找的书，不小心撞到了梅。书本散落一地，两人同时弯腰去捡，指尖不经意地触碰，那一刻，她们都红了脸。
    
    "对不起！" "没关系！" 两人异口同声地说。
    
    就这样，她们认识了。从图书馆的偶遇，到一起上课、一起吃饭、一起在操场散步，她们的友谊像春天的藤蔓一样，慢慢生长。
    
    昕垚喜欢安静地看书，梅喜欢热闹地讲笑话；昕垚做事认真细致，梅总是充满活力。她们性格互补，却又心意相通。
    
    一起哭过，一起笑过，一起经历了人生中最美好的青春年华。这份友谊，如同璀璨的星光，照亮彼此的人生道路。
    
    愿我们的友谊，天长地久，永远闪耀！
    """
    
    st.write(story)
    
    # 添加一些装饰性的分隔
    st.markdown("---")
    st.markdown("💖 **" + " ".join(["💕" for _ in range(20)]) + "**")

# 小游戏
def game_page():
    st.title("🎮 闺蜜小游戏")
    st.markdown("### 测试你们的默契程度")
    
    # 记忆翻牌游戏
    if 'cards' not in st.session_state:
        st.session_state.cards = []
        st.session_state.flipped = []
        st.session_state.matches = []
        st.session_state.moves = 0
    
    # 初始化游戏
    def init_game():
        emojis = ["💕", "💖", "🌸", "💝", "🎀", "💎", "✨", "🌟"] * 2
        random.shuffle(emojis)
        st.session_state.cards = emojis
        st.session_state.flipped = []
        st.session_state.matches = []
        st.session_state.moves = 0
    
    if st.button("🔄 开始新游戏"):
        init_game()
    
    # 显示游戏面板
    if st.session_state.cards:
        cols = st.columns(4)
        for i, emoji in enumerate(st.session_state.cards):
            col = cols[i % 4]
            is_flipped = i in st.session_state.flipped or i in st.session_state.matches
            
            if col.button(emoji if is_flipped else "❓", key=f"card_{i}", 
                         use_container_width=True, height=80):
                if i not in st.session_state.flipped and i not in st.session_state.matches:
                    st.session_state.flipped.append(i)
                    
                    if len(st.session_state.flipped) == 2:
                        st.session_state.moves += 1
                        idx1, idx2 = st.session_state.flipped
                        if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
                            st.session_state.matches.extend([idx1, idx2])
                        st.session_state.flipped = []
                        st.rerun()
        
        st.markdown(f"---\n**移动次数**: {st.session_state.moves}")
        
        if len(st.session_state.matches) == len(st.session_state.cards):
            st.success(f"🎉 恭喜！你用了 {st.session_state.moves} 步完成游戏！")
    
    else:
        init_game()
        st.rerun()

# 真心话问答
def qna_page():
    st.title("💬 真心话问答")
    st.markdown("### 加深彼此的了解")
    
    questions = [
        "你最喜欢对方的哪一点？",
        "你们第一次见面的场景还记得吗？",
        "如果只能用三个词形容对方，你会选什么？",
        "对方做过最让你感动的事是什么？",
        "你们之间有什么特别的小秘密吗？",
        "如果有机会一起旅行，你想去哪里？",
        "对方的缺点是什么？",
        "你们认识多久了？感觉时间过得快吗？",
        "如果对方遇到困难，你会怎么帮助她？",
        "你希望十年后你们的关系是什么样的？"
    ]
    
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    
    st.markdown(f"**问题 {st.session_state.current_q + 1}/{len(questions)}**")
    st.markdown(f"### {questions[st.session_state.current_q]}")
    
    # 答案输入
    answer = st.text_area("你的回答：", height=100)
    if st.button("💾 保存答案"):
        st.success("答案已保存！")
    
    # 导航按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.current_q > 0 and st.button("⬅️ 上一题"):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        if st.session_state.current_q < len(questions) - 1 and st.button("下一题 ➡️"):
            st.session_state.current_q += 1
            st.rerun()

# 心愿清单
def wishlist_page():
    st.title("✈️ 心愿清单")
    st.markdown("### 想和你一起去的地方")
    
    # 热门旅游目的地
    destinations = [
        {"name": "巴黎", "country": "法国", "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300"},
        {"name": "东京", "country": "日本", "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300"},
        {"name": "巴厘岛", "country": "印尼", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300"},
        {"name": "马尔代夫", "country": "马尔代夫", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300"},
        {"name": "悉尼", "country": "澳大利亚", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300"},
        {"name": "纽约", "country": "美国", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300"},
        {"name": "威尼斯", "country": "意大利", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300"},
        {"name": "普吉岛", "country": "泰国", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300"},
    ]
    
    # 心愿清单数据
    wishlist = load_data(WISHLIST_FILE)
    
    # 展示目的地网格
    st.subheader("🌍 选择想去的地方")
    cols = st.columns(4)
    for i, dest in enumerate(destinations):
        col = cols[i % 4]
        with col:
            st.image(dest["image"], caption=f"{dest['name']}, {dest['country']}", width=150)
            if st.button(f"➕ 添加到心愿单", key=f"add_{i}"):
                if dest["name"] not in [w["name"] for w in wishlist]:
                    wishlist.append(dest)
                    save_data(WISHLIST_FILE, wishlist)
                    st.success(f"已添加 {dest['name']}！")
                    st.rerun()
    
    # 显示心愿清单
    st.markdown("---")
    st.subheader("📋 我的心愿清单")
    if wishlist:
        for i, item in enumerate(wishlist):
            cols = st.columns([3, 1])
            with cols[0]:
                st.write(f"**{i+1}. {item['name']}, {item['country']}**")
            with cols[1]:
                if st.button("❌", key=f"remove_{i}"):
                    wishlist.pop(i)
                    save_data(WISHLIST_FILE, wishlist)
                    st.rerun()
    else:
        st.write("还没有添加任何心愿，快选择一个想去的地方吧！")

# 个人画像
def portrait_page():
    st.title("👩‍🦰 个人画像")
    st.markdown("### 了解我们")
    
    # 两个按钮
    col1, col2 = st.columns(2)
    with col1:
        yao_btn = st.button("👑 垚", use_container_width=True)
    with col2:
        mei_btn = st.button("🔥 梅", use_container_width=True)
    
    # 初始化状态
    if 'selected_portrait' not in st.session_state:
        st.session_state.selected_portrait = ''
    
    # 垚的画像
    if yao_btn:
        st.session_state.selected_portrait = 'yao'
    
    # 梅的画像
    if mei_btn:
        st.session_state.selected_portrait = 'mei'
    
    # 显示画像（气泡围绕美女形象四周）
    if st.session_state.selected_portrait == 'yao':
        st.markdown("""
        <div style="position: relative; padding: 40px; background: linear-gradient(135deg, #fce7f3 0%, #fdf2f8 100%); border-radius: 20px; margin-top: 20px;">
            <!-- 上方气泡 -->
            <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px;">
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 爱吃火锅</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 健身达人</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 羽毛球健将</span>
            </div>
            
            <!-- 左侧气泡 -->
            <div style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 15px;">
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 肌肉美女</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 舞担</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 喜欢漂亮的礼裙</span>
            </div>
            
            <!-- 中间美女形象 -->
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="width: 220px; height: 320px; background: linear-gradient(135deg, #ff6b9d, #ff8e53); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 100px; box-shadow: 0 10px 30px rgba(255, 107, 157, 0.3);">👗</div>
                <h3 style="color: #ec4899; margin-top: 20px;">气质美女 - 李昕垚</h3>
            </div>
            
            <!-- 右侧气泡 -->
            <div style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 15px;">
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 不喜欢吃鸡肉</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 不爱吃螺蛳粉</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 不爱喝牛奶</span>
            </div>
            
            <!-- 下方气泡 -->
            <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px;">
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 性格好惹但不准惹</span>
                <span style="background: white; color: #ec4899; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 喜欢照顾别人</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.selected_portrait == 'mei':
        st.markdown("""
        <div style="position: relative; padding: 40px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 20px; margin-top: 20px;">
            <!-- 上方气泡 -->
            <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px;">
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 有个性</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 喜欢酷酷的衣服</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 爱吃一切美食</span>
            </div>
            
            <!-- 左侧气泡 -->
            <div style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 15px;">
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 不爱喝纯牛奶</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 爱吃鸡公煲</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 羽毛球菜但爱打</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 想健身但不行动</span>
            </div>
            
            <!-- 中间美女形象 -->
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="width: 220px; height: 320px; background: linear-gradient(135deg, #f59e0b, #ef4444); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 100px; box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);">🔥</div>
                <h3 style="color: #f59e0b; margin-top: 20px;">活泼美女 - 陈昌梅</h3>
            </div>
            
            <!-- 右侧气泡 -->
            <div style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 15px;">
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 想跳舞但不行动</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 最近喜欢游泳</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 别惹我！</span>
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 粗糙</span>
            </div>
            
            <!-- 下方气泡 -->
            <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px;">
                <span style="background: white; color: #f59e0b; padding: 10px 20px; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">💬 自己都照顾不好</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 主程序
menu = sidebar()

if menu == "首页":
    home_page()
elif menu == "故事回顾":
    story_page()
elif menu == "小游戏":
    game_page()
elif menu == "真心话问答":
    qna_page()
elif menu == "心愿清单":
    wishlist_page()
elif menu == "个人画像":
    portrait_page()
