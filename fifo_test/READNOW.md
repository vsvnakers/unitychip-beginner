
# FIFO Test 卡死 / 失败问题：来龙去脉完整说明

## 一、项目背景

这是一个基于 **toffee** 的 **同步 FIFO（SyncFIFO）验证练习**，目标是：

* 用 **Bundle + Agent** 的方式
* 驱动 RTL 中的 `SyncFIFO`
* 通过 `pytest` 完成最基本的 smoke test

---

## 二、目录结构（当前实际结构）

```
fifo_test/
├── agent/
│   ├── __init__.py
│   └── fifo_agent.py        # FIFO 高层行为封装（Agent）
│
├── bundle/
│   ├── __init__.py
│   ├── write_bundle.py      # 写端 Bundle
│   ├── read_bundle.py       # 读端 Bundle
│   └── status_bundle.py     # full / empty Bundle
│
├── rtl/
│   └── SyncFIFO.v           # FIFO RTL
│
├── dut.py                   # create_dut()，实例化 RTL
├── test_smoke.py            # pytest 测试入口
├── pyproject.toml
└── README.md
```

---

## 三、测试的执行流程（**非常重要**）

### 1️⃣ 命令行执行

```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
pytest -v
```

---

### 2️⃣ pytest 入口

```python
# test_smoke.py
from dut import create_dut
from agent import FIFOAgent

def test_smoke_agent():
    dut = create_dut()
    agent = FIFOAgent(dut)

    assert agent.is_empty()

    agent.write_one(1)
    val = agent.read_one()
    assert val == 1
```

---

### 3️⃣ DUT 创建（关键点）

```python
# dut.py
def create_dut():
    dut = SyncFIFO(...)
    return dut
```

⚠️ **注意：**

* 这里并 **没有显式 reset 行为**
* reset 可能：

  * 已在 Verilog initial block
  * 或者是同步 reset，需要 clock 才生效

---

### 4️⃣ Agent 初始化流程（当前实际发生的）

```python
agent = FIFOAgent(dut)
```

进入：

```python
class FIFOAgent:
    def __init__(self, dut):
        self.status = StatusBundle()
        self.status.bind(dut)

        self._wait_empty_after_reset()
```

---

## 四、问题是怎么出现的（核心）

### ❌ 表面现象

pytest 报错：

```
RuntimeError: FIFO did not become empty after reset
```

或者：

```
assert agent.is_empty()  -> False
```

---

### ❌ 更严重的现象（之前出现过）

* pytest **卡住**
* 需要 `Ctrl + C`
* 输出：

```
KeyboardInterrupt
no tests ran in XXX seconds
```

---


