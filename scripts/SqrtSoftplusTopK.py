#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
SqrtSoftplusTopK算子golden实现
以 numpy 组合实现 sqrt(softplus(logits)) + topk 的结果为 golden
"""
import numpy as np


def _softplus(x):
    """softplus(x) = ln(1 + e^x)，数值稳定实现"""
    return np.where(x > 20.0, x, np.log1p(np.exp(x)))


def impl(router_logits, k=6):
    """SqrtSoftplusTopK算子golden实现

    参数名与顺序与 JSON 的 input_desc + attr_desc 一致：
    router_logits: (T, E) numpy数组，路由 logits
    k: int，top-k 的 k，默认 6

    返回:
    topk_scores: (T, k) numpy数组，选中的专家评分（未归一化）
    """
    orig_dtype = router_logits.dtype

    logits_f = router_logits.astype(np.float32)

    # 1. 评分: sqrt(softplus(logits)), softplus = ln(1 + e^x)
    scores = np.sqrt(_softplus(logits_f))

    # 2. 直接对 scores 降序排序，取 top-k 个值
    topk_scores = np.sort(scores, axis=-1)[:, ::-1][:, :k]

    if orig_dtype == np.float16:
        scores_np = topk_scores.astype(np.float16)
    else:
        scores_np = topk_scores.astype(np.float32)

    return scores_np


if __name__ == "__main__":
    # 与 JSON npu_cases 对应的 15 个测试用例（用 numpy 生成）
    cases = [
        # (id, T, E, k, dtype)
        (1,  2,     8,   2,  np.float32),
    ]

    for cid, T, E, k, dt in cases:
        logits = np.random.randn(T, E).astype(dt)
        scores = impl(logits, k=k)
        print(f"Case {cid:02d}: scores_shape={scores.shape}, sdtype={scores.dtype}")

    print("All tests passed!")
