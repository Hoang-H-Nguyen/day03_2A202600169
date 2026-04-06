import os
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        TODO: Implement the system prompt that instructs the agent to follow ReAct.
        Should include:
        1.  Available tools and their descriptions.
        2.  Format instructions: Thought, Action, Observation.
        """
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        return f"""
        You are an intelligent assistant. You have access to the following tools:
        {tool_descriptions}

        Use the following format:
        Thought: your line of reasoning.
        Action: tool_name(arguments)
        Observation: result of the tool call.
        ... (repeat Thought/Action/Observation if needed)
        Final Answer: your final response.
        """

    def run(self, user_input: str) -> str:
        """
        TODO: Implement the ReAct loop logic.
        1. Generate Thought + Action.
        2. Parse Action and execute Tool.
        3. Append Observation to prompt and repeat until Final Answer.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        current_context = f"User: {user_input}"
        steps = 0

        while steps < self.max_steps:
            # GỌI LLM: Nhận về kết quả (có thể là dict hoặc str)
            raw_result = self.llm.generate(current_context, system_prompt=self.get_system_prompt())
            
            # Trích xuất nội dung văn bản từ kết quả trả về
            if isinstance(raw_result, dict):
                result_text = raw_result.get('content', '')
            else:
                result_text = str(raw_result)
            
            print(f"\n--- Bước {steps + 1} ---")
            print(result_text)

            # Kiểm tra nếu có Final Answer
            if "Final Answer:" in result_text:
                final_response = result_text.split("Final Answer:")[-1].strip()
                logger.log_event("AGENT_END", {"steps": steps + 1, "status": "success"})
                return final_response

            # Parse Action dùng Regex trên chuỗi văn bản result_text
            action_match = re.search(r"Action:\s*(\w+)\((.*)\)", result_text)
            
            if action_match:
                tool_name = action_match.group(1)
                # Làm sạch tham số (bỏ dấu ngoặc đơn, kép thừa)
                tool_args = action_match.group(2).strip().strip("'").strip('"')
                
                # Thực thi công cụ
                observation = self._execute_tool(tool_name, tool_args)
                print(f"Observation: {observation}")
                
                # Cập nhật context cho lượt suy nghĩ tiếp theo
                current_context += f"\n{result_text}\nObservation: {observation}"
            else:
                # Nếu LLM quên không đưa ra Action đúng định dạng
                msg = "Lỗi: Bạn chưa đưa ra Action đúng định dạng (Action: ten_tool(tham_so))."
                current_context += f"\n{result_text}\nObservation: {msg}"

            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps, "status": "max_steps_reached"})
        return "Tôi đã đạt giới hạn bước xử lý nhưng chưa có câu trả lời cuối cùng."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Helper method to execute tools by name.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                # TODO: Implement dynamic function calling or simple if/else
                return f"Result of {tool_name}"
        return f"Tool {tool_name} not found."
