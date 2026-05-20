# 边缘世界农场计算器

![版本](https://img.shields.io/badge/版本-1.0-blue)
![游戏版本](https://img.shields.io/badge/游戏版本-1.5.4069-orange)

RimWorld 农场规划工具。输入殖民者数量、作物类型、土地类型，算出需要多少格农田、怎么布局、能养活多少人。

## 使用

### 安装

```bash
pip install -r requirements.txt
```

### 三种入口

```bash
python main.py      # 命令行界面
python gui.py       # 图形界面（tkinter）
python api.py       # FastAPI + MCP 服务（http://localhost:8000）
```

### API / MCP

启动后访问 `http://localhost:8000/mcp`，任何兼容 MCP 的客户端（Claude Desktop、Cursor 等）都可以直接调用。

端点：

| 端点 | 方法 | 说明 |
|---|---|---|
| `/api/crops` | GET | 列出所有作物及可种植土地 |
| `/api/soils` | GET | 列出所有土地类型及肥力 |
| `/api/calculate` | POST | 核心计算，参数：`crop_id`, `soil_id`, `population`, `growing_days` |

Claude Desktop 配置示例：

```json
{
  "mcpServers": {
    "farmCalculator": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 数据

### 作物

- 土豆：基础产量 11，肥力敏感度 0.4
- 玉米：基础产量 22，肥力敏感度 1.0
- 水稻：基础产量 6，肥力敏感度 1.0

### 土地

- 沙砾地块：肥力 0.7
- 普通土地：肥力 1.0
- 肥沃土地：肥力 1.4
- 水栽培植物盆：肥力 2.8（玉米不可用）

### 食物

- 每位殖民者每天消耗 1.6 营养值
- 简单饭菜：0.5 食材 → 0.9 营养值
- 营养膏：0.3 食材 → 0.9 营养值

## 计算逻辑

```
effective_fertility = 1 + (土壤肥力 - 1) × 作物肥力敏感度
年产量 = 基础产量 × 年收获次数 × effective_fertility
所需格数 = ceil(总营养需求 / (年产量 × 0.05) × 1.05)
```

其中 `总营养需求 = 殖民者数量 × 1.6 × 60`，1.05 为 5% 安全冗余。布局优先接近正方形。

## 文件

```
models.py      数据模型和游戏配置
calculator.py  计算逻辑（纯函数，无 IO）
api.py         FastAPI + fastapi-mcp
main.py        命令行界面
gui.py         图形界面（tkinter）
```

## 限制

- 数据基于游戏版本 1.5.4069
- 计算仅考虑营养产出，未包含光照、温度、种植者技能等因素
- 结果含 5% 冗余，布局允许 10% 长宽差异

## 作者

吾之野望

有问题或建议欢迎提 issue。
