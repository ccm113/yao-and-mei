<template>
  <div class="wishlist-container">
    <aside class="sidebar">
      <button @click="navigateTo('/')" class="nav-btn">首页</button>
      <button @click="navigateTo('/story')" class="nav-btn">故事回顾</button>
      <button @click="navigateTo('/game')" class="nav-btn">小游戏</button>
      <button @click="navigateTo('/qna')" class="nav-btn">相互了解</button>
      <button @click="navigateTo('/wishlist')" class="nav-btn active">心愿清单</button>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </aside>

    <main class="content">
      <div class="wishlist-wrapper">
        <div class="wishlist-header">
          <h1 class="wishlist-title">🌍 心愿清单</h1>
          <p class="wishlist-subtitle">想和你一起去的地方</p>
        </div>

        <div class="map-section">
          <div class="map-container">
            <div class="world-map">
              <svg viewBox="0 0 800 400" class="map-svg">
                <defs>
                  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ddd" stroke-width="0.5"/>
                  </pattern>
                  <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                      <feMergeNode in="coloredBlur"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
                
                <rect width="800" height="400" fill="url(#grid)"/>
                
                <path class="continent" d="M60,180 Q80,160 100,170 L120,150 Q140,140 150,150 L160,130 Q180,110 200,120 L220,100 Q240,90 250,100 L260,80 Q280,70 290,80 L300,60 Q320,50 330,60 L340,40" fill="#2d5a27" opacity="0.7"/>
                <path class="continent" d="M400,120 Q420,100 440,110 L460,90 Q480,80 490,90 L500,70 Q520,60 530,70 L540,50" fill="#2d5a27" opacity="0.7"/>
                <path class="continent" d="M550,150 Q570,130 590,140 L610,120 Q630,110 640,120 L650,100 Q670,90 680,100" fill="#2d5a27" opacity="0.7"/>
                <path class="continent" d="M350,250 Q370,230 390,240 L410,220 Q430,210 440,220 L450,200" fill="#2d5a27" opacity="0.7"/>
                <path class="continent" d="M150,280 Q170,260 190,270 L210,250 Q230,240 240,250 L250,230" fill="#2d5a27" opacity="0.7"/>
                <path class="continent" d="M600,280 Q620,260 640,270 L660,250 Q680,240 690,250" fill="#2d5a27" opacity="0.7"/>
                
                <g v-for="spot in destinations" :key="spot.name" 
                   class="destination-spot"
                   :class="{ selected: selectedDestination?.name === spot.name }"
                   :transform="`translate(${spot.x}, ${spot.y})`"
                   @click="selectDestination(spot)">
                  <circle r="12" :fill="selectedDestination?.name === spot.name ? '#ff6b9d' : '#4ecdc4'" filter="url(#glow)"/>
                  <text :y="30" text-anchor="middle" fill="#666" font-size="12">{{ spot.name }}</text>
                </g>
              </svg>
            </div>

            <div class="destination-selector">
              <label>选择目的地：</label>
              <select v-model="selectedDestinationName" @change="onDestinationChange">
                <option value="">请选择...</option>
                <option v-for="dest in destinations" :key="dest.name" :value="dest.name">
                  {{ dest.name }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="selectedDestination" class="guide-section">
          <div class="guide-card" :style="{ animation: 'fadeIn 0.5s ease-out' }">
            <div class="guide-header">
              <h2>{{ selectedDestination.emoji }} {{ selectedDestination.name }}</h2>
              <div class="guide-tags">
                <span v-for="tag in selectedDestination.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            
            <div class="guide-content">
              <div class="guide-image">
                <img :src="selectedDestination.image" :alt="selectedDestination.name" />
              </div>
              
              <div class="guide-info">
                <h3>📍 地理位置</h3>
                <p>{{ selectedDestination.location }}</p>
                
                <h3>✨ 必去景点</h3>
                <ul>
                  <li v-for="(spot, index) in selectedDestination.attractions" :key="index">
                    {{ spot }}
                  </li>
                </ul>
                
                <h3>🍽️ 特色美食</h3>
                <ul>
                  <li v-for="(food, index) in selectedDestination.foods" :key="index">
                    {{ food }}
                  </li>
                </ul>
                
                <h3>💡 旅行小贴士</h3>
                <p>{{ selectedDestination.tips }}</p>
              </div>
            </div>

            <button @click="addToWishlist" class="add-btn">
              {{ isInWishlist ? '❤️ 已添加到心愿清单' : '💝 添加到心愿清单' }}
            </button>
          </div>
        </div>

        <div v-if="wishlist.length > 0" class="wishlist-section">
          <h3>❤️ 我的心愿清单</h3>
          <div class="wishlist-items">
            <div v-for="item in wishlist" :key="item.name" class="wishlist-item">
              <span>{{ item.emoji }} {{ item.name }}</span>
              <button @click="removeFromWishlist(item.name)" class="remove-btn">×</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { sharedStore } from '../store/sharedStore'

const router = useRouter()

interface Destination {
  id?: string
  name: string
  x: number
  y: number
  emoji: string
  location: string
  image: string
  tags: string[]
  attractions: string[]
  foods: string[]
  tips: string
}

const destinations: Destination[] = [
  {
    name: '巴黎',
    x: 430,
    y: 100,
    emoji: '🗼',
    location: '法国，欧洲',
    image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400',
    tags: ['浪漫', '艺术', '美食'],
    attractions: ['埃菲尔铁塔', '卢浮宫', '巴黎圣母院', '香榭丽舍大街'],
    foods: ['法式蜗牛', '马卡龙', '可颂', '红酒'],
    tips: '最佳旅游时间是4-6月和9-11月，避开旅游旺季。'
  },
  {
    name: '东京',
    x: 720,
    y: 120,
    emoji: '🏯',
    location: '日本，亚洲',
    image: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400',
    tags: ['文化', '美食', '科技'],
    attractions: ['东京塔', '浅草寺', '涩谷十字路口', '富士山'],
    foods: ['寿司', '拉面', '天妇罗', '抹茶'],
    tips: '建议购买Suica卡方便出行，注意垃圾分类。'
  },
  {
    name: '马尔代夫',
    x: 550,
    y: 220,
    emoji: '🏝️',
    location: '印度洋',
    image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400',
    tags: ['海岛', '度假', '潜水'],
    attractions: ['水上别墅', '珊瑚礁潜水', '日落巡航', '白沙海滩'],
    foods: ['海鲜', '椰子', '热带水果'],
    tips: '建议提前预订水上别墅，注意防晒和保护珊瑚。'
  },
  {
    name: '纽约',
    x: 180,
    y: 120,
    emoji: '🗽',
    location: '美国，北美洲',
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400',
    tags: ['都市', '购物', '文化'],
    attractions: ['自由女神像', '时代广场', '中央公园', '百老汇'],
    foods: ['披萨', '汉堡', '热狗', '芝士蛋糕'],
    tips: '建议购买地铁通票，注意安全特别是夜间出行。'
  },
  {
    name: '悉尼',
    x: 680,
    y: 320,
    emoji: '🌉',
    location: '澳大利亚，大洋洲',
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',
    tags: ['海滩', '自然', '都市'],
    attractions: ['悉尼歌剧院', '海港大桥', '邦迪海滩', '蓝山国家公园'],
    foods: ['澳洲牛排', '海鲜', 'Tim Tam饼干'],
    tips: '注意季节差异，澳洲季节与北半球相反。'
  },
  {
    name: '威尼斯',
    x: 410,
    y: 110,
    emoji: '🚤',
    location: '意大利，欧洲',
    image: 'https://images.unsplash.com/photo-1548549166-23ac5536998d?w=400',
    tags: ['水城', '浪漫', '历史'],
    attractions: ['圣马可广场', '里亚托桥', '威尼斯大运河', '彩色岛'],
    foods: ['意面', '披萨', '提拉米苏', '意式冰淇淋'],
    tips: '建议穿舒适的鞋子，避开高峰期的人群。'
  }
]

const selectedDestinationName = ref('')
const wishlist = ref<Destination[]>([])

const loadSharedWishlist = () => {
  wishlist.value = sharedStore.wishlist.map(item => ({
    id: item.id,
    name: item.destination,
    x: 0,
    y: 0,
    emoji: '📍',
    location: '',
    image: '',
    tags: [],
    attractions: [],
    foods: [],
    tips: item.description || ''
  }))
}

const saveSharedWishlist = () => {
  sharedStore.wishlist = wishlist.value.map(item => ({
    id: item.id || Date.now().toString(),
    destination: item.name,
    description: item.tips || '',
    coordinates: { lat: 0, lng: 0 }
  }))
}

const selectedDestination = computed(() => {
  return destinations.find(d => d.name === selectedDestinationName.value)
})

const isInWishlist = computed(() => {
  return wishlist.value.some(d => d.name === selectedDestination.value?.name)
})

const selectDestination = (spot: Destination) => {
  selectedDestinationName.value = spot.name
}

const onDestinationChange = () => {
}

const addToWishlist = () => {
  if (selectedDestination.value && !isInWishlist.value) {
    wishlist.value.push(selectedDestination.value)
    saveSharedWishlist()
  }
}

const removeFromWishlist = (name: string) => {
  wishlist.value = wishlist.value.filter(d => d.name !== name)
  saveSharedWishlist()
}

const navigateTo = (path: string) => {
  router.push(path)
}

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}

