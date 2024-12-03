const fs = require('fs');

// Read the input file
const inputFile = 'grammar.ebnf'; // replace with your actual file path
let fileContent = fs.readFileSync(inputFile, 'utf8');

// Function to format the file
function formatGrammarFile(content) {
    // Split the file into lines
    const lines = content.split('\n');
    let formattedLines = [];
    let state = 0; // 是否发现规则头
    let length = 0;

    // Iterate through each line
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];

        // Rule 1: Check for lines containing a word with a '?' followed by ':', calculate length length
        const regex = /\??([a-zA-Z_][a-zA-Z0-9_]*)\s*:/;
        const match = line.match(regex);

        if (match) {
            length = match[0].length - 1; // length of the matched word with '?'
            state = 1;
        } else

            // Rule 2: If next line starts with "|", trim it and prepend spaces
            if (state == 1 && /^\s*\|/.test(line)) {
                line = ' '.repeat(length) + line.trimStart();  // Add spaces of length length to the current line
            }

        formattedLines.push(line);
    }

    return formattedLines.join('\n');
}

// Format the content
const formattedContent = formatGrammarFile(fileContent);

// Save the formatted content to a new file
const outputFile = inputFile;
fs.writeFileSync(outputFile, formattedContent, 'utf8');

