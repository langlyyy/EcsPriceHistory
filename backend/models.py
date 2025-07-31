from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RegionResponse(BaseModel):
    """地域响应模型"""
    region_id: str
    local_name: str


class ZoneResponse(BaseModel):
    """可用区响应模型"""
    zone_id: str
    local_name: str


class InstanceTypeResponse(BaseModel):
    """实例规格响应模型"""
    instance_type_id: str
    cpu_core_count: int
    memory_size: float


class SpotPriceHistoryRequest(BaseModel):
    """抢占式实例价格查询请求模型"""
    zone_id: str
    instance_types: List[str]
    network_type: str = "vpc"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    io_optimized: str = "optimized"
    os_type: str = "linux"
    include_pay_as_you_go: bool = False


class SpotPriceHistoryItem(BaseModel):
    """抢占式实例价格历史记录模型"""
    zone_id: str
    instance_type: str
    network_type: str
    spot_price: float
    pay_as_you_go_price: Optional[float] = None
    timestamp: str = ""
    io_optimized: str = "optimized"
    os_type: str = "linux"


class SpotPriceHistoryResponse(BaseModel):
    """抢占式实例价格历史响应模型"""
    success: bool
    message: str
    data: List[SpotPriceHistoryItem] = []


class ApiResponse(BaseModel):
    """通用API响应模型"""
    success: bool
    message: str
    data: Optional[dict] = None 