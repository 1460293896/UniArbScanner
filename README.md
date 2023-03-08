# Uniswap Arbitrage Scanner

This was a requested project for someone on the fly. This script scans for arbitrage opportunities across Uniswap pairs and prints out the best opportunities. It fetches data from Uniswap API endpoints using the requests library and processes the data using the pandas.

## Requirements

- Python 3.x
- requests
- pandas
- web3

## Usage

Clone the repository and navigate to the directory:

```bash
git clone https://github.com/username/repo.git
cd repo
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Open the script and replace the Infura API key in the following line with your own:

```python
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/your-infura-api-key"))
```

Run the script:

```python
python uniArb.py
```

The script will scan for arbitrage opportunities and print out the best opportunities. It will wait for 60 seconds before scanning again.

License
This script is licensed under the GNU General Public License v3.0. See LICENSE for more information.
