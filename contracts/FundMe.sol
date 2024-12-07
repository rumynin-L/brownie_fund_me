// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

/*
Para que estos imports funcionen, debemos de especificar a Brownie desde dónde los estamos extrayendo (la repo de github)
Y para que Brownie sepa qué significa @chainlink, también. Esto lo hacemos en el brownie-config.yaml
Descarga estas cositas y las agrega a la carpeta 'dependencies'
*/

/*
Para poder subir el source de este contrato a Etherscan, sebería de sustituir estos imports por el código explícito
Este proceso se conoce como flattening. Pero Brownie tiene una buena forma de solucionar esto
*/
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// Esto no es necesario a partir de solidity v0.8
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // using SafeMathChainlink for uint256

    // public so we can see and interact with the owner variable
    address public owner;
    // whatever I add here will be executed the instant I deploy the contract

    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        // bc the sender of the message is going to be the one who deploys the contract
        owner = msg.sender;
    }

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    function fund() public payable {
        uint256 minimumUsd = 1 * 10 ** 18;
        require(
            getConversionRate(msg.value) >= minimumUsd,
            "You have to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        // what the ETH -> USD conversion rate is
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        // donde esté la barrabaja es donde añadirá el resto de la función
        _;
    }

    // Esto no funciona en v0.8
    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        // este bucle vacía el mapping
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        // esta línea vacía el array
        funders = new address[](0);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (
            ,
            /* uint80 roundID */ int answer /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/,
            ,
            ,

        ) = priceFeed.latestRoundData();
        return uint256(answer * 10 ** 10);
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10 ** 18;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }
}
