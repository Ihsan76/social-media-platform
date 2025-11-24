<template>
  <div class="dashboard">
    <h1>مرحباً بك في نظام إدارة وسائل التواصل الاجتماعي</h1>
    <div class="stats">
      <div class="stat-card">
        <h3>الحسابات المتصلة</h3>
        <p class="number">0</p>
      </div>
      <div class="stat-card">
        <h3>المنشورات المجدولة</h3>
        <p class="number">0</p>
      </div>
      <div class="stat-card">
        <h3>التفاعلات</h3>
        <p class="number">0</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  color: #666;
  margin-bottom: 0.5rem;
}

.number {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}
</style>
