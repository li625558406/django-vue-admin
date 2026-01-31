<template>
  <div class="modern-user-layout">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-container">
        <!-- Logo -->
        <div class="navbar-brand">
          <router-link to="/user/dashboard" class="brand-link">
            <div class="brand-logo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
            </div>
            <span class="brand-name">用户中心</span>
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <div class="navbar-menu">
          <router-link to="/user/dashboard" class="nav-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="7" height="7"/>
              <rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/>
              <rect x="3" y="14" width="7" height="7"/>
            </svg>
            <span>仪表板</span>
          </router-link>
          <router-link to="/user/profile" class="nav-link">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <span>个人资料</span>
          </router-link>
        </div>

        <!-- 用户操作 -->
        <div class="navbar-actions">
          <div class="user-dropdown" @click="toggleUserMenu">
            <div class="user-avatar">
              <img v-if="avatar" :src="avatar" alt="用户头像" />
              <div v-else class="avatar-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
            </div>
            <div class="user-info">
              <span class="user-name">{{ displayName }}</span>
              <svg class="dropdown-arrow" :class="{ 'active': showUserMenu }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>

            <!-- 下拉菜单 -->
            <transition name="dropdown-slide">
              <div v-if="showUserMenu" class="dropdown-menu" @click.stop>
                <div class="dropdown-item" @click="handleLogout">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                    <polyline points="16 17 21 12 16 7"/>
                    <line x1="21" y1="12" x2="9" y2="12"/>
                  </svg>
                  <span>退出登录</span>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="main-content">
      <router-view :key="key" />
    </main>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'UserLayout',
  data() {
    return {
      showUserMenu: false
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'username',
      'avatar'
    ]),
    displayName() {
      return this.name || this.username || '用户'
    },
    key() {
      return this.$route.path
    }
  },
  methods: {
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
    },
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
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    handleClickOutside(event) {
      if (!event.target.closest('.user-dropdown')) {
        this.showUserMenu = false
      }
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
    },
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
.modern-user-layout {
  min-height: 100vh;
  background: var(--bg-color);
  font-family: 'Outfit', sans-serif;
}

// 导航栏
.navbar {
  background: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  .brand-link {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-1px);
    }
  }

  .brand-logo {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 4px 12px rgba(79, 209, 197, 0.25);
    transition: all 0.3s ease;

    svg {
      width: 22px;
      height: 22px;
    }

    .brand-link:hover & {
      box-shadow: 0 6px 16px rgba(79, 209, 197, 0.35);
    }
  }

  .brand-name {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.3px;
  }
}

.navbar-menu {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
  position: relative;

  .nav-icon {
    width: 18px;
    height: 18px;
  }

  &:hover {
    background: rgba(79, 209, 197, 0.08);
    color: var(--primary-color);
  }

  &.router-link-active {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    color: white;
    box-shadow: 0 2px 8px rgba(79, 209, 197, 0.3);

    svg {
      stroke: white;
    }
  }
}

.navbar-actions {
  display: flex;
  align-items: center;
}

.user-dropdown {
  position: relative;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(79, 209, 197, 0.06);
  }
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  flex-shrink: 0;

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
      width: 22px;
      height: 22px;
    }
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 12px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.dropdown-arrow {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
  transition: transform 0.3s ease;

  &.active {
    transform: rotate(180deg);
  }
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 160px;
  background: var(--surface-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  padding: 8px;
  z-index: 10;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;

  svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
    color: var(--text-secondary);
  }

  &:hover {
    background: rgba(79, 209, 197, 0.08);
    color: var(--primary-color);

    svg {
      color: var(--primary-color);
    }
  }
}

.dropdown-slide-enter-active, .dropdown-slide-leave-active {
  transition: all 0.2s ease;
}

.dropdown-slide-enter, .dropdown-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

// 主内容
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px;
  min-height: calc(100vh - 70px);
}

// 响应式
@media (max-width: 768px) {
  .navbar-container {
    padding: 0 16px;
    height: 64px;
  }

  .navbar-menu {
    display: none;
  }

  .main-content {
    padding: 20px 16px;
  }

  .navbar-brand .brand-name {
    display: none;
  }

  .user-info {
    display: none;
  }

  .user-dropdown {
    padding: 4px;
  }
}
</style>
