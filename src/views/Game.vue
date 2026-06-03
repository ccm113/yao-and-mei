<template>
  <div class="game-container">
    <aside class="sidebar">
      <button @click="navigateTo('/')" class="nav-btn">首页</button>
      <button @click="navigateTo('/story')" class="nav-btn">故事回顾</button>
      <button @click="navigateTo('/game')" class="nav-btn active">小游戏</button>
      <button @click="navigateTo('/qna')" class="nav-btn">相互了解</button>
      <button @click="navigateTo('/wishlist')" class="nav-btn">心愿清单</button>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </aside>

    <main class="content">
      <div class="game-wrapper">
        <div class="game-header">
          <h1 class="game-title">🎮 爱心大搜索</h1>
          <div class="game-info">
            <span class="score">得分: {{ score }}</span>
            <span class="time">时间: {{ timeLeft }}s</span>
            <span class="level">关卡: {{ level }}</span>
          </div>
        </div>

        <div v-if="gameState === 'start'" class="start-screen">
          <div class="start-content">
            <h2>💝 爱心大搜索</h2>
            <p>在限定时间内找到所有隐藏的爱心！</p>
            <p>点击爱心即可收集</p>
            <button @click="startGame" class="start-btn">开始游戏</button>
          </div>
        </div>

        <div v-else-if="gameState === 'playing'" class="game-area">
          <div v-for="heart in hearts" :key="heart.id" 
               class="heart-item"
               :class="{ found: heart.found, clicked: heart.clicked }"
               :style="heart.style"
               @click="collectHeart(heart)">
            💖
          </div>
        </div>

        <div v-else-if="gameState === 'win'" class="result-screen win">
          <div class="result-content">
            <h2>🎉 恭喜过关！</h2>
            <p>你找到了所有爱心！</p>
            <p class="final-score">得分: {{ score }}</p>
            <button @click="nextLevel" class="next-btn">下一关 →</button>
          </div>
        </div>

        <div v-else-if="gameState === 'lose'" class="result-screen lose">
          <div class="result-content">
            <h2>😢 时间到！</h2>
            <p>还有 {{ heartsLeft }} 个爱心没找到</p>
            <button @click="restartGame" class="restart-btn">重新开始</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const gameState = ref<'start' | 'playing' | 'win' | 'lose'>('start')
const score = ref(0)
const timeLeft = ref(30)
const level = ref(1)
const hearts = ref<Array<{ id: number; x: number; y: number; found: boolean; clicked: boolean; style: Record<string, string> }>>([])
let timer: number | null = null

const heartsLeft = computed(() => hearts.value.filter(h => !h.found).length)

const generateHearts = () => {
  const count = 5 + level.value * 2
  const newHearts: typeof hearts.value = []
  
  for (let i = 0; i < count; i++) {
    const x = 5 + Math.random() * 85
    const y = 5 + Math.random() * 85
    const scale = 0.8 + Math.random() * 0.6
    const rotation = -30 + Math.random() * 60
    
    newHearts.push({
      id: i,
      x,
      y,
      found: false,
      clicked: false,
      style: {
        left: `${x}%`,
        top: `${y}%`,
        transform: `scale(${scale}) rotate(${rotation}deg)`
      }
    })
  }
  
  hearts.value = newHearts
}

const startGame = () => {
  gameState.value = 'playing'
  score.value = 0
  timeLeft.value = 30 + level.value * 5
  generateHearts()
  
  timer = window.setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      endGame(false)
    }
  }, 1000)
}

const collectHeart = (heart: typeof hearts.value[0]) => {
  if (heart.found) return
  
  heart.found = true
  heart.clicked = true
  score.value += 10 * level.value
  
  setTimeout(() => {
    heart.clicked = false
  }, 300)
  
  if (heartsLeft.value === 0) {
    endGame(true)
  }
}

const endGame = (won: boolean) => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  
  gameState.value = won ? 'win' : 'lose'
}

const nextLevel = () => {
  level.value++
  startGame()
}

const restartGame = () => {
  level.value = 1
  startGame()
}

const navigateTo = (path: string) => {
  router.push(path)
}

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.game-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  display: flex;
}

.sidebar {
  width: 200px;
  background: rgba(255, 255, 255, 0.9);
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
}

.nav-btn {
  padding: 15px 20px;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(255, 107, 157, 0.4);
}

.nav-btn.active {
  background: linear-gradient(135deg, #c44569 0%, #ff6b9d 100%);
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
}

.logout-btn {
  margin-top: auto;
  padding: 15px 20px;
  background: #eee;
  color: #666;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: #ddd;
}

.content {
  flex: 1;
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.game-wrapper {
  background: white;
  border-radius: 20px;
  padding: 30px;
  width: 800px;
  height: 600px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.game-header {
  text-align: center;
  margin-bottom: 20px;
}

.game-title {
  font-size: 32px;
  color: #c44569;
  margin-bottom: 15px;
}

.game-info {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.game-info span {
  font-size: 18px;
  font-weight: bold;
  padding: 10px 20px;
  background: rgba(255, 107, 157, 0.1);
  border-radius: 20px;
  color: #c44569;
}

.start-screen, .result-screen {
  height: calc(100% - 120px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.start-content, .result-content {
  text-align: center;
}

.start-content h2, .result-content h2 {
  font-size: 36px;
  color: #c44569;
  margin-bottom: 20px;
}

.start-content p, .result-content p {
  font-size: 18px;
  color: #666;
  margin-bottom: 10px;
}

.final-score {
  font-size: 24px !important;
  color: #ff6b9d !important;
  font-weight: bold;
}

.start-btn, .next-btn, .restart-btn {
  margin-top: 30px;
  padding: 15px 40px;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 20px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.start-btn:hover, .next-btn:hover, .restart-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4);
}

.game-area {
  position: relative;
  height: calc(100% - 120px);
  background: linear-gradient(135deg, #ffeaa7 0%, #fd79a8 50%, #a29bfe 100%);
  border-radius: 15px;
  overflow: hidden;
}

.heart-item {
  position: absolute;
  font-size: 40px;
  cursor: pointer;
  transition: all 0.3s;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.heart-item:hover {
  transform: scale(1.2);
  filter: brightness(1.2);
}

.heart-item.clicked {
  animation: pop 0.3s ease-out forwards;
}

@keyframes pop {
  0% { transform: scale(1.5); opacity: 1; }
  100% { transform: scale(0); opacity: 0; }
}

.heart-item.found {
  opacity: 0;
  pointer-events: none;
}

.result-screen.win {
  background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);
  border-radius: 15px;
}

.result-screen.win h2 {
  color: white;
}

.result-screen.win p {
  color: rgba(255, 255, 255, 0.9);
}

.result-screen.win .next-btn {
  background: white;
  color: #00b894;
}

.result-screen.win .next-btn:hover {
  box-shadow: 0 10px 30px rgba(255, 255, 255, 0.3);
}

.result-screen.lose {
  background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%);
  border-radius: 15px;
}

.result-screen.lose h2 {
  color: white;
}

.result-screen.lose p {
  color: rgba(255, 255, 255, 0.9);
}
</style>
