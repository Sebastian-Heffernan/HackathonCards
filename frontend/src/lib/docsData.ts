// src/lib/docsData.js
export const docsData = {
    "getting-started": {
        title: "Overview",
        content: "An introduction to the language syntax."
    },
    "instructions": {
        title: "Instruction Set",
        content: "A complete list of available opcodes.",
        // Nested dictionary for specific instructions
        items: {
            "PUSH": {
                name: "PUSH",
                description: "Pushes a value onto the stack.",
                usage: "PUSH <value>",
                example: "PUSH 10",
            },
            "ADD": {
                name: "ADD",
                description: "Adds the top two values on the stack.",
                usage: "ADD",
                example: "ADD",
            }
        }
    }
};
