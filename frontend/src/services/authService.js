/**
 * Authentication Service
 * 处理用户认证相关的API调用
 */

import apiClient from './apiClient.js'
import { API_ENDPOINTS } from '@/config/api.js'

/**
 * 用户注册
 * @param {Object} credentials - 注册凭据
 * @param {string} credentials.name - 真实姓名
 * @param {string} credentials.email - 邮箱
 * @param {string} credentials.password - 密码
 * @param {string} credentials.confirmPassword - 确认密码
 * @param {string} [credentials.username] - 用户名
 * @param {string} credentials.module - 模块类型 (p2pai|edgeai|blockchain|crypto)
 * @returns {Promise<Object>} 注册响应
 */
export async function register(credentials) {
  const response = await apiClient.post(API_ENDPOINTS.AUTH.REGISTER, {
    name: credentials.name,
    email: credentials.email,
    password: credentials.password,
    confirm_password: credentials.confirmPassword,
    username: credentials.username,
    module: credentials.module
  })

  return response.data
}

/**
 * 用户登录
 * @param {Object} credentials - 登录凭据
 * @param {string} credentials.username - 用户名
 * @param {string} [credentials.email] - 邮箱
 * @param {string} [credentials.password] - 密码
 * @param {string} credentials.module - 模块类型 (p2pai|edgeai|blockchain|crypto)
 * @returns {Promise<Object>} 登录响应
 */
export async function login(credentials) {
  const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, {
    username: credentials.username,
    email: credentials.email,
    password: credentials.password,
    module: credentials.module
  })

  return response.data
}

/**
 * 用户登出
 * @returns {Promise<Object>} 登出响应
 */
export async function logout() {
  const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT)
  return response.data
}

/**
 * 获取用户信息
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 用户信息
 */
export async function getUserInfo(userId) {
  const url = API_ENDPOINTS.AUTH.USER.replace('{id}', userId)
  const response = await apiClient.get(url)
  return response.data
}

/**
 * 更新用户偏好设置
 * @param {string} userId - 用户ID
 * @param {Object} preferences - 偏好设置
 * @returns {Promise<Object>} 更新响应
 */
export async function updateUserPreferences(userId, preferences) {
  const url = API_ENDPOINTS.AUTH.PREFERENCES.replace('{id}', userId)
  const response = await apiClient.put(url, { preferences })
  return response.data
}

/**
 * 检查认证状态
 * @returns {Promise<Object>} 认证状态
 */
export async function checkAuthStatus() {
  try {
    const response = await apiClient.get(API_ENDPOINTS.SYSTEM.HEALTH)
    return {
      authenticated: true,
      data: response.data
    }
  } catch (error) {
    return {
      authenticated: false,
      error: error.message
    }
  }
}

/**
 * 刷新认证token（如果实现了token刷新机制）
 * @param {string} refreshToken - 刷新token
 * @returns {Promise<Object>} 新的token信息
 */
export async function refreshAuthToken(refreshToken) {
  // 注意: 当前后端API中没有token刷新端点，这里是预留实现
  const response = await apiClient.post('/api/common/auth/refresh', {
    refresh_token: refreshToken
  })
  return response.data
}

// 导出所有认证相关服务
export default {
  register,
  login,
  logout,
  getUserInfo,
  updateUserPreferences,
  checkAuthStatus,
  refreshAuthToken
}