watch(wishlist, () => {
  saveSharedWishlist()
}, { deep: true })

watch(selectedDestinationName, () => {
})

onMounted(() => {
  loadSharedWishlist()
})
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.wishlist-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
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
}

.wishlist-wrapper {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.wishlist-header {
  text-align: center;
  margin-bottom: 30px;
}

.wishlist-title {
  font-size: 32px;
  color: #00cec9;
  margin-bottom: 10px;
}

.wishlist-subtitle {
  font-size: 18px;
  color: #999;
}

.map-section {
  margin-bottom: 30px;
}

.map-container {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 20px;
}

.world-map {
  margin-bottom: 20px;
}

.map-svg {
  width: 100%;
  height: auto;
}

.continent {
  transition: fill 0.3s;
}

.continent:hover {
  fill: #3d7a35;
}

.destination-spot {
  cursor: pointer;
  transition: transform 0.3s;
}

.destination-spot:hover {
  transform: scale(1.1);
}

.destination-spot.selected circle {
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { r: 12; }
  50% { r: 16; }
}

.destination-selector {
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: center;
}

.destination-selector label {
  font-size: 18px;
  color: #666;
}

.destination-selector select {
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #4ecdc4;
  border-radius: 10px;
  background: white;
  color: #333;
  cursor: pointer;
}

.destination-selector select:focus {
  outline: none;
  border-color: #00cec9;
}

.guide-section {
  margin-bottom: 30px;
}

.guide-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e8f5e9 100%);
  border-radius: 15px;
  padding: 30px;
}

