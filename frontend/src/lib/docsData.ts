// src/lib/docsData.js
export const docsData = {
    "overview": {
        title: "Overview",
        content: "An introduction to the language syntax."
    },
    "instructions": {
        title: "Instruction Set",
        content: "A complete list of available opcodes.",
        // Nested dictionary for specific instructions
        items: {
            "ASSERT": {
                name: "ASSERT",
                description: "Makes a label a player's action",
                usage: "ASSERT [label: str] [player: int]",
                example: "ASSERT label1 0",
            },
            "CALL": {
                name: "CALL",
                description: "Starts processing label",
                usage: "CALL [label: str]",
                example: "CALL label2",
            }, 
            "COMPARE": {
              name: "COMPARE",
              description: "Sets x = x + y for COMPARE x + y.\nOn true executes n+1. On false, n+2",
              usage: "COMPARE [x: int][operator: Enum][y: int]",
              example: "COMPARE x + y"
            },
            "DECK": {
              name: "DECK",
              description: "Controls a specified deck by name through an action specified",
              usage: "DECK [(MAKE | SHUFFLE): str][name: str]",
              example: "DECK MAKE deck1"
            }, 
            "DRAW": {
              name: "DRAW",
              description: "Takes a card from deck name to a players hand by number of times",
              usage: "DRAW [deck_name: str][player_id: int][times: int]",
              example: "DRAW deck1 0 1"
            }
        }
    }
};
