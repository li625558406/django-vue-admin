<template>
  <div class="github-trending-container">
    <!-- 简化的筛选栏 -->
    <div class="filter-section">
      <div class="filter-left">
        <h1 class="page-title">GitHub 热榜</h1>
        <p class="page-subtitle">探索今日最热门的开源项目</p>
      </div>
      <div class="filter-right">
        <div class="toggle-buttons">
          <button
            :class="['toggle-btn', { active: selectedSince === 'daily' }]"
            @click="setSince('daily')"
          >
            日榜
          </button>
          <button
            :class="['toggle-btn', { active: selectedSince === 'weekly' }]"
            @click="setSince('weekly')"
          >
            周榜
          </button>
        </div>
        <button @click="fetchTrendingData" class="refresh-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 4v6h-6"/>
            <path d="M1 20v-6h6"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          刷新
        </button>
      </div>
    </div>

    <!-- 数据展示区 -->
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchTrendingData" class="retry-btn">重试</button>
    </div>

    <div v-else class="trending-grid">
      <div
        v-for="item in trendingList"
        :key="item.id"
        class="project-card"
        @click="openProject(item)"
      >
        <!-- 卡片头部：头像 + 标题 -->
        <div class="card-top">
          <img :src="item.avatar || '/default-avatar.png'" class="project-avatar" alt="" />
          <div class="project-header">
            <h3 class="project-title">{{ aiTitle(item) }}</h3>
            <p class="project-name">{{ cleanFullName(item.full_name) }}</p>
          </div>
        </div>

        <!-- 简介 -->
        <p class="project-desc">
          {{ aiSummary(item) }}
        </p>

        <!-- 统计数据 -->
        <div class="project-stats">
          <div class="stat">
            <span class="stat-icon">⭐</span>
            <span class="stat-value">{{ formatNumber(item.stars) }}</span>
          </div>
          <div class="stat">
            <span class="stat-icon">🔥</span>
            <span class="stat-value">+{{ formatNumber(item.current_period_stars) }}</span>
          </div>
          <div class="stat">
            <span class="stat-icon">🍴</span>
            <span class="stat-value">{{ formatNumber(item.forks) }}</span>
          </div>
        </div>

        <!-- 推荐指数 -->
        <div v-if="item.ai_analysis && item.ai_analysis.recommendation_score" class="recommendation">
          <div class="score-bar">
            <div
              class="score-fill"
              :style="{ width: item.ai_analysis.recommendation_score + '%' }"
            ></div>
          </div>
          <span class="score-label">{{ item.ai_analysis.recommendation_score }}% 推荐</span>
        </div>
      </div>

      <div v-if="trendingList.length === 0" class="empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9.172 16.172a4 4 0 0 1-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 1 1-18 0"/>
        </svg>
        <p>暂无数据</p>
      </div>
    </div>

    <!-- 项目详情弹窗 -->
    <el-dialog
      :visible.sync="dialogVisible"
      :show-close="true"
      class="project-dialog"
      :modal-append-to-body="false"
      :append-to-body="true"
      :lock-scroll="true"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
    >
      <div v-if="selectedProject" class="dialog-content">
        <!-- 头部 -->
        <div class="dialog-header">
          <img :src="selectedProject.avatar || '/default-avatar.png'" class="dialog-avatar" alt="" />
          <div class="dialog-title-section">
            <h2 class="dialog-title">{{ aiTitle(selectedProject) }}</h2>
            <p class="dialog-subtitle">{{ cleanFullName(selectedProject.full_name) }}</p>
          </div>
        </div>

        <!-- 统计数据 -->
        <div class="dialog-stats">
          <div class="dialog-stat-item">
            <span class="dialog-stat-icon">⭐</span>
            <div class="dialog-stat-info">
              <span class="dialog-stat-label">Stars</span>
              <span class="dialog-stat-value">{{ formatNumber(selectedProject.stars) }}</span>
            </div>
          </div>
          <div class="dialog-stat-item">
            <span class="dialog-stat-icon">🔥</span>
            <div class="dialog-stat-info">
              <span class="dialog-stat-label">今日新增</span>
              <span class="dialog-stat-value">+{{ formatNumber(selectedProject.current_period_stars) }}</span>
            </div>
          </div>
          <div class="dialog-stat-item">
            <span class="dialog-stat-icon">🍴</span>
            <div class="dialog-stat-info">
              <span class="dialog-stat-label">Forks</span>
              <span class="dialog-stat-value">{{ formatNumber(selectedProject.forks) }}</span>
            </div>
          </div>
        </div>

        <!-- AI 分析内容 -->
        <div v-if="selectedProject.ai_analysis" class="ai-analysis-content">
          <!-- 简介 -->
          <div class="analysis-section">
            <h3 class="section-title">📝 项目简介</h3>
            <p class="section-content">{{ aiSummary(selectedProject) }}</p>
          </div>

          <!-- 主要特点 -->
          <div v-if="selectedProject.ai_analysis.highlights" class="analysis-section">
            <h3 class="section-title">✨ 主要特点</h3>
            <ul class="feature-list">
              <li v-for="(highlight, index) in selectedProject.ai_analysis.highlights" :key="index">
                {{ highlight }}
              </li>
            </ul>
          </div>

          <!-- 技术栈 -->
          <div v-if="selectedProject.ai_analysis.tech_stack" class="analysis-section">
            <h3 class="section-title">🛠️ 技术栈</h3>
            <div class="tech-tags">
              <span
                v-for="(tech, index) in selectedProject.ai_analysis.tech_stack"
                :key="index"
                class="tech-tag"
              >
                {{ tech }}
              </span>
            </div>
          </div>

          <!-- 适用场景 -->
          <div v-if="selectedProject.ai_analysis.use_cases" class="analysis-section">
            <h3 class="section-title">🎯 适用场景</h3>
            <p class="section-content">{{ selectedProject.ai_analysis.use_cases }}</p>
          </div>

          <!-- 推荐指数 -->
          <div v-if="selectedProject.ai_analysis.recommendation_score" class="analysis-section">
            <h3 class="section-title">💎 AI 推荐指数</h3>
            <div class="recommendation-detail">
              <div class="score-bar-large">
                <div
                  class="score-fill-large"
                  :style="{ width: selectedProject.ai_analysis.recommendation_score + '%' }"
                >
                  <span class="score-text">{{ selectedProject.ai_analysis.recommendation_score }}%</span>
                </div>
              </div>
              <p v-if="selectedProject.ai_analysis.recommendation_reason" class="recommendation-reason">
                {{ selectedProject.ai_analysis.recommendation_reason }}
              </p>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="dialog-actions">
          <button @click="closeDialog" class="action-btn secondary">
            关闭
          </button>
          <button @click="openProjectUrl" class="action-btn primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            查看项目
          </button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GithubTrending',
  data() {
    return {
      selectedSince: 'daily', // daily 或 weekly
      limit: 50,
      loading: false,
      error: null,
      trendingList: [],
      dialogVisible: false,
      selectedProject: null
    }
  },
  mounted() {
    this.fetchTrendingData()
  },
  methods: {
    // 获取今天的日期
    getToday() {
      return new Date().toISOString().split('T')[0]
    },

    // 设置榜单类型
    setSince(since) {
      this.selectedSince = since
      this.fetchTrendingData()
    },

    // 清理项目名称中的多余空格
    cleanFullName(fullName) {
      if (!fullName) return ''
      return fullName.replace(/\s*\/\s*/g, '/').trim()
    },

    // 获取AI分析的标题
    aiTitle(item) {
      if (item.ai_analysis && item.ai_analysis.title) {
        return item.ai_analysis.title
      }
      return this.cleanFullName(item.full_name)
    },

    // 获取AI分析的简介
    aiSummary(item) {
      if (item.ai_analysis && item.ai_analysis.summary) {
        return item.ai_analysis.summary
      }
      return item.description || '暂无描述'
    },

    // 打开项目详情弹窗
    openProject(item) {
      this.selectedProject = item
      this.dialogVisible = true
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogVisible = false
    },

    // 打开项目链接
    openProjectUrl() {
      if (this.selectedProject && this.selectedProject.url) {
        window.open(this.selectedProject.url, '_blank')
      }
    },

    // 获取趋势数据
    async fetchTrendingData() {
      this.loading = true
      this.error = null

      try {
        const params = {
          date: this.getToday(), // 默认使用今天
          since: this.selectedSince,
          limit: this.limit
        }

        const response = await axios.get('/api/system/github/trending/', { params })

        if (response.data.data && response.data.data.success) {
          this.trendingList = response.data.data.data
        } else {
          this.error = (response.data.data && response.data.data.message) || '获取数据失败'
        }
      } catch (err) {
        console.error('获取 GitHub Trending 失败:', err)
        this.error = '网络错误，请稍后重试'
      } finally {
        this.loading = false
      }
    },

    // 格式化数字
    formatNumber(num) {
      if (!num) return 0
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k'
      }
      return num
    }
  }
}
</script>

