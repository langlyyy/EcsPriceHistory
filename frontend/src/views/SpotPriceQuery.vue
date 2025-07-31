<template>
     <div class="spot-price-query">
     <el-row :gutter="24">
       <!-- 左侧查询面板 -->
       <el-col :span="6">
        <el-card class="query-panel">
          <template #header>
            <div class="card-header">
              <span>查询条件</span>
            </div>
          </template>
          
                     <!-- 查询表单 -->
           <el-form :model="queryForm" label-width="80px" size="default">
            <el-form-item label="地域">
              <el-select 
                v-model="queryForm.regionId" 
                placeholder="请选择地域"
                @change="handleRegionChange"
                style="width: 100%"
              >
                <el-option
                  v-for="region in regions"
                  :key="region.region_id"
                  :label="region.local_name"
                  :value="region.region_id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="可用区">
              <el-select 
                v-model="queryForm.zoneId" 
                placeholder="请选择可用区"
                style="width: 100%"
                :disabled="!queryForm.regionId"
              >
                <el-option
                  v-for="zone in zones"
                  :key="zone.zone_id"
                  :label="zone.local_name"
                  :value="zone.zone_id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="实例规格">
              <el-select 
                v-model="queryForm.instanceTypes" 
                placeholder="请选择实例规格"
                multiple
                filterable
                clearable
                style="width: 100%"
                :disabled="!queryForm.regionId"
                :filter-method="filterInstanceTypes"
                :reserve-keyword="false"
              >
                <el-option
                  v-for="instance in filteredInstanceTypes"
                  :key="instance.instance_type_id"
                  :label="`${instance.instance_type_id} (${instance.cpu_core_count}核${instance.memory_size}GB)`"
                  :value="instance.instance_type_id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="网络类型">
              <el-radio-group v-model="queryForm.networkType">
                <el-radio label="vpc">VPC</el-radio>
                <el-radio label="classic">Classic</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="操作系统">
              <el-radio-group v-model="queryForm.osType">
                <el-radio label="linux">Linux</el-radio>
                <el-radio label="windows">Windows</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="时间范围">
              <el-date-picker
                v-model="timeRange"
                type="datetimerange"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                format="YYYY-MM-DD HH:mm:ss"
                value-format="YYYY-MM-DDTHH:mm:ss[Z]"
                style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="显示对比">
              <el-switch
                v-model="queryForm.includePayAsYouGo"
                active-text="显示按量付费价格"
                inactive-text="仅显示抢占式价格"
                style="width: 100%"
              />
            </el-form-item>

                         <el-form-item>
               <el-button 
                 type="primary" 
                 @click="queryPrices"
                 :loading="loading"
                 style="width: 100%"
                 size="default"
               >
                 {{ loading ? '查询中...' : '查询价格' }}
               </el-button>
             </el-form-item>
          </el-form>
        </el-card>
      </el-col>

             <!-- 右侧图表面板 -->
       <el-col :span="18">
        <el-card class="chart-panel">
          <template #header>
            <div class="card-header">
              <span>价格趋势图</span>
              <div class="header-actions">
                <el-button 
                  type="success" 
                  size="small" 
                  @click="exportData"
                  :disabled="!priceData.length"
                >
                  导出数据
                </el-button>
                <el-button 
                  type="warning" 
                  size="small" 
                  @click="clearChart"
                >
                  清除图表
                </el-button>
              </div>
            </div>
          </template>
          
                     <!-- 数据统计面板 -->
           <div v-if="priceData.length" class="stats-panel">
             <!-- 总体统计 -->
             <div class="stats-section">
               <h3 class="stats-title">📊 总体统计</h3>
               <el-row :gutter="20">
                 <el-col :span="6">
                   <div class="stat-card">
                     <div class="stat-icon">📊</div>
                     <div class="stat-content">
                       <div class="stat-value">{{ priceData.length }}</div>
                       <div class="stat-label">数据点</div>
                     </div>
                   </div>
                 </el-col>
                 <el-col :span="6">
                   <div class="stat-card">
                     <div class="stat-icon">💰</div>
                     <div class="stat-content">
                       <div class="stat-value">{{ minPrice }}元</div>
                       <div class="stat-label">最低价格</div>
                     </div>
                   </div>
                 </el-col>
                 <el-col :span="6">
                   <div class="stat-card">
                     <div class="stat-icon">📈</div>
                     <div class="stat-content">
                       <div class="stat-value">{{ maxPrice }}元</div>
                       <div class="stat-label">最高价格</div>
                     </div>
                   </div>
                 </el-col>
                 <el-col :span="6">
                   <div class="stat-card">
                     <div class="stat-icon">⚖️</div>
                     <div class="stat-content">
                       <div class="stat-value">{{ avgPrice }}元</div>
                       <div class="stat-label">平均价格</div>
                     </div>
                   </div>
                 </el-col>
               </el-row>
             </div>
             
             <!-- 实例规格统计 -->
             <div v-if="instanceStats.length > 1" class="stats-section">
               <h3 class="stats-title">🔍 实例规格对比</h3>
               <el-row :gutter="20">
                 <el-col 
                   v-for="stat in instanceStats" 
                   :key="stat.instanceType" 
                   :span="24 / Math.min(instanceStats.length, 4)"
                 >
                   <div class="instance-stat-card">
                     <div class="instance-name">{{ stat.instanceType }}</div>
                                           <div class="instance-stats">
                        <div class="instance-stat-item">
                          <span class="stat-label">抢占式最低:</span>
                          <span class="stat-value">{{ stat.spotMinPrice }}元</span>
                        </div>
                        <div class="instance-stat-item">
                          <span class="stat-label">抢占式最高:</span>
                          <span class="stat-value">{{ stat.spotMaxPrice }}元</span>
                        </div>
                        <div class="instance-stat-item">
                          <span class="stat-label">抢占式平均:</span>
                          <span class="stat-value">{{ stat.spotAvgPrice }}元</span>
                        </div>
                        <div v-if="stat.payAsYouGoMinPrice" class="instance-stat-item">
                          <span class="stat-label">按量付费最低:</span>
                          <span class="stat-value pay-as-you-go">{{ stat.payAsYouGoMinPrice }}元</span>
                        </div>
                        <div v-if="stat.payAsYouGoMaxPrice" class="instance-stat-item">
                          <span class="stat-label">按量付费最高:</span>
                          <span class="stat-value pay-as-you-go">{{ stat.payAsYouGoMaxPrice }}元</span>
                        </div>
                        <div v-if="stat.payAsYouGoAvgPrice" class="instance-stat-item">
                          <span class="stat-label">按量付费平均:</span>
                          <span class="stat-value pay-as-you-go">{{ stat.payAsYouGoAvgPrice }}元</span>
                        </div>
                      </div>
                   </div>
                 </el-col>
               </el-row>
             </div>
           </div>
           
                       <div class="chart-container">
              <div v-if="priceData.length" class="chart-wrapper">
                <div ref="chartRef" style="height: 600px; width: 100%;"></div>
              </div>
              <div v-else class="no-data">
                <el-empty description="暂无数据，请先查询价格" />
              </div>
            </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import apiService from '../api'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import dayjs from 'dayjs'

