from copy_static import copy_from_static
from generate_page import generate_page

source_path = "./static/"
destination_path = "./public/"
content_path = "./content/index.md"
template_path = "./template.html"
content_dest = "./public/index.html"

def main():
    copy_from_static(source_path, destination_path)
    generate_page(content_path, template_path, content_dest)

main()