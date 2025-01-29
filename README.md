# Git to Markdown Converter

A Python tool that clones a Git repository and converts its contents into well-formatted Markdown files. The tool processes all code files in the repository and creates organized Markdown documentation.

## Features

- Clones any public Git repository
- Converts code files to Markdown format with proper syntax highlighting
- Supports multiple programming languages
- Automatically splits large content into multiple files (500,000 words limit per file)
- Preserves file structure in the Markdown output
- Handles various code file extensions including `.py`, `.js`, `.java`, `.cpp`, and many more

## Prerequisites

- Python 3.x
- Git installed and accessible from command line
- Tree-sitter library

## Installation

1. Clone this repository:
```bash
git clone git@github.com:TokenBender/git_to_md.git
cd git_to_md
```

2. Install the required dependencies:
```bash
pip install tree-sitter
```

3. Build the Tree-sitter Markdown parser:
```bash
# The repository already includes the built parser in the build directory
# If you need to rebuild it, the script will do so automatically
```

## Usage

Run the script with a GitHub repository URL as an argument:

```bash
python git_to_md.py <github_repo_url>
```

For example:
```bash
python git_to_md.py https://github.com/username/repository.git
```

### Output

The script will generate one or more Markdown files with the following naming convention:
- `super_<repository-name>_1.md`
- `super_<repository-name>_2.md` (if content exceeds 500,000 words)
- etc.

Each file contains:
- File paths as headers
- Code content with appropriate syntax highlighting
- Organized structure matching the original repository

## Supported File Extensions

The tool supports a wide range of file extensions including:
- Python (.py)
- JavaScript (.js)
- Java (.java)
- C/C++ (.c, .cpp)
- Ruby (.rb)
- Go (.go)
- And many more (see code for complete list)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 