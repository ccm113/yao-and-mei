<template>
  <div class="home-container">
    <div v-if="showSplash" class="splash-screen">
      <div class="hearts-container">
        <div v-for="heart in hearts" :key="heart.id" 
             class="heart-particle"
             :style="heart.style">
        </div>
      </div>
      <div v-if="showText" class="love-text">
        <span v-for="(char, index) in textChars" :key="index" 
              class="char" :style="{ animationDelay: `${index * 0.1}s` }">
          {{ char }}
        </span>
      </div>
    </div>

    <div v-show="!showSplash" class="main-content">
      <aside class="sidebar">
        <button @click="navigateTo('/')" class="nav-btn active">首页</button>
        <button @click="navigateTo('/story')" class="nav-btn">故事回顾</button>
        <button @click="navigateTo('/game')" class="nav-btn">小游戏</button>
        <button @click="navigateTo('/qna')" class="nav-btn">相互了解</button>
        <button @click="navigateTo('/wishlist')" class="nav-btn">心愿清单</button>
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </aside>

      <main class="content">
        <section class="photo-section">
          <h2 class="section-title">📷 感谢相机</h2>
          <div class="simple-grid">
            <div v-for="(photo, index) in photos" :key="index" class="photo-item">
              <div class="photo-wrapper">
                <img :src="photo.url" :alt="photo.caption" />
              </div>
            </div>
            <div class="add-photo" @click="addPhoto">
              <span>+ 添加照片</span>
              <input ref="fileInput" type="file" accept="image/*" @change="handleFileSelect" />
            </div>
          </div>
        </section>

        <section class="wordcloud-section">
          <h2 class="section-title">💬 我俩关键词</h2>
          <div class="wordcloud-container">
            <canvas ref="wordcloudCanvas" width="700" height="350"></canvas>
          </div>
        </section>
      </main>
    </div>

    <input type="file" ref="hiddenFileInput" style="display: none;" accept="image/*" @change="handleFileSelect" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { sharedStore } from '../store/sharedStore'

interface Photo {
  id: string
  url: string
  caption?: string
}

const router = useRouter()
const showSplash = ref(true)
const showText = ref(false)
const hearts = ref<Array<{ id: number; style: Record<string, string> }>>([])
const textChars = ref('李昕垚 and 陈昌梅'.split(''))
const photos = ref<Photo[]>([])
const fileInput = ref<HTMLInputElement | null>(null)
const hiddenFileInput = ref<HTMLInputElement | null>(null)
const wordcloudCanvas = ref<HTMLCanvasElement | null>(null)

const defaultPhotos: Photo[] = [
  { id: '1', url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200', caption: '相识的那天' },
  { id: '2', url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200', caption: '第一次约会' },
  { id: '3', url: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=200', caption: '一起看日落' },
  { id: '4', url: 'https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=200', caption: '海边漫步' },
]

const loadSharedPhotos = () => {
  if (sharedStore.photos.length === 0) {
    sharedStore.photos = [...defaultPhotos]
  }
  photos.value = sharedStore.photos
}

const saveSharedPhotos = () => {
  sharedStore.photos = photos.value
}

const generateHearts = () => {
  const newHearts: Array<{ id: number; style: Record<string, string> }> = []
  for (let i = 0; i < 50; i++) {
    const size = 10 + Math.random() * 30
    const angle = (Math.PI * 2 * i) / 50
    const distance = 100 + Math.random() * 200
    const x = Math.cos(angle) * distance
    const y = Math.sin(angle) * distance
    const delay = Math.random() * 0.5
    const duration = 1 + Math.random() * 1
    
    newHearts.push({
      id: i,
      style: {
        width: `${size}px`,
        height: `${size}px`,
        '--x': `${x}px`,
        '--y': `${y}px`,
        animationDelay: `${delay}s`,
        animationDuration: `${duration}s`,
      }
    })
  }
  hearts.value = newHearts
}

const navigateTo = (path: string) => {
  router.push(path)
}



const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}

const addPhoto = () => {
  hiddenFileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      const newPhoto: Photo = {
        id: Date.now().toString(),
        url: e.target?.result as string,
        caption: `照片 ${photos.value.length + 1}`
      }
      photos.value.push(newPhoto)
      saveSharedPhotos()
      target.value = ''
    }
    reader.readAsDataURL(file)
  }
}

