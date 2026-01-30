from openai import OpenAI
import httpx
import logging
import sys

# Logging 設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 自訂 httpx client（公司網路用 verify=False，回家刪掉）
http_client = httpx.Client(verify=False, timeout=60.0)

client = OpenAI(
    api_key="",
    base_url="https://api.runpod.ai/v2/6pl7m1119d6uob/openai/v1",
    http_client=http_client
)

def ask_fortigate(prompt):
    response = None  # 先定義，避免 NameError
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "你是 FortiGate 安全專家，直接用中文回答，不要顯示思考過程。每個建議都要附上 Fortinet 官方文件連結或 KB 編號作為依據。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=9000,
            temperature=0.6
        )

        # 檢查 response 結構
        if response is None:
            logger.error("Response is None")
            return "Error: API returned None response"

        if not hasattr(response, 'choices') or not response.choices:
            logger.error("No choices in response")
            return "Error: No choices returned from model"

        choice = response.choices[0]
        if not hasattr(choice, 'message') or choice.message is None:
            logger.error("No message in choice")
            return "Error: No message in response choice"

        content = choice.message.content
        if content is None:
            logger.error("Content is None")
            return "Error: Model returned None content"

        logger.info(f"Success: {content[:100]}...")

        # 存檔
        with open("gpt_response.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- Prompt: {prompt}\nResponse: {content}\n\n")

        # cost 估算（確保在 response 存在時才算）
        if hasattr(response, 'usage') and response.usage:
            input_t = response.usage.prompt_tokens or 0
            output_t = response.usage.completion_tokens or 0
            est_cost = (input_t * 0.000002 + output_t * 0.000006)  # RunPod vLLM 粗估
            logger.info(f"Tokens: in={input_t}, out={output_t}, est. cost ~${est_cost:.6f}")

        return content

    except Exception as e:
        logger.error(f"API call or processing failed: {str(e)}")
        if response is not None:
            logger.debug(f"Partial response: {response}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = "介紹一下 FortiGate 的 model"

    result = ask_fortigate(user_prompt)
    print(result)