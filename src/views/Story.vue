<template>
  <div class="story-container">
    <aside class="sidebar">
      <button @click="navigateTo('/')" class="nav-btn">首页</button>
      <button @click="navigateTo('/story')" class="nav-btn active">故事回顾</button>
      <button @click="navigateTo('/game')" class="nav-btn">小游戏</button>
      <button @click="navigateTo('/qna')" class="nav-btn">相互了解</button>
      <button @click="navigateTo('/wishlist')" class="nav-btn">心愿清单</button>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </aside>

    <main class="content">
      <div class="story-book">
        <div class="book-header">
          <h1 class="book-title">📖 我们的故事</h1>
          <p class="book-subtitle">一段美好的闺蜜情谊</p>
        </div>

        <div class="story-chapters">
          <div v-for="(chapter, index) in chapters" :key="index" 
               class="chapter" :class="{ active: currentChapter === index }">
            <div class="chapter-number">{{ index + 1 }}</div>
            <div class="chapter-content">
              <h3>{{ chapter.title }}</h3>
              <div class="story-text">
                <p v-for="(paragraph, pIndex) in chapter.content" :key="pIndex">
                  {{ paragraph }}
                </p>
              </div>
              <div v-if="chapter.image" class="story-image">
                <img :src="chapter.image" :alt="chapter.title" />
              </div>
            </div>
          </div>
        </div>

        <div class="chapter-nav">
          <button @click="prevChapter" :disabled="currentChapter === 0" class="nav-arrow">←</button>
          <span class="chapter-indicator">{{ currentChapter + 1 }} / {{ chapters.length }}</span>
          <button @click="nextChapter" :disabled="currentChapter === chapters.length - 1" class="nav-arrow">→</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentChapter = ref(0)

const chapters = [
  {
    title: '初见·那年夏天',
    content: [
      '还记得那是一个炎热的夏天，阳光透过梧桐树叶洒在校园的小路上。',
      '我抱着一摞厚厚的课本，不小心撞到了一个同样抱着书本的女生。',
      '"对不起！"我们同时说道，然后相视一笑。',
      '她叫李昕垚，一个名字像诗一样美的女孩。',
      '那一刻，我知道，我们的故事开始了。'
    ],
    image: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400'
  },
  {
    title: '相知·一起成长',
    content: [
      '从那以后，我们成了形影不离的好朋友。',
      '一起去食堂吃饭，一起在图书馆自习，一起在操场上散步。',
      '她总是那么温柔，在我失落的时候安慰我，在我开心的时候比我还开心。',
      '我们分享彼此的小秘密，一起憧憬未来的美好。',
      '那些一起笑一起哭的日子，是我青春最珍贵的记忆。'
    ],
    image: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400'
  },
  {
    title: '相守·永远的闺蜜',
    content: [
      '时光荏苒，我们从青涩的少女变成了独立的女性。',
      '虽然我们不再每天见面，但心始终在一起。',
      '无论我遇到什么困难，第一个想到的总是她。',
      '她就像一束光，照亮我生命的每一个角落。',
      '李昕垚，谢谢你出现在我的生命里，这份情谊，我会好好珍惜一辈子。'
    ],
    image: 'https://images.unsplash.com/photo-1587440871875-191322ee64b0?w=400'
  }
]

const navigateTo = (path: string) => {
  router.push(path)
}

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}

const prevChapter = () => {
  if (currentChapter.value > 0) {
    currentChapter.value--
  }
}

const nextChapter = () => {
  if (currentChapter.value < chapters.length - 1) {
    currentChapter.value++
  }
}
</script>

<style scoped>
.story-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #a29bfe 0%, #fd79a8 100%);
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

.story-book {
  background: white;
  border-radius: 20px;
  padding: 40px;
  max-width: 800px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.book-header {
  text-align: center;
  margin-bottom: 40px;
}

.book-title {
  font-size: 36px;
  color: #c44569;
  margin-bottom: 10px;
}

.book-subtitle {
  font-size: 18px;
  color: #999;
}

.story-chapters {
  position: relative;
  min-height: 400px;
}

.chapter {
  display: none;
}

.chapter.active {
  display: block;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.chapter-number {
  display: inline-block;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}

.chapter-content h3 {
  font-size: 24px;
  color: #c44569;
  margin-bottom: 20px;
}

.story-text p {
  font-size: 18px;
  line-height: 1.8;
  color: #666;
  margin-bottom: 15px;
  text-indent: 2em;
}

.story-image {
  margin-top: 30px;
  text-align: center;
}

.story-image img {
  max-width: 100%;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.chapter-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.nav-arrow {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.nav-arrow:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 5px 20px rgba(255, 107, 157, 0.4);
}

.nav-arrow:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chapter-indicator {
  font-size: 18px;
  color: #999;
  min-width: 60px;
  text-align: center;
}
</style>
