import os
from supabase import create_client, Client
import traceback

# 从环境变量获取配置
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# 初始化 Supabase 客户端
supabase: Client = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Failed to initialize Supabase: {e}")

# 全局错误信息
last_error = None

# ========== 照片操作 ==========
def get_photos():
    global last_error
    if not supabase:
        return []
    try:
        response = supabase.table('photos').select('*').order('id', desc=False).execute()
        last_error = None
        return response.data if response.data else []
    except Exception as e:
        last_error = f"获取照片失败: {str(e)}"
        print(last_error)
        return []

def add_photo(url, caption, description):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('photos').insert({
            'url': url,
            'caption': caption,
            'description': description
        }).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"添加照片失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

def delete_photo(photo_id):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('photos').delete().eq('id', photo_id).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"删除照片失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

# ========== 悄悄话操作 ==========
def get_secrets():
    global last_error
    if not supabase:
        return []
    try:
        response = supabase.table('secrets').select('*').order('id', desc=True).execute()
        last_error = None
        return response.data if response.data else []
    except Exception as e:
        last_error = f"获取悄悄话失败: {str(e)}"
        print(last_error)
        return []

def add_secret(content, user_name, user_id, timestamp):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('secrets').insert({
            'content': content,
            'user_name': user_name,
            'user_id': user_id,
            'timestamp': timestamp
        }).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"添加悄悄话失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

def update_secret(secret_id, content):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('secrets').update({'content': content}).eq('id', secret_id).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"更新悄悄话失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

def delete_secret(secret_id):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('secrets').delete().eq('id', secret_id).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"删除悄悄话失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

# ========== 个人画像操作 ==========
def get_portrait(person):
    global last_error
    if not supabase:
        return []
    try:
        response = supabase.table('portrait').select('description').eq('person', person).execute()
        last_error = None
        return [item['description'] for item in response.data] if response.data else []
    except Exception as e:
        last_error = f"获取画像失败: {str(e)}"
        print(last_error)
        return []

def add_portrait(person, description):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('portrait').insert({
            'person': person,
            'description': description
        }).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"添加画像描述失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

# ========== 真心话操作 ==========
def get_qna():
    global last_error
    if not supabase:
        return []
    try:
        response = supabase.table('qna').select('*').order('id', desc=False).execute()
        last_error = None
        return response.data if response.data else []
    except Exception as e:
        last_error = f"获取真心话失败: {str(e)}"
        print(last_error)
        return []

def update_qna(qna_id, answers):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('qna').update({'answers': answers}).eq('id', qna_id).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"更新真心话失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

def add_qna(question):
    global last_error
    if not supabase:
        return False, "数据库未连接"
    try:
        response = supabase.table('qna').insert({
            'question': question,
            'answers': []
        }).execute()
        last_error = None
        return True, "成功"
    except Exception as e:
        error_msg = f"添加真心话失败: {str(e)}"
        last_error = error_msg
        print(error_msg)
        return False, error_msg

# 检查数据库是否连接成功
def is_db_connected():
    return supabase is not None

# 获取最后错误信息
def get_last_error():
    return last_error