# Web3 AI Agent (Local LLM)

这是一个基于本地大模型（Qwen 2.5）和 LangChain 构建的 Web3 链上只读智能助手。

## 🌟 核心特性

- **本地化推理**：使用 Ollama 运行 Qwen2.5:7b，零 API 费用，数据不出本地。
- **链上真实数据直连**：通过 `web3.py` 直连以太坊主网公共 RPC 节点，无需中心化 API Key。
- **ReAct Agent 架构**：利用 LangChain Tool Calling，大模型可自主解析自然语言，生成函数调用请求，提取真实链上余额。

## 🛠️ 技术栈

- **LLM 推理**：Ollama (Qwen2.5:7b)
- **Agent 框架**：LangChain (langchain-classic)
- **Web3 交互**：web3.py (以太坊 RPC)
- **开发语言**：Python 3.10+

## 🚀 快速开始

1. 克隆项目并安装依赖：
   ```bash
   pip install web3 langchain langchain-ollama langchain-classic
   ```
2. 确保本地已启动 Ollama 并拉取模型：
   ```bash
   ollama pull qwen2.5:7b
   ```
3. 运行 Agent：
   ```bash
   python agent_local.py
   ```

## 💡 运行示例

运行后，Agent 会自动识别用户意图并调用工具。
