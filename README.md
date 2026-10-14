# SqrtSoftplusTopK 昇腾算子竞赛

目标：使用 Ascend C 实现每行 `sqrt(softplus(logits))` 的降序 top-k，只输出分数。原题见 [doc/题目.md](doc/题目.md)，题目解读及设计见 [实施草案](doc/实施草案.md)，协作规则见 [AGENT.md](AGENT.md)。

## 当前状态

新增可编译的 C++ FP32 小根堆算法原型与 host 行调度模型，代码及验证命令见 [开发清单](doc/开发清单.md)。原型目录为 `reference/cpp/`，尚未接入 NPU。

已建立 Python 工具、输入约束、PyTorch FP32 参考实现、候选优化验证和 host/device 目录。尚未接入 CANN、实现 NPU kernel 或测量设备性能。

## 本地运行

保留现有 Python 3.14 与 uv 工程配置。基础工具无需运行时第三方依赖：

```powershell
uv sync
uv run cann-competition --smoke
uv run python -m unittest discover -s tests -v
```

参考实现需要 PyTorch，请在 PyTorch 支持的 Python/平台环境中安装：

```powershell
uv sync --extra reference
uv run python -m unittest discover -s tests -v
```

昇腾运行环境的 Python 版本应依据实际 CANN/torch_npu 兼容性单独确定，现有配置不代表设备兼容性已经验证。未安装 torch 时，数值测试明确跳过，基础约束测试仍可运行。

如果网络不可用，可直接从源码运行基础检查：

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
python -m unittest discover -s tests -v
python -c "from cann_competition import main; import sys; sys.argv=['cann-competition','--smoke']; main()"
```

本次初始化的源码检查已通过；`uv sync` 因默认缓存访问受限失败，改用 `--cache-dir .uv-cache` 后创建了虚拟环境，但受网络限制未完成依赖解析/安装，也未生成锁文件。uv 会解析可选依赖，即使基础运行不需要 torch，也可能访问其包索引。

## 目录

| 路径 | 用途 |
| --- | --- |
| doc/ | 原题及实施草案 |
| src/cann_competition/ | 约束、参考实现、CLI |
| op_host/ | 待接入注册和 tiling |
| op_kernel/ | 待实现 Ascend C kernel |
| tests/ | 约束和候选优化数值验证 |
| benchmarks/ | 设备性能记录约定 |

下一步需要目标 NPU 型号、CANN 版本、官方提交工程模板及测试/计时入口。
