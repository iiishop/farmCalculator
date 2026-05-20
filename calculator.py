"""纯计算逻辑——无IO，可直接被CLI/GUI/API调用"""
import math
from models import Crop, Soil, FarmResult, MEALS, YEAR_DAYS


def optimal_layout(tiles: int) -> str:
    """计算最佳种植布局（最接近正方形）"""
    if tiles <= 0:
        return "无需种植"

    best_w, best_h = 1, tiles
    best_diff = float('inf')

    for w in range(1, min(int(tiles**0.5 * 2), tiles) + 1):
        h = math.ceil(tiles / w)
        diff = abs(w - h) + (w * h - tiles) * 0.1

        if diff < best_diff and w * h >= tiles:
            best_diff, best_w, best_h = diff, w, h

    if best_w == best_h:
        return f"{best_w}×{best_h}"
    return f"{best_w}×{best_h} (共{best_w * best_h}格)"


def calculate_farmland(crop: Crop, soil: Soil, population: int, growing_days: int) -> FarmResult:
    """计算农场需求和产出"""
    # 验证生长期
    crop_growth_days = crop.growth_days.get(soil.name)
    if crop_growth_days is None:
        raise ValueError(f"{crop.name}不能种植在{soil.display}")
    if crop_growth_days > growing_days:
        raise ValueError(
            f"{crop.name}需要{crop_growth_days}天生长期，但当前只有{growing_days}天"
        )

    # 计算产量
    effective_fertility = 1 + (soil.fertility - 1) * crop.fertility_sensitivity
    harvests = growing_days // crop_growth_days
    annual_yield = crop.base_yield * harvests * effective_fertility

    # 计算格数需求
    nutrition_needed = population * 1.6 * YEAR_DAYS
    tiles_needed = math.ceil(nutrition_needed / (annual_yield * 0.05) * 1.05)

    # 计算餐饮产出
    total_nutrition = annual_yield * tiles_needed * 0.05
    meal_data = {}

    for name, meal in MEALS.items():
        meals_count = int(total_nutrition // meal.input)
        nutrition_output = meals_count * meal.output
        supported = nutrition_output / (1.6 * YEAR_DAYS)

        meal_data[name] = {
            "total_meals": meals_count,
            "daily_meals": round(meals_count / YEAR_DAYS, 1),
            "supported_people": round(supported, 1),
        }

    return FarmResult(
        crop_name=crop.name,
        soil_name=soil.display,
        tiles=tiles_needed,
        harvests=harvests,
        layout=optimal_layout(tiles_needed),
        annual_yield=annual_yield * tiles_needed,
        meal_data=meal_data,
    )
