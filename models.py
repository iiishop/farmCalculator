"""farmCalculator 数据模型和游戏配置数据"""
from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass
class Crop:
    id: int
    name: str
    fertility_sensitivity: float
    base_yield: float
    growth_days: Dict[str, Optional[float]]


@dataclass
class Soil:
    id: int
    name: str
    display: str
    fertility: float


@dataclass
class MealType:
    input: float
    output: float


@dataclass
class FarmResult:
    crop_name: str
    soil_name: str
    tiles: int
    harvests: int
    layout: str
    annual_yield: float
    meal_data: Dict[str, Dict[str, Union[int, float]]]


# === 游戏常量 ===
YEAR_DAYS = 60  # 游戏年总天数

# === 作物数据 ===
CROPS = [
    Crop(1, "土豆", 0.4, 11, {"沙砾": 12.17, "普通": 10.71, "肥沃": 9.23, "水培": 6.23}),
    Crop(2, "玉米", 1.0, 22, {"沙砾": 29.8, "普通": 20.86, "肥沃": 14.9, "水培": None}),
    Crop(3, "水稻", 1.0, 6, {"沙砾": 7.91, "普通": 5.54, "肥沃": 3.96, "水培": 1.98}),
]

# === 土地数据 ===
SOILS = [
    Soil(1, "沙砾", "沙砾地块", 0.7),
    Soil(2, "普通", "普通土地", 1.0),
    Soil(3, "肥沃", "肥沃土地", 1.4),
    Soil(4, "水培", "水栽培植物盆", 2.8),
]

# === 餐饮数据 ===
MEALS = {
    "简单饭菜": MealType(0.5, 0.9),
    "营养膏": MealType(0.3, 0.9),
}
