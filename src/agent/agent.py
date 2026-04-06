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
        
        current_prompt = user_input
        steps = 0

        while steps < self.max_steps:
            # TODO: Generate LLM response
            # result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            
            # TODO: Parse Thought/Action from result
            
            # TODO: If Action found -> Call tool -> Append Observation
            
            # TODO: If Final Answer found -> Break loop
            
            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps})
        return "Not implemented. Fill in the TODOs!"

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Thực thi các công cụ dựa trên tên.
        """
        # Giả lập Database (Thay bằng database thật của bạn)
        database = [
            {"truong": "ĐH Bách Khoa", "nganh": "CNTT", "diem_chuan": 28.15},
            {"truong": "ĐH Kinh Tế Quốc Dân", "nganh": "Logistics", "diem_chuan": 27.0},
            {"truong": "ĐH Công Nghệ - ĐHQGHN", "nganh": "CNTT", "diem_chuan": 27.5},
            {"truong": "ĐH Giao Thông Vận Tải", "nganh": "CNTT", "diem_chuan": 24.5},
        ]

        if tool_name == "tra_cuu_diem":
            # Tìm ngành theo tên
            res = [d for d in database if args.lower() in d['nganh'].lower()]
            return str(res) if res else "Không tìm thấy dữ liệu ngành này."
        
        elif tool_name == "loc_truong_theo_diem":
            try:
                diem_hs = float(args)
                res = [d for d in database if d['diem_chuan'] <= diem_hs]
                return str(res)
            except:
                return "Lỗi: Tham số điểm phải là một số thực."

        return f"Cảnh báo: Công cụ '{tool_name}' không tồn tại trong danh sách."