<style lang="scss" scoped>
.github-trending-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  font-family: var(--font-family), -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #FFFFFF 0%, #E0F2FE 50%, #F0FDFA 100%);
  min-height: 100vh;
}

.filter-section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  padding: 24px 28px;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-lg);
  margin-bottom: 36px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  border: 1px solid rgba(255, 255, 255, 0.6);

  .filter-left {
    .page-title {
      font-size: 32px;
      font-weight: 800;
      color: var(--text-primary);
      margin: 0 0 8px 0;
      letter-spacing: -0.8px;
      line-height: 1.2;
    }

    .page-subtitle {
      font-size: 15px;
      color: var(--text-secondary);
      margin: 0;
      font-weight: 600;
    }
  }

  .filter-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .toggle-buttons {
    display: flex;
    gap: 10px;

    .toggle-btn {
      padding: 10px 20px;
      background: white;
      color: var(--text-secondary);
      border: 2px solid var(--border-light);
      border-radius: var(--radius-md);
      cursor: pointer;
      font-size: 14px;
      font-weight: 700;
      transition: all var(--transition-base);

      &:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
        transform: translateY(-1px);
      }

      &.active {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
        color: white;
        border-color: transparent;
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);
      }
    }
  }

  .refresh-btn {
    padding: 10px 24px;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    font-weight: 700;
    transition: all var(--transition-spring);
    display: flex;
    align-items: center;
    gap: 8px;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(20, 184, 166, 0.3);
    }
  }
}

