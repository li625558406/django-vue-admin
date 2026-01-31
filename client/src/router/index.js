import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layouts */
import Layout from '@/layout'  // 管理端布局
import UserLayout from '@/layout-user'  // 用户端布局

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
 *    perms: ['admin','editor']    control the page perms (you can set multiple perms)
 *    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
 *    icon: 'svg-name'             the icon show in the sidebar
 *    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
 *    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
 *  }
 */

/**
 * ========================================
 * 用户端路由 (USER PORTAL ROUTES)
 * ========================================
 * 面向普通用户的公开访问页面
 */
export const userRoutes = [
  // 根路径重定向到用户登录
  {
    path: '/',
    redirect: '/login'
  },

  // 用户登录页
  {
    path: '/login',
    component: () => import('@/views/user-login/index'),
    hidden: true
  },

  // 用户注册页（预留）
  {
    path: '/register',
    component: () => import('@/views/user-login/index'), // 临时复用登录页
    hidden: true
  },

  // 忘记密码页（预留）
  {
    path: '/forgot-password',
    component: () => import('@/views/user-login/index'), // 临时复用登录页
    hidden: true
  },

  // 用户中心（需要UserLayout）
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'UserDashboard',
        component: () => import('@/views/user-dashboard/index'),
        meta: { title: '用户中心', icon: 'user' }
      },
      // GitHub Trending 热榜页
      {
        path: 'github-trending',
        name: 'GithubTrending',
        component: () => import('@/views/github-trending/index'),
        meta: { title: 'GitHub 热榜', icon: 'star' }
      },
      // 可以添加更多用户端页面
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('@/views/user-dashboard/index'),
        meta: { title: '个人资料', icon: 'user' },
        hidden: true
      }
    ]
  },

  // GitHub Trending 公开访问页（不需要登录）
  {
    path: '/github-trending',
    name: 'GithubTrendingPublic',
    component: () => import('@/views/github-trending/index'),
    hidden: true
  }
]

/**
 * ========================================
 * 管理端路由 (ADMIN PORTAL ROUTES)
 * ========================================
 * 隐藏的管理系统，路径复杂化防止被猜测
 */
