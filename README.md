### Picker 对同步 FIFO（SyncFIFO）进行基础验证的示例。

##### 主要验证内容包括：

* 复位行为是否正确
* 复位后 FIFO 状态是否初始化为预期值
* FIFO 的基本读写功能（冒烟测试）

目录结构说明：

* rtl/SyncFIFO.v
  同步 FIFO 的 RTL 设计代码
* test_smoke.py
  测试脚本，包含 reset 测试、assert 检查以及冒烟测试
* SyncFIFO/
  由 picker 自动生成的 DUT 目录（无需手动修改）

---

运行步骤如下：

第一步：生成 DUT
在 fifo_test 目录下执行一次即可：

picker export rtl/SyncFIFO.v --sname SyncFIFO --lang python --sim verilator -w SyncFIFO.fst

这一步会自动生成 SyncFIFO 目录，用于 Python 驱动仿真。

---

第二步：运行测试
在 fifo_test 目录下执行：

python test_smoke.py

如果运行正常，终端会依次输出：

* Reset test (default) finished
* Reset test (imme) finished
* Reset assert test passed
* Smoke test passed!

---

第三步：查看波形
测试过程中会生成 fst 波形文件（如 smoke.fst），可使用 GTKWave 查看：

