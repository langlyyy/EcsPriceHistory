import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API请求失败:', error)
    return Promise.reject(error)
  }
)

// API方法
export const apiService = {
  // 获取地域列表
  getRegions() {
    return api.get('/regions')
  },

  // 获取可用区列表
  getZones(regionId) {
    return api.get(`/zones/${regionId}`)
  },

  // 获取实例规格列表
  getInstanceTypes(regionId) {
    return api.get(`/instance-types/${regionId}`)
  },

  // 获取抢占式实例价格历史
  getSpotPriceHistory(params) {
    return api.post('/spot-price-history', params)
  },

  // 健康检查
  healthCheck() {
    return api.get('/health')
  }
}

export default apiService 