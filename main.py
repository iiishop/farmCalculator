import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

# === 终端颜色定义 ===


class Color:
    # 基本颜色
    RESET = "\033[0m"  # 重置所有颜色和样式
    BOLD = "\033[1m"  # 粗体

    # 前景色（文字颜色）
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # 明亮的前景色
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

# === 数据模型 ===


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


# === 配置数据 ===
YEAR_DAYS = 60  # 游戏年总天数

# 使用常量定义配置数据
CROPS = [
    Crop(1, "土豆", 0.4, 11, {"沙砾": 12.17, "普通": 10.71, "肥沃": 9.23, "水培": 6.23}),
    Crop(2, "玉米", 1.0, 22, {"沙砾": 29.8, "普通": 20.86, "肥沃": 14.9, "水培": None}),
    Crop(3, "水稻", 1.0, 6, {"沙砾": 7.91, "普通": 5.54, "肥沃": 3.96, "水培": 1.98})
]

SOILS = [
    Soil(1, "沙砾", "沙砾地块", 0.7),
    Soil(2, "普通", "普通土地", 1.0),
    Soil(3, "肥沃", "肥沃土地", 1.4),
    Soil(4, "水培", "水栽培植物盆", 2.8)
]

MEALS = {
    "简单饭菜": MealType(0.5, 0.9),
    "营养膏": MealType(0.3, 0.9)
}

# === 计算函数 ===


def calculate_farmland(crop: Crop, soil: Soil, population: int, growing_days: int) -> FarmResult:
    """计算农场需求和产出"""
    # 验证生长期
    crop_growth_days = crop.growth_days.get(soil.name)
    if crop_growth_days is None:
        raise ValueError(f"{crop.name}不能种植在{soil.display}")
    if crop_growth_days > growing_days:
        raise ValueError(
            f"{crop.name}需要{crop_growth_days}天生长期，但当前只有{growing_days}天")

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
            "supported_people": round(supported, 1)
        }

    return FarmResult(
        crop_name=crop.name,
        soil_name=soil.display,
        tiles=tiles_needed,
        harvests=harvests,
        layout=optimal_layout(tiles_needed),
        annual_yield=annual_yield * tiles_needed,
        meal_data=meal_data
    )


def optimal_layout(tiles: int) -> str:
    """计算最佳种植布局"""
    if tiles <= 0:
        return "无需种植"

    # 找到最接近正方形的布局
    best_w, best_h = 1, tiles
    best_diff = float('inf')

    for w in range(1, min(int(tiles**0.5 * 2), tiles) + 1):
        h = math.ceil(tiles / w)
        diff = abs(w - h) + (w * h - tiles) * 0.1

        if diff < best_diff and w * h >= tiles:
            best_diff, best_w, best_h = diff, w, h

    # 格式化输出
    return f"{best_w}×{best_h}" if best_w == best_h else f"{best_w}×{best_h} (共{best_w*best_h}格)"

# === 用户界面函数 ===


def select_from_menu(items: List[Union[Crop, Soil]], title: str) -> Union[Crop, Soil]:
    """显示选择菜单并返回选择"""
    print(f"\n{Color.BOLD}{Color.CYAN}=== {title} ==={Color.RESET}")
    for item in items:
        name = getattr(item, 'display', item.name)
        print(f"{Color.YELLOW}{item.id}.{Color.RESET} {name}")

    while True:
        try:
            choice = int(input(f"{Color.GREEN}请选择编号: {Color.RESET}"))
            selected = next((x for x in items if x.id == choice), None)
            if selected:
                return selected
            print(f"{Color.RED}错误：无效编号，请重新输入{Color.RESET}")
        except ValueError:
            print(f"{Color.RED}错误：请输入数字{Color.RESET}")


def get_number_input(prompt: str, min_val: int, max_val: int) -> int:
    """获取数字输入并验证范围"""
    while True:
        try:
            value = int(input(f"{Color.GREEN}{prompt}{Color.RESET}"))
            if min_val <= value <= max_val:
                return value
            print(f"{Color.RED}错误：请输入{min_val}-{max_val}之间的整数{Color.RESET}")
        except ValueError:
            print(f"{Color.RED}错误：请输入有效数字{Color.RESET}")


