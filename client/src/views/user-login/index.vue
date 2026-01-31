<template>
  <div class="modern-login-container">
    <!-- 背景装饰 -->
    <div class="background-elements">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="grid-pattern"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- Logo 区域 -->
      <div class="logo-section">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
            <polyline points="10 17 15 12 10 7"/>
            <line x1="15" y1="12" x2="3" y2="12"/>
          </svg>
        </div>
        <h1 class="title">欢迎回来</h1>
        <p class="subtitle">登录以继续您的旅程</p>
      </div>

      <!-- 登录表单 -->
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.native.prevent="handleLogin"
      >
        <!-- 账号输入 -->
        <div class="form-group">
          <label class="form-label">
            <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            账号
          </label>
          <el-input
            v-model="loginForm.account"
            placeholder="用户名 / 手机号 / 邮箱"
            class="modern-input"
            @keyup.enter.native="handleLogin"
          >
            <i slot="prefix" class="el-icon-user input-icon"></i>
          </el-input>
        </div>

        <!-- 密码输入 -->
        <div class="form-group">
          <label class="form-label">
            <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            密码
          </label>
          <el-input
            v-model="loginForm.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="请输入密码"
            class="modern-input"
            @keyup.enter.native="handleLogin"
          >
            <i slot="prefix" class="el-icon-lock input-icon"></i>
            <i
              slot="suffix"
              :class="showPassword ? 'el-icon-eye-open' : 'el-icon-eye'"
              class="password-toggle"
              @click="togglePassword"
            ></i>
          </el-input>
        </div>

        <!-- 记住我 & 忘记密码 -->
        <div class="form-options">
          <el-checkbox v-model="loginForm.remember" class="modern-checkbox">
            <span>记住我</span>
          </el-checkbox>
          <router-link to="/forgot-password" class="forgot-link">
            忘记密码？
          </router-link>
        </div>

        <!-- 登录按钮 -->
        <el-button
          type="primary"
          :loading="loading"
          class="login-btn"
          native-type="submit"
        >
          <span v-if="!loading">登录</span>
          <span v-else>登录中...</span>
        </el-button>

        <!-- 错误提示 -->
        <transition name="slide-down">
          <div v-if="errorMessage" class="error-message">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ errorMessage }}
          </div>
        </transition>
      </el-form>

      <!-- 注册链接 -->
      <div class="register-section">
        <p class="register-text">
          还没有账户？
          <router-link to="/register" class="register-link">
            立即注册
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    const validateAccount = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入账号'))
      } else if (value.length < 3) {
        callback(new Error('账号长度至少3位'))
      } else {
        callback()
      }
    }

    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码长度至少6位'))
      } else {
        callback()
      }
    }

    return {
      loginForm: {
        account: '',
        password: '',
        remember: false
      },
      loginRules: {
        account: [{ required: true, trigger: 'blur', validator: validateAccount }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      showPassword: false,
      errorMessage: '',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    async handleLogin() {
      this.errorMessage = ''

      try {
        const valid = await this.$refs.loginForm.validate()
        if (!valid) return

        this.loading = true

        await this.$store.dispatch('user/login', {
          username: this.loginForm.account,
          password: this.loginForm.password
        })

        if (this.loginForm.remember) {
          localStorage.setItem('rememberAccount', this.loginForm.account)
        } else {
          localStorage.removeItem('rememberAccount')
        }

        await this.$store.dispatch('user/getInfo')

        this.$message.success('登录成功！')

        this.$router.push({ path: this.redirect || '/user/dashboard' })

      } catch (error) {
        console.error('登录失败:', error)
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || '登录失败，请检查账号密码'
        } else {
          this.errorMessage = '登录失败，请稍后重试'
        }
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    const rememberedAccount = localStorage.getItem('rememberAccount')
    if (rememberedAccount) {
      this.loginForm.account = rememberedAccount
      this.loginForm.remember = true
    }
  }
}
</script>

<style lang="scss" scoped>
.modern-login-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
  font-family: 'Outfit', sans-serif;
}

// 背景装饰元素
.background-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-color) 100%);
  opacity: 0.08;
  animation: float 20s ease-in-out infinite;

  &.circle-1 {
    width: 500px;
    height: 500px;
    top: -200px;
    right: -150px;
    animation-delay: 0s;
  }

  &.circle-2 {
    width: 400px;
    height: 400px;
    bottom: -150px;
    left: -100px;
    animation-delay: -7s;
  }

  &.circle-3 {
    width: 300px;
    height: 300px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation-delay: -14s;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-30px) scale(1.05);
  }
}

