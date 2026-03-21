"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config


PROVIDER_OPENAI = "openai"
PROVIDER_GROQ = "groq"
PROVIDER_FIREWORKS = "fireworks"
SUPPORTED_PROVIDERS = {
    PROVIDER_OPENAI,
    PROVIDER_GROQ,
    PROVIDER_FIREWORKS,
}


def resolve_llm_provider_settings(
    *,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, str]:
    resolved_provider = (provider or Config.LLM_PROVIDER or PROVIDER_OPENAI).strip().lower()
    if resolved_provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported LLM provider: {resolved_provider}")

    if resolved_provider == PROVIDER_GROQ:
        resolved_api_key = api_key or Config.GROQ_API_KEY
        resolved_base_url = base_url or Config.GROQ_BASE_URL
        resolved_model = model or Config.GROQ_MODEL_NAME
    elif resolved_provider == PROVIDER_FIREWORKS:
        resolved_api_key = api_key or Config.FIREWORKS_API_KEY
        resolved_base_url = base_url or Config.FIREWORKS_BASE_URL
        resolved_model = model or Config.FIREWORKS_MODEL_NAME
    else:
        resolved_api_key = api_key or Config.LLM_API_KEY
        resolved_base_url = base_url or Config.LLM_BASE_URL
        resolved_model = model or Config.LLM_MODEL_NAME

    if not resolved_api_key:
        env_name = {
            PROVIDER_OPENAI: "LLM_API_KEY / OPENAI_API_KEY",
            PROVIDER_GROQ: "GROQ_API_KEY",
            PROVIDER_FIREWORKS: "FIREWORKS_API_KEY",
        }[resolved_provider]
        raise ValueError(f"{env_name} 未配置")

    return {
        "provider": resolved_provider,
        "api_key": resolved_api_key,
        "base_url": resolved_base_url,
        "model": resolved_model,
    }


class LLMClient:
    """LLM客户端"""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        settings = resolve_llm_provider_settings(
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            model=model,
        )
        self.provider = settings["provider"]
        self.api_key = settings["api_key"]
        self.base_url = settings["base_url"]
        self.model = settings["model"]
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        # 部分模型（如MiniMax M2.5）会在content中包含<think>思考内容，需要移除
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
        *,
        use_response_format: bool = True,
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            解析后的JSON对象
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"} if use_response_format else None,
        )
        return self.parse_json_text(response)

    @staticmethod
    def parse_json_text(response: str) -> Dict[str, Any]:
        # 清理markdown代码块标记
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"LLM返回的JSON格式无效: {cleaned_response}")
