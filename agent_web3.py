from web3 import Web3
from langchain_core.tools import tool

# 1. 连接区块链
rpc_url = "https://ethereum-rpc.publicnode.com"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# 2. 用 LangChain 的 @tool 装饰器，把函数变成 Agent 的工具
@tool
def get_wallet_balance(address: str) -> str:
    """查询指定以太坊地址的 ETH 余额。输入必须是 0x 开头的合法地址。"""
    try:
        # 校验地址是否合法
        if not w3.is_address(address):
            return "错误：无效的以太坊地址格式。"
        
        # 查询余额
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return f"地址 {address} 的当前余额为: {balance_eth} ETH"
    except Exception as e:
        return f"查询失败: {str(e)}"

# 3. 测试这个工具
if __name__ == "__main__":
    print("=== 正在测试工具 ===")
    # 让大模型知道这个工具能干什么
    print(get_wallet_balance.name)
    print(get_wallet_balance.description)
    
    # 直接调用这个工具
    result = get_wallet_balance.invoke("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    print(result)