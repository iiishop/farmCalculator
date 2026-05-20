"""farmCalculator API —— FastAPI + MCP 端点"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi_mcp import FastApiMCP

from models import CROPS, SOILS, MEALS
from calculator import calculate_farmland


app = FastAPI(
    title="边缘世界农场计算器 API",
    description="RimWorld 农场规划工具——计算种植面积、布局和餐饮产出",
    version="1.0.0",
)


class CalculateRequest(BaseModel):
    crop_id: int = Field(..., ge=1, le=3, description="作物ID: 1=土豆, 2=玉米, 3=水稻")
    soil_id: int = Field(..., ge=1, le=4, description="土地ID: 1=沙砾, 2=普通, 3=肥沃, 4=水培")
    population: int = Field(..., ge=1, le=1000, description="殖民者数量")
    growing_days: int = Field(..., ge=1, le=60, description="生长期天数（游戏年天数，默认60）")


@app.get("/api/crops")
def list_crops():
    """列出所有可用作物及其属性"""
    return [
        {
            "id": c.id,
            "name": c.name,
            "fertility_sensitivity": c.fertility_sensitivity,
            "base_yield": c.base_yield,
            "supported_soils": [
                soil_name for soil_name, days in c.growth_days.items() if days is not None
            ],
        }
        for c in CROPS
    ]


@app.get("/api/soils")
def list_soils():
    """列出所有土地类型及其肥力"""
    return [
        {"id": s.id, "name": s.name, "display": s.display, "fertility": s.fertility}
        for s in SOILS
    ]


@app.post("/api/calculate")
def api_calculate(req: CalculateRequest):
    """
    计算农场需求。

    根据殖民者数量、作物类型、土地类型和生长期，
    返回所需种植格数、最佳布局、年产量和餐饮供养能力。
    """
    crop = next((c for c in CROPS if c.id == req.crop_id), None)
    soil = next((s for s in SOILS if s.id == req.soil_id), None)

    if crop is None:
        raise HTTPException(status_code=404, detail=f"作物ID {req.crop_id} 不存在")
    if soil is None:
        raise HTTPException(status_code=404, detail=f"土地ID {req.soil_id} 不存在")

    try:
        result = calculate_farmland(crop, soil, req.population, req.growing_days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "crop_name": result.crop_name,
        "soil_name": result.soil_name,
        "tiles": result.tiles,
        "harvests": result.harvests,
        "layout": result.layout,
        "annual_yield": round(result.annual_yield, 1),
        "meal_data": result.meal_data,
    }


# 挂载 MCP —— 所有端点自动暴露为 MCP tools
mcp = FastApiMCP(app)
mcp.mount()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
