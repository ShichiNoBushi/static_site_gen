import os
import shutil

from textnode import *
from nodeconverter import *

def copy_files(source, destination):
    if os.path.exists(destination):
        print(f"Deleting {destination}")
        shutil.rmtree(destination)
    print(f"Making new directory at {destination}")
    os.mkdir(destination)

    source_dir = os.listdir(source)

    for i in source_dir:
        source_path = os.path.join(source, i)
        destination_path = os.path.join(destination, i)
        if os.path.isdir(source_path):
            print(f"Making new directory at {destination}")
            os.mkdir(destination_path)
            print(f"Entering directory: {source_path}")
            copy_files(source_path, destination_path)
        elif os.path.isfile(source_path):
            print(f"Copying {i} from {source} to {destination}")
            shutil.copy(source_path, destination_path)

def generate_page(from_path, template_path, destination_path):
    print(f"Generating page from {from_path} to {destination_path} using {template_path}.")
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html_code = markdown_to_html_node(markdown).to_html()
    html_code_untagged = html_code.removeprefix("<html>").removesuffix("</html>")
    title = extract_title(markdown)

    html_to_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_code_untagged)

    os.makedirs(os.path.dirname(destination_path), exist_ok = True)
    with open(destination_path, "w") as destination_file:
        destination_file.write(html_to_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)

    for i in dir_list:
        content = os.path.join(dir_path_content, i)
        if os.path.isdir(content):
            destination = os.path.join(dest_dir_path, i)
            if not os.path.exists(destination):
                os.mkdir(destination)
            generate_pages_recursive(content, template_path, destination)
        elif os.path.isfile(content) and i.endswith(".md"):
            destination = os.path.join(dest_dir_path, i.removesuffix(".md") + ".html")
            generate_page(content, template_path, destination)

def main():
    copy_files("static", "public")

    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

main()