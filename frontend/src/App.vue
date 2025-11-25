<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        🚀 إدارة وسائل التواصل الاجتماعي
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">الرئيسية</router-link>
        <router-link to="/accounts" class="nav-link">الحسابات</router-link>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f5f5;
  direction: rtl;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background 0.3s ease;
}

.nav-link:hover, .nav-link.router-link-active {
  background: rgba(255,255,255,0.2);
}

.main-content {
  padding: 2rem;
  min-height: calc(100vh - 80px);
}

.dashboard, .accounts {
  max-width: 1200px;
  margin: 0 auto;
}

button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  margin: 1rem 0;
}

button:hover {
  background: #5a6fd8;
}
</style>
