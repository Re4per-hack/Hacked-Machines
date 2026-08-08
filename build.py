#!/usr/bin/env python3
"""Convert Obsidian writeups into Jekyll posts.

What it does, so you never touch HTML:
  1. Reads every .md under Easy/, Medium/, Hard/  (Linux/ and Windows/ subfolders).
  2. Rewrites Obsidian image embeds  ![[Pasted image X.png]]  ->  standard markdown
     pointing at /assets/images/, with spaces url-encoded so they work on the web.
  3. Adds the Jekyll "front matter" (title, difficulty, os) automatically from the
     folder structure and file name.
  4. Copies the converted posts into _posts/ and the images into assets/images/.

Your workflow stays: write in Obsidian with ![[image.png]], drop images in Images/,
then run  `python build.py`  and push.
"""

from __future__ import annotations

import datetime
import re
import shutil
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
# --- Configuration -------------------------------------------------------
# Where your writeups live. If your difficulty folders (Easy/, Hard/...) are
# directly in the repo root, set: CONTENT_DIR = ROOT
# If they live inside a subfolder like HTB/, set: CONTENT_DIR = ROOT / "HTB"
CONTENT_DIR = ROOT / "HTB"

SOURCE_DIRS = ["Easy", "Medium", "Hard"]        # difficulty folders
IMAGES_SRC = CONTENT_DIR / "Images"             # where Obsidian dumps images
POSTS_OUT = ROOT / "_posts"
IMAGES_OUT = ROOT / "assets" / "images"

# Matches Obsidian embeds like: ![[Pasted image 20260407192912.png]]
EMBED_RE = re.compile(r"!\[\[([^\]]+?\.(?:png|jpg|jpeg|gif|webp))\]\]", re.IGNORECASE)
# Matches Obsidian internal links like [[nc]] -> we turn them into plain text `nc`
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)\]\]")


BASEURL = "/Hacked-Machines"


def web_image_path(filename: str) -> str:
    encoded = urllib.parse.quote(filename.strip())
    return BASEURL + "/assets/images/" + encoded


def convert_body(text: str) -> str:
    # 1) image embeds -> standard markdown with url-encoded path
    text = EMBED_RE.sub(lambda m: f"![]({web_image_path(m.group(1))})", text)
    # 2) leftover [[wikilinks]] -> just the inner text (Jekyll has no vault)
    text = WIKILINK_RE.sub(lambda m: f"`{m.group(1)}`", text)
    return text


def make_front_matter(title: str, difficulty: str, os_name: str) -> str:
    return (
        "---\n"
        "layout: writeup\n"
        f'title: "{title}"\n'
        f"difficulty: {difficulty}\n"
        f"os: {os_name}\n"
        "---\n\n"
    )


def build() -> None:
    POSTS_OUT.mkdir(parents=True, exist_ok=True)
    IMAGES_OUT.mkdir(parents=True, exist_ok=True)

    # Copy every image once, keeping the original name (spaces handled in links).
    if IMAGES_SRC.exists():
        for img in IMAGES_SRC.iterdir():
            if img.is_file():
                shutil.copy2(img, IMAGES_OUT / img.name)

    count = 0
    for diff in SOURCE_DIRS:
        diff_dir = CONTENT_DIR / diff
        if not diff_dir.exists():
            continue
        for os_dir in diff_dir.iterdir():
            if not os_dir.is_dir():
                continue
            os_name = os_dir.name  # "Linux" or "Windows"
            for md in os_dir.glob("*.md"):
                title = md.stem
                body = convert_body(md.read_text(encoding="utf-8"))
                # Jekyll requires posts to be named YYYY-MM-DD-title.md.
                # Use the file's own modification date so each writeup keeps its real date.
                mtime = datetime.date.fromtimestamp(md.stat().st_mtime)
                slug = title.lower().replace(" ", "-")
                out_name = f"{mtime.isoformat()}-{slug}.md"
                (POSTS_OUT / out_name).write_text(
                    make_front_matter(title, diff, os_name) + body,
                    encoding="utf-8",
                )
                count += 1
                print(f"  converted: {diff}/{os_name}/{md.name}")

    print(f"\nDone. {count} writeups converted. Now: git add . && git commit && git push")


if __name__ == "__main__":
    build()
