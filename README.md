Uniswap 套利扫描器
这是一个为飞行中的人请求的项目。此脚本扫描 Uniswap 对中的套利机会并打印出最佳机会。它使用请求库从 Uniswap API 端点获取数据，并使用 pandas 处理数据。

要求
Python 3.x
请求
熊猫
网络3
用法
克隆存储库并导航到目录：

git clone https://github.com/username/repo.git
cd repo
安装所需的软件包：

pip install -r requirements.txt
打开脚本，将以下行中的 Infura API 密钥替换为您自己的密钥：

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/your-infura-api-key"))
运行脚本：

python uniArb.py
该脚本将扫描套利机会并打印出最佳机会。它将等待 60 秒，然后再次扫描。

许可证 此脚本在 GNU 通用公共许可证 v3.0 下获得许可。有关详细信息，请参阅 LICENSE。
