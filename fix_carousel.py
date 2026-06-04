import re

# 读取文件
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到照片墙部分的开始和结束位置
start_marker = "# 照片展示"
end_marker = "# 处理照片操作"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # 新的照片墙代码
    new_photo_section = """    # 照片展示
    st.markdown("---")
    st.header("📷 感谢相机")
    photos = load_data(PHOTOS_FILE)
    
    # 使用简单的网格布局
    if photos:
        cols = st.columns(4)
        for i, photo in enumerate(photos):
            with cols[i % 4]:
                st.image(photo['url'], use_column_width=True)
    
    # 添加照片按钮
    if st.button("➕ 添加新照片"):
        photos.append({
            "url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200",
            "caption": "新照片"
        })
        save_data(PHOTOS_FILE, photos)
        st.rerun()

"""
    
    # 替换旧代码
    new_content = content[:start_idx] + new_photo_section + content[end_idx:]
    
    # 写入文件
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("修复成功！")
else:
    print("未找到标记位置")