const drawWordcloud = () => {
  const canvas = wordcloudCanvas.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  const colors = [
    '#E91E63', '#FF4081', '#F06292', '#F48FB1', '#F8BBD9',
    '#9C27B0', '#BA68C8', '#CE93D8', '#D4A5C4', '#E1BEE7',
    '#673AB7', '#7E57C2', '#9575CD', '#B39DDB', '#CE93D8',
    '#3F51B5', '#5C6BC0', '#7986CB', '#9FA8DA', '#C5CAE9',
    '#2196F3', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB',
    '#03A9F4', '#039BE5', '#0288D1', '#0277BD', '#81D4FA',
    '#00BCD4', '#26C6DA', '#4DD0E1', '#80DEEA', '#B2EBF2',
    '#009688', '#26A69A', '#4DB6AC', '#80CBC4', '#B2DFDB',
    '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9',
    '#8BC34A', '#9CCC65', '#AED581', '#C5E1A5', '#DCEDC8',
    '#FF9800', '#FFA726', '#FFB74D', '#FFCC80', '#FFE0B2',
    '#FF5722', '#FF7043', '#FF8A65', '#FFAB91', '#FFCCBC'
  ]
  
  const wordList = [
    { text: '垚', weight: 12 },
    { text: '梅', weight: 12 },
    { text: '闺蜜', weight: 10 },
    { text: '幸福', weight: 10 },
    { text: '快乐', weight: 10 },
    { text: '友情', weight: 9 },
    { text: '美好', weight: 9 },
    { text: '欢笑', weight: 8 },
    { text: '开心', weight: 8 },
    { text: '温暖', weight: 8 },
    { text: '温馨', weight: 8 },
    { text: '永远', weight: 8 },
    { text: '温柔', weight: 7 },
    { text: '美丽', weight: 7 },
    { text: '可爱', weight: 7 },
    { text: '善良', weight: 7 },
    { text: '青春', weight: 7 },
    { text: '回忆', weight: 7 },
    { text: '甜蜜', weight: 7 },
    { text: '梦想', weight: 6 },
    { text: '勇敢', weight: 6 },
    { text: '勇敢冲', weight: 6 },
    { text: '聪明', weight: 6 },
    { text: '吃货', weight: 6 },
    { text: '笨蛋', weight: 5 },
    { text: '上当', weight: 5 },
    { text: '闪闪发光', weight: 6 },
    { text: '独一无二', weight: 6 },
    { text: '善解人意', weight: 6 },
    { text: '姐妹情深', weight: 6 },
    { text: '友谊万岁', weight: 6 },
    { text: '心心相印', weight: 5 },
    { text: '形影不离', weight: 5 },
    { text: '携手同行', weight: 5 },
    { text: '快乐时光', weight: 5 },
    { text: '友谊长存', weight: 5 },
    { text: '梦想成真', weight: 5 },
    { text: '幸福永远', weight: 5 },
    { text: '美好未来', weight: 5 },
    { text: '天长地久', weight: 5 },
    { text: '李昕垚', weight: 11 },
    { text: '最可爱', weight: 7 },
    { text: '最爱', weight: 7 },
    { text: '最善良', weight: 7 },
    { text: '美丽动人', weight: 6 },
    { text: '心中', weight: 5 },
    { text: '独', weight: 5 },
    { text: '最', weight: 5 },
    { text: '冲', weight: 5 },
    { text: '本蛋', weight: 5 },
    { text: '美', weight: 5 },
    { text: '走', weight: 4 },
    { text: '快', weight: 4 },
    { text: '万', weight: 4 },
    { text: '实现梦想', weight: 6 },
  ]
  
  const words = wordList.map((word, index) => ({
    ...word,
    color: colors[index % colors.length]
  }))
  
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  const padding = 15
  const minGap = 8
  
  const placedWords: Array<{ x: number; y: number; width: number; height: number }> = []
  
  const checkCollision = (x: number, y: number, width: number, height: number) => {
    for (const placed of placedWords) {
      const left1 = x - width / 2
      const right1 = x + width / 2
      const top1 = y - height / 2
      const bottom1 = y + height / 2
      
      const left2 = placed.x - placed.width / 2
      const right2 = placed.x + placed.width / 2
      const top2 = placed.y - placed.height / 2
      const bottom2 = placed.y + placed.height / 2
      
      if (right1 > left2 + minGap && 
          left1 < right2 - minGap && 
          bottom1 > top2 + minGap && 
          top1 < bottom2 - minGap) {
        return true
      }
    }
    return false
  }
  
  const sortedWords = [...words].sort((a, b) => b.weight - a.weight)
  
  sortedWords.forEach((word) => {
    const fontSize = word.weight * 6 + 10
    ctx.font = `${fontSize}px 'Microsoft YaHei', 'PingFang SC', 'SimHei', sans-serif`
    const metrics = ctx.measureText(word.text)
    const textWidth = metrics.width
    const textHeight = fontSize * 1.2
    
    let attempts = 0
    let placed = false
    let x = 0
    let y = 0
    
    while (!placed && attempts < 5000) {
      x = padding + textWidth / 2 + Math.random() * (canvas.width - textWidth - padding * 2)
      y = padding + textHeight / 2 + Math.random() * (canvas.height - textHeight - padding * 2)
      
      if (!checkCollision(x, y, textWidth, textHeight)) {
        placed = true
      }
      attempts++
    }
    
    if (placed) {
      placedWords.push({ x, y, width: textWidth, height: textHeight })
      
      const shouldRotate = Math.random() > 0.75
      const rotation = shouldRotate ? (Math.random() - 0.5) * 12 : 0
      
      ctx.save()
      ctx.translate(x, y)
      ctx.rotate((rotation * Math.PI) / 180)
      
      ctx.font = `${fontSize}px 'Microsoft YaHei', 'PingFang SC', 'SimHei', sans-serif`
      ctx.fillStyle = word.color
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      
      ctx.fillText(word.text, 0, 0)
      
      ctx.restore()
    }
  })
}

