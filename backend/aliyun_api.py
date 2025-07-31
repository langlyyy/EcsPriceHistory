from typing import List, Dict, Any, Optional
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceTypesRequest import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526.DescribeSpotPriceHistoryRequest import DescribeSpotPriceHistoryRequest
import json
from datetime import datetime, timedelta
from config import ACCESS_KEY, ACCESS_SECRET, DEFAULT_REGION


class AliyunAPI:
    """阿里云API调用类"""
    
    def __init__(self, region_id: str = DEFAULT_REGION):
        """
        初始化阿里云API客户端
        
        Args:
            region_id: 地域ID，默认为杭州
        """
        self.client = AcsClient(ACCESS_KEY, ACCESS_SECRET, region_id)
        self.region_id = region_id
    
    def get_regions(self) -> List[Dict[str, str]]:
        """
        获取所有可用地域
        
        Returns:
            地域列表，包含region_id和local_name
        """
        try:
            request = DescribeRegionsRequest()
            response = self.client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            regions = []
            for region in response_json.get('Regions', {}).get('Region', []):
                regions.append({
                    'region_id': region.get('RegionId'),
                    'local_name': region.get('LocalName')
                })
            
            return regions
        except Exception as e:
            print(f"获取地域列表失败: {e}")
            return []
    
    def get_zones(self, region_id: str) -> List[Dict[str, str]]:
        """
        获取指定地域的可用区
        
        Args:
            region_id: 地域ID
            
        Returns:
            可用区列表，包含zone_id和local_name
        """
        try:
            # 临时切换到指定地域
            temp_client = AcsClient(ACCESS_KEY, ACCESS_SECRET, region_id)
            request = DescribeZonesRequest()
            response = temp_client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            zones = []
            for zone in response_json.get('Zones', {}).get('Zone', []):
                zones.append({
                    'zone_id': zone.get('ZoneId'),
                    'local_name': zone.get('LocalName')
                })
            
            return zones
        except Exception as e:
            print(f"获取可用区列表失败: {e}")
            return []
    
    def get_instance_types(self, region_id: str) -> List[Dict[str, str]]:
        """
        获取指定地域的实例规格
        
        Args:
            region_id: 地域ID
            
        Returns:
            实例规格列表，包含instance_type_id和cpu_core_count
        """
        try:
            # 临时切换到指定地域
            temp_client = AcsClient(ACCESS_KEY, ACCESS_SECRET, region_id)
            request = DescribeInstanceTypesRequest()
            response = temp_client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            instance_types = []
            for instance_type in response_json.get('InstanceTypes', {}).get('InstanceType', []):
                instance_types.append({
                    'instance_type_id': instance_type.get('InstanceTypeId'),
                    'cpu_core_count': instance_type.get('CpuCoreCount'),
                    'memory_size': instance_type.get('MemorySize')
                })
            
            return instance_types
        except Exception as e:
            print(f"获取实例规格列表失败: {e}")
            return []
    
    def get_spot_price_history(self,
                              zone_id: str,
                              instance_type: str,
                              network_type: str = "vpc",
                              start_time: Optional[str] = None,
                              end_time: Optional[str] = None,
                              io_optimized: str = "optimized",
                              os_type: str = "linux") -> List[Dict[str, Any]]:
        """
        获取抢占式实例历史价格
        
        Args:
            zone_id: 可用区ID
            instance_type: 实例规格
            network_type: 网络类型 (classic | vpc)
            start_time: 开始时间 (yyyy-MM-ddTHH:mm:ssZ格式)
            end_time: 结束时间 (yyyy-MM-ddTHH:mm:ssZ格式)
            io_optimized: 是否I/O优化 (optimized | none)
            os_type: 操作系统类型 (linux | windows)
            
        Returns:
            价格历史记录列表
        """
        try:
            # 如果没有指定时间，默认查询最近24小时
            if not start_time:
                start_time = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
            if not end_time:
                end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # 确保时间格式正确，移除可能存在的时区信息
            if start_time and not start_time.endswith('Z'):
                start_time = start_time.replace('+00:00', 'Z').replace('+08:00', 'Z')
            if end_time and not end_time.endswith('Z'):
                end_time = end_time.replace('+00:00', 'Z').replace('+08:00', 'Z')
            
            # 切换到可用区所在的地域
            zone_region = zone_id.split('-')[0] + '-' + zone_id.split('-')[1]
            temp_client = AcsClient(ACCESS_KEY, ACCESS_SECRET, zone_region)
            
            request = DescribeSpotPriceHistoryRequest()
            request.set_ZoneId(zone_id)
            request.set_InstanceType(instance_type)
            request.set_NetworkType(network_type)
            request.set_StartTime(start_time)
            request.set_EndTime(end_time)
            request.set_IoOptimized(io_optimized)
            request.set_OSType(os_type)
            
            response = temp_client.do_action_with_exception(request)
            response_json = json.loads(response)
            
            price_history = []
            for spot_price in response_json.get('SpotPrices', {}).get('SpotPriceType', []):
                price_history.append({
                    'zone_id': spot_price.get('ZoneId') or zone_id,
                    'instance_type': spot_price.get('InstanceType') or instance_type,
                    'network_type': spot_price.get('NetworkType') or network_type,
                    'spot_price': float(spot_price.get('SpotPrice', 0)),
                    'timestamp': spot_price.get('Timestamp') or '',
                    'io_optimized': spot_price.get('IoOptimized') or io_optimized,
                    'os_type': spot_price.get('OSType') or os_type
                })
            
            return price_history
        except Exception as e:
            print(f"获取抢占式实例价格历史失败: {e}")
            return [] 