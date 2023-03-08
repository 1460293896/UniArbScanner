import requests
import time
import pandas as pd
from web3 import Web3

# Set up the web3 provider
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/your_infura_api_key"))

# Set up the Uniswap API endpoints
uni_api_url = [
    'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
    'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
]
uni_query = [
    '''
    query {
      pairs(first: 1000, where: {volumeUSD_gt: "100000", reserve0_gt: "1000", reserve1_gt: "1000"}) {
        id
        token0 {
          symbol
        }
        token1 {
          symbol
        }
        reserve0
        reserve1
        reserveUSD
        volumeToken0
        volumeToken1
        volumeUSD
        txCount
        createdAtTimestamp
      }
    }
    ''',
    '''
    query {
      pools(first: 1000, where: {totalValueLockedUSD_gt: "1000"}) {
        id
        token0 {
          symbol
        }
        token1 {
          symbol
        }
        token0Price
        token1Price
        liquidity
        volumeToken0
        volumeToken1
        volumeUSD
        feeTier
        txCount
        createdAtTimestamp
      }
    }
    '''
]

def fetch_uni_data(api_url, query):
    """Fetch data from the Uniswap API."""
    response = requests.post(api_url, json={'query': query})
    if response.status_code != 200:
        raise ValueError(f'Failed to fetch data from {api_url}')
    return response.json()['data']['pairs'] if 'pairs' in response.json()['data'] else response.json()['data']['pools']


def calculate_arbitrage(pair, pairs):
    """Calculate the arbitrage opportunity for a given Uniswap pair."""
    token0 = pair['token0']['symbol']
    token1 = pair['token1']['symbol']
    if 'reserve0' not in pair:
        # print(f"Error: 'reserve0' not found in pair: {pair}")
        return None
    reserve0 = float(pair['reserve0'])
    if 'reserve1' not in pair:
        # print(f"Error: 'reserve1' not found in pair: {pair}")
        return None
    reserve1 = float(pair['reserve1'])

    # Find other pairs that involve the same tokens
    other_pairs = [p for p in pairs if (p['token0']['symbol'] == token0 or p['token1']['symbol'] == token0) and
                   (p['token0']['symbol'] == token1 or p['token1']['symbol'] == token1) and p != pair]
    if len(other_pairs) == 0:
        return None

    # Calculate the price of token0 and token1 in ETH for the current pair
    price0 = reserve1 / reserve0
    price1 = reserve0 / reserve1

    # Calculate the maximum amount of token0 and token1 that can be bought with the reserve amounts
    max_amount0 = reserve0 * 0.99
    max_amount1 = reserve1 * 0.99

    # Calculate the potential profit for each other pair
    profits = []
    for other_pair in other_pairs:
        other_token0 = other_pair['token0']['symbol']
        other_token1 = other_pair['token1']['symbol']
        other_reserve0 = float(other_pair['reserve0'])
        other_reserve1 = float(other_pair['reserve1'])

        # Calculate the price of token0 and token1 in ETH for the other pair
        other_price0 = other_reserve1 / other_reserve0
        other_price1 = other_reserve0 / other_reserve1

        # Find the best arbitrage opportunity between the two pairs
        if token0 == other_token0:
            # Buy token0 from current pair and sell token0 to other pair
            amount0 = min(max_amount0, other_reserve0 * 0.99)
            amount1 = amount0 * price0 * other_price1
            profit = (amount1 / other_reserve1 - 1) * 100
            profits.append((other_token0, other_token1, profit))
        elif token0 == other_token1:
            # Buy token0 from current pair and sell token1 to other pair
            amount0 = min(max_amount0, other_reserve1 * 0.99)
            amount1 = amount0 * price0 / other_price0
            profit = (amount1 / other_reserve0 - 1) * 100
            profits.append((other_token1, other_token0, profit))
        elif token1 == other_token0:
            # Buy token1 from current pair and sell token0 to other pair
            amount1 = min(max_amount1, other_reserve0 * 0.99)
            amount0 = amount1 * price1 / other_price1
            profit = (amount0 / other_reserve1 - 1) * 100
            profits.append((other_token0, other_token1, profit))
        elif token1 == other_token1:
            # Buy token1 from current pair and sell token1 to other pair
            amount1 = min(max_amount1, other_reserve1 * 0.99)
            amount0 = amount1 * price1 * other_price0
            profit = (amount0 / other_reserve0 - 1) * 100
            profits.append((other_token1, other_token0, profit))

    # Find the best arbitrage opportunity
    if len(profits) == 0:
        return None
    else:
        best_profit = max(profits, key=lambda x: x[2])
        return {
            'pair': pair['id'],
            'token0': token0,
            'token1': token1,
            'profit': best_profit[2],
            'trade': f"Buy {best_profit[0]} from {token0}-{token1} pair, sell {best_profit[1]} on other pair"
        }

def scan_for_arbitrage():
    """Scan for arbitrage opportunities across Uniswap pairs."""
    # Set up the Uniswap API endpoints
    uni_api_urls = [
        'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
        'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
    ]
    # Calculate arbitrage opportunities for each pair from each endpoint
    opportunities = []
    for i in range(len(uni_api_urls)):
        pairs = fetch_uni_data(uni_api_urls[i], uni_query[i])
        for pair in pairs:
            opportunity = calculate_arbitrage(pair, pairs)
            if opportunity:
                opportunities.append(opportunity)

    # Sort opportunities by profit
    opportunities.sort(key=lambda x: x['profit'], reverse=True)

    # Print out the best opportunities
    for opportunity in opportunities[:5]:
        print(f"Profit: {opportunity['profit']}%  Trade: {opportunity['trade']}")



if __name__ == '__main__':
    scan_for_arbitrage()
    time.sleep(60) # Wait 1 minute before scanning again
