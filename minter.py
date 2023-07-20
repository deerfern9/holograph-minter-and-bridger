import random
import time
from web3 import Web3
from colorama import init, Fore
init()

delay = (40, 60)    # delay between minting nft
gwei = 1
rpc = 'https://bsc.blockpi.network/v1/rpc/public'
web3 = Web3(Web3.HTTPProvider(rpc))
contract_address = web3.toChecksumAddress('0xe5325804D68033eDF65a86403B2592a99E1f06de')


def read_file(filename):
    result = []
    with open(filename, 'r') as file:
        for tmp in file.readlines():
            result.append(tmp.replace('\n', ''))

    return result


def write_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(f'{text}\n')


def mint(private):
    address = web3.eth.account.from_key(private).address
    data = '0xefef39a10000000000000000000000000000000000000000000000000000000000000001'
    nonce = web3.eth.getTransactionCount(address)

    tx = {
        'from': address,
        'to': contract_address,
        'value': 0,  # Set value if needed
        # 'gas': 150000,  # Set an appropriate gas limit for the transaction
        'gasPrice': web3.toWei(gwei, 'gwei'),
        'nonce': nonce,
        'data': data,
    }
    try:
        tx['gas'] = web3.eth.estimateGas(tx)+50000
    except Exception as e:
        print(e)
        tx['gas'] = 350000

    try:
        tx_create = web3.eth.account.sign_transaction(tx ,private)
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        write_to_file('hashes.txt', tx_hash.hex())
        print(f"Transaction hash: {tx_hash.hex()}")
    except Exception as e:
        write_to_file('ERRORS.txt', f'{private}:{e}')


if __name__ == '__main__':
    privates = read_file('privates.txt')
    random.shuffle(privates)

    for n, priv in enumerate(privates):
        print(f'{Fore.BLUE}' if n % 2 == 0 else f'{Fore.GREEN}')
        write_to_file('MINT DONE.txt', priv)
        mint(priv)
        time.sleep(random.randint(*delay))