.floating-shape {
  position: absolute;
  background: var(--primary-color);
  opacity: 0.03;
  border-radius: var(--radius-lg);
  animation: floatRotate 25s ease-in-out infinite;

  &.shape-1 {
    width: 120px;
    height: 120px;
    top: 15%;
    left: 10%;
    animation-delay: -5s;
  }

  &.shape-2 {
    width: 80px;
    height: 80px;
    bottom: 20%;
    right: 15%;
    animation-delay: -12s;
  }
}

@keyframes floatRotate {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-40px) rotate(180deg);
  }
}

.grid-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(var(--border-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
  background-size: 60px 60px;
  opacity: 0.3;
}

// 登录卡片
.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  margin: 20px;
  padding: 48px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(255, 255, 255, 0.8);
  animation: cardAppear 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

// Logo 区域
.logo-section {
  text-align: center;
  margin-bottom: 40px;
  animation: fadeInDown 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s backwards;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.logo-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 20px rgba(79, 209, 197, 0.3);
  transition: all 0.3s ease;

  svg {
    width: 32px;
    height: 32px;
  }

  &:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 12px 28px rgba(79, 209, 197, 0.4);
  }
}

.title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 15px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

// 表单
.login-form {
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-group {
  margin-bottom: 24px;

  &:last-of-type {
    margin-bottom: 20px;
  }
}

.form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;

  .label-icon {
    width: 16px;
    height: 16px;
    color: var(--primary-color);
  }
}

::v-deep .modern-input {
  .el-input__inner {
    height: 50px;
    padding: 0 45px;
    border: 2px solid var(--border-color);
    border-radius: var(--radius-md);
    background: white;
    font-size: 15px;
    color: var(--text-primary);
    font-family: 'Outfit', sans-serif;
    transition: all 0.3s ease;

    &::placeholder {
      color: #CBD5E0;
      font-weight: 400;
    }

    &:focus {
      border-color: var(--primary-color);
      box-shadow: 0 0 0 3px rgba(79, 209, 197, 0.1);
    }

    &:hover {
      border-color: #CBD5E0;
    }
  }

  .input-icon {
    left: 16px;
    color: var(--text-secondary);
    font-size: 18px;
  }

  .password-toggle {
    right: 16px;
    color: var(--text-secondary);
    font-size: 18px;
    cursor: pointer;
    transition: color 0.3s ease;

    &:hover {
      color: var(--primary-color);
    }
  }
}

::v-deep .el-form-item__error {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 6px;
  font-size: 13px;
  color: #FC8181;
  font-weight: 500;
}

// 表单选项
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

::v-deep .modern-checkbox {
  .el-checkbox__label {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 500;
  }

  .el-checkbox__input.is-checked + .el-checkbox__label {
    color: var(--primary-color);
  }

  .el-checkbox__inner {
    border-radius: 4px;
    border-color: var(--border-color);

    &:hover {
      border-color: var(--primary-color);
    }
  }

  .el-checkbox__input.is-checked .el-checkbox__inner {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
  }
}

.forgot-link {
  font-size: 14px;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;

  &:hover {
    color: var(--primary-dark);
    text-decoration: underline;
  }
}

// 登录按钮
.login-btn {
  width: 100%;
  height: 52px;
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Outfit', sans-serif;
  box-shadow: 0 4px 12px rgba(79, 209, 197, 0.35);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  margin-bottom: 16px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79, 209, 197, 0.45);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &.is-loading {
    opacity: 0.8;
  }

  span {
    font-weight: 600;
  }
}

// 错误消息
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #FED7D7;
  border: 1px solid #FC8181;
  border-radius: var(--radius-md);
  color: #C53030;
  font-size: 14px;
  font-weight: 500;

  svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
  }
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

// 注册区域
.register-section {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
  text-align: center;
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.3s backwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.register-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.register-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: all 0.3s ease;

  &:hover {
    color: var(--primary-dark);
    text-decoration: underline;
  }
}

// 响应式
@media (max-width: 576px) {
  .login-card {
    margin: 16px;
    padding: 32px 24px;
    border-radius: var(--radius-lg);
  }

  .title {
    font-size: 26px;
  }

  .logo-icon {
    width: 56px;
    height: 56px;

    svg {
      width: 28px;
      height: 28px;
    }
  }
}
</style>
