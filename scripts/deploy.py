from brownie import FundMe, MockV3Aggregator, config, accounts, network
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# Para que funcione el puto ganache-cli
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)


def deploy_fund_me():
    account = get_account()

    """
    Problemón: hemos añadido ganache-local a "ethereum", por lo que
    intenta leer lo primero, no lo segundo D:
    """
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # Este precio de gas solamente se establece en las dev networks,
        # para que funcione el puto ganache
        gas_price(gas_strategy)
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # publish_source=True NO FUNCIONA AAAAAAA
        # .get("verify") hace que nuestra vida sea mucho más sencilla en lugar de
        # usar ["verify"], por si acaso me olvido de añadirlo en la config
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract has been deployed to {fund_me.address}")
    return fund_me


"""
Va genial, ahora podemos desplegar este contrato en Sepolia, pero y si queremos
desplegarlo en una testnet? No podemos tal cual, ya que tiene una dirección
hard-coded en él, además de que los PriceFeeds no funcionan en redes locales
Para solventar esto, podemos hacer dos cosas:
1. Mocking
2. Forking
"""

"""
Tras hacer los cambios necesarios en el contrato, hay que cambiar la función deploy
para pasarle una dirección.
"""


def main():
    deploy_fund_me()
