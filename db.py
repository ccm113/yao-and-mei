import os
from supabase import create_client, Client

# 从环境变量获取配置
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# 初始化 Supabase 客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# ========== 照片操作 ==========
def get_photos():
    if not supabase:
        return []
    try:
        response = supabase.table('photos').select('*').order('id', desc=False).execute()
        return response.data if response.data else []
    except:
        return []

def add_photo(url, caption, description):
    if not supabase:
        return False
    try:
        supabase.table('photos').insert({
            'url': url,
            'caption': caption,
            'description': description
        }).execute()
        return True
    except:
        return False

def delete_photo(photo_id):
    if not supabase:
        return False
    try:
        supabase.table('photos').delete().eq('id', photo_id).execute()
        return True
    except:
        return False

# ========== 悄悄话操作 ==========
def get_secrets():
    if not supabase:
        return []
    try:
        response = supabase.table('secrets').select('*').order('id', desc=True).execute()
        return response.data if response.data else []
    except:
        return []

def add_secret(content, user_name, user_id, timestamp):
    if not supabase:
        return False
    try:
        supabase.table('secrets').insert({
            'content': content,
            'user_name': user_name,
            'user_id': user_id,
            'timestamp': timestamp
        }).execute()
        return True
    except:
        return False

# ========== 个人画像操作 ==========
def get_portrait(person):
    if not supabase:
        return []
    try:
        response = supabase.table('portrait').select('description').eq('person', person).execute()
        return [item['description'] for item in response.data] if response.data else []
    except:
        return []

def add_portrait(person, description):
    if not supabase:
        return False
    try:
        supabase.table('portrait').insert({
            'person': person,
            'description': description
        }).execute()
        return True
    except:
        return False

# ========== 真心话操作 ==========
def get_qna():
    if not supabase:
        return []
    try:
        response = supabase.table('qna').select('*').order('id', desc=False).execute()
        return response.data if response.data else []
    except:
        return []

def update_qna(qna_id, answers):
    if not supabase:
        return False
    try:
        supabase.table('qna').update({'answers': answers}).eq('id', qna_id).execute()
        return True
    except:
        return False

def add_qna(question):
    if not supabase:
        return False
    try:
        supabase.table('qna').insert({
            'question': question,
            'answers': []
        }).execute()
        return True
    except:
        return False

# 检查数据库是否连接成功
def is_db_connected():
    return supabase is not None