.loading, .error {
  text-align: center;
  padding: 80px 20px;
  font-size: 17px;
  color: var(--text-secondary);
  font-weight: 500;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 20px;
  border: 4px solid var(--border-light);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: var(--danger-color);

  .retry-btn {
    margin-top: 16px;
    padding: 10px 24px;
    background: var(--danger-color);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    font-weight: 700;
    transition: all var(--transition-base);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(239, 68, 68, 0.3);
    }
  }
}

.trending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
  animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.project-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(255, 255, 255, 0.6);
  transition: all var(--transition-spring);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 16px;

  &:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-xl);
    border-color: rgba(20, 184, 166, 0.2);
  }

  .card-top {
    display: flex;
    align-items: flex-start;
    gap: 14px;

    .project-avatar {
      width: 52px;
      height: 52px;
      border-radius: var(--radius-lg);
      object-fit: cover;
      box-shadow: var(--shadow-sm);
      flex-shrink: 0;
    }

    .project-header {
      flex: 1;
      min-width: 0;

      .project-title {
        font-size: 18px;
        font-weight: 800;
        color: var(--primary-color);
        margin: 0 0 4px 0;
        line-height: 1.3;
        letter-spacing: -0.3px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }

      .project-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-tertiary);
        margin: 0;
        font-family: 'Consolas', 'Monaco', monospace;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
  }

  .project-desc {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }

  .project-stats {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;

    .stat {
      display: flex;
      align-items: center;
      gap: 6px;

      .stat-icon {
        font-size: 16px;
      }

      .stat-value {
        font-size: 14px;
        font-weight: 700;
        color: var(--text-primary);
      }
    }
  }

  .recommendation {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border-light);

    .score-bar {
      flex: 1;
      height: 8px;
      background: var(--surface-alt);
      border-radius: var(--radius-sm);
      overflow: hidden;

      .score-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--mint-green) 100%);
        border-radius: var(--radius-sm);
        transition: width 0.6s ease;
      }
    }

    .score-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--primary-color);
      white-space: nowrap;
    }
  }
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
  font-size: 16px;
  font-weight: 500;

  svg {
    width: 64px;
    height: 64px;
    margin: 0 auto 16px;
    opacity: 0.5;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;

    .filter-right {
      flex-direction: column;
      width: 100%;

      .toggle-buttons {
        width: 100%;
        justify-content: center;
      }

      .refresh-btn {
        width: 100%;
        justify-content: center;
      }
    }
  }

  .trending-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .github-trending-container {
    padding: 16px;
  }

  .filter-section {
    padding: 20px;

    .filter-left .page-title {
      font-size: 24px;
    }
  }
}