watch(photos, () => {
  saveSharedPhotos()
}, { deep: true })

onMounted(() => {
  generateHearts()
  
  setTimeout(() => {
    showText.value = true
  }, 1500)
  
  setTimeout(() => {
    showSplash.value = false
    loadSharedPhotos()
    nextTick(() => {
      drawWordcloud()
    })
  }, 4000)
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  position: relative;
  background: transparent;
}

.main-content {
  display: flex;
  min-height: 100vh;
  position: relative;
  z-index: 1;
  background: transparent;
}

.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow: hidden;
}

.hearts-container {
  position: absolute;
  width: 100%;
  height: 100%;
}

.heart-particle {
  position: absolute;
  top: 50%;
  left: 50%;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffffff'%3E%3Cpath d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z'/%3E%3C/svg%3E") no-repeat;
  background-size: contain;
  animation: explode 1s ease-out forwards;
  opacity: 0;
}

@keyframes explode {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 1;
  }
  100% {
    transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scale(1);
    opacity: 0;
  }
}

.love-text {
  display: flex;
  gap: 10px;
  font-size: 48px;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

.char {
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-content {
  display: flex;
  min-height: 100vh;
  position: relative;
  z-index: 1;
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
}

.section-title {
  font-size: 24px;
  color: #c44569;
  margin-bottom: 30px;
  text-align: center;
}

.photo-section {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 248, 250, 0.9) 50%, rgba(255, 245, 248, 0.95) 100%);
  padding: 30px;
  border-radius: 24px;
  margin-bottom: 30px;
  box-shadow: 
    0 8px 32px rgba(255, 107, 157, 0.15),
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 107, 157, 0.1);
  position: relative;
  overflow: hidden;
}

.photo-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 107, 157, 0.3) 50%, transparent 100%);
}

.photo-section::after {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 182, 193, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.simple-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  justify-items: center;
}

.photo-item {
  width: 100%;
  max-width: 200px;
}

.photo-wrapper {
  width: 100%;
  height: 150px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.photo-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.add-photo {
  width: 200px;
  height: 150px;
  border: 3px dashed #ff6b9d;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ff6b9d;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(255, 107, 157, 0.05);
}

.add-photo:hover {
  background: rgba(255, 107, 157, 0.1);
  border-style: solid;
}

.add-photo input {
  display: none;
}

.wordcloud-section {
  background: transparent;
  padding: 20px 0;
  border: none;
}

.wordcloud-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.wordcloud-container canvas {
  width: 100%;
  max-width: 800px;
  height: auto;
  background: transparent;
}
</style>
