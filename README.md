# SqrtSoftplusTopK Ascend C 工程

当前使用提供的直接调用模板。旧原型在 old/。需求见 [题目](docs/题目.md)，实现与验收清单见 [开发清单](docs/开发清单.md)，效率改动见 [性能优化记录](docs/性能优化记录.md)。

## 修改范围

算子实现集中在 kernel.asc。main.asc、run.sh、CMakeLists.txt、data_utils.h 和 scripts/ 保持 Git HEAD 模板状态。没有元数据文件依赖，也没有更改输入生成、golden 或验证规则。

## Ascend C 实现

run_kernel 检查张量描述并启动 float/half 的 vector-core kernel。每核处理互不重叠的 token 行，k=1 使用 ReduceMax，其他 k 使用 Sort32 和分级 MrgSort，提取前 k 个 logits 后评分。评分在设备上通过 AscendC 矢量指令完成，全部使用 FP32，最后转换为输入 dtype。

x>20 时直接取 x；x<-2 时使用八项 log1p 级数避免消减误差。输出用 DataCopyPad 按实际字节长度写出，覆盖 k=1/6 等非对齐情况。代码包含 Doxygen 注释及显式流水同步。

选择阶段已移除 O(E*k) 的标量插入循环，改用设备排序与归并。普通区间评分跳过多项式，全大正数只执行 sqrt；FP32 输出复用评分缓冲区。尚无优化版设备性能结论。

## 运行

在模板对应的 Linux CANN 环境设置 ASCEND_HOME_PATH 后执行原入口：

```bash
bash run.sh
```

原入口只运行模板 case0：(T,E)=(8,64)、k=4、float32。FP16 和其他 shape/k 仍需要设备验证。没有 CASE_ID 或额外元数据参数。

当前 Windows 环境缺少 CANN 和 NPU，尚未进行优化版 ASC 编译、设备精度和性能验证。实际 Kernel 类在同步 CPU API 模型下通过 2090 组检查；模型不能验证真实设备指令、异步同步或 DMA 行为。
