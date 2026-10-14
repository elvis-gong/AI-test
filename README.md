# SqrtSoftplusTopK Ascend C 工程

当前使用提供的直接调用模板。旧原型在 old/。需求见 [题目](docs/题目.md)，实现与验收清单见 [开发清单](docs/开发清单.md)，效率改动见 [性能优化记录](docs/性能优化记录.md)。

## 修改范围

算子实现集中在 kernel.asc。main.asc、run.sh、CMakeLists.txt、data_utils.h 和 scripts/ 保持 Git HEAD 模板状态。没有元数据文件依赖，也没有更改输入生成、golden 或验证规则。

## Ascend C 实现

run_kernel 检查张量描述并启动 float/half 的 vector-core kernel。每核处理互不重叠的 token 行，k=1 使用一至两级 WholeReduceMax，其他 k 使用 Sort32 与精确的截断归并 top-k：每个中间有序段只保留足够的候选值。评分均使用设备 FP32 矢量指令，最后转换为输入 dtype。

x>20 时直接取 x；x<-2 时使用八项 log1p 级数避免消减误差。输出用 DataCopyPad 按实际字节长度写出，覆盖 k=1/6 等非对齐情况。代码包含 Doxygen 注释及显式流水同步。

选择阶段已移除 O(E*k) 的标量插入循环，改用设备排序与归并。普通区间评分跳过多项式，全大正数只执行 sqrt；FP32 输出复用评分缓冲区。

用户反馈单行优化版 15 个测试点全部 Pass，按展示耗时估算均分约 20.16。当前候选统一为一套自适应 1–16 行 tile 实现；k=1 在编译期选择归约模式，移除重复单行/批处理实现。DMA 和归并参数在初始化阶段准备，padding 只初始化一次，FP32 直接复用输入 UB。张量内存不超过 120 KiB/核。

## 运行

在模板对应的 Linux CANN 环境设置 ASCEND_HOME_PATH 后执行原入口：

```bash
bash run.sh
```

原入口只运行模板 case0：(T,E)=(8,64)、k=4、float32。FP16 和其他 shape/k 仍需要设备验证。没有 CASE_ID 或额外元数据参数。

当前 Windows 环境缺少 CANN 和 NPU，尚未进行本轮截断归并版 ASC 编译、设备精度和性能验证。同步 CPU API 模型检查覆盖实际 Kernel 类、多行搬运、截断归并和中间选中值；模型不能验证真实设备指令、异步同步或 DMA 行为。各轮记录见性能优化文档。
