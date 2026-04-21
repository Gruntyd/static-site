import os
from textnode import TextNode, TextType
from copystatic import copy_files_recursive, clear_dir
from gencontent import generate_page, generate_pages_recursive

def main():
	node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
	print(node)

	clear_dir("public")
	copy_files_recursive("static", "public")

	# generate_page("content/index.md", "template.html", "public/index.html")
	generate_pages_recursive("content", "template.html", "public")

main()
