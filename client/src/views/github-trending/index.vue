<template>
  <div class="github-trending-container">
    <!-- 头部筛选区 -->
    <div class="filter-section">
      <div class="filter-item">
        <label>日期：</label>
        <input
          v-model="selectedDate"
          type="date"
          :max="today"
          @change="fetchTrendingData"
        />
      </div>

      <div class="filter-item">
        <label>编程语言：</label>
        <select v-model="selectedLanguage" @change="fetchTrendingData">
          <option value="">全部</option>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="go">Go</option>
          <option value="rust">Rust</option>
          <option value="java">Java</option>
          <option value="typescript">TypeScript</option>
        </select>
      </div>

      <div class="filter-item">
        <label>显示数量：</label>
        <select v-model="limit" @change="fetchTrendingData">
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>

      <button @click="fetchTrendingData" class="refresh-btn">刷新</button>
    </div>

    <!-- 数据展示区 -->
    <div v-if="loading" class="loading">
      加载中...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="trending-list">
      <div
        v-for="item in trendingList"
        :key="item.id"
        class="trending-card"
      >
        <div class="card-header">
          <div class="project-info">
            <img :src="item.avatar || '/default-avatar.png'" class="avatar" />
            <div>
              <h3 class="project-name">{{ item.full_name }}</h3>
              <p class="project-description">{{ item.description || '暂无描述' }}</p>
            </div>
          </div>
          <div class="stats">
            <div class="stat-item">
              <span class="stat-label">⭐</span>
              <span class="stat-value">{{ formatNumber(item.stars) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">🔥</span>
              <span class="stat-value">+{{ formatNumber(item.current_period_stars) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">🍴</span>
              <span class="stat-value">{{ formatNumber(item.forks) }}</span>
            </div>
          </div>
        </div>

        <!-- AI 分析结果 -->
        <div v-if="item.ai_analysis && Object.keys(item.ai_analysis).length > 0" class="ai-analysis">
          <div class="analysis-section">
            <h4>🤖 AI 分析</h4>
            <div class="analysis-content">
              <div class="analysis-item">
                <strong>核心功能：</strong>
                <p>{{ item.ai_analysis.core_features || '暂无' }}</p>
              </div>

              <div class="analysis-item">
                <strong>技术栈：</strong>
                <div class="tags">
                  <span
                    v-for="(tech, idx) in (item.ai_analysis.tech_stack || [])"
                    :key="idx"
                    class="tag tech-tag"
                  >
                    {{ tech }}
                  </span>
                </div>
              </div>

              <div class="analysis-item">
                <strong>应用场景：</strong>
                <p>{{ item.ai_analysis.use_cases || '暂无' }}</p>
              </div>

              <div class="analysis-item">
                <strong>亮点特色：</strong>
                <ul>
                  <li v-for="(highlight, idx) in (item.ai_analysis.highlights || [])" :key="idx">
                    {{ highlight }}
                  </li>
                </ul>
              </div>

              <div class="analysis-item score-section">
                <strong>推荐指数：</strong>
                <div class="score-bar">
                  <div
                    class="score-fill"
                    :style="{ width: (item.ai_analysis.recommendation_score || 0) + '%' }"
                  ></div>
                  <span class="score-text">{{ item.ai_analysis.recommendation_score || 0 }}/100</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <div class="language">
            <span
              class="language-dot"
              :style="{ backgroundColor: getLanguageColor(item.language) }"
            ></span>
            {{ item.language || 'Unknown' }}
          </div>
          <a :href="item.url" target="_blank" class="view-link">查看项目 →</a>
        </div>
      </div>

      <div v-if="trendingList.length === 0" class="empty">
        暂无数据
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GithubTrending',
  data() {
    return {
      selectedDate: this.getToday(),
      selectedLanguage: '',
      limit: 50,
      loading: false,
      error: null,
      trendingList: [],
      today: this.getToday()
    }
  },
  mounted() {
    this.fetchTrendingData()
  },
  methods: {
    getToday() {
      return new Date().toISOString().split('T')[0]
    },

    async fetchTrendingData() {
      this.loading = true
      this.error = null

      try {
        const params = {
          date: this.selectedDate,
          language: this.selectedLanguage,
          limit: this.limit
        }

        const response = await axios.get('/api/github/trending/', { params })

        if (response.data.success) {
          this.trendingList = response.data.data
        } else {
          this.error = response.data.message || '获取数据失败'
        }
      } catch (err) {
        console.error('获取 GitHub Trending 失败:', err)
        this.error = '网络错误，请稍后重试'
      } finally {
        this.loading = false
      }
    },

    formatNumber(num) {
      if (!num) return 0
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k'
      }
      return num
    },

    getLanguageColor(language) {
      const colors = {
        'Python': '#3572A5',
        'JavaScript': '#f1e05a',
        'Go': '#00ADD8',
        'Rust': '#dea584',
        'Java': '#b07219',
        'TypeScript': '#2b7489',
      }
      return colors[language] || '#cccccc'
    }
  }
}
</script>

<style lang="scss" scoped>
.github-trending-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
  min-height: 100vh;
}

.filter-section {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  margin-bottom: 30px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;

  .filter-item {
    display: flex;
    align-items: center;
    gap: 10px;

    label {
      font-weight: 600;
      color: var(--text-primary);
    }

    input, select {
      padding: 8px 12px;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      font-size: 14px;
      outline: none;
      transition: all 0.3s;

      &:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 209, 197, 0.1);
      }
    }
  }

  .refresh-btn {
    padding: 8px 20px;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;

    &:hover {
      background: var(--primary-dark);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(79, 209, 197, 0.3);
    }
  }
}

