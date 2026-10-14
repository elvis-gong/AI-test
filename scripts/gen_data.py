import numpy as np
import os
import sys

try:
    from ml_dtypes import bfloat16
except ImportError:
    bfloat16 = None

sys.path.insert(0, os.path.dirname(__file__))
from SqrtSoftplusTopK import impl

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)


# --- Case 0 ---
np.random.seed(42 + 0)
os.makedirs("input/case0", exist_ok=True)
router_logits = np.random.uniform(low=-5.0, high=5.0, size=(8, 64)).astype(np.float32)
router_logits.tofile("input/case0/router_logits.bin")

k = 4

os.makedirs("output/golden_case0", exist_ok=True)
golden = impl(router_logits, k=k)
if golden is not None:
    golden.tofile("output/golden_case0/golden_topk_scores.bin")

print(f"Generated test data and golden output for 1 cases.")
