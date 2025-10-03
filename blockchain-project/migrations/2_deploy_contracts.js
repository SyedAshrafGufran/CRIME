const FIRStorage = artifacts.require("FIRStorage");

module.exports = function(deployer) {
  deployer.deploy(FIRStorage);
};