from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import uvicorn

from aliyun_api import AliyunAPI
from models import (
    RegionResponse, ZoneResponse, InstanceTypeResponse,
    SpotPriceHistoryRequest, SpotPriceHistoryItem, SpotPriceHistoryResponse, ApiResponse
)
from config import HOST, PORT, DEBUG, ALLOWED_ORIGINS

# 创建FastAPI应用
app = FastAPI(
    title="阿里云抢占式实例价格查询API",
    description="提供阿里云抢占式实例历史价格查询服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化阿里云API客户端
aliyun_api = AliyunAPI()


@app.get("/", response_model=ApiResponse)
async def root():
    """根路径，返回API信息"""
    return ApiResponse(
        success=True,
        message="阿里云抢占式实例价格查询API服务运行正常",
        data={
            "version": "1.0.0",
            "endpoints": {
                "regions": "/api/regions",
                "zones": "/api/zones/{region_id}",
                "instance_types": "/api/instance-types/{region_id}",
                "spot_price_history": "/api/spot-price-history"
            }
        }
    )


@app.get("/api/regions", response_model=List[RegionResponse])
async def get_regions():
    """获取所有可用地域"""
    try:
        regions = aliyun_api.get_regions()
        return [RegionResponse(**region) for region in regions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取地域列表失败: {str(e)}")


@app.get("/api/zones/{region_id}", response_model=List[ZoneResponse])
async def get_zones(region_id: str):
    """获取指定地域的可用区"""
    try:
        zones = aliyun_api.get_zones(region_id)
        return [ZoneResponse(**zone) for zone in zones]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取可用区列表失败: {str(e)}")


@app.get("/api/instance-types/{region_id}", response_model=List[InstanceTypeResponse])
async def get_instance_types(region_id: str):
    """获取指定地域的实例规格"""
    try:
        instance_types = aliyun_api.get_instance_types(region_id)
        return [InstanceTypeResponse(**instance_type) for instance_type in instance_types]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取实例规格列表失败: {str(e)}")


@app.post("/api/spot-price-history", response_model=SpotPriceHistoryResponse)
async def get_spot_price_history(request: SpotPriceHistoryRequest):
    """获取抢占式实例历史价格"""
    try:
        all_price_history = []
        
        for instance_type in request.instance_types:
            price_history = aliyun_api.get_spot_price_history(
                zone_id=request.zone_id,
                instance_type=instance_type,
                network_type=request.network_type,
                start_time=request.start_time,
                end_time=request.end_time,
                io_optimized=request.io_optimized,
                os_type=request.os_type,
                include_pay_as_you_go=request.include_pay_as_you_go
            )
            all_price_history.extend(price_history)
        
        return SpotPriceHistoryResponse(
            success=True,
            message=f"成功获取{len(request.instance_types)}个实例规格的价格历史",
            data=[SpotPriceHistoryItem(**item) for item in all_price_history]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取价格历史失败: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    ) 