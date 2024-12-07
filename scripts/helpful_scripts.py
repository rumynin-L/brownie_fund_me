# Ahora sí que funciona network xd, supongo que porque no uso la keyword
from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


# Tenemos que decirle a Brownie que cuando estemos trabajando con un fork, me cree una
# cuenta fake con 100 ETH
def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        # Esto por sí solo devuelve otro error, porque por defecto no existen cuentas
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # Mocking
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    # Esto solo se ejecuta si todavía no hemos creado ningún mock
    # MockV3Aggregator funciona como una lista de los mocks que hemos hecho
    if len(MockV3Aggregator) <= 0:
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS,
            Web3.to_wei(STARTING_PRICE, "ether"),
            {"from": get_account()},
        )
    # Usa el mock desplegado más recientemente
    print("Mocks deployed!")
