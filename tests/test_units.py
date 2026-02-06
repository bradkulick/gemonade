import unittest
import json
from pathlib import Path
from tests.test_helper import BaseGemonadeTest
from core import gemonade

class TestGemonadeUnits(BaseGemonadeTest):
    
    def test_validate_gem_name(self):
        """Test gem name validation logic."""
        self.assertEqual(gemonade.validate_gem_name("my-gem"), "my-gem")
        self.assertEqual(gemonade.validate_gem_name("gem.v1"), "gem.v1")
        
        with self.assertRaises(ValueError):
            gemonade.validate_gem_name("../evil")
        with self.assertRaises(ValueError):
            gemonade.validate_gem_name("gem name")
        with self.assertRaises(ValueError):
            gemonade.validate_gem_name("gem/slash")

    def test_load_config(self):
        """Test config loading with overrides."""
        config = gemonade.load_config(self.config_file)
        self.assertEqual(config["G_PACKAGE_ROOT"], str(self.pkg_root))
        self.assertEqual(config["G_KNOWLEDGE_DIR"], str(self.knowledge_dir))

    def test_find_persona_file(self):
        """Test persona file discovery precedence."""
        config = gemonade.load_config(self.config_file)
        
        # 1. Create in Core
        self.create_gem(self.core_pkg, "sys", "Built-in sys")
        path = gemonade.find_persona_file("sys", config)
        self.assertTrue(str(path).endswith("core/sys/persona.md"))
        
        # 2. Local shadows Core
        self.create_gem(self.local_pkg, "sys", "Local sys override")
        path = gemonade.find_persona_file("sys", config)
        self.assertTrue(str(path).endswith("local/sys/persona.md"))

    def test_get_gems_list(self):
        """Test the logic for gathering the list of gems."""
        config = gemonade.load_config(self.config_file)
        self.create_gem(self.installed_pkg, "community-gem", "Helpful tool")
        
        gems = gemonade.get_gems_list(config)
        self.assertIn("smoke-gem", [g[0] for g in gems["LOCAL"]])
        self.assertIn("community-gem", [g[0] for g in gems["INSTALLED"]])

if __name__ == "__main__":
    unittest.main()
