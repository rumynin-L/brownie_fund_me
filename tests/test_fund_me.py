from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    # Es bueno dar un pelín más de pasta por si hace falta para lo que sea
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    # Hacemos accounts[3] para elegir una puta cuenta que tenga fondos suficientes
    bad_actor = accounts[3]
    with pytest.raises(exceptions.VirtualMachineError):
        # ¿Por qué hace falta un gas_limit y allow_revert?
        # Ni putísima idea, pero esto hace revert D:
        fund_me.withdraw(
            {
                "from": bad_actor,
                "gas_limit": 12000000,
                "allow_revert": True,
            }
        )
