import sys
from copy_static import copy_from_static
from generate_page import generate_all_content

source_path = "./static/"
destination_path = "./docs/"
# content_path = "./content/index.md"
content_path = "./content/"
template_path = "./template.html"
# content_dest = "./public/index.html"


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_from_static(source_path, destination_path)
    generate_all_content(content_path, template_path, destination_path, base_path)

main()