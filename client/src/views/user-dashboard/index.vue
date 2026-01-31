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
  font-family: var(--font-family), sans-serif;
  position: relative;
}

// 欢迎卡片
.welcome-card {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
  border-radius: var(--radius-2xl);
  padding: 48px;
  margin-bottom: 40px;
  box-shadow: var(--shadow-xl);
  color: white;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -15%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 25s ease-in-out infinite;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 20s ease-in-out infinite reverse;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) scale(1.1) rotate(180deg);
  }
}

.welcome-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
  gap: 40px;
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 40px;
  font-weight: 800;
  margin: 0 0 16px 0;
  letter-spacing: -1px;
  line-height: 1.15;
}

.welcome-subtitle {
  font-size: 17px;
  margin: 0;
  opacity: 0.95;
  font-weight: 500;
  line-height: 1.6;
}

.user-avatar-large {
  width: 110px;
  height: 110px;
  border-radius: var(--radius-2xl);
  overflow: hidden;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px);
  border: 4px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);

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
      width: 56px;
      height: 56px;
    }
  }
}

// 章节标题
.section-title {
  margin-bottom: 24px;

  h2 {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.6px;
  }
}

// 操作卡片网格
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.action-card {
  background: var(--surface-color);
  border-radius: var(--radius-xl);
  padding: 32px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-spring);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, var(--primary-color), var(--sky-blue-dark));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform var(--transition-base);
  }

  &:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-lg);

    &::before {
      transform: scaleX(1);
    }

    .action-icon {
      transform: scale(1.12) rotate(-5deg);
    }
  }

  h3 {
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 20px 0 8px 0;
    letter-spacing: -0.4px;
  }

  p {
    font-size: 15px;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 500;
  }
}

.action-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-spring);
  box-shadow: var(--shadow-soft);

  svg {
    width: 30px;
    height: 30px;
  }

  &.logout {
    background: linear-gradient(135deg, #FB7185 0%, #F43F5E 100%);
    color: white;
  }

  &.profile {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
    color: white;
  }

  &.security {
    background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
    color: white;
  }
}

// 信息卡片
.info-card {
  background: var(--surface-color);
  border-radius: var(--radius-xl);
  padding: 36px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 20px;
  background: var(--surface-alt);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  border: 1px solid transparent;

  &:hover {
    background: rgba(20, 184, 166, 0.04);
    border-color: rgba(20, 184, 166, 0.1);
    transform: translateX(6px);
  }
}

.info-icon {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.2);

  svg {
    width: 26px;
    height: 26px;
  }
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.info-value {
  font-size: 17px;
  color: var(--text-primary);
  font-weight: 700;
}

// 装饰元素
.decorative-dots {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 400px;
  background-image: radial-gradient(var(--primary-color) 1.5px, transparent 1.5px);
  background-size: 24px 24px;
  opacity: 0.18;
  pointer-events: none;
  z-index: -1;
  filter: blur(0.5px);
}

// 响应式
@media (max-width: 768px) {
  .welcome-card {
    padding: 32px 24px;
  }

  .welcome-content {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }

  .welcome-title {
    font-size: 32px;
  }

  .welcome-subtitle {
    font-size: 15px;
  }

  .user-avatar-large {
    width: 90px;
    height: 90px;
    margin: 0 auto;

    .avatar-placeholder svg {
      width: 44px;
      height: 44px;
    }
  }

  .action-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .section-title h2 {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .welcome-title {
    font-size: 28px;
  }

  .action-card, .info-card {
    padding: 24px 20px;
  }

  .action-icon {
    width: 56px;
    height: 56px;

    svg {
      width: 26px;
      height: 26px;
    }
  }
}
</style>
