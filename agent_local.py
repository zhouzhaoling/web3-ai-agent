from web3 import Web3
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Web3 连接（不变）
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

tools = [get_wallet_balance]

# 本地 Ollama
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的 Web3 助手。你可以使用提供的工具查询以太坊地址的余额。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    print("=== Web3 本地 AI 助手已启动 ===")
    question = "帮我查一下 Vitalik 的地址 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 现在有多少 ETH？"
    print(f"用户: {question}")
    response = agent_executor.invoke({"input": question})
    print(f"\nAI 回复: {response['output']}")