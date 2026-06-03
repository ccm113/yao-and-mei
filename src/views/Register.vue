<template>
  <div class="register-container">
    <div class="register-box">
      <h1 class="title">💝 加入我们</h1>
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label>用户名</label>
          <input v-model="username" type="text" placeholder="请输入用户名" />
        </div>
        <div class="input-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" />
        </div>
        <div class="input-group">
          <label>确认密码</label>
          <input v-model="confirmPassword" type="password" placeholder="请再次输入密码" />
        </div>
        <button type="submit" class="register-btn">注册</button>
      </form>
      <p class="login-link">
        已有账号？<a href="/login">立即登录</a>
      </p>
    </div>
    <div class="hearts-bg">
      <div v-for="i in 20" :key="i" class="heart" :style="getHeartStyle(i)"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const getHeartStyle = (_index: number) => {
  const left = Math.random() * 100
  const animationDelay = Math.random() * 5
  const animationDuration = 3 + Math.random() * 4
  return {
    left: `${left}%`,
    animationDelay: `${animationDelay}s`,
    animationDuration: `${animationDuration}s`
  }
}

const handleRegister = () => {
  if (!username.value || !password.value || !confirmPassword.value) {
    alert('请填写完整信息')
    return
  }
  
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致')
    return
  }
  
  const users = JSON.parse(localStorage.getItem('users') || '[]')
  const exists = users.some((u: { username: string }) => u.username === username.value)
  
  if (exists) {
    alert('用户名已存在')
    return
  }
  
  const newUser = {
    username: username.value,
    password: password.value,
    createdAt: new Date().toISOString()
  }
  
  users.push(newUser)
  localStorage.setItem('users', JSON.stringify(users))
  localStorage.setItem('user', JSON.stringify(newUser))
  router.push('/')
}
</script>

<style scoped>
.register-container {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  overflow: hidden;
}

.hearts-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.heart {
  position: absolute;
  width: 20px;
  height: 20px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ff6b6b'%3E%3Cpath d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z'/%3E%3C/svg%3E") no-repeat;
  background-size: contain;
  animation: float 4s ease-in-out infinite;
  opacity: 0.5;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-50px) rotate(180deg); }
}

.register-box {
  position: relative;
  z-index: 10;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 350px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #ff6b9d;
  font-size: 28px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #666;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #eee;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input-group input:focus {
  outline: none;
  border-color: #ff6b9d;
}

.register-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: #c44569;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.register-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(255, 154, 158, 0.4);
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #999;
}

.login-link a {
  color: #ff6b9d;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
