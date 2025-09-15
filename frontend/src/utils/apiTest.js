/**
 * API Integration Test Utilities
 * 用于测试API集成是否正常工作
 */

import { authService, p2paiService, edgeaiService } from '@/services/index.js'
import apiClient from '@/services/apiClient.js'
import { API_ENDPOINTS } from '@/config/api.js'

/**
 * 测试后端连接
 */
export async function testBackendConnection() {
  try {
    const response = await apiClient.get('/health')
    console.log('✅ Backend connection successful:', response.data)
    return { success: true, data: response.data }
  } catch (error) {
    console.error('❌ Backend connection failed:', error)
    return { success: false, error: error.message }
  }
}

/**
 * 测试认证API
 */
export async function testAuthAPI() {
  try {
    console.log('🔐 Testing Auth API...')
    
    // 测试登录
    const loginResult = await authService.login({
      username: 'testuser',
      email: 'test@example.com',
      password: 'password',
      module: 'p2pai'
    })
    
    console.log('Login test result:', loginResult)
    return { success: true, data: loginResult }
  } catch (error) {
    console.error('❌ Auth API test failed:', error)
    return { success: false, error: error.message }
  }
}

/**
 * 测试P2P AI API
 */
export async function testP2PAIAPI() {
  try {
    console.log('🤖 Testing P2P AI API...')
    
    // 测试获取项目列表
    const projectsResult = await p2paiService.projects.getProjects()
    console.log('P2P AI Projects:', projectsResult)
    
    // 测试获取节点列表
    const nodesResult = await p2paiService.nodes.getNodes()
    console.log('P2P AI Nodes:', nodesResult)
    
    return { 
      success: true, 
      data: { 
        projects: projectsResult, 
        nodes: nodesResult 
      } 
    }
  } catch (error) {
    console.error('❌ P2P AI API test failed:', error)
    return { success: false, error: error.message }
  }
}

/**
 * 测试Edge AI API
 */
export async function testEdgeAIAPI() {
  try {
    console.log('🔄 Testing Edge AI API...')
    
    // 测试获取项目列表
    const projectsResult = await edgeaiService.projects.getProjects()
    console.log('Edge AI Projects:', projectsResult)
    
    // 测试获取性能指标
    const metricsResult = await edgeaiService.performance.getMetrics()
    console.log('Edge AI Performance:', metricsResult)
    
    return { 
      success: true, 
      data: { 
        projects: projectsResult, 
        performance: metricsResult 
      } 
    }
  } catch (error) {
    console.error('❌ Edge AI API test failed:', error)
    return { success: false, error: error.message }
  }
}

/**
 * 运行完整的API集成测试
 */
export async function runFullAPITest() {
  console.group('🚀 Starting Full API Integration Test')
  
  const results = {
    backend: await testBackendConnection(),
    auth: await testAuthAPI(),
    p2pai: await testP2PAIAPI(),
    edgeai: await testEdgeAIAPI()
  }
  
  // 汇总结果
  const successCount = Object.values(results).filter(r => r.success).length
  const totalCount = Object.keys(results).length
  
  console.log(`\n📊 Test Results: ${successCount}/${totalCount} passed`)
  
  Object.entries(results).forEach(([test, result]) => {
    const icon = result.success ? '✅' : '❌'
    console.log(`${icon} ${test}: ${result.success ? 'PASSED' : 'FAILED'}`)
    if (!result.success) {
      console.log(`   Error: ${result.error}`)
    }
  })
  
  console.groupEnd()
  
  return {
    success: successCount === totalCount,
    results,
    summary: `${successCount}/${totalCount} tests passed`
  }
}

// 在控制台暴露测试函数
if (typeof window !== 'undefined') {
  window.apiTest = {
    testBackendConnection,
    testAuthAPI,
    testP2PAIAPI,
    testEdgeAIAPI,
    runFullAPITest
  }
  
  console.log('🛠️  API Test utilities available at window.apiTest')
  console.log('   • window.apiTest.runFullAPITest() - 运行完整测试')
  console.log('   • window.apiTest.testBackendConnection() - 测试后端连接')
  console.log('   • window.apiTest.testAuthAPI() - 测试认证API')
}