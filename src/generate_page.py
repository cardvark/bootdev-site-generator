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
    html_content = html_template.replace("{{ Content }}", content_to_html)

    dest_directory = os.path.dirname(dest_path)
    if dest_directory and not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    with open (dest_path, "w") as f:
        f.write(html_content)

    