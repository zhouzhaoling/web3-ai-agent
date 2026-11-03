import os
from dotenv import load_dotenv 
# 在代码最上方加载 .env 文件
load_dotenv()
from web3 import Web3
from langchain_core.tools import tool
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_redis import RedisVectorStore, RedisConfig
from langchain_core.tools.retriever import create_retriever_tool

# ================= 1. Web3 链上工具 =================
w3 = Web3(Web3.HTTPProvider("https://ethereum-rpc.publicnode.com"))

@tool
def get_wallet_balance(address: str) -> str:
    """查询指定以太坊地址的 ETH 余额。输入必须是 0x 开头的合法地址。"""
    try:
        if not w3.is_address(address):
            return "错误：无效的以太坊地址格式。"
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return f"地址 {address} 的当前余额为: {balance_eth} ETH"
    except Exception as e:
        return f"查询失败: {str(e)}"

# ================= 2. 构建本地 RAG 工具 =================
print("正在加载本地文档并写入 Redis...")
# 读取文档
loader = TextLoader("./aave_rules.txt", encoding="utf-8")
docs = loader.load()

# 切分文档（比如按 500 字符切分，重叠 50 字符）
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# 使用你本地的 mxbai-embed-large 模型进行向量化
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 连接到你的本地 Redis (默认端口 6379)
# 注意：这会自动创建一个名为 "aave_index" 的索引
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_config = RedisConfig(index_name="aave_index", redis_url=REDIS_URL)
vectorstore = RedisVectorStore.from_documents(
    documents=splits,
    embedding=embeddings,
    config=redis_config
)

# 创建检索器，并封装成 Agent 可以调用的 Tool
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
doc_tool = create_retriever_tool(
    retriever,
    name="retrieve_aave_rules",
    description="当需要查询 Aave 协议的借贷规则、LTV、清算阈值等文档知识时，使用此工具。"
)

# 将所有工具打包
tools = [get_wallet_balance, doc_tool]

# ================= 3. 组装 Agent =================
# 使用本地千问
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# 注意这里的 System Prompt，我们要明确告诉大模型它有这两个工具
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的 Web3 研究员。你既能查询链上真实数据，也能查阅 DeFi 协议文档。遇到规则问题请查文档，遇到数据问题请查链上。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# ================= 4. 跑起来测试 =================
if __name__ == "__main__":
    print("\n=== Web3 智能研究员已上线 ===")
    
    # 测试问题（它会先查文档，再查链上余额）
    question = "我想了解一下 Aave 的 LTV 是多少。另外，帮我查一下 Vitalik 的地址 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 现在有多少 ETH？"
    print(f"用户提问: {question}\n")
    
    response = agent_executor.invoke({"input": question})
    print(f"\nAI 最终回复:\n{response['output']}")