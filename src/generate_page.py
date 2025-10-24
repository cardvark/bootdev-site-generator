import re
import os

from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    header = re.search(r"^#.*", markdown)
    if not header:
        raise Exception("No header found. Documents must contain headers.")


    return header.group(0)[2:].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        html_template = f.read()

    title = extract_title(markdown_content)
    content_to_html = markdown_to_html_node(markdown_content).to_html()

    # print(title)
    # print(content_to_html)

    html_content = html_template.replace("{{ Title }}", title)
    html_content = html_content.replace("{{ Content }}", content_to_html)

    dest_directory = os.path.dirname(dest_path)
    if dest_directory and not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    with open (dest_path, "w") as f:
        f.write(html_content)

def generate_all_content(working_path, template_path, dest_path):
    # takes a source folder and a destination folder, then recursively looks through each source folder and generates html for each final in that folder, calling itself again with an updated working path and dest path, based on the next folder.
    
    for path in os.listdir(working_path):
        full_working_path = os.path.join(working_path, path)
        full_dest_path = os.path.join(dest_path, path)

        if os.path.isfile(full_working_path):
            if os.path.splitext(full_working_path)[1] != ".md":
                continue

            full_dest_path = full_dest_path.replace(".md", ".html")
            
            print(f"This is a markdown file: {path}")
            print(f"Generating to destination: {full_dest_path}")

            generate_page(full_working_path, template_path, full_dest_path)

        elif os.path.isdir(full_working_path):
            print(f"This is a folder: {full_working_path}")
            print(f"Running generate_all_content with working dir: {full_working_path} and destination path: {full_dest_path}")

            generate_all_content(full_working_path, template_path, full_dest_path)
