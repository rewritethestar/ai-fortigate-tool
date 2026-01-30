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

#### 1. Clone repo
   ``bash
   git clone https://github.com/yourusername/ai-fortigate-tool.git
   cd ai-fortigate-tool

#### 2. 建立虛擬環境（強烈建議）cmdpython -m venv venv

venv\Scripts\activate.bat

#### 3. 安裝依賴cmdpip install openai httpx

#### 4. 複製並修改 script 中的 API key 與 base_url（非常重要，勿 commit）
打開 call_gpt_oss.py
修改 api_key 與 base_url 為你自己的 RunPod endpoint

#### 5. 執行cmdpython call_gpt_oss.py "你的問題"範例：cmdpython call_gpt_oss.py "FortiGate 1200D end of support 後有哪些風險"
python call_gpt_oss.py "這段 log 有什麼問題：date=2026-01-29 time=19:00:00 devname=FG1200D logid=0100040704 type=event subtype=system level=alert vd=root msg="Admin login failed" user="admin" srcip=10.1.1.100 reason="incorrect_password""

### 輸出會存到

螢幕（print）
gpt_response.txt（追加模式）

## 目前已知問題

公司網路下必須 verify=False（安全性風險，請只在內網用）
模型偶爾回 None content 或 choices 為空（已加防禦檢查）
token 成本未嚴格限制（一次 1000 output token ≈ $0.006，累積會貴）
回應品質不穩定（需人工驗證，不能直接套用在 production）

## 下一步規劃（我自己的 todo list）

-[] 寫 requirements.txt 與 requirements-dev.txt
-[] 加 config.yaml 抽離 API key / base_url / model
-[]  加讀 log 檔功能（自動分析 FortiGate log）
-[]  加 retry mechanism（exponential backoff）
-[]  加 cost 上限警報（超過 $0.05 就警告）
-[]  寫基本 unit test（pytest）
-[]  加 CLI 介面（用 click 或 argparse）
-[]  整合到日常工作（e.g. VS Code extension 或 FortiAnalyzer plugin idea）

歡迎 issue / PR，但目前還在早期開發階段，主要給自己用。
### License
MIT（隨便用，但請保留原作者資訊）
最後更新：2026-01-29
