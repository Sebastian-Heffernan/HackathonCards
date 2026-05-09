// src/lib/docsData.js
export const docsData = {
  "overview": {
    title: "Overview",
    content: "An introduction to the language syntax. How to read the notation",
  },
  "commenting": {
    title: "Commenting",
    content: "How to comment files",
    examples: [
      "# Commenting line\nASSERT label",
      ""
    ],
    warning: {
      about: "If you put comments at the end of your line, if improperly set they can leak through into your arguments for the respective command",
      example: "END_TURN # Same player plays the turn again"
    }
  },
  "instructions": {
    title: "Instruction Set",
    content: "A complete list of available opcodes.",
    // Nested dictionary for specific instructions
    items: {
      "ASSERT": {
        name: "ASSERT",
        description: "Makes a label into the player's action.\n Additional arguments can be left empty in order to call assert for all players.",
        usage: "ASSERT[label: str][[OPTIONAL] player: int]",
        example: "ASSERT label1 0",
      },
      "CALL": {
        name: "CALL",
        description: "Jumps to a specific label and process, while retaining where it left off.\n Requires calling RETURN in order to return back to where it left off.\n",
        usage: "CALL [label: str]",
        example: "CALL label2",
      }, 
      "COMPARE": {
        name: "COMPARE",
        description: "Sets x = x + y for COMPARE x + y.\nOn true executes n+1. On false, n+2.\n Operators Include '==', '!=', '>', '<', '>=', '<='.",
        usage: "COMPARE [x: int][operator: '==' | '!=' | '>' | '<' | '>=' | '<=' |][y: int]",
        example: "COMPARE x + y"
      },
      "DECK": {
        name: "DECK",
        description: "Controls a specified deck by name through an action specified.",
        usage: "DECK [('MAKE' | 'SHUFFLE' | 'CLEAR' | 'RESET'): str][name: str]",
        example: "DECK MAKE deck1"
      }, 
      "DRAW": {
        name: "DRAW",
        description: "Takes a card from deck name to a players hand by a given number of times.",
        usage: "DRAW [deck_name: str][player_id: int][times: int]",
        example: "DRAW deck1 0 1"
      },
      "END_TURN": {
        name: "END_TURN",
        description: "Finishes the player's turn through finishing a label execution initiated by an action. Can break a loop",
        usage: "END_TURN [] | [next_index: int] | [VAR1][+ | -][VAR2 | i: int]",
        example: "END_TURN 1"
      },
      "GOTO": {
        name: "GOTO",
        description: "Jumps process to a given label, and begins processing its data.\n Does not retain its previous location during execution.\nSee CALL for more deatils.",
        usage: "GOTO [LABEL]",
        example: "GOTO LABEL"
      },
      "HANDLEN": {
        name: "HANDLEN",
        description: "Stores the hand length of player, 'p' in VAR",
        usage: "VALUE [VAR][p: int][c: int]",
        example: "VALUE CARDPLACE 0 1",
      },
      "MATH": {
        name: "MATH",
        description: "Performs mathematical operations between two labels, such as \n addition, subtraction, multiplication, division and modulus",
        usage: "MATH [x: str][enum: '+' | '-' | '*' | '/' | '%' ][y: str]",
        example: "MATH X + Y # Equivalent would be X = X + Y"
      },
      "MOVE": {
        name: "MOVE",
        description: "Moves a card from a player's hand and then move it to a specified deck",
        usage: "MOVE [DECK][p: int][c: int]",
        example: "MOVE DISCARD 1 2"
      },
      "REVEAL": {
        name: "REVEAL",
        description: "Specify a player's most recently drawn card (Lastmost Index).\n Sets its global visibility flag to TRUE for everybody.",
        usage: "REVEAL [p: int: int]",
        example: "REVEAL 2"
      },
      "SUIT": {
        name: "SUIT",
        description: "Stores the suit of the card of player [p], in their hand at [c] into [VAR]",
        usage: "SUIT [VAR: str][p: int][c: int]",
        examples: "SUIT VARSUIT 0 1"
      },
      "VALUE": {
        name: "VALUE",
        description: "Stores the value of the card at VAR",
        usage: "VALUE [VAR: str][p: int][c: int]",
        examples: "VALUE VARVALUE 0 1"
      },
      "VARG": {
        name: "VARG",
        description: "Declares a 'Game State' Variable. Server-Sided/Global Variable",
        usage: "VARG [SET][VAR][v: str | int]",
        example: "VARG TOTAL 5"
      },
      "VARP": {
        name: "VARP",
        description: "Declares a Variable related to a given player.\n Client-Sided/Local Variable",
        usage: "VARP [SET][playerID: int][name: str][value: str]",
        example: "VARP 2 TOTAL 5 # Player 2 has a TOTAL of 5"
      },
      "SHOWVAR": {
        name: "SHOWVAR",
        description: "Adds a variable to showVars array, to then be shown to every client",
        usage: "SHOWVAR [NAME]",
        example: "VARP 2 TOTAL 5",
        warning: {
          about: "Be careful about when you do SHOWVAR because you can logically get away with setting SHOWVAR after a VARG",
          code: "SHOWVAR variable\nVARG variable 1",
        }
      },
      "RETURN": {
        name: "RETURN",
        description: "Returns back to the last CALL on the stack trace.\n Works in Unison with CALL command.",
        usage: "VARP [SET][playerID: int][name: str][value: str/int]",
        example: "VARP 2 TOTAL 5 # Player 2 has a TOTAL of 5"
      },
    }
  },
  "registry": {
    title: "Registeries",
    content: "The regisiters in the game engine",
    items: {
      "$turnPlayer": {
        name: "Turn Player Register",
        description: "Tracks the current player's turn. \n Starts with a value of 0 for the first player"
      },
      "$selectedCardId": {
        name: "Selected Card Register",
        description: "Tracks the currently selected card.\n On Default, value is -1 if nothing is selected",
      },
      "$playerCount": {
        name: "Player Count Register",
        description: "Tracks how many players are in the current game session.\n Checks game state. "
      },
      "$turnCount": {
        name: "Turn Count Register",
        description: "Tracks the count of turns performed by every player each game.\n Initially Starts off at 0 turns for the first turn."
      },
      "$winner": {
        name: "Winner Flag Register",
        description: "Simple Flag which checks if there is a Winner.\n Initially starts off at -1 to declare that there are no winners.\n Call a value of 1 to declare a winner"
      }
    }
  }
};