// 弹窗样式
::v-deep .project-dialog {
  .el-dialog {
    border-radius: var(--radius-2xl) !important;
    max-width: 700px;
    width: 90%;
    overflow: hidden !important;
  }

  .el-dialog__header {
    padding: 0;
  }

  .el-dialog__body {
    padding: 0;
  }

  .el-dialog__headerbtn {
    top: 20px;
    right: 20px;
    z-index: 10;
    font-size: 24px;
  }
}

.dialog-content {
  padding: 32px;
  max-height: 70vh;
  overflow-y: auto;
  background: white;

.dialog-header {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 2px solid var(--border-light);

  .dialog-avatar {
    width: 80px;
    height: 80px;
    border-radius: var(--radius-xl);
    object-fit: cover;
    box-shadow: var(--shadow-md);
    flex-shrink: 0;
  }

  .dialog-title-section {
    flex: 1;

    .dialog-title {
      font-size: 24px;
      font-weight: 800;
      color: var(--primary-color);
      margin: 0 0 8px 0;
      line-height: 1.3;
      letter-spacing: -0.5px;
    }

    .dialog-subtitle {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-tertiary);
      margin: 0;
      font-family: 'Consolas', 'Monaco', monospace;
    }
  }
}

.dialog-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 28px;

  .dialog-stat-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: var(--surface-alt);
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);

    &:hover {
      background: rgba(20, 184, 166, 0.08);
      transform: translateY(-2px);
    }

    .dialog-stat-icon {
      font-size: 28px;
    }

    .dialog-stat-info {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .dialog-stat-label {
        font-size: 12px;
        color: var(--text-secondary);
        font-weight: 600;
      }

      .dialog-stat-value {
        font-size: 18px;
        font-weight: 800;
        color: var(--text-primary);
      }
    }
  }
}

.ai-analysis-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.analysis-section {
  .section-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    letter-spacing: -0.3px;
  }

  .section-content {
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.7;
    margin: 0;
    font-weight: 500;
  }
}

.feature-list, .use-case-list {
  margin: 0;
  padding-left: 20px;

  li {
    color: var(--text-secondary);
    margin-bottom: 10px;
    font-weight: 500;
    line-height: 1.6;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;

  .tech-tag {
    padding: 8px 16px;
    background: linear-gradient(135deg, var(--mint-green) 0%, var(--sky-blue) 100%);
    color: white;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(20, 184, 166, 0.2);
  }
}

.recommendation-detail {
  .score-bar-large {
    position: relative;
    width: 100%;
    height: 48px;
    background: var(--surface-alt);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.08);
    margin-bottom: 16px;

    .score-fill-large {
      height: 100%;
      background: linear-gradient(90deg, var(--primary-color) 0%, var(--mint-green) 100%);
      border-radius: var(--radius-lg);
      transition: width 0.8s ease;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 16px;

      .score-text {
        font-size: 18px;
        font-weight: 800;
        color: white;
      }
    }
  }

  .recommendation-reason {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
    font-weight: 500;
    font-style: italic;
  }
}

.dialog-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 2px solid var(--border-light);

  .action-btn {
    flex: 1;
    padding: 12px 24px;
    border: none;
    border-radius: var(--radius-lg);
    font-size: 15px;
    font-weight: 700;
    font-family: var(--font-family), sans-serif;
    cursor: pointer;
    transition: all var(--transition-spring);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    svg {
      flex-shrink: 0;
    }

    &.secondary {
      background: var(--surface-alt);
      color: var(--text-secondary);

      &:hover {
        background: var(--border-color);
        transform: translateY(-2px);
      }
    }

    &.primary {
      background: linear-gradient(135deg, var(--primary-color) 0%, var(--sky-blue-dark) 100%);
      color: white;
      box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(20, 184, 166, 0.35);
      }
    }
  }
}

// 弹窗响应式
@media (max-width: 768px) {
  ::v-deep .project-dialog .el-dialog {
    width: 95%;
    margin: 0 auto;
  }

  .dialog-content {
    padding: 24px 20px;
  }

  .dialog-header {
    flex-direction: column;
    align-items: center;
    text-align: center;

    .dialog-avatar {
      width: 64px;
      height: 64px;
    }
  }

  .dialog-stats {
    grid-template-columns: 1fr;
  }

  .dialog-actions {
    flex-direction: column;
  }
}
</style>
