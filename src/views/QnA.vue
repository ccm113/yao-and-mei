<template>
  <div class="qna-container">
    <aside class="sidebar">
      <button @click="navigateTo('/')" class="nav-btn">首页</button>
      <button @click="navigateTo('/story')" class="nav-btn">故事回顾</button>
      <button @click="navigateTo('/game')" class="nav-btn">小游戏</button>
      <button @click="navigateTo('/qna')" class="nav-btn active">相互了解</button>
      <button @click="navigateTo('/wishlist')" class="nav-btn">心愿清单</button>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </aside>

    <main class="content">
      <div class="qna-wrapper">
        <div class="qna-header">
          <h1 class="qna-title">💬 真心话问答</h1>
          <p class="qna-subtitle">了解彼此的小秘密</p>
        </div>

        <div class="qna-content">
          <div class="question-card">
            <div class="question-number">{{ currentIndex + 1 }} / {{ questions.length }}</div>
            <h2 class="question-text">{{ currentQuestion.text }}</h2>
            
            <div class="answer-options">
              <button v-for="(option, index) in currentQuestion.options" :key="index"
                      @click="selectOption(option)"
                      class="option-btn"
                      :class="{ selected: selectedAnswer === option, correct: showResult && option === currentQuestion.correct }">
                {{ option }}
              </button>
            </div>

            <div v-if="showResult" class="result-message" :class="isCorrect ? 'correct' : 'wrong'">
              <p>{{ isCorrect ? '🎉 回答正确！' : '😢 回答错误！' }}</p>
              <p class="correct-answer">正确答案: {{ currentQuestion.correct }}</p>
            </div>

            <button v-if="showResult" @click="nextQuestion" class="next-btn">
              {{ currentIndex < questions.length - 1 ? '下一题' : '查看结果' }}
            </button>
          </div>

          <div v-if="showFinalResult" class="final-result">
            <h2>📊 测试结果</h2>
            <div class="score-circle">
              <span class="score-value">{{ score }}</span>
              <span class="score-total">/{{ questions.length }}</span>
            </div>
            <p class="result-text">{{ getResultMessage() }}</p>
            <button @click="restartQuiz" class="restart-btn">再玩一次</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showResult = ref(false)
const showFinalResult = ref(false)
const score = ref(0)

const questions = [
  {
    text: '李昕垚最喜欢的颜色是什么？',
    options: ['粉色', '蓝色', '紫色', '红色'],
    correct: '粉色'
  },
  {
    text: '李昕垚最喜欢吃的食物是？',
    options: ['火锅', '寿司', '蛋糕', '披萨'],
    correct: '蛋糕'
  },
  {
    text: '李昕垚的梦想是什么？',
    options: ['环游世界', '成为画家', '开一家咖啡店', '当老师'],
    correct: '环游世界'
  },
  {
    text: '李昕垚最喜欢的季节是？',
    options: ['春天', '夏天', '秋天', '冬天'],
    correct: '春天'
  },
  {
    text: '李昕垚最喜欢的动物是？',
    options: ['猫', '狗', '兔子', '熊猫'],
    correct: '猫'
  },
  {
    text: '李昕垚最擅长的事情是？',
    options: ['唱歌', '跳舞', '画画', '做饭'],
    correct: '画画'
  },
  {
    text: '李昕垚的口头禅是什么？',
    options: ['太棒了！', '真的吗？', '哎呀！', '哈哈哈'],
    correct: '哎呀！'
  },
  {
    text: '李昕垚最喜欢的电影类型是？',
    options: ['喜剧', '爱情', '悬疑', '动画'],
    correct: '爱情'
  }
]

const currentQuestion = computed(() => questions[currentIndex.value])
const isCorrect = computed(() => selectedAnswer.value === currentQuestion.value.correct)

const selectOption = (option: string) => {
  if (showResult.value) return
  selectedAnswer.value = option
  showResult.value = true
  if (isCorrect.value) {
    score.value++
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value++
    selectedAnswer.value = ''
    showResult.value = false
  } else {
    showFinalResult.value = true
  }
}

const getResultMessage = () => {
  const percentage = (score.value / questions.length) * 100
  if (percentage === 100) return '完美！你是李昕垚的超级闺蜜！💖'
  if (percentage >= 75) return '太棒了！你很了解李昕垚！🌟'
  if (percentage >= 50) return '不错！继续努力了解她吧！💪'
  if (percentage >= 25) return '加油！多和李昕垚聊聊吧！😊'
  return '需要多了解一下李昕垚哦！🤗'
}

const restartQuiz = () => {
  currentIndex.value = 0
  selectedAnswer.value = ''
  showResult.value = false
  showFinalResult.value = false
  score.value = 0
}

const navigateTo = (path: string) => {
  router.push(path)
}

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.qna-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.qna-wrapper {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 600px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.qna-header {
  text-align: center;
  margin-bottom: 30px;
}

.qna-title {
  font-size: 32px;
  color: #764ba2;
  margin-bottom: 10px;
}

.qna-subtitle {
  font-size: 18px;
  color: #999;
}

.qna-content {
  min-height: 400px;
}

.question-card {
  text-align: center;
}

.question-number {
  display: inline-block;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 16px;
  margin-bottom: 20px;
}

.question-text {
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
  line-height: 1.5;
}

.answer-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.option-btn {
  padding: 20px;
  background: #f8f9fa;
  border: 2px solid #eee;
  border-radius: 15px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-btn:hover:not(.selected) {
  background: #eee;
  border-color: #667eea;
}

.option-btn.selected {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.option-btn.correct {
  background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
  color: white;
  border-color: #00b894;
}

.result-message {
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.result-message.correct {
  background: rgba(0, 184, 148, 0.1);
  color: #00b894;
}

.result-message.wrong {
  background: rgba(255, 118, 117, 0.1);
  color: #ff7675;
}

.result-message p {
  margin: 5px 0;
}

.correct-answer {
  font-size: 16px;
  opacity: 0.8;
}

.next-btn, .restart-btn {
  padding: 15px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.next-btn:hover, .restart-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.final-result {
  text-align: center;
}

.final-result h2 {
  font-size: 32px;
  color: #764ba2;
  margin-bottom: 30px;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 30px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.score-value {
  font-size: 48px;
  font-weight: bold;
  color: white;
}

.score-total {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.8);
}

.result-text {
  font-size: 20px;
  color: #666;
  margin-bottom: 30px;
}
</style>
