import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

// 用户端白名单（无需登录即可访问）
const userWhiteList = ['/login', '/register', '/forgot-password']

// 管理端白名单（管理员登录页）
const adminWhiteList = ['/sys-admin-2024/login', '/404']

// 判断是否是用户端路由
function isUserRoute(path) {
  return path.startsWith('/user') ||
         userWhiteList.some(route => path === route || path.startsWith(route + '/'))
}

// 判断是否是管理端路由
function isAdminRoute(path) {
  return path.startsWith('/admin-panel') ||
         path.startsWith('/sys-admin-2024') ||
         adminWhiteList.includes(path)
}

router.beforeEach(async(to, from, next) => {
  // 调试信息
  console.log('🔍 Route Guard Debug:', {
    to: to.path,
    from: from.path,
    hasToken: !!getToken(),
    isInUserWhiteList: userWhiteList.includes(to.path),
    isInAdminWhiteList: adminWhiteList.includes(to.path),
    isUserRoute: isUserRoute(to.path),
    isAdminRoute: isAdminRoute(to.path)
  })

  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  const hasToken = getToken()

  // ========== 用户端路由处理 ==========
  if (isUserRoute(to.path)) {
    if (hasToken) {
      // 已登录用户访问登录页，重定向到用户中心
      if (to.path === '/login') {
        next({ path: '/user/dashboard' })
        NProgress.done()
      } else {
        next()
      }
    } else {
      // 未登录用户
      if (userWhiteList.indexOf(to.path) !== -1) {
        // 在白名单中，直接访问
        next()
      } else if (to.path.startsWith('/user')) {
        // 需要登录的用户页面，重定向到登录页
        next(`/login?redirect=${to.path}`)
        NProgress.done()
      } else {
        next()
      }
    }
  }
  // ========== 管理端路由处理 ==========
  else if (isAdminRoute(to.path)) {
    if (hasToken) {
      // 已登录且有权限的管理员访问管理端登录页，重定向到管理端首页
      if (to.path === '/sys-admin-2024/login') {
        // 检查是否已有权限信息
        const hasPerms = store.getters.perms && store.getters.perms.length > 0
        if (hasPerms) {
          // 有权限才重定向到管理后台
          next({ path: '/admin-panel/dashboard' })
          NProgress.done()
        } else {
          // 有token但没有权限信息，尝试获取权限
          try {
            await store.dispatch('user/getInfo')
            const { perms } = store.getters
            if (perms && perms.length > 0) {
              next({ path: '/admin-panel/dashboard' })
              NProgress.done()
            } else {
              // 没有管理权限，清除token并重定向到用户端
              await store.dispatch('user/resetToken')
              Message.warning('您没有管理权限')
              next('/login')
              NProgress.done()
            }
          } catch (error) {
            await store.dispatch('user/resetToken')
            Message.error('获取权限信息失败')
            next('/login')
            NProgress.done()
          }
        }
      } else {
        // determine whether the user has obtained his permission perms through getInfo
        const hasPerms = store.getters.perms && store.getters.perms.length > 0
        if (hasPerms) {
          next()
        } else {
          try {
            // get user info
            // note: perms must be a object array! such as: ['admin'] or ,['developer','editor']
            const { perms } = await store.dispatch('user/getInfo')

            // 如果用户没有任何权限，不允许访问管理端
            if (!perms || perms.length === 0) {
              Message.warning('您没有权限访问管理系统')
              next('/user/dashboard')
              NProgress.done()
              return
            }

            // generate accessible routes map based on perms
            const accessRoutes = await store.dispatch('permission/generateRoutes', perms)

            // dynamically add accessible routes
            router.addRoutes(accessRoutes)

            // hack method to ensure that addRoutes is complete
            // set the replace: true, so the navigation will not leave a history record
            next({ ...to, replace: true })
          } catch (error) {
            // remove token and go to login page to re-login
            await store.dispatch('user/resetToken')
            Message.error(error || 'Has Error')
            next(`/sys-admin-2024/login?redirect=${to.path}`)
            NProgress.done()
          }
        }
      }
    } else {
      /* has no token*/

      if (adminWhiteList.indexOf(to.path) !== -1) {
        // in the free login whitelist, go directly
        next()
      } else {
        // other pages that do not have permission to access are redirected to the login page.
        next(`/sys-admin-2024/login?redirect=${to.path}`)
        NProgress.done()
      }
    }
  }
  // ========== 根路径处理 ==========
  else if (to.path === '/') {
    // 根路径重定向到用户登录页
    next('/login')
    NProgress.done()
  }
  // ========== 其他路由处理 ==========
  else {
    // 其他路径默认重定向到用户登录页
    next('/login')
    NProgress.done()
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
