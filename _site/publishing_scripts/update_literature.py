import os
import re

# Define the paths
repo_path = "/Users/emaybachwork/bioinform.co/"
papers_path = os.path.join(repo_path, "collections/_papers")
scripts_path = os.path.join(repo_path, "publishing_scripts")

# Define the filenames
entries = [f"entry{i}" for i in range(1, 6)]

def read_new_content(entry):
    with open(os.path.join(scripts_path, f"{entry}.txt"), "r") as file:
        content = file.read()
    title = re.search(r'Title:\s*(.*)', content).group(1)
    date = re.search(r'Date:\s*(.*)', content).group(1)
    link = re.search(r'Link to article:\s*(.*)', content).group(1)
    citation = re.search(r'Citation:\s*(.*)', content).group(1)
    abstract = re.search(r'Abstract:\s*(.*)', content).group(1)
    return title, date, link, citation, abstract

def get_markdown_filename(entry):
    for filename in os.listdir(papers_path):
        if re.match(r'\d{4}-\d{2}-\d{2}-' + entry + r'\.md', filename):
            return filename
    return None

def update_markdown(entry, title, date, link, citation, abstract):
    md_filename = get_markdown_filename(entry)
    if not md_filename:
        print(f"Markdown file for {entry} not found.")
        return

    md_filepath = os.path.join(papers_path, md_filename)
    with open(md_filepath, "r") as file:
        md_content = file.read()

    # Update header
    md_content = re.sub(r'title: ".*?"', f'title: "{title}"', md_content)
    md_content = re.sub(r'date: .*?Z', f'date: {date}', md_content)
    
    # Update Link to article
    md_content = re.sub(r'# Link to article\n\[.*?\]\(.*?\){: .btn}', f'# Link to article\n[Click to Access]({link}){{: .btn}}', md_content)
    
    # Update Citation
    md_content = re.sub(r'# Citation\n.*?\n\n', f'# Citation\n{citation}\n\n', md_content)
    
    # Update Abstract
    md_content = re.sub(r'# Abstract\n > .*', f'# Abstract\n > {abstract}', md_content, flags=re.DOTALL)
    
    with open(md_filepath, "w") as file:
        file.write(md_content)

def main():
    for entry in entries:
        title, date, link, citation, abstract = read_new_content(entry)
        update_markdown(entry, title, date, link, citation, abstract)
    print("Markdown files updated successfully.")

if __name__ == "__main__":
    main()

