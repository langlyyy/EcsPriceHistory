<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>阿里云抢占式实例价格查询</h1>
          <p>实时查询和对比阿里云抢占式实例的历史价格趋势</p>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <p>&copy; 2024 阿里云抢占式实例价格查询工具</p>
      </el-footer>
    </el-container>
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

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  height: auto !important;
}

.el-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  pointer-events: none;
}

.header-content {
  position: relative;
  z-index: 1;
}

.header-content h1 {
  margin: 0 0 15px 0;
  font-size: 2.4em;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.header-content p {
  margin: 0;
  font-size: 1.2em;
  opacity: 0.95;
  font-weight: 300;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.el-main {
  padding: 0;
  background: transparent;
  flex: 1;
}

.el-footer {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  text-align: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.el-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain2" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.05"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.05"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.05"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.05"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23grain2)"/></svg>');
  pointer-events: none;
}

.el-footer p {
  margin: 0;
  font-size: 0.95em;
  position: relative;
  z-index: 1;
  opacity: 0.9;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-content h1 {
    font-size: 2.2em;
  }
  
  .el-header {
    padding: 35px 20px;
  }
}

@media (max-width: 768px) {
  .header-content h1 {
    font-size: 1.8em;
  }
  
  .header-content p {
    font-size: 1em;
  }
  
  .el-header {
    padding: 30px 15px;
  }
}

@media (max-width: 480px) {
  .header-content h1 {
    font-size: 1.4em;
  }
  
  .header-content p {
    font-size: 0.9em;
  }
  
  .el-header {
    padding: 25px 10px;
  }
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}
</style> 