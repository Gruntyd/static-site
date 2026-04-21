import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_not_equal_different_text(self):
		a = TextNode("First", TextType.BOLD)
		b = TextNode("Second", TextType.BOLD)
		self.assertNotEqual(a, b)

	def test_not_equal_different_type(self):
		a = TextNode("Same text", TextType.BOLD)
		b = TextNode("Same text", TextType.ITALIC)
		self.assertNotEqual(a, b)

	def test_not_equal_different_url_vs_none(self):
		a = TextNode("Link text", TextType.LINK, url="https://example.com")
		b = TextNode("Link text", TextType.LINK, url=None)
		self.assertNotEqual(a, b)

	def test_equal_when_both_url_none(self):
		a = TextNode("No url", TextType.TEXT, url=None)
		b = TextNode("No url", TextType.TEXT, url=None)
		self.assertEqual(a, b)

	def test_not_equal_other_type_comparison(self):
		a = TextNode("other", TextType.TEXT)
		self.assertNotEqual(a, "other")

	def test_hash_consistancy_if_appplicable(self):
		a = TextNode("hashme", TextType.BOLD)
		b = TextNode("hashme", TextType.BOLD)
		try:
			self.assertEqual(hash(a), hash(b))
		except TypeError:
			pass

	def test_text(self):
	    node = TextNode("This is a text node", TextType.TEXT)
	    html_node = text_node_to_html_node(node)
	    self.assertEqual(html_node.tag, None)
	    self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
	    node = TextNode("This is a bold node", TextType.BOLD)
	    html_node = text_node_to_html_node(node)
	    self.assertEqual(html_node.tag, "b")
	    self.assertEqual(html_node.value, "This is a bold node")

	def test_image(self):
		node = TextNode("This is an image node", TextType.IMAGE, "https://example.com/img.png")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, {"src": "https://example.com/img.png", "alt": "This is an image node"})

if __name__ == "__main__":
	unittest.main()
