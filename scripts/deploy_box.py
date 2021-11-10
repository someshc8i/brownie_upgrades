from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import Box, TransparentUpgradeableProxy, Contract, ProxyAdmin, BoxV2


def main():
    account = get_account()
    print('Deploying...')

    box = Box.deploy({'from': account})
    # print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({'from': account})

    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data(initializer)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_initializer_function, {
            'from': account,
            'gas_limit': 1000000
        })
    print(f'Proxy deployed to {proxy} you can now upgrade to v2')
    proxy_box = Contract.from_abi('Box', proxy.address, Box.abi)
    tx = proxy_box.store(1, {'from': account})
    tx.wait(1)
    print(proxy_box.retrieve())

    print('Upgrading...')
    box_v2 = BoxV2.deploy({'from': account})
    upgrade_tx = upgrade(account,
                         proxy,
                         box_v2.address,
                         proxy_admin_contract=proxy_admin)
    upgrade_tx.wait(1)
    print('proxy has been upgraded')
    proxy_box = Contract.from_abi('BoxV2', proxy.address, BoxV2.abi)
    increment_tx = proxy_box.increment({'from': account})
    increment_tx.wait(1)
    print(proxy_box.retrieve())
