<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="title">💖 欢迎回来</h1>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>用户名</label>
          <input v-model="username" type="text" placeholder="请输入用户名" />
        </div>
        <div class="input-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" />
        </div>
        <button type="submit" class="login-btn">登录</button>
      </form>
      <p class="register-link">
        还没有账号？<a href="/register">立即注册</a>
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

const handleLogin = () => {
  if (!username.value || !password.value) {
    alert('请填写用户名和密码')
    return
  }
  
  const users = JSON.parse(localStorage.getItem('users') || '[]')
  const user = users.find((u: { username: string; password: string }) => 
    u.username === username.value && u.password === password.value
  )
  
  if (user) {
    localStorage.setItem('user', JSON.stringify(user))
    router.push('/')
  } else {
    alert('用户名或密码错误')
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
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
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffc0cb'%3E%3Cpath d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z'/%3E%3C/svg%3E") no-repeat;
  background-size: contain;
  animation: float 4s ease-in-out infinite;
  opacity: 0.6;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-50px) rotate(180deg); }
}

.login-box {
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
  color: #c44569;
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

.login-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.login-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4);
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #999;
}

.register-link a {
  color: #ff6b9d;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
