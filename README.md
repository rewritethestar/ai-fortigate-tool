# AI FortiGate Assistant

一個用 Python + RunPod vLLM + openai SDK 呼叫開源 LLM 的小工具，目前主要用來問 FortiGate 相關問題（policy 優化、log 分析、升級建議等）。

目前階段：**玩具 → 個人工具**（還遠遠不到 production-ready）

## 現況與限制（誠實版）

- 目前只有單一 script：`call_gpt_oss.py`
- 模型：openai/gpt-oss-20b（在 RunPod Serverless vLLM 上跑）
- 公司網路環境：必須用 `verify=False`（因為 MITM proxy + 自簽 CA），**回家或用手機熱點時請移除這行**
- 沒有 unit test、沒有 CI、沒有依賴鎖定（requirements.txt 還沒寫）
- 沒有成本監控上限（RunPod 按 token / GPU 時間計費，忘記關會燒錢）
- 模型回應準確度：約 60–70%，常見知識 OK，但細節（特定版本、公司環境）容易錯或過度樂觀，**必須人工驗證**
- 沒有 log 檔案輸入、沒有 policy snippet 生成、沒有自動化整合

## 安裝與使用（2026 年 1 月版）

### 環境需求
- Windows 10/11（目前在公司 domain 機器測試）
- Python 3.10+（建議 3.12）
- RunPod 帳號 + Serverless vLLM endpoint（已部署 openai/gpt-oss-20b）

### 步驟

1. Clone repo
   ```bash
   git clone https://github.com/yourusername/ai-fortigate-tool.git
   cd ai-fortigate-tool
