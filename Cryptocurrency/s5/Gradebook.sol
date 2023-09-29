// SPDX-License-Identifier: GPL-3.0-or-later

// This file is part of the http://github.com/aaronbloomfield/ccc repository,
// and is released under the GPL 3.0 license.

pragma solidity ^0.8.17;

import "./IGradebook.sol";

contract Gradebook is IGradebook {

    

    //events are imported

    //Implement first 6 functions. 

    //function tas(address ta) external view returns (bool);
    mapping (address => bool) public override tas;


    // Returns the max score for the given assignment
    //function max_scores(uint id) external view returns (uint);
    mapping (uint => uint) public override max_scores;

    // Returns the name of the given assignment
    //function assignment_names(uint id) external view returns (string memory);
    mapping (uint => string ) public override assignment_names;

    // Returns the score for the given assignment ID and the given
    // student
    //function scores(uint id, string memory userid) external view returns (uint);
    mapping (uint => mapping(string => uint)) public override scores;

    // Returns how many assignments there are; the assignments are
    // assumed to be indexed from 0
    //function num_assignments() external view returns (uint);
    uint public override num_assignments;

    // Returns the address of the instructor, who is the person who
    // deployed this smart contract
    //function instructor() external view returns (address);
    address public override instructor;

    //TODO

    constructor() {
        instructor = msg.sender; //for testing, this may need to be hardcoded to properly work?
    }



    // Designates the passed address as a teaching assistant; re-designating
    // an address a TA does not do anything special (no revert).  ONLY the
    // instructor can designated TAs.
    function designateTA(address ta) override public {
        //should i require that the address is valid?

        //ensure they are not already a TA
        //use ta fn
        //require(!tas[ta], "Person is already designated as a TA!");
        require(ta != instructor, "Instructor cannot be a TA! ");


        //require that designator is the instructor!!!
        //fn to get instructor address
        require(msg.sender == instructor, "Instructor must be the designator of TA status");

        tas[ta] = true;

    }

    // Adds an assignment of the given name with the given maximum score.  It
    // should revert if called by somebody other than the instructor or an
    // already designated teaching assistant.  It does not check if an
    // assignment with the same name already exists; thus, you can have
    // multiple assignments with the same name (but different IDs).  It
    // returns the assignment ID.
    function addAssignment(string memory name, uint max_score) override public returns (uint)  {
        require(msg.sender == instructor || tas[msg.sender] == true, "Creator of assignment is not an instructor or TA");

        require(max_score >= 0, "max score cannot be negative");

        //prolly not needed
        //require(name != "", "name of assignment cannot be an empty string");

        //update apprpriate fields

        //assignment has a unique id, a non-unique name, and a max score. map it
        //add mappings
        //figure out the unique uint for an assignment, then add the mapping to these two functions. 

        max_scores[num_assignments] = max_score;

        assignment_names[num_assignments] = name;

        emit assignmentCreationEvent(num_assignments);

        //one more assignment
        num_assignments++;

        return num_assignments - 1;
        
    }

    // Adds the given grade for the given student and the given assignment.
    // This should revert if (a) the caller is not the instructor or TA, or
    // (b) the assignment ID is invalid, or (c) the score is higher than the
    // allowed maximum score.
    function addGrade(string memory student, uint assignment, uint score) override public {
        require(msg.sender == instructor || tas[msg.sender] == true, "Adder of assignment is not an instructor or TA");

        //Check that the assignment id is valid. 
        // require(assignment_names[assignment], "Assignment id is not valid!");
        require(assignment < num_assignments, "Assignment id is not valid!");

        //check it is a valid score
        require(max_scores[assignment] >= score, "Score can't be higher than the max");

        require(score >= 0, "score on assignment can't be less than zero");

        //Should i do any requires on string student?

        //update the scores mapping
        scores[assignment][student] = score;

        //emit event for grade entry
        emit gradeEntryEvent(assignment); //check if this is correct arg passed
    }

    // Obtains the average of the given student's scores.  Each assignment is
    // weighted based on the number of points for that assignment.  So a 5/10
    // on one assignment and a 20/20 on another assignment would yield 25/30
    // points, or 83.33.  This returns 100 times that, or 8333.  Note that
    // the value is truncated, not rounded; so if the average were 16.67%, it
    // would return 1666.  A student with no grades entered should have an
    // average of 0.
    function getAverage(string memory student) override public view returns (uint) {
        
        //use scores and the num of assignments and max score for assignment to figure out avg
        uint maxAvg = 0; //keep adding max score possible on each assignment
        uint studentTotal = 0; //track student's total points
        for (uint i = 0; i < num_assignments; i++) {
            maxAvg = maxAvg + max_scores[i];
            studentTotal = studentTotal + scores[i][student];
        }

        //after loop, find truncated int avg
        require(maxAvg > 0, "maximum score is zero. Assignments need to be created first");
        uint result = (studentTotal * 10000) / maxAvg; //100 * 100. one for format they want. one for solidity division to get percent
        
        return result;

    }

    // This function is how we are going to test your program -- we are going
    // to request TA access.  For this assignment, it will automatically make
    // msg.sender a TA, and has no effect if the sender is already a TA
    // (or instructor).  In reality, this would revert(), as only the
    // instructor (and other TAs) can make new TAs.
    function requestTAAccess() override public {
        tas[msg.sender] = true;
    }



    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
        return interfaceId == type(IGradebook).interfaceId || interfaceId == 0x01ffc9a7;
    }



}