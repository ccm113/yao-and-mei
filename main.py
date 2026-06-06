import streamlit as st
import json
import os
import base64
import random

# 数据文件路径
USERS_FILE = "users.json"
PHOTOS_FILE = "photos.json"
QNA_FILE = "qna.json"
PORTRAIT_FILE = "portrait.json"
SECRET_FILE = "secrets.json"

# 将本地图片转换为 Base64
@st.cache_data(ttl=3600)
def image_to_base64(img_path):
    try:
        from PIL import Image, ImageOps
        import io
        
        # 打开图片
        with Image.open(img_path) as img:
            # 修复EXIF方向问题
            img = ImageOps.exif_transpose(img)
            
            # 缩小图片尺寸（增大限制以提高清晰度）
            max_size = 600
            width, height = img.size
            if max(width, height) > max_size:
                ratio = max_size / max(width, height)
                img = img.resize((int(width * ratio), int(height * ratio)), Image.Resampling.LANCZOS)
            
            # 转换为JPEG格式并压缩（提高质量）
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=90)
            return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
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
    
    # 初始化真心话数据
    if not os.path.exists(QNA_FILE):
        default_qna = [
            {"question": "你最喜欢对方的哪一点？", "answers": []},
            {"question": "你们第一次见面的场景还记得吗？", "answers": []},
            {"question": "如果只能用三个词形容对方，你会选什么？", "answers": []},
            {"question": "对方做过最让你感动的事是什么？", "answers": []},
            {"question": "你们之间有什么特别的小秘密吗？", "answers": []},
            {"question": "如果有机会一起旅行，你想去哪里？", "answers": []},
            {"question": "对方的缺点是什么？", "answers": []},
            {"question": "你们认识多久了？感觉时间过得快吗？", "answers": []},
            {"question": "如果对方遇到困难，你会怎么帮助她？", "answers": []},
            {"question": "你希望十年后你们的关系是什么样的？", "answers": []},
            {"question": "对方最吸引你的地方是什么？", "answers": []},
            {"question": "你们之间发生过最有趣的事是什么？", "answers": []},
            {"question": "如果对方突然消失一天，你会怎么办？", "answers": []},
            {"question": "你觉得对方最大的优点是什么？", "answers": []},
            {"question": "你们有什么共同的梦想吗？", "answers": []},
            {"question": "对方做过让你生气的事吗？后来怎么解决的？", "answers": []},
            {"question": "如果用一首歌形容你们的友谊，你会选哪首？", "answers": []},
            {"question": "你最想和对方一起做但还没做的事是什么？", "answers": []},
            {"question": "对方说过最让你暖心的话是什么？", "answers": []},
            {"question": "如果可以交换一天人生，你愿意和对方交换吗？", "answers": []},
            {"question": "你觉得你们的友谊能维持一辈子吗？", "answers": []},
            {"question": "对方的什么习惯让你觉得很可爱？", "answers": []},
            {"question": "你们之间有没有吵过架？最后怎么和好的？", "answers": []},
            {"question": "如果对方谈恋爱了，你会有什么感觉？", "answers": []},
            {"question": "你最想从对方身上学到什么品质？", "answers": []}
        ]
        with open(QNA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_qna, f, ensure_ascii=False)
    
    # 初始化画像描述数据
    if not os.path.exists(PORTRAIT_FILE):
        default_portrait = {
            "yao": [
                "🍲 爱吃火锅",
                "💪 健身达人",
                "🏸 羽毛球健将",
                "💥 肌肉美女",
                "💃 舞担",
                "👗 喜欢漂亮的礼裙",
                "🐔 不喜欢吃鸡肉",
                "🍜 不爱吃螺蛳粉",
                "🥛 不爱喝牛奶",
                "😇 性格好惹但不准惹",
                "🤗 喜欢照顾别人"
            ],
            "mei": [
                "😎 有个性",
                "👖 喜欢酷酷的衣服",
                "🍕 爱吃一切美食",
                "🥛 不爱喝纯牛奶",
                "🍗 爱吃鸡公煲",
                "🏸 羽毛球菜但爱打",
                "💭 想健身但不行动",
                "💭 想跳舞但不行动",
                "🏊 最近喜欢游泳",
                "😠 别惹我！",
                "🪵 粗糙",
                "😅 自己都照顾不好"
            ]
        }
        with open(PORTRAIT_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_portrait, f, ensure_ascii=False)
    
    # 初始化悄悄话数据
    if not os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)

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