.loading, .error {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: var(--text-secondary);
}

.error {
  color: #e53e3e;
}

.trending-list {
  display: grid;
  gap: 20px;
}

.trending-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-lg);
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  }

  .card-header {
    margin-bottom: 20px;

    .project-info {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;

      .avatar {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        object-fit: cover;
      }

      .project-name {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 8px 0;
      }

      .project-description {
        color: var(--text-secondary);
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
      }
    }

    .stats {
      display: flex;
      gap: 24px;

      .stat-item {
        display: flex;
        align-items: center;
        gap: 6px;

        .stat-label {
          font-size: 18px;
        }

        .stat-value {
          font-weight: 700;
          color: var(--text-primary);
        }
      }
    }
  }

  .ai-analysis {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;

    .analysis-section h4 {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-primary);
      margin: 0 0 16px 0;
    }

    .analysis-content {
      .analysis-item {
        margin-bottom: 16px;

        &:last-child {
          margin-bottom: 0;
        }

        strong {
          display: block;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 8px;
        }

        p {
          margin: 0;
          color: var(--text-secondary);
          line-height: 1.6;
        }

        ul {
          margin: 0;
          padding-left: 20px;

          li {
            color: var(--text-secondary);
            margin-bottom: 6px;
          }
        }

        .tags {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;

          .tag {
            padding: 4px 12px;
            background: var(--primary-color);
            color: white;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 600;
          }

          .tech-tag {
            background: var(--primary-dark);
          }
        }

        .score-bar {
          position: relative;
          width: 100%;
          height: 24px;
          background: white;
          border-radius: 12px;
          overflow: hidden;
          box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);

          .score-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-light) 100%);
            transition: width 0.5s ease;
          }

          .score-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: 700;
            color: var(--text-primary);
          }
        }
      }
    }
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16px;
    border-top: 1px solid var(--border-color);

    .language {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      color: var(--text-primary);

      .language-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
      }
    }

    .view-link {
      color: var(--primary-color);
      text-decoration: none;
      font-weight: 600;
      transition: all 0.3s;

      &:hover {
        color: var(--primary-dark);
        transform: translateX(4px);
      }
    }
  }
}

.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
  font-size: 16px;
}
</style>