export const adminRoutes = [
  // 管理系统登录页 - 使用复杂路径
  {
    path: '/sys-admin-2024/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  // 404页面
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  // 管理系统主路由 - 使用复杂前缀
  {
    path: '/admin-panel',
    component: Layout,
    redirect: '/admin-panel/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  // 修改密码
  {
    path: '/admin-panel/changepassword',
    component: Layout,
    redirect: '/admin-panel/changepassword',
    name: 'ChangePW',
    meta: { title: '修改密码', icon: 'tree' },
    hidden: true,
    children: [
      {
        path: '',
        name: 'ChangePassword',
        component: () => import('@/views/system/changepassword'),
        meta: { title: '修改密码', noCache: true, icon: '' },
        hidden: true
      }
    ]
  }
]

/**
 * ========================================
 * 管理端异步路由 (ADMIN ASYNC ROUTES)
 * ========================================
 * 需要动态权限加载的管理端路由
 */
export const adminAsyncRoutes = [
  {
    path: '/admin-panel/workflow',
    component: Layout,
    redirect: '/admin-panel/workflow/index',
    name: 'workflow',
    meta: { title: '工作流', icon: 'example', perms: ['workflow_manage'] },
    children: [
      {
        path: 'index',
        name: 'index',
        component: () => import('@/views/workflow/index'),
        meta: { title: '工作流', icon: 'example', perms: ['workflow_index'] }
      },
      {
        path: 'ticket',
        name: 'ticket',
        component: () => import('@/views/workflow/ticket'),
        meta: { title: '工单管理', icon: 'example', noCache: true, perms: ['workflow_ticket'] }
      },
      {
        path: 'workFlowTickets',
        name: 'workFlowTickets',
        component: () => import('@/views/workflow/workFlowTickets'),
        meta: { title: '工单', icon: 'example', noCache: true },
        hidden: true
      },
      {
        path: 'configuration',
        name: 'configuration',
        component: () => import('@/views/workflow/configuration'),
        meta: { title: '工作流配置', icon: 'example' },
        hidden: true
      },
      {
        path: 'ticketHandle',
        name: 'ticketHandle',
        component: () => import('@/views/workflow/ticketHandle'),
        meta: { title: '工单处理', icon: 'example', noCache: true },
        hidden: true
      },
      {
        path: 'ticketDetail',
        name: 'ticketDetail',
        component: () => import('@/views/workflow/ticketDetail'),
        meta: { title: '工单详情', icon: 'example', noCache: true },
        hidden: true
      }
    ]
  },
  {
    path: '/admin-panel/system',
    component: Layout,
    redirect: '/admin-panel/system/user',
    name: 'System',
    meta: { title: '系统管理', icon: 'example', perms: ['system_manage'] },
    children: [
      {
        path: 'user',
        name: 'User',
        component: () => import('@/views/system/user.vue'),
        meta: { title: '用户管理', icon: 'user', perms: ['user_manage'] }
      },
      {
        path: 'organization',
        name: 'Organization',
        component: () => import('@/views/system/organization'),
        meta: { title: '部门管理', icon: 'tree', perms: ['org_manage'] }
      },
      {
        path: 'role',
        name: 'Role',
        component: () => import('@/views/system/role'),
        meta: { title: '角色管理', icon: 'lock', perms: ['role_manage'] }
      },
      {
        path: 'position',
        name: 'Postion',
        component: () => import('@/views/system/position'),
        meta: { title: '岗位管理', icon: 'position', perms: ['position_manage'] }
      },
      {
        path: 'dict',
        name: 'Dict',
        component: () => import('@/views/system/dict'),
        meta: { title: '数据字典', icon: 'example', perms: ['dict_manage'] }
      },
      {
        path: 'file',
        name: 'File',
        component: () => import('@/views/system/file'),
        meta: { title: '文件库', icon: 'documentation', perms: ['file_room'] }
      },
      {
        path: 'task',
        name: 'Task',
        component: () => import('@/views/system/task'),
        meta: { title: '定时任务', icon: 'list', perms: ['ptask_manage'] }
      },
      {
        path: 'github-trending',
        name: 'GithubTrendingAdmin',
        component: () => import('@/views/system/github-trending-admin'),
        meta: { title: 'GitHub 热榜', icon: 'star', perms: ['github_trending_manage'] }
      }
    ]
  },
  {
    path: '/admin-panel/monitor',
    component: Layout,
    redirect: '/admin-panel/monitor/service',
    name: 'Monitor',
    meta: { title: '系统监控', icon: 'example', perms: ['monitor_set'] },
    children: [
      {
        path: 'service',
        name: 'service',
        component: () => import('@/views/monitor/service'),
        meta: { title: '服务监控', icon: 'example', perms: ['service_manage'] }
      }
    ]
  },
  {
    path: '/admin-panel/develop',
    component: Layout,
    redirect: '/admin-panel/develop/perm',
    name: 'Develop',
    meta: { title: '开发配置', icon: 'example', perms: ['dev_set'] },
    children: [
      {
        path: 'perm',
        name: 'Perm',
        component: () => import('@/views/system/perm'),
        meta: { title: '权限菜单', icon: 'example', perms: ['perm_manage'] }
      },
      {
        path: 'form-gen-link',
        component: Layout,
        children: [
          {
            path: 'https://jakhuang.github.io/form-generator/',
            meta: { title: '表单设计器', icon: 'link', perms: ['dev_form_gen'] }
          }
        ]
      },
      {
        path: 'docs',
        component: Layout,
        children: [
          {
            path: process.env.VUE_APP_BASE_API + '/redoc/',
            meta: { title: '接口文档', icon: 'link', perms: ['dev_docs'] }
          }
        ]
      },
      {
        path: 'swagger',
        component: Layout,
        children: [
          {
            path: process.env.VUE_APP_BASE_API + '/swagger/',
            meta: { title: 'Swagger文档', icon: 'link', perms: ['dev_docs'] }
          }
        ]
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

/**
 * ========================================
 * 路由创建 (CREATE ROUTER)
 * ========================================
 */
const createRouter = () => new Router({
  mode: 'history', // 使用 history 模式避免 hash 路由冲突
  scrollBehavior: () => ({ y: 0 }),
  routes: [...userRoutes, ...adminRoutes]
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
