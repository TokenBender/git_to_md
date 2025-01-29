import os
import sys
import subprocess
import tempfile
import shutil
from tree_sitter import Language, Parser

# Build the Tree-sitter Markdown parser
Language.build_library(
    'build/my-languages.so',
    [
        './tree-sitter-markdown/tree-sitter-markdown'  # Update this path
    ]
)

Markdown_LANGUAGE = Language('build/my-languages.so', 'markdown')

def count_words(text):
    return len(text.split())

def extract_headings(code):
    parser = Parser()
    parser.set_language(Markdown_LANGUAGE)
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node

    headings = []

    def traverse(node):
        if node.type == 'atx_heading':
            # Extract the heading text
            start = node.child_by_field_name('text').start_byte
            end = node.child_by_field_name('text').end_byte
            heading = code[start:end].strip()
            level = node.child_count  # Number of '#' symbols
            headings.append((level, heading))
        for child in node.children:
            traverse(child)

    traverse(root_node)
    return headings

def organize_markdown_files(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                headings = extract_headings(content)
                if not headings:
                    continue

                # Example: Create directories based on top-level headings
                top_level = next((h for h in headings if h[0] == 1), None)
                if top_level:
                    dir_name = top_level[1].replace(' ', '_')
                    target_path = os.path.join(target_dir, dir_name)
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)
                    
                    # Move or copy the file to the new directory
                    shutil.copy(file_path, target_path)
                    print(f"Organized {file} into {target_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <github_repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    temp_dir = tempfile.mkdtemp()

    try:
        # Clone only the latest commit
        subprocess.check_call(['git', 'clone', '--depth', '1', repo_url, temp_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        code_extensions = {
            '.py', '.c', '.cpp', '.ipynb', '.java', '.js', '.rb', '.go', '.cs',
            '.php', '.html', '.css', '.swift', '.kt', '.m', '.mm', '.ts', '.rs',
            '.scala', '.pl', '.sh', '.bat', '.ps1', '.lua', '.erl', '.ex', '.dart',
            '.r', '.jl', '.md', ".MD"
        }

        file_contents = []
        for root, dirs, files in os.walk(temp_dir):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                file_path = os.path.join(root, file)
                _, file_extension = os.path.splitext(file)
                if file_extension.lower() in code_extensions:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    relative_path = os.path.relpath(file_path, temp_dir)
                    md_content = f'# {relative_path}\n\n```{file_extension[1:]}\n{content}\n```\n\n'
                    file_contents.append(md_content)

        # Split into multiple files
        word_count = 0
        file_number = 1
        current_file_content = []

        for content in file_contents:
            content_word_count = count_words(content)
            if word_count + content_word_count > 500000:
                # Write current content to file
                output_file = f'super_{repo_name}_{file_number}.md'
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(''.join(current_file_content))
                print(f"Content has been saved in '{output_file}'.")
                
                # Reset for next file
                file_number += 1
                word_count = 0
                current_file_content = []

            current_file_content.append(content)
            word_count += content_word_count

        # Write any remaining content
        if current_file_content:
            output_file = f'super_{repo_name}_{file_number}.md'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(''.join(current_file_content))
            print(f"Content has been saved in '{output_file}'.")

    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
    finally:
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()