import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas
from tkinter.font import Font
import math
import sys
import os
from PIL import Image, ImageTk, ImageDraw

# 从main.py导入所有数据模型、配置和计算函数
from importlib import import_module
import importlib.util

# 动态导入main.py模块
spec = importlib.util.spec_from_file_location(
    "farm_calc", os.path.join(os.path.dirname(__file__), "main.py"))
farm_calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(farm_calc)

# 从main.py中导入所有数据模型和计算函数
Crop = farm_calc.Crop
Soil = farm_calc.Soil
MealType = farm_calc.MealType
FarmResult = farm_calc.FarmResult
YEAR_DAYS = farm_calc.YEAR_DAYS
CROPS = farm_calc.CROPS
SOILS = farm_calc.SOILS
MEALS = farm_calc.MEALS
calculate_farmland = farm_calc.calculate_farmland
optimal_layout = farm_calc.optimal_layout

# === GUI应用程序 ===


class FarmCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("边缘世界农场工具")
        self.geometry("1000x700")
        self.minsize(900, 650)

        # 设置主题颜色
        self.bg_color = "#f0f0f0"
        self.accent_color = "#3498db"  # 蓝色
        self.success_color = "#2ecc71"  # 绿色
        self.warning_color = "#e74c3c"  # 红色
        self.heading_color = "#2c3e50"  # 深蓝色
        self.neutral_color = "#7f8c8d"  # 灰色

        # 加载和设置图标（如果存在）
        try:
            self.iconbitmap("farm_icon.ico")
        except:
            pass  # 如果图标不存在，忽略错误

        # 配置全局样式
        self.configure(bg=self.bg_color)
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用更现代的主题

        # 定义自定义样式
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure(
            "TLabel", background=self.bg_color, font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)

        # 定义主按钮样式
        self.style.configure("Accent.TButton",
                             background=self.accent_color,
                             foreground="white")
        self.style.map("Accent.TButton",
                       background=[('active', '#2980b9')])

        # 定义成功按钮样式
        self.style.configure("Success.TButton",
                             background=self.success_color,
                             foreground="white")
        self.style.map("Success.TButton",
                       background=[('active', '#27ae60')])

        # 定义标题和副标题样式
        self.style.configure("Heading.TLabel",
                             font=("Arial", 22, "bold"),
                             foreground=self.heading_color)
        self.style.configure("Subheading.TLabel",
                             font=("Arial", 16, "bold"),
                             foreground=self.heading_color)

        # 定义信息卡片样式
        self.style.configure("Card.TFrame",
                             background="white",
                             relief="flat",
                             borderwidth=0)

        # 创建主框架
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建界面组件
        self.create_widgets()

        # 默认显示主菜单
        self.show_main_menu()

    def create_widgets(self):
        """创建所有GUI组件"""
        # 创建顶部横幅
        self.banner_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        self.banner_frame.pack(fill=tk.X, padx=10, pady=10)

        # 在横幅中添加图标和标题
        banner_content = ttk.Frame(self.banner_frame, style="Card.TFrame")
        banner_content.pack(padx=20, pady=15)


        # 标题和版本信息
        title_frame = ttk.Frame(banner_content, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, padx=(15, 0))

        self.title_label = ttk.Label(
            title_frame,
            text="边缘世界农场工具",
            style="Heading.TLabel",
            background="white"
        )
        self.title_label.pack(anchor="w")

        self.version_label = ttk.Label(
            title_frame,
            text="作者：吾之野望 | 数据版本：1.5.4069",
            background="white",
            foreground=self.neutral_color
        )
        self.version_label.pack(anchor="w")

        # 创建内容框架 - 将根据当前界面动态填充
        self.content_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def clear_content(self):
        """清除内容框架中的所有组件"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """显示主菜单"""
        self.clear_content()

        # 创建卡片式菜单
        menu_frame = ttk.Frame(self.content_frame, style="TFrame")
        menu_frame.pack(expand=True, fill=tk.BOTH)

        # 欢迎卡片
        welcome_card = ttk.Frame(menu_frame, style="Card.TFrame")
        welcome_card.pack(fill=tk.X, padx=20, pady=10)

        # 欢迎信息
        welcome_content = ttk.Frame(welcome_card, style="Card.TFrame")
        welcome_content.pack(padx=20, pady=15)

        welcome_title = ttk.Label(
            welcome_content,
            text="欢迎使用边缘世界农场计算工具",
            font=("Arial", 18, "bold"),
            background="white",
            foreground=self.heading_color
        )
        welcome_title.pack(anchor="w", pady=(0, 10))

        welcome_text = ttk.Label(
            welcome_content,
            text="这个工具可以帮助您计算殖民地农场需求，优化作物种植布局，\n"
                 "并估算不同土地和作物组合下的餐饮产出。",
            background="white",
            foreground=self.neutral_color,
            wraplength=800
        )
        welcome_text.pack(anchor="w", pady=(0, 10))

        # 选项卡片
        options_frame = ttk.Frame(menu_frame)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 创建两列布局
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        # 计算选项卡片
        calc_card = ttk.Frame(options_frame, style="Card.TFrame")
        calc_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        calc_content = ttk.Frame(calc_card, style="Card.TFrame")
        calc_content.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        calc_title = ttk.Label(
            calc_content,
            text="进行农场计算",
            font=("Arial", 16, "bold"),
            background="white",
            foreground=self.heading_color
        )
        calc_title.pack(anchor="w", pady=(0, 10))

        calc_desc = ttk.Label(
            calc_content,
            text="计算殖民地的最佳农场布局，包括所需格数、\n"
                 "推荐布局、餐饮生产能力等。",
            background="white",
            foreground=self.neutral_color,
            wraplength=350,
            justify="left"
        )
        calc_desc.pack(anchor="w", pady=(0, 20))

        calculate_btn = ttk.Button(
            calc_content,
            text="开始计算",
            command=self.show_calculator,
            style="Accent.TButton",
            width=15
        )
        calculate_btn.pack(anchor="w")

        # 退出选项卡片
        exit_card = ttk.Frame(options_frame, style="Card.TFrame")
        exit_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        exit_content = ttk.Frame(exit_card, style="Card.TFrame")
        exit_content.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        exit_title = ttk.Label(
            exit_content,
            text="退出程序",
            font=("Arial", 16, "bold"),
            background="white",
            foreground=self.heading_color
        )
        exit_title.pack(anchor="w", pady=(0, 10))

        exit_desc = ttk.Label(
            exit_content,
            text="关闭农场计算工具。\n"
                 "您的计算结果不会被保存。",
            background="white",
            foreground=self.neutral_color,
            wraplength=350,
            justify="left"
        )
        exit_desc.pack(anchor="w", pady=(0, 20))

        exit_btn = ttk.Button(
            exit_content,
            text="退出程序",
            command=self.quit,
            width=15
        )
        exit_btn.pack(anchor="w")

    def show_calculator(self):
        """显示计算器界面"""
        self.clear_content()

        # 创建主容器 - 使用两列布局
        main_container = ttk.Frame(self.content_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.columnconfigure(0, weight=2)  # 输入表单区域
        main_container.columnconfigure(1, weight=3)  # 结果显示区域

        # === 左侧: 输入表单区域 ===
        form_card = ttk.Frame(main_container, style="Card.TFrame")
        form_card.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        form_content = ttk.Frame(form_card, style="Card.TFrame")
        form_content.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # 表单标题
        form_title = ttk.Label(
            form_content,
            text="输入计算参数",
            font=("Arial", 16, "bold"),
            background="white",
            foreground=self.heading_color
        )
        form_title.pack(anchor="w", pady=(0, 20))

        # 创建输入表单
        form_frame = ttk.Frame(form_content, style="Card.TFrame")
        form_frame.pack(fill=tk.X, padx=0, pady=0)

        # 殖民者数量
        pop_frame = ttk.Frame(form_frame, style="Card.TFrame")
        pop_frame.pack(fill=tk.X, pady=10)

        pop_label = ttk.Label(
            pop_frame,
            text="殖民者数量:",
            background="white",
            foreground=self.heading_color
        )
        pop_label.pack(side=tk.LEFT, padx=(0, 10))

        self.population = tk.StringVar(value="5")
        pop_entry = ttk.Entry(
            pop_frame,
            textvariable=self.population,
            width=8
        )
        pop_entry.pack(side=tk.LEFT)

        # 生长期天数
        days_frame = ttk.Frame(form_frame, style="Card.TFrame")
        days_frame.pack(fill=tk.X, pady=10)

        days_label = ttk.Label(
            days_frame,
            text="生长期天数:",
            background="white",
            foreground=self.heading_color
        )
        days_label.pack(side=tk.LEFT, padx=(0, 10))

        self.growing_days = tk.StringVar(value="60")
        days_entry = ttk.Entry(
            days_frame,
            textvariable=self.growing_days,
            width=8
        )
        days_entry.pack(side=tk.LEFT)

        # 作物选择
        crop_frame = ttk.Frame(form_frame, style="Card.TFrame")
        crop_frame.pack(fill=tk.X, pady=10)

        crop_label = ttk.Label(
            crop_frame,
            text="选择作物:",
            background="white",
            foreground=self.heading_color
        )
        crop_label.pack(side=tk.LEFT, padx=(0, 10))

        self.crop_var = tk.StringVar()
        crop_combobox = ttk.Combobox(
            crop_frame,
            textvariable=self.crop_var,
            width=15,
            state="readonly"
        )
        crop_combobox['values'] = [crop.name for crop in CROPS]
        crop_combobox.current(0)
        crop_combobox.pack(side=tk.LEFT)

        # 土地选择
        soil_frame = ttk.Frame(form_frame, style="Card.TFrame")
        soil_frame.pack(fill=tk.X, pady=10)

        soil_label = ttk.Label(
            soil_frame,
            text="选择土地:",
            background="white",
            foreground=self.heading_color
        )
        soil_label.pack(side=tk.LEFT, padx=(0, 10))

        self.soil_var = tk.StringVar()
        soil_combobox = ttk.Combobox(
            soil_frame,
            textvariable=self.soil_var,
            width=15,
            state="readonly"
        )
        soil_combobox['values'] = [soil.display for soil in SOILS]
        soil_combobox.current(0)
        soil_combobox.pack(side=tk.LEFT)

        # 按钮区域
        button_frame = ttk.Frame(form_content, style="Card.TFrame")
        button_frame.pack(fill=tk.X, pady=20)

        calculate_btn = ttk.Button(
            button_frame,
            text="计算",
            command=self.perform_calculation,
            style="Accent.TButton",
            width=10
        )
        calculate_btn.pack(side=tk.LEFT, padx=(0, 10))

        back_btn = ttk.Button(
            button_frame,
            text="返回主菜单",
            command=self.show_main_menu,
            width=12
        )
        back_btn.pack(side=tk.LEFT)

        # === 右侧: 结果显示区域 ===
        self.result_card = ttk.Frame(main_container, style="Card.TFrame")
        self.result_card.grid(row=0, column=1, padx=(
            10, 0), pady=0, sticky="nsew")

        self.result_content = ttk.Frame(self.result_card, style="Card.TFrame")
        self.result_content.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # 结果初始提示
        result_title = ttk.Label(
            self.result_content,
            text="计算结果",
            font=("Arial", 16, "bold"),
            background="white",
            foreground=self.heading_color
        )
        result_title.pack(anchor="w", pady=(0, 10))

        initial_msg = ttk.Label(
            self.result_content,
            text="请在左侧输入参数并点击计算按钮",
            background="white",
            foreground=self.neutral_color
        )
        initial_msg.pack(pady=50)

    def perform_calculation(self):
        """执行农场计算并以图形方式显示结果"""
        try:
            # 获取输入值
            population = int(self.population.get())
            growing_days = int(self.growing_days.get())

            # 验证输入范围
            if not (1 <= population <= 1000):
                raise ValueError("殖民者数量必须在1到1000之间")

            if not (1 <= growing_days <= 60):
                raise ValueError("生长期天数必须在1到60之间")

            # 获取选择的作物和土地
            crop_name = self.crop_var.get()
            soil_display = self.soil_var.get()

            crop = next((c for c in CROPS if c.name == crop_name), None)
            soil = next((s for s in SOILS if s.display == soil_display), None)

            if not crop or not soil:
                raise ValueError("请选择有效的作物和土地")

            # 执行计算 - 使用1.py中的计算函数
            result = calculate_farmland(crop, soil, population, growing_days)

            # 清除旧的结果内容
            for widget in self.result_content.winfo_children():
                widget.destroy()

            # 创建滚动区域以容纳结果
            result_canvas = Canvas(self.result_content,
                                   background="white",
                                   highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.result_content,
                                      orient="vertical",
                                      command=result_canvas.yview)

            result_canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # 创建可滚动的内容框架
            result_frame = ttk.Frame(result_canvas, style="Card.TFrame")
            result_canvas.create_window(
                (0, 0), window=result_frame, anchor="nw", tags="result_frame")

            # ===== 结果标题 =====
            result_title = ttk.Label(
                result_frame,
                text="计算结果",
                font=("Arial", 18, "bold"),
                background="white",
                foreground=self.heading_color
            )
            result_title.pack(anchor="w", pady=(0, 20))

            # ===== 基本信息卡片 =====
            basic_card = ttk.Frame(result_frame, style="Card.TFrame")
            basic_card.pack(fill=tk.X, pady=10)
            basic_card.configure(relief="solid", borderwidth=1)

            basic_title = ttk.Label(
                basic_card,
                text="基本信息",
                font=("Arial", 14, "bold"),
                background="white",
                foreground=self.heading_color
            )
            basic_title.pack(anchor="w", padx=15, pady=(10, 15))

            # 创建信息网格
            basic_grid = ttk.Frame(basic_card, style="Card.TFrame")
            basic_grid.pack(fill=tk.X, padx=15, pady=(0, 15))

            # 添加基本信息
            info_items = [
                ("作物：", result.crop_name, 0, 0),
                ("土地：", result.soil_name, 0, 1),
                ("年收获次数：", f"{result.harvests}次", 1, 0),
                ("所需格数：", f"{result.tiles}格 (含5%冗余)", 1, 1),
                ("推荐布局：", result.layout, 2, 0),
                ("总产量：", f"{result.annual_yield:.0f}单位", 2, 1)
            ]

            for label_text, value_text, row, col in info_items:
                label = ttk.Label(
                    basic_grid,
                    text=label_text,
                    background="white",
                    foreground=self.neutral_color
                )
                label.grid(row=row, column=col*2, sticky="w",
                           padx=(0 if col == 0 else 20, 5), pady=5)

                value = ttk.Label(
                    basic_grid,
                    text=value_text,
                    background="white",
                    foreground=self.heading_color,
                    font=("Arial", 10, "bold")
                )
                value.grid(row=row, column=col*2+1, sticky="w", pady=5)

            # 创建可视化的地块布局图
            self.create_layout_visualization(
                result_frame, result.tiles, result.layout)

            # ===== 餐饮生产卡片 =====
            meals_card = ttk.Frame(result_frame, style="Card.TFrame")
            meals_card.pack(fill=tk.X, pady=(20, 10))
            meals_card.configure(relief="solid", borderwidth=1)

            meals_title = ttk.Label(
                meals_card,
                text="餐饮生产能力",
                font=("Arial", 14, "bold"),
                background="white",
                foreground=self.heading_color
            )
            meals_title.pack(anchor="w", padx=15, pady=(10, 15))

            # 为每种餐饮类型创建一个卡片
            for meal_type, data in result.meal_data.items():
                meal_frame = ttk.Frame(meals_card, style="Card.TFrame")
                meal_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

                # 判断是否满足人口需求
                is_sufficient = data['supported_people'] >= population
                status_color = self.success_color if is_sufficient else self.warning_color
                status_text = "充足" if is_sufficient else "不足"

                # 餐饮类型和状态
                meal_header = ttk.Frame(meal_frame, style="Card.TFrame")
                meal_header.pack(fill=tk.X, pady=(0, 10))

                meal_type_label = ttk.Label(
                    meal_header,
                    text=meal_type,
                    font=("Arial", 12, "bold"),
                    background="white",
                    foreground=self.heading_color
                )
                meal_type_label.pack(side=tk.LEFT)

                status_label = ttk.Label(
                    meal_header,
                    text=status_text,
                    font=("Arial", 12, "bold"),
                    background="white",
                    foreground=status_color
                )
                status_label.pack(side=tk.RIGHT)

                # 创建进度条来显示支持人口百分比
                percent = min(100, data['supported_people'] / population * 100)

                progress_frame = ttk.Frame(meal_frame, style="Card.TFrame")
                progress_frame.pack(fill=tk.X, pady=(0, 10))

                progress_canvas = Canvas(
                    progress_frame,
                    height=24,
                    background="#f0f0f0",
                    highlightthickness=0
                )
                progress_canvas.pack(fill=tk.X)

                # 绘制进度条
                bar_color = self.success_color if is_sufficient else self.warning_color
                progress_canvas.create_rectangle(
                    0, 0,
                    progress_canvas.winfo_width() * percent / 100, 24,
                    fill=bar_color, width=0, tags="progress"
                )

                # 进度条文本
                text_x = progress_canvas.winfo_width() // 2
                progress_canvas.create_text(
                    text_x, 12,
                    text=f"{data['supported_people']}/{population} 人 ({percent:.1f}%)",
                    fill="white",
                    font=("Arial", 10, "bold"),
                    tags="progress_text"
                )

                # 更新进度条尺寸的事件
                def update_progress(event, canvas=progress_canvas, percent=percent):
                    canvas.delete("progress")
                    canvas.delete("progress_text")

                    width = event.width
                    # 绘制新的进度条
                    canvas.create_rectangle(
                        0, 0, width * percent / 100, 24,
                        fill=bar_color, width=0, tags="progress"
                    )

                    # 添加文本
                    canvas.create_text(
                        width // 2, 12,
                        text=f"{data['supported_people']}/{population} 人 ({percent:.1f}%)",
                        fill="white" if percent > 50 else self.heading_color,
                        font=("Arial", 10, "bold"),
                        tags="progress_text"
                    )

                progress_canvas.bind("<Configure>", update_progress)

                # 详细数据
                details_frame = ttk.Frame(meal_frame, style="Card.TFrame")
                details_frame.pack(fill=tk.X)

                details = [
                    ("全年总产量：", f"{data['total_meals']}份"),
                    ("日均生产：", f"{data['daily_meals']}份/天"),
                    ("供养能力：", f"{data['supported_people']}人")
                ]

                for i, (label_text, value_text) in enumerate(details):
                    label = ttk.Label(
                        details_frame,
                        text=label_text,
                        background="white",
                        foreground=self.neutral_color
                    )
                    label.grid(row=i, column=0, sticky="w", pady=2)

                    value = ttk.Label(
                        details_frame,
                        text=value_text,
                        background="white",
                        foreground=self.heading_color,
                        font=("Arial", 10, "bold")
                    )
                    value.grid(row=i, column=1, sticky="w", padx=5, pady=2)

                    if i == 2:  # 供养能力行
                        value.configure(foreground=status_color)

            # ===== 说明信息 =====
            note_frame = ttk.Frame(result_frame, style="Card.TFrame")
            note_frame.pack(fill=tk.X, pady=(10, 0))

            note_title = ttk.Label(
                note_frame,
                text="说明",
                font=("Arial", 12, "bold"),
                background="white",
                foreground=self.heading_color
            )
            note_title.pack(anchor="w")

            notes = [
                "• 此程序布局优先近似正方形，允许10%以内长宽差异",
                "• 已包含5%产量冗余，防止意外损失",
                "• 餐饮产出基于理想情况，实际生产中可能存在浪费"
            ]

            for note_text in notes:
                note = ttk.Label(
                    note_frame,
                    text=note_text,
                    background="white",
                    foreground=self.neutral_color,
                    wraplength=500
                )
                note.pack(anchor="w", pady=(5, 0))

            # 配置滚动区域
            result_frame.update_idletasks()
            result_canvas.config(scrollregion=result_canvas.bbox("all"))

            # 添加鼠标滚轮支持
            def _on_mousewheel(event):
                result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            result_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
        except Exception as e:
            messagebox.showerror("计算错误", f"发生错误：{str(e)}")

    def create_layout_visualization(self, parent_frame, tiles, layout_text):
        """创建农场布局的可视化展示"""
        # 解析布局文本获取宽度和高度
        w, h = None, None

        if "×" in layout_text:
            parts = layout_text.split("×")
            try:
                w = int(parts[0].strip())
                h_text = parts[1].split("(")[0].strip(
                ) if "(" in parts[1] else parts[1].strip()
                h = int(h_text)
            except:
                w, h = 1, tiles  # 默认为1×n布局
        else:
            w, h = 1, tiles

        # 创建布局可视化卡片
        layout_card = ttk.Frame(parent_frame, style="Card.TFrame")
        layout_card.pack(fill=tk.X, pady=10)
        layout_card.configure(relief="solid", borderwidth=1)

        layout_title = ttk.Label(
            layout_card,
            text="推荐种植布局",
            font=("Arial", 14, "bold"),
            background="white",
            foreground=self.heading_color
        )
        layout_title.pack(anchor="w", padx=15, pady=(10, 15))

        # 创建布局可视化
        layout_viz_frame = ttk.Frame(layout_card, style="Card.TFrame")
        layout_viz_frame.pack(padx=15, pady=(0, 15))

        # 计算合适的方格大小
        max_width = 500  # 可视化区域最大宽度
        max_height = 200  # 可视化区域最大高度

        # 单元格尺寸 (取决于网格大小，保持适当的比例)
        cell_size = min(max_width / w, max_height / h, 40)  # 最大单元格尺寸为40px

        # 创建Canvas来绘制布局网格
        layout_canvas = Canvas(
            layout_viz_frame,
            width=w * cell_size,
            height=h * cell_size,
            background="white",
            highlightthickness=1,
            highlightbackground="#e0e0e0"
        )
        layout_canvas.pack(padx=10, pady=10)

        # 绘制网格
        field_colors = ["#8BC34A", "#AED581", "#C5E1A5"]  # 不同深浅的绿色

        for row in range(h):
            for col in range(w):
                idx = row * w + col

                # 如果超出实际所需格数，使用不同颜色
                is_active = idx < tiles
                color = field_colors[idx % len(
                    field_colors)] if is_active else "#f0f0f0"

                # 绘制方格
                layout_canvas.create_rectangle(
                    col * cell_size, row * cell_size,
                    (col + 1) * cell_size, (row + 1) * cell_size,
                    fill=color,
                    outline="#dddddd" if is_active else "#e0e0e0"
                )

                # 如果格子足够大，添加坐标文本
                if cell_size >= 20 and is_active:
                    layout_canvas.create_text(
                        col * cell_size + cell_size / 2,
                        row * cell_size + cell_size / 2,
                        text=f"{idx+1}",
                        fill="#33691E" if is_active else "#9e9e9e",
                        font=("Arial", int(cell_size / 3))
                    )

        # 添加说明文字
        layout_info = ttk.Label(
            layout_viz_frame,
            text=f"总格数: {tiles}，布局: {w}×{h}" +
            (f" (需要{tiles}格，共{w*h}格)" if w*h > tiles else ""),
            background="white",
            foreground=self.neutral_color
        )
        layout_info.pack(pady=(5, 0))

        # 如果有额外格子，添加说明
        if w * h > tiles:
            extra_info = ttk.Label(
                layout_viz_frame,
                text=f"注: 浅色方格为额外格子，实际仅需{tiles}格。",
                background="white",
                foreground=self.neutral_color,
                font=("Arial", 9, "italic")
            )
            extra_info.pack(pady=(5, 0))


# 启动应用程序
if __name__ == "__main__":
    app = FarmCalculatorApp()
    app.mainloop()
