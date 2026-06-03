<template>
  <div class="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Microsoft YaHei', sans-serif;
}

body {
  background: 
    radial-gradient(ellipse at 30% 20%, rgba(255, 182, 193, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 80%, rgba(255, 152, 152, 0.25) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(255, 107, 157, 0.2) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(255, 228, 236, 0.4) 0%, transparent 40%),
    radial-gradient(ellipse at 20% 80%, rgba(255, 200, 210, 0.35) 0%, transparent 45%),
    linear-gradient(135deg, #fff5f7 0%, #ffeef0 25%, #fdf2f6 50%, #fce7ed 75%, #faf0f5 100%);
  background-attachment: fixed;
}

#app {
  height: 100%;
  position: relative;
}
</style>