# 初始化用户ID
if 'user_id' not in st.session_state:
    import hashlib
    import time
    # 生成唯一用户ID
    user_id = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8]
    st.session_state.user_id = user_id

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
        menu = st.radio("选择页面", ["首页", "见信如面", "真心话问答", "个人画像", "悄悄话"])
        return menu

# 首页
def home_page():
    # 精美头部装饰
    st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 50%, #fbcfe8 100%);
        border-radius: 24px;
        padding: 60px 40px;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(236, 72, 153, 0.15);
        position: relative;
        overflow: hidden;
    }
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(251, 146, 60, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .header-container::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .title-text {
        font-size: 48px;
        font-weight: bold;
        color: #be185d;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 4px 20px rgba(236, 72, 153, 0.3);
    }
    .subtitle-text {
        font-size: 18px;
        color: #831843;
        text-align: center;
        opacity: 0.9;
    }
    .decoration {
        text-align: center;
        margin-top: 20px;
        font-size: 24px;
        letter-spacing: 10px;
    }
    .stats-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    .stats-number {
        font-size: 36px;
        font-weight: bold;
        color: #f472b6;
    }
    .stats-label {
        font-size: 14px;
        color: #9ca3af;
        margin-top: 5px;
    }
    .quote-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #fbbf24;
        border-radius: 0 16px 16px 0;
        padding: 24px 30px;
        margin: 30px 0;
    }
    .quote-text {
        font-size: 18px;
        color: #92400e;
        font-style: italic;
        line-height: 1.8;
    }
    .quote-author {
        text-align: right;
        color: #b45309;
        font-weight: bold;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 精美头部
    st.markdown("""
    <div class="header-container">
        <div class="title-text">💕 垚 & 槑</div>
        <div class="subtitle-text">欢迎来到我们的精神小世界</div>
        <div class="decoration">✨ ✨ ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">6+</div>
            <div class="stats-label">年闺蜜情</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">∞</div>
            <div class="stats-label">美好回忆</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">💕</div>
            <div class="stats-label">真心相伴</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">💫</div>
            <div class="stats-label">未来可期</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 引言语录（自动切换）
    friendship_quotes = [
        {"text": "真正的友谊不是花言巧语，而是在最困难的时候，朋友依然在你身边，默默支持你。", "author": "垚 & 槑"},
        {"text": "闺蜜是世界上另一个自己，懂你的喜怒哀乐，陪你走过春夏秋冬。", "author": "垚 & 槑"},
        {"text": "好朋友就像星星，不一定经常见到，但你知道他们一直在那里。", "author": "垚 & 槑"},
        {"text": "友谊是人生路上最美的风景，有你同行，旅途不再孤单。", "author": "垚 & 槑"},
        {"text": "真正的朋友会在你需要的时候出现，不需要华丽的言语，只需要一个拥抱。", "author": "垚 & 槑"},
        {"text": "闺蜜之间的默契，一个眼神就能明白彼此的心意。", "author": "垚 & 槑"},
        {"text": "友谊不是一幕短暂的烟火，而是一幅真心的画卷。", "author": "垚 & 槑"},
        {"text": "最好的朋友是那种不喜欢多说，却能与你默默相对而又息息相通的人。", "author": "垚 & 槑"},
        {"text": "闺蜜就是，当你想哭诉的时候，她会把肩膀借给你靠，当你想疯狂的时候，她会陪你一起疯。", "author": "垚 & 槑"},
        {"text": "真正的友谊，是一株成长缓慢的植物，需要用心呵护才能茁壮成长。", "author": "垚 & 槑"},
        {"text": "朋友是生命中最珍贵的礼物，让我们的人生更加丰富多彩。", "author": "垚 & 槑"},
        {"text": "闺蜜之间，没有秘密，没有距离，只有无尽的理解和支持。", "author": "垚 & 槑"},
        {"text": "友谊的真谛在于理解和宽容，在于真诚和信任。", "author": "垚 & 槑"},
        {"text": "最好的友情，是你不说，她却都懂。", "author": "垚 & 槑"},
        {"text": "朋友是冬日里的暖阳，夏日里的清风，永远温暖着我们的心灵。", "author": "垚 & 槑"},
        {"text": "闺蜜是那个陪你笑、陪你哭、陪你一起犯傻的人。", "author": "垚 & 槑"},
        {"text": "真正的友谊经得起时间的考验，经得起距离的考验。", "author": "垚 & 槑"},
        {"text": "友谊就像一杯清茶，越品越香，越陈越浓。", "author": "垚 & 槑"},
        {"text": "好朋友是一面镜子，让你看到最好的自己。", "author": "垚 & 槑"},
        {"text": "闺蜜之间的感情，比爱情更坚固，比亲情更贴心。", "author": "垚 & 槑"},
        {"text": "友谊是一朵盛开的花，需要用真心去浇灌，才能绽放出最美的光彩。", "author": "垚 & 槑"},
        {"text": "真正的朋友会在你成功时为你高兴，在你失败时给你鼓励。", "author": "垚 & 槑"},
        {"text": "闺蜜是那个知道你所有缺点却依然爱你的人。", "author": "垚 & 槑"},
        {"text": "友谊不是等来的，而是用心经营出来的。", "author": "垚 & 槑"},
        {"text": "最好的友情，是各自忙碌，又互相牵挂。", "author": "垚 & 槑"},
        {"text": "朋友是人生路上的灯塔，照亮我们前行的道路。", "author": "垚 & 槑"},
        {"text": "闺蜜之间的约定，是一辈子的承诺。", "author": "垚 & 槑"},
        {"text": "真正的友谊，是在你最需要的时候伸出援手，而不是锦上添花。", "author": "垚 & 槑"},
        {"text": "友谊是一首动听的歌，旋律优美，让人回味无穷。", "author": "垚 & 槑"},
        {"text": "好朋友就像一本好书，每次阅读都有新的收获。", "author": "垚 & 槑"},
        {"text": "闺蜜是那个陪你从校服到婚纱的人，见证你人生的每一个重要时刻。", "author": "垚 & 槑"},
        {"text": "真正的友谊，是不计较得失，只在乎彼此的感受。", "author": "垚 & 槑"},
        {"text": "友谊是人生最宝贵的财富，千金难买，万金不换。", "author": "垚 & 槑"},
        {"text": "闺蜜之间的默契，是不需要言语的心灵相通。", "author": "垚 & 槑"},
        {"text": "真正的朋友，是无论多久没见，见面依然如故。", "author": "垚 & 槑"},
        {"text": "友谊就像一颗种子，需要用心培育，才能长成参天大树。", "author": "垚 & 槑"}
    ]
    
    # 初始化当前句子索引
    if 'current_quote_index' not in st.session_state:
        st.session_state.current_quote_index = 0
    
    # 获取当前句子
    current_quote = friendship_quotes[st.session_state.current_quote_index]
    
    st.markdown("""
    <style>
    .quote-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #fbbf24;
        border-radius: 0 16px 16px 0;
        padding: 24px 30px;
        margin: 30px 0;
        position: relative;
        overflow: hidden;
    }
    .quote-box::before {
        content: '💬';
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 80px;
        opacity: 0.1;
    }
    .quote-text {
        font-size: 18px;
        color: #92400e;
        font-style: italic;
        line-height: 1.8;
        transition: opacity 0.5s ease;
    }
    .quote-author {
        text-align: right;
        color: #b45309;
        font-weight: bold;
        margin-top: 15px;
    }
    .quote-counter {
        text-align: center;
        color: #d97706;
        font-size: 14px;
        margin-top: 10px;
        opacity: 0.7;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="quote-box">
        <div class="quote-text">"{current_quote['text']}"</div>
        <div class="quote-author">—— {current_quote['author']}</div>
        <div class="quote-counter">第 {st.session_state.current_quote_index + 1} / {len(friendship_quotes)} 句</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 添加手动切换按钮
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("◀️ 上一句"):
            st.session_state.current_quote_index = (st.session_state.current_quote_index - 1) % len(friendship_quotes)
            st.rerun()
    with col2:
        if st.button("下一句 ▶️"):
            st.session_state.current_quote_index = (st.session_state.current_quote_index + 1) % len(friendship_quotes)
            st.rerun()
    
    # 添加自动切换的JavaScript
    st.markdown("""
    <script>
    // 每隔10分钟（600000毫秒）自动刷新页面，实现句子切换
    setTimeout(function() {
        window.location.reload();
    }, 600000); // 10分钟 = 600000毫秒
    </script>
    """, unsafe_allow_html=True)
    
    # 照片展示
    st.markdown("---")
    st.markdown("""
    <style>
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #be185d;
        text-align: center;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    .section-title::before,
    .section-title::after {
        content: '';
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #f472b6);
    }
    .section-title::after {
        background: linear-gradient(90deg, #f472b6, transparent);
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-title">📷 分享一张故事照片</div>', unsafe_allow_html=True)
    
    # 加载照片数据
    photos = load_data(PHOTOS_FILE)
    
    # 状态管理
    if 'selected_photo' not in st.session_state:
        st.session_state.selected_photo = None
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False
    
    # 使用加载状态
    with st.spinner("正在加载照片..."):
        # 预加载所有图片
        photo_urls = []
        for photo in photos:
            url = photo["url"]
            if os.path.exists(url):
                base64_str = image_to_base64(url)
                if base64_str:
                    url = f"data:image/jpeg;base64,{base64_str}"
            photo_urls.append({"url": url, "caption": photo.get("caption", ""), "description": photo.get("description", "")})
        
        # 使用 Streamlit 原生组件展示照片网格（不带标题）
        if photos:
            num_cols = min(4, len(photos))
            cols = st.columns(num_cols)
            
            for i, photo in enumerate(photo_urls):
                col = cols[i % num_cols]
                with col:
                    # 检查是否选中了当前照片
                    is_selected = st.session_state.selected_photo == i
                    
                    # 显示图片（使用CSS hover实现悬停按钮效果）
                    st.markdown(f"""
                    <style>
                    .photo-container {{
                        position: relative;
                        display: inline-block;
                        width: 100%;
                    }}
                    .photo-container img {{
                        width: 100%;
                        border-radius: 8px;
                        cursor: pointer;
                    }}
                    .photo-container .photo-overlay {{
                        position: absolute;
                        bottom: 10px;
                        left: 50%;
                        transform: translateX(-50%);
                        display: none;
                        gap: 10px;
                    }}
                    .photo-container:hover .photo-overlay,
                    .photo-container.selected .photo-overlay {{
                        display: flex;
                    }}
                    .photo-btn {{
                        padding: 6px 16px;
                        border: none;
                        border-radius: 15px;
                        cursor: pointer;
                        font-weight: bold;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                        transition: transform 0.2s;
                    }}
                    .photo-btn:hover {{
                        transform: scale(1.05);
                    }}
                    .btn-detail {{
                        background: rgba(255,255,255,0.95);
                        color: #be185d;
                    }}
                    .btn-delete {{
                        background: rgba(239,68,68,0.95);
                        color: white;
                    }}
                    </style>
                    <div class="photo-container {'selected' if is_selected else ''}">
                        <img src="{photo['url']}" />
                        <div class="photo-overlay">
                            <button class="photo-btn btn-detail" onclick="document.getElementById('btn-detail-{i}').click()">详情</button>
                            <button class="photo-btn btn-delete" onclick="document.getElementById('btn-delete-{i}').click()">删除</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 隐藏的详情按钮（使用空按钮）
                    detail_clicked = st.button(" ", key=f"btn-detail-{i}", help="详情")
                    if detail_clicked:
                        st.session_state.selected_photo = i if st.session_state.selected_photo != i else None
                        st.rerun()
                    
                    # 隐藏的删除按钮（使用空按钮）
                    delete_clicked = st.button("  ", key=f"btn-delete-{i}", help="删除")
                    if delete_clicked:
                        del photos[i]
                        save_data(PHOTOS_FILE, photos)
                        st.session_state.selected_photo = None
                        st.success("照片已删除！")
                        st.rerun()
            
            # 详情弹窗
            if st.session_state.selected_photo is not None:
                photo = photo_urls[st.session_state.selected_photo]
                st.markdown(f"### 📖 照片详情")
                st.image(photo["url"], width=300)
                st.markdown(f"**描述：** {photo['description']}")
    
    # 本地图片上传功能
    st.markdown("---")
    uploaded_file = st.file_uploader("🖼️ 添加图片", type=["jpg", "jpeg", "png", "gif"])
    
    if uploaded_file is not None:
        # 使用 session_state 防止重复上传
        if 'uploaded_file_id' not in st.session_state:
            st.session_state.uploaded_file_id = None
        
        # 生成文件唯一标识（基于文件名和文件大小）
        file_identifier = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # 检查是否已经处理过这个文件
        if st.session_state.uploaded_file_id != file_identifier:
            # 将图片转换为 Base64 编码
            import base64
            import io
            from PIL import Image, ImageOps
            
            try:
                # 读取图片
                img = Image.open(uploaded_file)
                # 修复EXIF方向问题
                img = ImageOps.exif_transpose(img)
                
                # 缩小图片尺寸（提高加载速度）
                max_size = 800
                width, height = img.size
                if max(width, height) > max_size:
                    ratio = max_size / max(width, height)
                    img = img.resize((int(width * ratio), int(height * ratio)), Image.Resampling.LANCZOS)
                
                # 转换为JPEG格式并压缩
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                base64_str = base64.b64encode(buffer.getvalue()).decode()
                
                # 生成 Base64 URL
                base64_url = f"data:image/jpeg;base64,{base64_str}"
                
                # 获取描述
                description = st.text_input("请添加照片描述：", key="desc_input")
                
                # 添加到照片列表（使用 Base64 编码直接存储）
                photos.append({
                    "url": base64_url,
                    "caption": f"照片 {len(photos) + 1}",
                    "description": description if description else "暂无描述"
                })
                save_data(PHOTOS_FILE, photos)
                
                # 更新 session_state 标记已处理
                st.session_state.uploaded_file_id = file_identifier
                
                st.success("图片上传成功！")
                st.rerun()
            except Exception as e:
                st.error(f"图片处理失败：{str(e)}")
        else:
            # 显示描述输入（如果是重复上传但还没填描述）
            if 'desc_input' not in st.session_state:
                description = st.text_input("请添加照片描述：", key="desc_input")
                if st.button("保存描述"):
                    photos[-1]["description"] = description if description else "暂无描述"
                    save_data(PHOTOS_FILE, photos)
                    st.success("描述已保存！")
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

# 见信如面
def story_page():
    st.title("💌 见信如面")
    
    # 使用HTML实现首行缩进和右对齐
    st.markdown("---")
    st.markdown("""
    <style>
    .letter-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 40px;
        background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(236, 72, 153, 0.1);
    }
    .letter-title {
        text-align: center;
        color: #be185d;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .letter-paragraph {
        font-size: 16px;
        line-height: 2;
        color: #4c1d4e;
        text-indent: 2em;
        margin-bottom: 20px;
    }
    .letter-closing {
        font-size: 16px;
        line-height: 2;
        color: #4c1d4e;
        text-indent: 2em;
        margin-bottom: 30px;
    }
    .letter-sender {
        text-align: right;
        color: #7c2d7c;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .letter-signature {
        text-align: right;
        color: #7c2d7c;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="letter-container">
        <div class="letter-title">📜 吾友昕垚，展信好。</div>
        
        <div class="letter-paragraph">
            认识你至今，已过六年有余。每当想起我们一起穿着作训服训练的日子，心里仍旧温热，像冬日里捂着一杯热茶。那时你从一名普通学员，渐渐成长为优秀的班长，最后成了协会里许多人抬头就能看见的光。我也曾被这光照亮，但更多时候，我甘愿站在你身后，做那光下的阴影——因为看不得别人利用你的善良、欺负你的隐忍，便总抢着去当那个“坏人”。而你始终情绪稳定，事事为人着想，哪怕自己累得顾不上喘一口气。
        </div>
        
        <div class="letter-paragraph">
            我知道，以你的性情，走到哪里都能结交知心的朋友。所以从不担心你会过不好。可人生无常，恰是寻常。并不是你足够好，身边就全是好人——总有蛇鼠之辈，总有愤懑之事，把你的日子填得满满当当。可也正是这些，让你一点点变得更结实。
        </div>
        
        <div class="letter-paragraph">
            那两年，我们断断续续地联系，许久未见。你我相隔江河千里，但心中念着你，便不觉遥远。我去外地求学之前，你专程奔波百里来送我。当时并未觉得什么，到了异乡才慢慢明白——哪儿都不如家乡好。于是那份送别的情意，便一天天在心里变得厚重。
        </div>
        
        <div class="letter-paragraph">
            后来你辞了工作，来到我所在的城市。虽然每日不知你在忙些什么，但总算能连续几日与你朝夕相处。只是一想到你总提着大包小包东奔西跑，什么事都自己扛，生怕麻烦别人，便又心疼又怨你——怨你为什么不信，我可以替你托底。或许是你的家教使你事事尽心，乐善好施；也或许是我真的还不够强大，不足以为你依靠。但我仍旧贪心，盼你能多依赖我一些。
        </div>
        
        <div class="letter-paragraph">
            今年见到你带了男朋友来，我是真心高兴。你们站在一起，身高长相般配，言谈举止间也势均力敌。我想，这下好了，终于有人可以照顾你了。你不需要总做那个照顾别人的人，让他好好照顾你吧。放心大胆去爱，无论如何，你还有我。当然，也别见色忘友，要时常抽空来见我。
        </div>
        
        <div class="letter-paragraph">
            今年终于能一起过你的生日了。
        </div>
        
        <div class="letter-closing">
            生日快乐。<br>
            永远快乐。<br>
            永远一往无前，永远能战，永远做你自己。
        </div>
        
        <div class="letter-sender">你的挚友</div>
        <div class="letter-signature">梅</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("💖 " + "💕" * 20 + " 💖")

# 真心话问答
def qna_page():
    st.title("💬 真心话问答")
    st.markdown("### 加深彼此的了解")
    
    # 加载真心话数据
    qna_data = load_data(QNA_FILE)
    
    # 状态管理
    if 'qna_view_mode' not in st.session_state:
        st.session_state.qna_view_mode = 'quiz'  # 'quiz' 或 'view_all'
    
    # 切换按钮
    if st.session_state.qna_view_mode == 'quiz':
        if st.button("📋 查看所有真心话"):
            st.session_state.qna_view_mode = 'view_all'
            st.rerun()
    else:
        if st.button("🔙 返回答题"):
            st.session_state.qna_view_mode = 'quiz'
            st.rerun()
    
    # 答题模式
    if st.session_state.qna_view_mode == 'quiz':
        # 随机选择一个题目（每次进入可能不同）
        if 'random_q_index' not in st.session_state:
            st.session_state.random_q_index = random.randint(0, len(qna_data) - 1)
        
        current_q = qna_data[st.session_state.random_q_index]
        
        st.markdown(f"### 🎯 {current_q['question']}")
        
        # 答案输入
        answer = st.text_area("你的回答：", height=100)
        username = st.session_state.get('username', '匿名用户')
        
        if st.button("💾 保存答案"):
            if answer.strip():
                # 添加答案到数据
                qna_data[st.session_state.random_q_index]['answers'].append({
                    "user": username,
                    "user_id": st.session_state.get('user_id', '未知ID'),
                    "answer": answer.strip(),
                    "timestamp": st.session_state.get('login_time', '未知时间')
                })
                save_data(QNA_FILE, qna_data)
                st.success("答案已保存！")
                # 随机下一题
                st.session_state.random_q_index = random.randint(0, len(qna_data) - 1)
                st.rerun()
            else:
                st.warning("请先输入回答内容")
        
        # 换一题按钮
        if st.button("🔄 换一题"):
            st.session_state.random_q_index = random.randint(0, len(qna_data) - 1)
            st.rerun()
    
    # 查看所有真心话模式
    else:
        st.subheader("📚 所有真心话题目和答案")
        
        for i, item in enumerate(qna_data, 1):
            with st.expander(f"问题 {i}：{item['question']}"):
                if item['answers']:
                    for j, ans in enumerate(item['answers'], 1):
                        st.markdown(f"**{j}. {ans['user']}** (ID: {ans.get('user_id', '未知ID')})")
                        st.markdown(f"> {ans['answer']}")
                        st.markdown(f"*回答时间：{ans.get('timestamp', '未知')}*")
                        st.markdown("---")
                else:
                    st.markdown("暂无回答")

# 个人画像
def portrait_page():
    st.title("👩‍🦰 个人画像")
    st.markdown("### 了解我们")
    
    # 加载画像数据
    portrait_data = load_data(PORTRAIT_FILE)
    
    # 两个按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👸 垚", use_container_width=True):
            st.session_state.selected_portrait = 'yao'
    with col2:
        if st.button("🤸 梅", use_container_width=True):
            st.session_state.selected_portrait = 'mei'
    
    # 垚的画像
    if st.session_state.get('selected_portrait') == 'yao':
        st.subheader("👸 气质美女 - 李昕垚")
        
        # 生成气泡HTML
        bubbles_html = ""
        for desc in portrait_data.get('yao', []):
            bubbles_html += f'<span style="background: white; color: #be185d; padding: 10px 20px; border-radius: 20px; font-weight: bold; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">{desc}</span>'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%); border-radius: 16px; padding: 30px; margin-top: 10px;">
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #f472b6, #fb7185); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 70px; box-shadow: 0 8px 25px rgba(244, 114, 182, 0.3); border: 4px solid white;">👸</div>
            </div>
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 12px;">
                {bubbles_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 添加描述按钮
        st.markdown("---")
        new_desc = st.text_input("添加新描述：", placeholder="输入对垚的描述...")
        if st.button("➕ 增加描述"):
            if new_desc.strip():
                # 添加表情前缀
                emojis = ["💕", "💖", "✨", "🌟", "💝", "🎀", "💎", "🌸"]
                emoji = random.choice(emojis)
                new_desc_with_emoji = f"{emoji} {new_desc.strip()}"
                
                portrait_data['yao'].append(new_desc_with_emoji)
                save_data(PORTRAIT_FILE, portrait_data)
                st.success("描述已添加！")
                st.rerun()
    
    # 梅的画像
    elif st.session_state.get('selected_portrait') == 'mei':
        st.subheader("� 活泼美女 - 陈昌梅")
        
        # 生成气泡HTML
        bubbles_html = ""
        for desc in portrait_data.get('mei', []):
            bubbles_html += f'<span style="background: white; color: #d97706; padding: 10px 20px; border-radius: 20px; font-weight: bold; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">{desc}</span>'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%); border-radius: 16px; padding: 30px; margin-top: 10px;">
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #fbbf24, #f97316); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 70px; box-shadow: 0 8px 25px rgba(251, 191, 36, 0.3); border: 4px solid white;">🤸</div>
            </div>
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 12px;">
                {bubbles_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 添加描述按钮
        st.markdown("---")
        new_desc = st.text_input("添加新描述：", placeholder="输入对梅的描述...")
        if st.button("➕ 增加描述"):
            if new_desc.strip():
                # 添加表情前缀
                emojis = ["💕", "💖", "✨", "🌟", "💝", "🎀", "💎", "�"]
                emoji = random.choice(emojis)
                new_desc_with_emoji = f"{emoji} {new_desc.strip()}"
                
                portrait_data['mei'].append(new_desc_with_emoji)
                save_data(PORTRAIT_FILE, portrait_data)
                st.success("描述已添加！")
                st.rerun()

# 主程序
# 悄悄话
def secret_page():
    st.title("💌 悄悄话")
    
    # 导览文字
    st.markdown("""
    **我想让你知道但不好直说的事情，悄悄留了个言，看你什么时候发现。**
    """)
    
    # 状态管理
    if 'secret_view_mode' not in st.session_state:
        st.session_state.secret_view_mode = 'write'  # 'write' 或 'view_all'
    if 'editing_index' not in st.session_state:
        st.session_state.editing_index = None
    
    # 写悄悄话模式
    if st.session_state.secret_view_mode == 'write':
        # 输入框
        secret_text = st.text_area("写下你的悄悄话：", height=100, placeholder="想说但不好意思当面说的话...")
        
        # 发送按钮
        if st.button("✉️ 发送悄悄话"):
            if secret_text.strip():
                secrets = load_data(SECRET_FILE)
                secrets.append({
                    "id": len(secrets) + 1,
                    "content": secret_text.strip(),
                    "user": st.session_state.get('username', '匿名用户'),
                    "user_id": st.session_state.get('user_id', '未知ID'),
                    "timestamp": st.session_state.get('login_time', '未知时间')
                })
                save_data(SECRET_FILE, secrets)
                st.success("悄悄话已发送！")
        
        # 查看所有悄悄话按钮
        if st.button("📋 查看所有悄悄话"):
            st.session_state.secret_view_mode = 'view_all'
            st.rerun()
    
    # 查看所有悄悄话模式
    else:
        st.subheader("📚 所有悄悄话")
        
        secrets = load_data(SECRET_FILE)
        
        if secrets:
            for i, secret in enumerate(secrets):
                with st.expander(f"悄悄话 {secret['id']} · {secret['user']}"):
                    # 编辑模式
                    if st.session_state.editing_index == i:
                        new_content = st.text_area("修改内容：", value=secret['content'], height=100)
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✅ 保存修改 {i}", key=f"save_{i}"):
                                secrets[i]['content'] = new_content.strip()
                                save_data(SECRET_FILE, secrets)
                                st.session_state.editing_index = None
                                st.success("修改已保存！")
                                st.rerun()
                        with col2:
                            if st.button(f"❌ 取消 {i}", key=f"cancel_{i}"):
                                st.session_state.editing_index = None
                                st.rerun()
                    else:
                        st.markdown(f"> {secret['content']}")
                        st.markdown(f"*发送者：{secret['user']} (ID: {secret.get('user_id', '未知ID')}) · {secret.get('timestamp', '未知时间')}*")
                        
                        # 显示回复列表
                        replies = secret.get('replies', [])
                        if replies:
                            st.markdown("---")
                            st.markdown("**回复：**")
                            for j, reply in enumerate(replies):
                                st.markdown(f"🔹 **{reply['user']}** (ID: {reply.get('user_id', '未知ID')})")
                                st.markdown(f"> {reply['content']}")
                                st.markdown(f"*回复时间：{reply.get('timestamp', '未知时间')}*")
                                if st.button(f"🗑️ 删除回复 {j}", key=f"delete_reply_{i}_{j}"):
                                    del secrets[i]['replies'][j]
                                    save_data(SECRET_FILE, secrets)
                                    st.success("回复已删除！")
                                    st.rerun()
                        
                        # 回复输入框
                        st.markdown("---")
                        reply_text = st.text_input(f"回复悄悄话 {secret['id']}：", key=f"reply_input_{i}")
                        if st.button(f"💬 发送回复", key=f"send_reply_{i}"):
                            if reply_text.strip():
                                if 'replies' not in secrets[i]:
                                    secrets[i]['replies'] = []
                                secrets[i]['replies'].append({
                                    "user": st.session_state.get('username', '匿名用户'),
                                    "user_id": st.session_state.get('user_id', '未知ID'),
                                    "content": reply_text.strip(),
                                    "timestamp": st.session_state.get('login_time', '未知时间')
                                })
                                save_data(SECRET_FILE, secrets)
                                st.success("回复已发送！")
                                st.rerun()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✏️ 修改 {i}", key=f"edit_{i}"):
                                st.session_state.editing_index = i
                                st.rerun()
                        with col2:
                            if st.button(f"🗑️ 删除 {i}", key=f"delete_secret_{i}"):
                                del secrets[i]
                                save_data(SECRET_FILE, secrets)
                                st.success("悄悄话已删除！")
                                st.rerun()
        else:
            st.markdown("暂无悄悄话")
        
        # 返回按钮
        if st.button("🔙 返回写悄悄话"):
            st.session_state.secret_view_mode = 'write'
            st.session_state.editing_index = None
            st.rerun()


menu = sidebar()

if menu == "首页":
    home_page()
elif menu == "见信如面":
    story_page()
elif menu == "真心话问答":
    qna_page()
elif menu == "个人画像":
    portrait_page()
elif menu == "悄悄话":
    secret_page()
