import unittest

import comfyui_primitive_ops


class StringSplit2Tests(unittest.TestCase):
    def setUp(self):
        self.node_class = comfyui_primitive_ops.NODE_CLASS_MAPPINGS["JWStringSplit2"]
        self.node = self.node_class()

    def test_node_interface(self):
        inputs = self.node_class.INPUT_TYPES()["required"]
        self.assertEqual(inputs["source"], ("STRING", {"forceInput": True}))
        self.assertEqual(set(inputs), {"source", "split_by"})
        self.assertEqual(self.node_class.RETURN_TYPES, ("STRING_LIST",))
        self.assertEqual(
            comfyui_primitive_ops.NODE_DISPLAY_NAME_MAPPINGS["JWStringSplit2"],
            "String Split 2",
        )

    def test_splits_all_and_removes_empty_trimmed_items(self):
        self.assertEqual(
            self.node.execute(" , first, , second,\n third , ", ","),
            (["first", "second", "third"],),
        )

    def test_no_delimiter_and_empty_results(self):
        self.assertEqual(self.node.execute("  single  ", ","), (["single"],))
        self.assertEqual(self.node.execute(" , \t, ", ","), ([],))
        self.assertEqual(self.node.execute("", ","), ([],))

    def test_multicharacter_delimiter_and_empty_delimiter(self):
        self.assertEqual(self.node.execute(" a :: b :: c ", "::"), (["a", "b", "c"],))
        with self.assertRaises(ValueError):
            self.node.execute("a", "")

    def test_original_split_remains_unchanged(self):
        node = comfyui_primitive_ops.NODE_CLASS_MAPPINGS["JWStringSplit"]()
        self.assertEqual(node.execute(" a,b,c ", ",", "false"), (" a", "b,c "))
        self.assertEqual(node.execute(" a,b,c ", ",", "true"), (" a,b", "c "))


if __name__ == "__main__":
    unittest.main()
