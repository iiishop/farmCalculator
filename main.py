"""farmCalculator CLI 入口 —— 边缘世界农场计算器"""
from models import CROPS, SOILS
from calculator import calculate_farmland

# === 终端颜色定义 ===


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


# === 用户界面函数 ===


def select_from_menu(items, title):
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


def get_number_input(prompt, min_val, max_val):
    """获取数字输入并验证范围"""
    while True:
        try:
            value = int(input(f"{Color.GREEN}{prompt}{Color.RESET}"))
            if min_val <= value <= max_val:
                return value
            print(f"{Color.RED}错误：请输入{min_val}-{max_val}之间的整数{Color.RESET}")
        except ValueError:
            print(f"{Color.RED}错误：请输入有效数字{Color.RESET}")


def display_results(result, population):
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
        print(f"  全年总量：{Color.BRIGHT_WHITE}{data['total_meals']}份{Color.RESET}")
        print(f"  日均生产：{Color.BRIGHT_WHITE}{data['daily_meals']}份/天{Color.RESET}")

        support_color = Color.BRIGHT_GREEN if is_sufficient else Color.BRIGHT_RED
        print(f"  供养能力：{support_color}{data['supported_people']}人{Color.RESET}")

    print(f"\n{Color.MAGENTA}说明{Color.RESET}")
    print(f"{Color.MAGENTA}- 此程序布局优先近似正方形，允许10%以内长宽差异{Color.RESET}")
    print(f"{Color.MAGENTA}- 已包含5%产量冗余，防止意外损失{Color.RESET}")


# === 主程序 ===


def run_calculator():
    """运行农场计算器主功能"""
    try:
        population = get_number_input("\n请输入殖民者数量: ", 1, 1000)
        growing_days = get_number_input("请输入生长期天数 (1-60): ", 1, 60)

        crop = select_from_menu(CROPS, "选择作物")
        soil = select_from_menu(SOILS, "选择土地类型")

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
    """主程序入口"""
    print(f"\n{Color.BOLD}{Color.BRIGHT_CYAN}=== 边缘世界农场工具 ==={Color.RESET}")
    print(f"{Color.BRIGHT_MAGENTA}作者：吾之野望 | 数据版本：1.5.4069{Color.RESET}")

    while True:
        choice = show_main_menu()
        if choice == 1:
            run_calculator()
            print(f"\n{Color.GREEN}计算完成，按回车键返回主菜单...{Color.RESET}")
            input()
        elif choice == 2:
            print(f"\n{Color.BRIGHT_YELLOW}感谢使用边缘世界农场工具，再见！{Color.RESET}")
            break


if __name__ == "__main__":
    main()
