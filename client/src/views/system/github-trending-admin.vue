<template>
  <div class="app-container">
    <div class="github-trending-admin">
      <!-- 页面头部 -->
      <div class="page-header">
        <h2>GitHub 热门项目管理</h2>
        <div class="header-actions">
          <el-button type="primary" icon="el-icon-refresh" @click="fetchData" size="small">
            刷新数据
          </el-button>
          <el-button type="success" icon="el-icon-download" @click="triggerTask" size="small" :loading="taskLoading">
            {{ taskLoading ? '任务执行中...' : '手动触发任务' }}
          </el-button>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-date-picker
          v-model="filterDate"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
          @change="handleFilterChange"
        />
        <el-select v-model="filterLanguage" placeholder="编程语言" clearable @change="handleFilterChange">
          <el-option label="全部" value="" />
          <el-option label="Python" value="Python" />
          <el-option label="JavaScript" value="JavaScript" />
          <el-option label="Go" value="Go" />
          <el-option label="Rust" value="Rust" />
          <el-option label="Java" value="Java" />
          <el-option label="TypeScript" value="TypeScript" />
        </el-select>
      </div>

      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />

        <el-table-column label="项目信息" width="300">
          <template #default="{ row }">
            <div class="project-info">
              <img :src="row.avatar" class="project-avatar" />
              <div>
                <div class="project-name">{{ row.full_name }}</div>
                <div class="project-url">
                  <a :href="row.url" target="_blank">{{ row.url }}</a>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="description" label="项目描述" show-overflow-tooltip />

        <el-table-column label="编程语言" width="120">
          <template #default="{ row }">
            <el-tag :type="getLanguageType(row.language)" size="small">
              {{ row.language || 'Unknown' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="stars" label="Stars" width="100" sortable>
          <template #default="{ row }">
            {{ formatNumber(row.stars) }}
          </template>
        </el-table-column>

        <el-table-column prop="forks" label="Forks" width="100" sortable>
          <template #default="{ row }">
            {{ formatNumber(row.forks) }}
          </template>
        </el-table-column>

        <el-table-column prop="current_period_stars" label="今日新增" width="100" sortable>
          <template #default="{ row }">
            <span style="color: #67C23A; font-weight: bold;">
              +{{ formatNumber(row.current_period_stars) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="collection_date" label="采集日期" width="120" sortable />

        <el-table-column label="AI 分析" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.ai_analysis && Object.keys(row.ai_analysis).length > 0" type="success" size="small">
              已分析
            </el-tag>
            <el-tag v-else type="info" size="small">
              未分析
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="viewDetail(row)">
              查看详情
            </el-button>
            <el-button type="text" size="small" @click="openProjectUrl(row.url)">
              打开项目
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="项目详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <div class="detail-section">
          <h3>基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="项目名称">{{ currentItem.full_name }}</el-descriptions-item>
            <el-descriptions-item label="编程语言">{{ currentItem.language }}</el-descriptions-item>
            <el-descriptions-item label="Stars">{{ currentItem.stars }}</el-descriptions-item>
            <el-descriptions-item label="Forks">{{ currentItem.forks }}</el-descriptions-item>
            <el-descriptions-item label="今日新增">
              <span style="color: #67C23A;">+{{ currentItem.current_period_stars }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="采集日期">{{ currentItem.collection_date }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div v-if="currentItem.ai_analysis" class="detail-section">
          <h3>AI 分析结果</h3>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="核心功能">
              {{ currentItem.ai_analysis.core_features || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="技术栈">
              <el-tag
                v-for="(tech, idx) in (currentItem.ai_analysis.tech_stack || [])"
                :key="idx"
                size="small"
                style="margin-right: 5px;"
              >
                {{ tech }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="应用场景">
              {{ currentItem.ai_analysis.use_cases || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="亮点特色">
              <ul>
                <li v-for="(highlight, idx) in (currentItem.ai_analysis.highlights || [])" :key="idx">
                  {{ highlight }}
                </li>
              </ul>
            </el-descriptions-item>
            <el-descriptions-item label="推荐指数">
              <el-progress
                :percentage="currentItem.ai_analysis.recommendation_score || 0"
                :color="getScoreColor(currentItem.ai_analysis.recommendation_score)"
              />
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GithubTrendingAdmin',
  data() {
    return {
      loading: false,
      taskLoading: false,
      tableData: [],
      filterDate: this.getToday(),
      filterLanguage: '',
      currentPage: 1,
      pageSize: 20,
      total: 0,
      detailDialogVisible: false,
      currentItem: null
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    getToday() {
      return new Date().toISOString().split('T')[0]
    },

    async fetchData() {
      this.loading = true
      try {
        const params = {
          date: this.filterDate,
          language: this.filterLanguage,
          limit: this.pageSize,
          offset: (this.currentPage - 1) * this.pageSize
        }

        const response = await axios.get('/api/github/trending/', { params })

        if (response.data.success) {
          this.tableData = response.data.data
          // 这里简单处理，实际应该从后端返回总数
          this.total = response.data.data.length
        } else {
          this.$message.error(response.data.message || '获取数据失败')
        }
      } catch (error) {
        console.error('获取数据失败:', error)
        this.$message.error('网络错误，请稍后重试')
      } finally {
        this.loading = false
      }
    },

    async triggerTask() {
      this.$confirm('确定要手动触发 GitHub Trending 数据获取任务吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        this.taskLoading = true
        try {
          const response = await axios.post('/api/github/trending/trigger/')

          if (response.data.success) {
            this.$message.success('任务已触发，请稍后查看数据')
            // 3秒后自动刷新数据
            setTimeout(() => {
              this.fetchData()
            }, 3000)
          } else {
            this.$message.error(response.data.message || '任务触发失败')
          }
        } catch (error) {
          console.error('触发任务失败:', error)
          this.$message.error('任务触发失败，请稍后重试')
        } finally {
          this.taskLoading = false
        }
      })
    },

    handleFilterChange() {
      this.currentPage = 1
      this.fetchData()
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchData()
    },

    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchData()
    },

    viewDetail(row) {
      this.currentItem = row
      this.detailDialogVisible = true
    },

    openProjectUrl(url) {
      window.open(url, '_blank')
    },

    formatNumber(num) {
      if (!num) return 0
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k'
      }
      return num
    },

    getLanguageType(language) {
      const types = {
        'Python': '',
        'JavaScript': 'success',
        'Go': 'warning',
        'Rust': 'danger',
        'Java': 'info',
        'TypeScript': 'success'
      }
      return types[language] || 'info'
    },

    getScoreColor(score) {
      if (score >= 90) return '#67C23A'
      if (score >= 70) return '#E6A23C'
      return '#F56C6C'
    }
  }
}
</script>

<style lang="scss" scoped>
.github-trending-admin {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
    }

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .filter-bar {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    padding: 15px;
    background: #f5f7fa;
    border-radius: 4px;
  }

  .project-info {
    display: flex;
    gap: 10px;
    align-items: center;

    .project-avatar {
      width: 40px;
      height: 40px;
      border-radius: 6px;
    }

    .project-name {
      font-weight: 600;
      color: #303133;
    }

    .project-url a {
      color: #409EFF;
      text-decoration: none;
      font-size: 12px;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .detail-content {
    .detail-section {
      margin-bottom: 30px;

      &:last-child {
        margin-bottom: 0;
      }

      h3 {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #303133;
      }

      ul {
        margin: 0;
        padding-left: 20px;

        li {
          margin-bottom: 5px;
          color: #606266;
        }
      }
    }
  }
}
</style>
