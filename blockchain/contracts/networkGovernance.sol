// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NetworkGovernance {

    struct DecisionLog {
        string decision;
        uint256 bandwidth;
        string context;
        uint256 timestamp;
    }

    DecisionLog[] public logs;

    function logDecision(
        string memory _decision,
        uint256 _bandwidth,
        string memory _context
    ) public {
        logs.push(DecisionLog(
            _decision,
            _bandwidth,
            _context,
            block.timestamp
        ));
    }

    function getLogsCount() public view returns (uint256) {
        return logs.length;
    }
}
