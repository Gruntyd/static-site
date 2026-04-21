import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
	# station 1
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	# station 2
	with open(from_path) as f:
		contents = f.read()
	# station 3
	with open(template_path) as f:
		template = f.read()
	# station 4
	node = markdown_to_html_node(contents)
	html = node.to_html()
	# station 5
	title = extract_title(contents)
	# station 6
	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", html)
	# station 7 part a
	dest_dir_path = os.path.dirname(dest_path)
	if dest_dir_path != "":
		os.makedirs(dest_dir_path, exist_ok=True)
	# station 7 part b
	with open(dest_path, "w") as f:
		f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            generate_page(src_path, template_path, dst_path.replace(".md", ".html"))
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path)

def extract_title(markdown):
	for line in markdown.splitlines():
		stripped = line.lstrip()
		if stripped.startswith('# '):
			return stripped[2:].strip()
	raise ValueError("No h1 header found in markdown")