// 注册ECharts组件
echarts.use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

export default {
  name: 'SpotPriceQuery',
  setup() {
    const regions = ref([])
    const zones = ref([])
    const instanceTypes = ref([])
    const filteredInstanceTypes = ref([])
    const priceData = ref([])
    const loading = ref(false)
    const timeRange = ref([])
    const chartRef = ref(null)
    let chartInstance = null

    const queryForm = reactive({
      regionId: '',
      zoneId: '',
      instanceTypes: [],
      networkType: 'vpc',
      osType: 'linux',
      ioOptimized: 'optimized',
      includePayAsYouGo: false
    })

    const loadRegions = async () => {
      try {
        const data = await apiService.getRegions()
        regions.value = data
      } catch (error) {
        ElMessage.error('加载地域列表失败')
      }
    }

    const handleRegionChange = async () => {
      queryForm.zoneId = ''
      queryForm.instanceTypes = []
      zones.value = []
      instanceTypes.value = []
      filteredInstanceTypes.value = []

      if (queryForm.regionId) {
        try {
          const [zonesData, instanceTypesData] = await Promise.all([
            apiService.getZones(queryForm.regionId),
            apiService.getInstanceTypes(queryForm.regionId)
          ])
          zones.value = zonesData
          instanceTypes.value = instanceTypesData
          filteredInstanceTypes.value = instanceTypesData
        } catch (error) {
          ElMessage.error('加载地域数据失败')
        }
      }
    }

    const filterInstanceTypes = (query) => {
      if (query === '') {
        filteredInstanceTypes.value = instanceTypes.value
      } else {
        filteredInstanceTypes.value = instanceTypes.value.filter(instance => {
          const searchText = query.toLowerCase()
          const instanceId = instance.instance_type_id.toLowerCase()
          const cpuCore = instance.cpu_core_count.toString()
          const memorySize = instance.memory_size.toString()
          
          return instanceId.includes(searchText) || 
                 cpuCore.includes(searchText) || 
                 memorySize.includes(searchText)
        })
      }
    }

    const queryPrices = async () => {
      if (!queryForm.zoneId || !queryForm.instanceTypes.length) {
        ElMessage.warning('请选择可用区和实例规格')
        return
      }

      loading.value = true
      
      // 清除之前的图表
      if (chartInstance) {
        chartInstance.dispose()
        chartInstance = null
      }
      
      try {
        const params = {
          zone_id: queryForm.zoneId,
          instance_types: queryForm.instanceTypes,
          network_type: queryForm.networkType,
          os_type: queryForm.osType,
          io_optimized: queryForm.ioOptimized,
          include_pay_as_you_go: queryForm.includePayAsYouGo
        }

        if (timeRange.value && timeRange.value.length === 2) {
          // 确保时间格式正确，转换为UTC时间
          params.start_time = timeRange.value[0].replace('+00:00', 'Z').replace('+08:00', 'Z')
          params.end_time = timeRange.value[1].replace('+00:00', 'Z').replace('+08:00', 'Z')
        }

        const response = await apiService.getSpotPriceHistory(params)
        priceData.value = response.data
        
        // 添加成功消息和动画效果
        ElMessage({
          message: `成功获取${response.data.length}条价格记录`,
          type: 'success',
          duration: 3000,
          showClose: true
        })
        
                 // 延迟一下再初始化图表，让用户看到加载效果
         setTimeout(() => {
           if (priceData.value.length) {
             initChart()
             updateChart()
             // 确保图表正确渲染
             setTimeout(() => {
               if (chartInstance) {
                 chartInstance.resize()
               }
             }, 100)
           }
         }, 500)
        
      } catch (error) {
        ElMessage.error('查询价格失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        loading.value = false
      }
    }

    const exportData = () => {
      ElMessage.info('导出功能待实现')
    }

    const clearChart = () => {
      priceData.value = []
      timeRange.value = []
      if (chartInstance) {
        chartInstance.dispose()
        chartInstance = null
      }
      ElMessage.success('图表已清除')
    }

             const initChart = () => {
       if (chartRef.value && !chartInstance) {
         chartInstance = echarts.init(chartRef.value, null, {
           renderer: 'canvas',
           useDirtyRect: true
         })
         console.log('图表已初始化:', chartInstance)
       }
     }

        const updateChart = () => {
      if (!chartInstance || !priceData.value.length) {
        return
      }

      console.log('priceData:', priceData.value) // 调试日志
      
      // 按实例规格分组数据
      const groupedData = {}
      const payAsYouGoData = {}
      const allTimestamps = new Set()
      
      priceData.value.forEach(item => {
        if (!groupedData[item.instance_type]) {
          groupedData[item.instance_type] = []
          payAsYouGoData[item.instance_type] = []
        }
        groupedData[item.instance_type].push({
          timestamp: item.timestamp,
          price: item.spot_price
        })
        if (item.pay_as_you_go_price) {
          payAsYouGoData[item.instance_type].push({
            timestamp: item.timestamp,
            price: item.pay_as_you_go_price
          })
        }
        allTimestamps.add(item.timestamp)
      })

      // 排序时间戳
      const sortedTimestamps = Array.from(allTimestamps).sort((a, b) => new Date(a) - new Date(b))
      
      // 生成图表系列数据
      const series = []
      const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399', '#9c27b0', '#ff9800', '#795548', '#2196f3', '#4caf50']
      const payAsYouGoColors = ['#ff6b6b', '#ff8e8e', '#ffb3b3', '#ffd6d6', '#ffe6e6', '#ff9999', '#ffcccc', '#ffb366', '#ffcc99', '#ffdb4d']
      
      Object.keys(groupedData).forEach((instanceType, index) => {
        const data = groupedData[instanceType]
        
        // 按时间戳排序数据
        const sortedData = data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
        
        // 为每个时间戳创建数据点，如果没有数据则设为null
        const seriesData = sortedTimestamps.map(timestamp => {
          const dataPoint = sortedData.find(item => item.timestamp === timestamp)
          return dataPoint ? dataPoint.price : null
        })

        // 添加抢占式实例价格线
        series.push({
          name: `${instanceType} (抢占式)`,
          type: 'line',
          data: seriesData,
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            width: 4,
            color: colors[index % colors.length]
          },
          itemStyle: {
            color: colors[index % colors.length],
            borderColor: colors[index % colors.length],
            borderWidth: 3
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [{
                offset: 0, color: colors[index % colors.length] + '30' // 30%透明度
              }, {
                offset: 1, color: colors[index % colors.length] + '05' // 5%透明度
              }]
            }
          }
        })

        // 如果启用了按量付费价格对比，添加按量付费价格线
        if (queryForm.includePayAsYouGo && payAsYouGoData[instanceType] && payAsYouGoData[instanceType].length > 0) {
          const payAsYouGoSortedData = payAsYouGoData[instanceType].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
          
          const payAsYouGoSeriesData = sortedTimestamps.map(timestamp => {
            const dataPoint = payAsYouGoSortedData.find(item => item.timestamp === timestamp)
            return dataPoint ? dataPoint.price : null
          })

          series.push({
            name: `${instanceType} (按量付费)`,
            type: 'line',
            data: payAsYouGoSeriesData,
            smooth: true,
            symbol: 'diamond',
            symbolSize: 6,
            lineStyle: {
              width: 3,
              color: payAsYouGoColors[index % payAsYouGoColors.length],
              type: 'dashed'
            },
            itemStyle: {
              color: payAsYouGoColors[index % payAsYouGoColors.length],
              borderColor: payAsYouGoColors[index % payAsYouGoColors.length],
              borderWidth: 2
            }
          })
        }
      })

      console.log('分组数据:', groupedData)
      console.log('时间戳:', sortedTimestamps)
      console.log('系列数据:', series)

             const option = {
         title: {
           text: queryForm.includePayAsYouGo ? '实例价格趋势对比 (抢占式 vs 按量付费)' : '抢占式实例价格趋势对比',
           left: 'center',
           top: 20,
           textStyle: {
             fontSize: 20,
             fontWeight: '600',
             color: '#2c3e50'
           }
         },
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderColor: '#e6e6e6',
          borderWidth: 1,
          textStyle: {
            color: '#333'
          },
                     formatter: function(params) {
             let result = `<div style="padding: 8px;">
               <div style="font-weight: bold; margin-bottom: 8px; color: #2c3e50;">${params[0].name}</div>`
             
             params.forEach(param => {
               if (param.value !== null) {
                 const priceType = param.seriesName.includes('按量付费') ? '按量付费' : '抢占式'
                 const priceColor = param.seriesName.includes('按量付费') ? '#ff6b6b' : '#409eff'
                 result += `<div style="color: #666; margin-bottom: 4px;">
                   <span style="display: inline-block; width: 12px; height: 12px; background: ${param.color}; margin-right: 8px; border-radius: 2px;"></span>
                   ${param.seriesName}: <span style="color: ${priceColor}; font-weight: bold;">${param.value} 元/小时</span>
                 </div>`
               }
             })
             
             result += '</div>'
             return result
           }
        },
                                   legend: {
            data: series.map(s => s.name),
            top: 60,
            textStyle: {
              color: '#666',
              fontSize: 14
            },
            itemGap: 30
          },
                 grid: {
           left: '5%',
           right: '5%',
           top: '20%',
           bottom: '15%',
           containLabel: true
         },
                 xAxis: {
           type: 'category',
           data: sortedTimestamps.map(timestamp => 
             dayjs(timestamp).format('MM-DD HH:mm')
           ),
           axisLabel: {
             rotate: 45,
             color: '#666',
             fontSize: 12
           },
           axisLine: {
             lineStyle: {
               color: '#e0e0e0',
               width: 1
             }
           },
           axisTick: {
             lineStyle: {
               color: '#e0e0e0',
               width: 1
             }
           }
         },
                 yAxis: {
           type: 'value',
           name: '价格 (元/小时)',
           nameTextStyle: {
             color: '#666',
             fontSize: 14
           },
           axisLabel: {
             formatter: '{value} 元',
             color: '#666',
             fontSize: 12
           },
           axisLine: {
             lineStyle: {
               color: '#e0e0e0',
               width: 1
             }
           },
           splitLine: {
             lineStyle: {
               color: '#f5f5f5',
               type: 'solid',
               width: 1
             }
           }
         },
        series: series,
        color: colors
      }

      chartInstance.setOption(option)
      console.log('图表配置已更新')
    }

    // 计算统计数据
    const minPrice = computed(() => {
      if (!priceData.value.length) return '0.000'
      const min = Math.min(...priceData.value.map(item => item.spot_price))
      return min.toFixed(3)
    })

    const maxPrice = computed(() => {
      if (!priceData.value.length) return '0.000'
      const max = Math.max(...priceData.value.map(item => item.spot_price))
      return max.toFixed(3)
    })

    const avgPrice = computed(() => {
      if (!priceData.value.length) return '0.000'
      const sum = priceData.value.reduce((acc, item) => acc + item.spot_price, 0)
      const avg = sum / priceData.value.length
      return avg.toFixed(3)
    })

    // 计算每个实例规格的统计数据
    const instanceStats = computed(() => {
      if (!priceData.value.length) return []
      
      const groupedData = {}
      const payAsYouGoData = {}
      
      priceData.value.forEach(item => {
        if (!groupedData[item.instance_type]) {
          groupedData[item.instance_type] = []
          payAsYouGoData[item.instance_type] = []
        }
        groupedData[item.instance_type].push(item.spot_price)
        if (item.pay_as_you_go_price) {
          payAsYouGoData[item.instance_type].push(item.pay_as_you_go_price)
        }
      })
      
      return Object.keys(groupedData).map(instanceType => {
        const spotPrices = groupedData[instanceType]
        const payAsYouGoPrices = payAsYouGoData[instanceType]
        
        const spotMin = Math.min(...spotPrices)
        const spotMax = Math.max(...spotPrices)
        const spotAvg = spotPrices.reduce((acc, price) => acc + price, 0) / spotPrices.length
        
        let payAsYouGoMin = null
        let payAsYouGoMax = null
        let payAsYouGoAvg = null
        
        if (payAsYouGoPrices.length > 0) {
          payAsYouGoMin = Math.min(...payAsYouGoPrices)
          payAsYouGoMax = Math.max(...payAsYouGoPrices)
          payAsYouGoAvg = payAsYouGoPrices.reduce((acc, price) => acc + price, 0) / payAsYouGoPrices.length
        }
        
        return {
          instanceType,
          spotMinPrice: spotMin.toFixed(3),
          spotMaxPrice: spotMax.toFixed(3),
          spotAvgPrice: spotAvg.toFixed(3),
          payAsYouGoMinPrice: payAsYouGoMin ? payAsYouGoMin.toFixed(3) : null,
          payAsYouGoMaxPrice: payAsYouGoMax ? payAsYouGoMax.toFixed(3) : null,
          payAsYouGoAvgPrice: payAsYouGoAvg ? payAsYouGoAvg.toFixed(3) : null
        }
      })
    })

    // 监听价格数据变化
    watch(priceData, () => {
      nextTick(() => {
        if (priceData.value.length) {
          initChart()
          updateChart()
        }
      })
    }, { deep: true })

         onMounted(() => {
       loadRegions()
       
       // 监听窗口大小变化，重新调整图表大小
       window.addEventListener('resize', () => {
         if (chartInstance) {
           chartInstance.resize()
         }
       })
     })

    return {
      regions,
      zones,
      instanceTypes,
      filteredInstanceTypes,
      priceData,
      loading,
      timeRange,
      queryForm,
      chartRef,
      minPrice,
      maxPrice,
      avgPrice,
      instanceStats,
      handleRegionChange,
      filterInstanceTypes,
      queryPrices,
      exportData,
      clearChart
    }
  }
}
</script>

