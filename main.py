import os
from dotenv import load_dotenv
from src.core.gemini_provider import GeminiProvider
from src.agent.agent import ReActAgent
from src.tools.admission_tools import TOOLS_CONFIG

# 1. Load API Key từ .env
load_dotenv()


def main():
    # 3. Khởi tạo LLM và Agent
    llm = GeminiProvider()
    agent = ReActAgent(llm=llm, tools=TOOLS_CONFIG)

    # 4. Câu hỏi thử nghiệm
    query = "Tôi thi được hai mươi bảy điểm thì có thể đậu vào trường đại học nào ở Hà Nội?"
    
    print(f"--- ĐANG XỬ LÝ CÂU HỎI: {query} ---")
    response = agent.run(query)
    
    print("\n" + "="*50)
    print("PHẢN HỒI CUỐI CÙNG:")
    print(response)
    print("="*50)

if __name__ == "__main__":
    main()