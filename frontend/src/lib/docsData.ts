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
      },
      "END_TURN": {
        name: "END_TURN",
        description: "Finishes the player's turn through finishing a label execution initiated by an action. Can break a loop",
        usage: "END_TURN [next_index(Next Pointer)/None]",
        example: "END_TURN 1 # Finishes up the current player's turn, go to pointer 1"
      },
      "GOTO": {
        name: "GOTO",
        description: "Jumps process to a given label.",
        usage: "GOTO [LABEL]",
        example: "GOTO LABEL"
      },
      "HANDLEN": {
        name: "HANDLEN",
        description: "Stores hand length of player, 'p' in VAR",
        usage: "VALUE [VAR][p: int][c: int]",
        example: "VALUE CARDPLACE 0 1",
      },
      "MATH": {
        name: "MATH",
        description: "Performs mathematical operations between two labels, such as \n addition, subtraction, multiplication, division and modulus",
        usage: "MATH [LABEL1][ + | - | * | / | % ][LABEL2]",
        example: "MATH X + Y # Equivalent would be X = X + Y"
      },
      "MOVE": {
        name: "MOVE",
        description: "Moves a card from a player's hand and then move it to a specified deck",
        usage: "MOVE [Deck][PlayerID][CardID]",
        example: "MOVE DISCARD 1 2 # Move a card to the discard pile from player 1, card 2"
      },
      "REVEAL": {
        name: "REVEAL",
        description: "Specify a player's most recent drawn card (-1)",
        usage: "REVEAL [PlayerID]",
        example: "REVEAL 2 # Show Player 2's Last Card"
      },
      "SUIT": {
        name: "SUIT",
        description: "Stores the suit of the card of player, p, in their hand at c into VAR",
        usage: "SUIT [VAR][p: int][c: int]",
        examples: "SUIT VARSUIT 0 1"
      },
      "VALUE": {
        name: "VALUE",
        description: "Stores the value of the card at VAR",
        usage: "VALUE [VAR][p: int][c: int]",
        examples: "VALUE VARVALUE 0 1"
      },
      "VARG": {
        name: "VARG",
        description: "Declares a 'Game State' Variable. Server-Sided/Global Variable",
        usage: "VARG [SET][NAME][VALUE]",
        example: "VARG TOTAL 5 # Everyone can access this value"
      },
      "VARP": {
        name: "VARP",
        description: "Declares a Variable related to a given player.\n Client-Sided/Local Variable",
        usage: "VARP [SET][playerID][name][value]",
        example: "VARP 2 TOTAL 5 # Player 2 has a TOTAL of 5"
      },
      "RETURN": {
        name: "RETURN",
        description: "Returns back to the last CALL on the stack trace",
        usage: "VARP [SET][playerID][name][value]",
        example: "VARP 2 TOTAL 5 # Player 2 has a TOTAL of 5"
      },
    }
  }
};
