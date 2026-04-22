import os
import sys
from textnode import TextNode, TextType
from copystatic import copy_files_recursive, clear_dir
from gencontent import generate_page, generate_pages_recursive

def main():
	node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
	print(node)

	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	else:
		basepath = "/"

	clear_dir("docs")
	copy_files_recursive("static", "docs")

	generate_pages_recursive("content", "template.html", "docs", basepath)

main()
