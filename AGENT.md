# 项目协作约定

## 目标与依据

实现 Ascend C SqrtSoftplusTopK 高性能算子，以 `doc/题目.md` 为需求来源，`doc/实施草案.md` 为当前设计。先确保精度，再优化耗时。

## 不可改变的计算契约

- 输入二维 ND，float16/float32；T ∈ [1,131072]，E ∈ [64,1024]，允许非 2 的幂。
- k 默认 6，范围 [1,64] 且 k ≤ E。输出 (T,k)，类型同输入，按分数降序，仅含未归一化分数。
- softplus、sqrt 均用 FP32；x > 20 时 softplus 取 x；处理大负数时保护有效精度。
- 不输出专家 ID，不添加 softmax、sigmoid 或归一化；不自行扩展 bfloat16/int32 支持。
- 先选 logits 再评分是候选优化，必须对照完整评分参考实现验证后采用。

## 开发方式

- 修改前读取相关源码和草案。保留原题，不修改题目来适配实现。
- host 放 `op_host/`，device 放 `op_kernel/`，Python 工具放 `src/cann_competition/`。
- 未确认 NPU 型号、CANN/编译器版本及提交格式前，不编造 API、构建成功或设备性能。接入时使用对应版本的官方文档与官方工程模板。
- 不将 Python 参考实现或 CPU 示例称为 NPU 算子；不把跳过的测试称为通过。
- 每次算法修改检查随机输入、重复值、大正负数、20 附近、k=1/64、两种 dtype、全部 E。
- 性能记录必须包含硬件、软件版本、shape/dtype/k、预热与重复次数、计时方式及精度结果。
- 不提交缓存、设备安装包或大体积数据。不得擅自提交比赛、推送或发布。

## 验证入口

`uv run cann-competition --smoke`；`uv run python -m unittest discover -s tests -v`。
FP32 参考检查需要先安装 reference extra；没有 torch 时测试会明确 skip。

## 完成报告

说明修改内容、实际执行的检查、未执行的设备验证和剩余依赖。后续工程进度更新到实施草案。

参考资料：

- 昇腾文档： https://www.hiascend.com/document?tab=document

## 新模板目录约定（2026-10-14，优先于旧布局）

用户已将旧代码迁至 old/，当前实现须遵循根目录 kernel.asc、main.asc、scripts/ 和 run.sh 模板。保留 run_kernel 的调用协议；kernel.asc 为被包含文件，不添加 main 或头文件保护。C++ 接口采用 Doxygen 注释，Python 使用参数/返回/异常 docstring。设备编译与精度未实际执行时必须明确标注，不得将 NumPy 数值模型测试称为 kernel 测试通过。

## 用户修正后的开发边界

run.sh 不得修改；scripts/ 保持原模板的数据、golden 和验证规则。当前算子工作集中在 kernel.asc，main.asc 保留原调用模板。不再新增元数据协议或用 Python/CPU 模型替代 Ascend C 设备实现与验证。