def display_results(result: FarmResult, population: int):
    """显示计算结果"""
    print(f"\n{Color.BOLD}{Color.CYAN}=== 种植数据 ==={Color.RESET}")
    print(f"{Color.BOLD}作物：{Color.BRIGHT_YELLOW}{result.crop_name}{Color.RESET}")
    print(f"{Color.BOLD}土地：{Color.BRIGHT_YELLOW}{result.soil_name}{Color.RESET}")
    print(f"{Color.BOLD}年收获次数：{Color.BRIGHT_WHITE}{result.harvests}次{Color.RESET}")
    print(f"{Color.BOLD}所需格数：{Color.BRIGHT_WHITE}{result.tiles}格{Color.RESET}（含5%冗余）")
    print(f"{Color.BOLD}推荐布局：{Color.BRIGHT_WHITE}{result.layout}{Color.RESET}")

    print(f"\n{Color.BOLD}{Color.CYAN}=== 餐饮生产 ==={Color.RESET}")
    for meal_type, data in result.meal_data.items():
        is_sufficient = data['supported_people'] >= population
        status_color = Color.BRIGHT_GREEN if is_sufficient else Color.BRIGHT_RED
        status = "充足" if is_sufficient else "不足"
        print(f"\n{Color.BOLD}{meal_type} {status_color}{status}{Color.RESET}")
        print(
            f"  全年总量：{Color.BRIGHT_WHITE}{data['total_meals']}份{Color.RESET}")
        print(
            f"  日均生产：{Color.BRIGHT_WHITE}{data['daily_meals']}份/天{Color.RESET}")

        # 为人口支持能力添加颜色
        support_color = Color.BRIGHT_GREEN if is_sufficient else Color.BRIGHT_RED
        print(
            f"  供养能力：{support_color}{data['supported_people']}人{Color.RESET}")

    print(f"\n{Color.MAGENTA}说明{Color.RESET}")
    print(f"{Color.MAGENTA}- 此程序布局优先近似正方形，允许10%以内长宽差异{Color.RESET}")
    print(f"{Color.MAGENTA}- 已包含5%产量冗余，防止意外损失{Color.RESET}")

# === 主程序 ===


def run_calculator():
    """运行农场计算器主功能"""
    try:
        # 用户输入
        population = get_number_input("\n请输入殖民者数量: ", 1, 1000)
        growing_days = get_number_input("请输入生长期天数 (1-60): ", 1, 60)

        # 菜单选择
        crop = select_from_menu(CROPS, "选择作物")
        soil = select_from_menu(SOILS, "选择土地类型")

        # 计算并显示结果
        result = calculate_farmland(crop, soil, population, growing_days)
        display_results(result, population)

    except Exception as e:
        print(f"\n{Color.RED}发生错误：{str(e)}{Color.RESET}")


def show_main_menu():
    """显示主菜单"""
    print(f"\n{Color.BOLD}{Color.CYAN}=== 边缘世界农场工具主菜单 ==={Color.RESET}")
    print(f"{Color.YELLOW}1. {Color.BRIGHT_WHITE}进行农场计算{Color.RESET}")
    print(f"{Color.YELLOW}2. {Color.BRIGHT_WHITE}退出程序{Color.RESET}")

    while True:
        try:
            choice = int(input(f"\n{Color.GREEN}请选择操作: {Color.RESET}"))
            if choice in [1, 2]:
                return choice
            print(f"{Color.RED}错误：无效选择，请输入1或2{Color.RESET}")
        except ValueError:
            print(f"{Color.RED}错误：请输入数字{Color.RESET}")


def main():
    """主程序入口 - 命令模式循环"""
    print(f"\n{Color.BOLD}{Color.BRIGHT_CYAN}=== 边缘世界农场工具 ==={Color.RESET}")
    print(f"{Color.BRIGHT_MAGENTA}作者：吾之野望 | 数据版本：1.5.4069{Color.RESET}")

    while True:
        choice = show_main_menu()

        if choice == 1:
            # 运行计算器
            run_calculator()
            print(f"\n{Color.GREEN}计算完成，按回车键返回主菜单...{Color.RESET}")
            input()
        elif choice == 2:
            # 退出程序
            print(f"\n{Color.BRIGHT_YELLOW}感谢使用边缘世界农场工具，再见！{Color.RESET}")
            break


if __name__ == "__main__":
    main()
