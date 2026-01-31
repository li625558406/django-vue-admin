<template>
  <div class="modern-dashboard">
    <!-- 欢迎卡片 -->
    <div class="welcome-card">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1 class="welcome-title">欢迎回来，{{ userName }}！👋</h1>
          <p class="welcome-subtitle">这是您的个人仪表板，查看和管理您的账户信息</p>
        </div>
        <div class="user-avatar-large">
          <img v-if="avatar" :src="avatar" alt="用户头像" />
          <div v-else class="avatar-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作卡片 -->
    <div class="section-title">
      <h2>快捷操作</h2>
    </div>
    <div class="action-grid">
      <div class="action-card" @click="handleLogout">
        <div class="action-icon logout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </div>
        <h3>退出登录</h3>
        <p>安全退出您的账户</p>
      </div>

      <div class="action-card">
        <div class="action-icon profile">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <h3>个人资料</h3>
        <p>管理您的个人信息</p>
      </div>

      <div class="action-card">
        <div class="action-icon security">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div>
        <h3>修改密码</h3>
        <p>更新您的登录密码</p>
      </div>
    </div>

    <!-- 账户信息卡片 -->
    <div class="section-title">
      <h2>账户信息</h2>
    </div>
    <div class="info-card">
      <div class="info-grid">
        <div class="info-item">
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <div class="info-content">
            <span class="info-label">用户名</span>
            <span class="info-value">{{ username }}</span>
          </div>
        </div>

        <div class="info-item">
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <div class="info-content">
            <span class="info-label">姓名</span>
            <span class="info-value">{{ userName }}</span>
          </div>
        </div>

        <div class="info-item">
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <div class="info-content">
            <span class="info-label">角色</span>
            <span class="info-value">{{ roles && roles.length ? roles.join(', ') : '普通用户' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 装饰元素 -->
    <div class="decorative-dots"></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'UserDashboard',
  computed: {
    ...mapGetters([
      'name',
      'username',
      'avatar',
      'roles'
    ]),
    userName() {
      return this.name || this.username || '用户'
    }
  },
  methods: {
    async handleLogout() {
      try {
        await this.$store.dispatch('user/logout')
        this.$router.push('/login')
        this.$message.success('已成功退出登录')
      } catch (error) {
        console.error('退出登录失败:', error)
        this.$message.error('退出登录失败，请重试')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-dashboard {
  font-family: 'Outfit', sans-serif;
  position: relative;
}

// 欢迎卡片
.welcome-card {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius-xl);
  padding: 40px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-xl);
  color: white;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    animation: float 20s ease-in-out infinite;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -5%;
    width: 200px;
    height: 200px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 50%;
    animation: float 15s ease-in-out infinite reverse;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

.welcome-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
  gap: 32px;
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.95;
  font-weight: 400;
  line-height: 1.5;
}

.user-avatar-large {
  width: 100px;
  height: 100px;
  border-radius: var(--radius-xl);
  overflow: hidden;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 3px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;

    svg {
      width: 50px;
      height: 50px;
    }
  }
}

// 章节标题
.section-title {
  margin-bottom: 20px;

  h2 {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.3px;
  }
}

// 操作卡片网格
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.action-card {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: 28px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--primary-dark));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);

    &::before {
      transform: scaleX(1);
    }

    .action-icon {
      transform: scale(1.1);
    }
  }

  h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 16px 0 6px 0;
  }

  p {
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 400;
  }
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);

  svg {
    width: 26px;
    height: 26px;
  }

  &.logout {
    background: linear-gradient(135deg, #FC8181 0%, #F56565 100%);
    color: white;
  }

  &.profile {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    color: white;
  }

  &.security {
    background: linear-gradient(135deg, #63B3ED 0%, #4299E1 100%);
    color: white;
  }
}

// 信息卡片
.info-card {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--bg-color);
  border-radius: var(--radius-md);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(79, 209, 197, 0.05);
    transform: translateX(4px);
  }
}

.info-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);

  svg {
    width: 24px;
    height: 24px;
  }
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 16px;
  color: var(--text-primary);
  font-weight: 600;
}

// 装饰元素
.decorative-dots {
  position: fixed;
  top: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background-image: radial-gradient(var(--primary-color) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.15;
  pointer-events: none;
  z-index: -1;
}

// 响应式
@media (max-width: 768px) {
  .welcome-card {
    padding: 28px;
  }

  .welcome-content {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .welcome-title {
    font-size: 28px;
  }

  .welcome-subtitle {
    font-size: 14px;
  }

  .user-avatar-large {
    width: 80px;
    height: 80px;
    margin: 0 auto;

    .avatar-placeholder svg {
      width: 40px;
      height: 40px;
    }
  }

  .action-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .section-title h2 {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .welcome-title {
    font-size: 24px;
  }

  .action-card, .info-card {
    padding: 20px;
  }
}
</style>
