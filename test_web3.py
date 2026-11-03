from web3 import Web3

# 1. 连接区块链的公共节点 (这里用的是免费的以太坊主网节点)
rpc_url = "https://ethereum-rpc.publicnode.com"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# 检查是否连接成功
if w3.is_connected():
    print("✅ 成功连接到以太坊主网！")

# 2. 试试查一下你的钱包地址余额
my_address = "0xBFeC3271441384E47216Ad738Db13BC166fB3e6A"
balance_wei = w3.eth.get_balance(my_address)
# 把单位从 wei 转换成 ETH
balance_eth = w3.from_wei(balance_wei, 'ether')
print(f"你的钱包余额: {balance_eth} ETH")

# 3. 为了让结果好看点，我们查一下以太坊创始人 V神 (Vitalik) 的钱包
vitalik_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
v_balance_wei = w3.eth.get_balance(vitalik_address)
v_balance_eth = w3.from_wei(v_balance_wei, 'ether')
print(f"V神的钱包余额: {v_balance_eth} ETH")