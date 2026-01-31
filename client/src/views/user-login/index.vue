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
  background: linear-gradient(135deg, #FFFFFF 0%, #E0F2FE 50%, #F0FDFA 100%);
  font-family: var(--font-family), sans-serif;
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
  background: linear-gradient(135deg, var(--mint-green) 0%, var(--sky-blue) 100%);
  opacity: 0.12;
  animation: float 25s ease-in-out infinite;
  filter: blur(60px);

  &.circle-1 {
    width: 600px;
    height: 600px;
    top: -250px;
    right: -150px;
    animation-delay: 0s;
  }

  &.circle-2 {
    width: 500px;
    height: 500px;
    bottom: -200px;
    left: -100px;
    animation-delay: -8s;
  }

  &.circle-3 {
    width: 350px;
    height: 350px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation-delay: -16s;
    opacity: 0.08;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-40px) scale(1.08);
  }
}

.floating-shape {
  position: absolute;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue) 100%);
  opacity: 0.04;
  border-radius: var(--radius-lg);
  animation: floatRotate 30s ease-in-out infinite;
  filter: blur(40px);

  &.shape-1 {
    width: 150px;
    height: 150px;
    top: 12%;
    left: 8%;
    animation-delay: -6s;
  }

  &.shape-2 {
    width: 100px;
    height: 100px;
    bottom: 15%;
    right: 12%;
    animation-delay: -15s;
  }
}

@keyframes floatRotate {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-50px) rotate(120deg);
  }
}

.grid-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(var(--border-light) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-light) 1px, transparent 1px);
  background-size: 80px 80px;
  opacity: 0.4;
}

// 登录卡片
.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 460px;
  margin: 20px;
  padding: 56px 48px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(24px);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl),
              0 0 0 1px rgba(255, 255, 255, 0.6),
              inset 0 1px 0 rgba(255, 255, 255, 0.8);
  animation: cardAppear 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

// Logo 区域
.logo-section {
  text-align: center;
  margin-bottom: 48px;
  animation: fadeInDown 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.12s backwards;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.logo-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 12px 32px rgba(20, 184, 166, 0.25),
              0 4px 12px rgba(20, 184, 166, 0.15);
  transition: all var(--transition-spring);

  svg {
    width: 36px;
    height: 36px;
  }

  &:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 16px 40px rgba(20, 184, 166, 0.35),
                0 6px 16px rgba(20, 184, 166, 0.2);
  }
}

.title {
  font-size: 34px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  letter-spacing: -0.8px;
  line-height: 1.2;
}

.subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

// 表单
.login-form {
  animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-group {
  margin-bottom: 28px;

  &:last-of-type {
    margin-bottom: 24px;
  }
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;

  .label-icon {
    width: 18px;
    height: 18px;
    color: var(--primary-color);
  }
}

::v-deep .modern-input {
  .el-input__inner {
    height: 54px;
    padding: 0 48px;
    border: 2px solid var(--border-light);
    border-radius: var(--radius-md);
    background: white;
    font-size: 15px;
    color: var(--text-primary);
    font-family: var(--font-family), sans-serif;
    transition: all var(--transition-base);
    box-shadow: 0 1px 3px rgba(148, 163, 184, 0.05);

    &::placeholder {
      color: var(--text-tertiary);
      font-weight: 500;
    }

    &:focus {
      border-color: var(--primary-color);
      box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.08),
                  0 2px 8px rgba(148, 163, 184, 0.08);
      background: rgba(255, 255, 255, 1);
    }

    &:hover {
      border-color: var(--border-color);
    }
  }

  .input-icon {
    left: 18px;
    color: var(--text-tertiary);
    font-size: 18px;
  }

  .password-toggle {
    right: 18px;
    color: var(--text-tertiary);
    font-size: 18px;
    cursor: pointer;
    transition: color var(--transition-fast);

    &:hover {
      color: var(--primary-color);
    }
  }
}

::v-deep .el-form-item__error {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 8px;
  font-size: 13px;
  color: var(--danger-color);
  font-weight: 600;
}

// 表单选项
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

::v-deep .modern-checkbox {
  .el-checkbox__label {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 600;
  }

  .el-checkbox__input.is-checked + .el-checkbox__label {
    color: var(--primary-color);
  }

  .el-checkbox__inner {
    border-radius: 6px;
    border-color: var(--border-color);
    transition: all var(--transition-fast);

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
  font-weight: 700;
  transition: all var(--transition-fast);

  &:hover {
    color: var(--primary-dark);
    text-decoration: underline;
  }
}

// 登录按钮
.login-btn {
  width: 100%;
  height: 54px;
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
  color: white;
  font-size: 16px;
  font-weight: 700;
  font-family: var(--font-family), sans-serif;
  box-shadow: 0 6px 16px rgba(20, 184, 166, 0.3),
              0 2px 6px rgba(20, 184, 166, 0.15);
  transition: all var(--transition-spring);
  margin-bottom: 20px;
  letter-spacing: 0.3px;

  &:hover:not(:disabled) {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(20, 184, 166, 0.4),
                0 4px 10px rgba(20, 184, 166, 0.2);
  }

  &:active:not(:disabled) {
    transform: translateY(-1px);
  }

  &.is-loading {
    opacity: 0.85;
  }

  span {
    font-weight: 700;
  }
}

// 错误消息
.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
  border: 1px solid var(--danger-color);
  border-radius: var(--radius-md);
  color: #DC2626;
  font-size: 14px;
  font-weight: 600;

  svg {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
  }
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all var(--transition-base);
}

.slide-down-enter, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

// 注册区域
.register-section {
  margin-top: 32px;
  padding-top: 28px;
  border-top: 1px solid var(--border-light);
  text-align: center;
  animation: fadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s backwards;
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
  font-size: 15px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

.register-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 700;
  margin-left: 6px;
  transition: all var(--transition-fast);

  &:hover {
    color: var(--primary-dark);
    text-decoration: underline;
  }
}

// 响应式
@media (max-width: 576px) {
  .login-card {
    margin: 16px;
    padding: 40px 28px;
    border-radius: var(--radius-xl);
  }

  .title {
    font-size: 28px;
  }

  .subtitle {
    font-size: 15px;
  }

  .logo-icon {
    width: 64px;
    height: 64px;

    svg {
      width: 32px;
      height: 32px;
    }
  }

  .form-group {
    margin-bottom: 24px;
  }
}
</style>
