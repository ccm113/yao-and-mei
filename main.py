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
        menu = st.radio("选择页面", ["首页", "见信如面", "真心话问答", "个人画像"])
        return menu

# 首页
def home_page():
    st.title("💕 垚＆槑")
    st.markdown("### 欢迎来到我们的精神小世界")
    
    # 照片展示
    st.markdown("---")
    st.header("📷 分享一张故事照片")
    
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
                    st.image(photo["url"], width=150, use_column_width=True)
                    # 显示按钮
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"详情 {i+1}", key=f"detail_{i}"):
                            st.session_state.selected_photo = i
                            st.session_state.show_details = True
                    with col2:
                        if st.button(f"删除 {i+1}", key=f"delete_{i}"):
                            del photos[i]
                            save_data(PHOTOS_FILE, photos)
                            st.success("照片已删除！")
                            st.rerun()
        
        # 详情弹窗
        if st.session_state.show_details and st.session_state.selected_photo is not None:
            photo = photo_urls[st.session_state.selected_photo]
            st.markdown(f"### 📖 照片详情")
            st.image(photo["url"], width=300)
            st.markdown(f"**描述：** {photo['description']}")
            if st.button("关闭详情"):
                st.session_state.show_details = False
                st.session_state.selected_photo = None
                st.rerun()
    
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
            # 创建上传目录
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # 生成唯一文件名
            import uuid
            file_extension = uploaded_file.name.split('.')[-1]
            file_name = f"{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join(upload_dir, file_name)
            
            # 保存文件
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 获取描述
            description = st.text_input("请添加照片描述：", key="desc_input")
            
            # 添加到照片列表
            photos.append({
                "url": file_path,
                "caption": f"照片 {len(photos) + 1}",
                "description": description if description else "暂无描述"
            })
            save_data(PHOTOS_FILE, photos)
            
            # 更新 session_state 标记已处理
            st.session_state.uploaded_file_id = file_identifier
            
            st.success("图片上传成功！")
            st.rerun()
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
    
    # 使用简单的Markdown显示信件内容
    st.markdown("---")
    st.markdown("""
    **吾友昕垚，展信安康。**

    认识你六年有余，每每回想起我们一起穿着作训服训练的日子，眼眶总会发热。你在协会里一步步成长为优秀的学员、班长，最后成了所有人眼中的光。我也曾被这束光照亮过，但更多时候，我甘愿做你发光背后的阴影。我看不惯别人利用你、欺负你，于是主动去当那个“坏人”。而你却始终情绪稳定，凡事为他人着想，哪怕自己累到没时间顾及自己的需求。你如愿成了大家都喜欢的人。

    我曾觉得，以你的性格，走到哪里都能交到好朋友。所以我不清楚，毕业后我在你心里还能占多少分量。两年断断续续的联系，加上一直没见面，我几乎要放弃这份友情了。可毕业后第一次见面，我们立刻又回到了从前。即便如此，我还是希望能经常见面，解一解我这边的相思之苦。

    其实我也暗自跟你较过劲——因为你在协会里实在太优秀了。但最后我承认，自己在运动上的天赋确实不如你，于是便全心全意地欣赏你了。这样既有博弈又有爱的关系，反而让我们更加真实。

    今年终于可以一起过你的生日了。也很高兴看到你开始了新的感情——这世上多了一个人爱你，我替你感到幸福。

    生日快乐。
    永远快乐。
    永远一往无前，永远战斗，永远做自己。

    **你的挚友**
    **梅**
    """)
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
menu = sidebar()

if menu == "首页":
    home_page()
elif menu == "见信如面":
    story_page()
elif menu == "真心话问答":
    qna_page()
elif menu == "个人画像":
    portrait_page()