.guide-header {
  margin-bottom: 20px;
}

.guide-header h2 {
  font-size: 28px;
  color: #2d5a27;
  margin-bottom: 10px;
}

.guide-tags {
  display: flex;
  gap: 10px;
}

.tag {
  padding: 5px 15px;
  background: #4ecdc4;
  color: white;
  border-radius: 20px;
  font-size: 14px;
}

.guide-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 20px;
}

.guide-image img {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.guide-info h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
}

.guide-info p {
  color: #666;
  line-height: 1.6;
}

.guide-info ul {
  list-style: none;
  padding: 0;
}

.guide-info li {
  padding: 8px 0;
  color: #666;
  border-bottom: 1px solid #eee;
}

.guide-info li:last-child {
  border-bottom: none;
}

.add-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(255, 107, 157, 0.4);
}

.wishlist-section {
  background: rgba(255, 107, 157, 0.1);
  border-radius: 15px;
  padding: 20px;
}

.wishlist-section h3 {
  font-size: 20px;
  color: #c44569;
  margin-bottom: 15px;
}

.wishlist-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.wishlist-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.wishlist-item span {
  font-size: 16px;
  color: #333;
}

.remove-btn {
  width: 25px;
  height: 25px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background 0.3s;
}

.remove-btn:hover {
  background: #ee5253;
}
</style>
