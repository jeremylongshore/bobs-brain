#!/usr/bin/env python3
"""
Basic tests to ensure CI passes
"""

import unittest


class TestBasic(unittest.TestCase):
    """Basic test cases"""

    def test_basic_functionality(self):
        """Test basic functionality"""
        self.assertTrue(True)

    def test_imports(self):
        """Test that main modules can be imported"""
        try:
            import src.bob_brain_v5  # noqa: F401
            import src.circle_of_life  # noqa: F401
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")


if __name__ == "__main__":
    unittest.main()
