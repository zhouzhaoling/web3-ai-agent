# Web3 AI Agent (Local LLM)

这是一个基于本地大模型（Qwen 2.5）和 LangChain 构建的 Web3 智能研究员。它不仅可以直接查询真实的链上数据，还能结合本地 DeFi 协议知识库（RAG）进行复杂的业务推理。

## 🌟 核心特性 (V2 版本)

- **本地化推理**：使用 Ollama 运行 Qwen2.5:7b，零 API 费用，数据不出本地。
- **链上真实数据直连**：通过 `web3.py` 直连以太坊主网公共 RPC 节点。
- **本地 RAG 知识库**：结合 Redis + `mxbai-embed-large` 向量模型，构建 DeFi 协议（如 Aave）规则知识库。
- **双核 ReAct Agent**：大模型可自主判断，同时调用“文档检索工具”和“链上查询工具”，完成跨领域推理（如：结合 Aave 的 LTV 规则，计算某个链上地址的最大借款额度）。
- **生产级环境隔离**：使用 `.env` 和 `python-dotenv` 管理敏感配置。

## 🛠️ 技术栈

- **LLM 推理**：Ollama (Qwen2.5:7b)
- **Agent 框架**：LangChain (langchain-classic)
- **Web3 交互**：web3.py (以太坊 RPC)
- **RAG 组件**：Redis (RedisVectorStore) + OllamaEmbeddings (mxbai-embed-large)
- **开发语言**：Python 3.10+

## 🚀 快速开始

1. 克隆项目并安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 准备环境变量（在根目录新建 `.env` 文件）：
   ```env
   REDIS_URL=redis://localhost:6379
   ```

3. 确保本地已启动 Ollama 并拉取模型：
   ```bash
   ollama pull qwen2.5:7b
   ollama pull mxbai-embed-large
   ```

4. 运行 Agent：
   ```bash
   python agent_rag_web3.py
   ```