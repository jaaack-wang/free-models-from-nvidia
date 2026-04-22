# free-models-from-nvidia

English | [中文](#中文说明)

A small Python repo for testing which NVIDIA Build free models are currently callable with your NVIDIA API key.

## What this repo does

- Stores a curated list of NVIDIA Build free model strings.
- Calls NVIDIA's OpenAI-compatible endpoint.
- Checks which models appear usable for your API key.
- Treats a model as **working** if it either returns successfully within the timeout or does **not** raise an error before the timeout.

This is useful because some models may be temporarily unavailable, gated, rate-limited, or behave differently for different accounts.

## Files

- `free_models_from_nvidia.py` — main script with model list and helper functions.
- `requirements.txt` — Python dependency list.

## Install

```bash
pip install -r requirements.txt
```

## Set your API key

### macOS / Linux

```bash
export NVIDIA_API_KEY="your_key_here"
```

### Windows PowerShell

```powershell
$env:NVIDIA_API_KEY="your_key_here"
```

## Quick start

```python
from free_models_from_nvidia import FREE_MODELS, check_models

working_models, failed_models = check_models(
    models=FREE_MODELS,
    prompt="Just say hi",
    timeout=0.5,
    max_workers=16,
)

print("Working models:")
print(working_models)

print("Failed models:")
print(failed_models)
```

## Example: call one model directly

```python
from free_models_from_nvidia import get_completion

reply = get_completion(
    prompt="Say hi in one sentence.",
    model="google/gemma-2-2b-it",
)

print(reply)
```

## Notes

- NVIDIA Build uses an OpenAI-compatible API base URL:
  `https://integrate.api.nvidia.com/v1`
- Not every model string in the list is guaranteed to stay free forever.
- A timeout-based probe is only a practical heuristic, not a perfect availability check.
- Some background threads may continue briefly after timeout.

---

# 中文说明

这是一个小型 Python 仓库，用来测试 NVIDIA Build 上哪些免费模型在你自己的 NVIDIA API key 下当前可以调用。

## 这个仓库做什么

- 保存一份整理过的 NVIDIA Build 免费模型字符串列表。
- 调用 NVIDIA 的 OpenAI 兼容接口。
- 检查哪些模型在你的 API key 下看起来可用。
- 如果某个模型在超时时间内成功返回，或者在超时时间内**没有报错**，就把它视为**可用**。

这个仓库适合用来快速排查，因为有些模型可能会临时不可用、被限制访问、触发速率限制，或者在不同账号下表现不一样。

## 文件说明

- `free_models_from_nvidia.py` —— 主脚本，包含模型列表和辅助函数。
- `requirements.txt` —— Python 依赖。

## 安装

```bash
pip install -r requirements.txt
```

## 设置 API key

### macOS / Linux

```bash
export NVIDIA_API_KEY="your_key_here"
```

### Windows PowerShell

```powershell
$env:NVIDIA_API_KEY="your_key_here"
```

## 快速开始

```python
from free_models_from_nvidia import FREE_MODELS, check_models

working_models, failed_models = check_models(
    models=FREE_MODELS,
    prompt="Just say hi",
    timeout=0.5,
    max_workers=16,
)

print("Working models:")
print(working_models)

print("Failed models:")
print(failed_models)
```

## 示例：直接调用一个模型

```python
from free_models_from_nvidia import get_completion

reply = get_completion(
    prompt="Say hi in one sentence.",
    model="google/gemma-2-2b-it",
)

print(reply)
```

## 说明

- NVIDIA Build 使用的是 OpenAI 兼容接口，base URL 为：
  `https://integrate.api.nvidia.com/v1`
- 列表中的模型不保证会一直免费。
- 基于超时的探测方式只是一个实用判断，不是绝对准确的可用性检测。
- 超时后，部分后台线程可能还会短暂继续运行。

## License

MIT