<style scoped>
.spot-price-query {
  max-width: 1600px;
  margin: 0 auto;
  padding: 24px;
  padding-top: 40px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 120px);
}

.query-panel {
  height: fit-content;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
  position: sticky;
  top: 24px;
}

.chart-panel {
  height: fit-content;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20px;
}

.card-header span {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-panel {
  margin: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  border: 1px solid #e9ecef;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2em;
  margin-right: 15px;
  opacity: 0.8;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.8em;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9em;
  color: #666;
  font-weight: 500;
}

.stats-section {
  margin-bottom: 20px;
}

.stats-section:last-child {
  margin-bottom: 0;
}

.stats-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e9ecef;
}

.instance-stat-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
  height: 100%;
}

.instance-stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.instance-name {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
  word-break: break-all;
}

.instance-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.instance-stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.instance-stat-item .stat-label {
  color: #666;
  font-weight: 500;
}

 .instance-stat-item .stat-value {
   color: #409eff;
   font-weight: 600;
   font-size: 14px;
 }

 .instance-stat-item .stat-value.pay-as-you-go {
   color: #ff6b6b;
 }

.chart-container {
  min-height: 700px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  border-radius: 16px;
  background: #fff;
  margin: 24px;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chart-wrapper {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.chart-placeholder {
  text-align: center;
  color: #666;
}

.chart-placeholder h3 {
  margin-bottom: 10px;
  color: #2c3e50;
}

.no-data {
  width: 100%;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border: 2px dashed #dee2e6;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .spot-price-query {
    padding: 20px;
    padding-top: 35px;
  }
  
  .chart-container {
    min-height: 600px;
  }
  
  .stat-card {
    padding: 15px;
  }
  
  .stat-value {
    font-size: 1.5em;
  }
  
  .instance-stat-card {
    padding: 12px;
  }
  
  .instance-name {
    font-size: 13px;
  }
  
  .instance-stat-item {
    font-size: 12px;
  }
}

@media (max-width: 1200px) {
  .spot-price-query {
    padding: 16px;
    padding-top: 30px;
  }
  
  .chart-container {
    min-height: 550px;
  }
}

@media (max-width: 768px) {
  .spot-price-query {
    padding: 12px;
    padding-top: 25px;
  }
  
  .query-panel {
    position: static;
    margin-bottom: 20px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .chart-container {
    min-height: 450px;
    margin: 12px;
  }
  
  .stats-panel {
    margin: 12px;
    padding: 15px;
  }
  
  .stat-card {
    padding: 12px;
    margin-bottom: 10px;
  }
  
  .stat-icon {
    font-size: 1.5em;
    margin-right: 10px;
  }
  
  .stat-value {
    font-size: 1.3em;
  }
  
  .stat-label {
    font-size: 0.8em;
  }
  
  .instance-stat-card {
    padding: 10px;
    margin-bottom: 10px;
  }
  
  .instance-name {
    font-size: 12px;
  }
  
  .instance-stat-item {
    font-size: 11px;
  }
  
  .stats-title {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .spot-price-query {
    padding: 10px;
    padding-top: 20px;
  }
  
  .chart-container {
    min-height: 400px;
    margin: 10px;
  }
  
  .stats-panel {
    margin: 10px;
    padding: 12px;
  }
}

/* 动画效果 */
.query-panel, .chart-panel {
  transition: all 0.3s ease;
}

.query-panel:hover, .chart-panel:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 按钮样式优化 */
:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

:deep(.el-button--primary:hover) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}

:deep(.el-button--success) {
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, #e6a23c 0%, #d49426 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(230, 162, 60, 0.3);
}

/* 表单样式优化 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: #2c3e50;
}

:deep(.el-select), :deep(.el-date-editor) {
  border-radius: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 卡片样式优化 */
:deep(.el-card) {
  border-radius: 16px;
  border: none;
  overflow: hidden;
}

:deep(.el-card__header) {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #f0f0f0;
  padding: 20px 24px;
}

:deep(.el-card__body) {
  padding: 24px;
}
</style> 