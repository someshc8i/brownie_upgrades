from brownie import (
    network,
    accounts,
    config
)
import eth_utils
NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat", "development", "ganache"]

LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr='0x')
    return initializer.encode_input(*args)

def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    tx = None
    if proxy_admin_contract:
        if initializer:
            encoded_initializer_function = encode_function_data(initializer, *args)
            tx = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_initializer_function,
                {'from': account}
            )
        else:
            tx = proxy_admin_contract.upgrade(
                proxy.address,
                new_implementation_address,
                {'from': account}
            )
    else:
        if initializer:
            encoded_initializer_function = encode_function_data(initializer, *args)
            tx = proxy.upgradeAndCall(
                    proxy.address,
                    new_implementation_address,
                    encoded_initializer_function,
                    {'from': account}
                )
        else:
            tx = proxy.upgrade(
                    proxy.address,
                    new_implementation_address,
                    {'from': account}
                )
    return tx
