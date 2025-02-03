"""SSG entrypoint"""

import os
import shutil

from markdown_blocks import extract_title, markdown_to_html_node


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    cp_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def cp_directory(src: str, dst: str) -> None:
    if not os.path.exists(src):
        raise ValueError("source directory does not exists")
    os.mkdir(dst)
    content = os.listdir(src)
    for item in content:
        item_path = os.path.join(src, item)
        item_dst_path = os.path.join(dst, item)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, item_dst_path)
        else:
            cp_directory(item_path, item_dst_path)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    template = ""
    with open(from_path, encoding="utf-8") as md_file:
        md = md_file.read()
    with open(template_path, encoding="utf-8") as template_file:
        template = template_file.read()
    with open(dest_path, "+w", encoding="utf-8") as html_file:
        html = markdown_to_html_node(md).to_html()
        title = extract_title(md)
        content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
        html_file.write(content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    if not os.path.exists(dir_path_content):
        raise ValueError("source directory does not exists")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    content = os.listdir(dir_path_content)
    for item in content:
        item_path = os.path.join(dir_path_content, item)
        item_dst_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        print(item_path, item_dst_path)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, item_dst_path)
        else:
            generate_pages_recursive(item_path, template_path, item_dst_path)


if __name__ == "__main__":
    main()
