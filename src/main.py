"""SSG entrypoint"""

import os
import shutil


def main():
    cp_directory("static", "public")


def cp_directory(src: str, dst: str) -> None:
    if not os.path.exists(src):
        raise ValueError("source directory does not exists")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    content = os.listdir(src)
    for item in content:
        item_path = os.path.join(src, item)
        item_dst_path = os.path.join(dst, item)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, item_dst_path)
        else:
            cp_directory(item_path, item_dst_path)


if __name__ == "__main__":
    main()
