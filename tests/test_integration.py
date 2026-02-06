import unittest
import json
from pathlib import Path
from tests.test_helper import BaseGemonadeTest

class TestGemonadeIntegration(BaseGemonadeTest):

    def test_run_dry_run_state(self):
        """Verify the 'run' command dry-run state output."""
        result = self.run_cli(["run", "smoke-gem", "--project=test-proj", "--scope=global", "--dry-run"])
        self.assertEqual(result.returncode, 0)
        
        state = json.loads(result.stdout)
        self.assertEqual(state["project_context"], "test-proj")
        self.assertEqual(state["scope"], "global")
        self.assertIn("Active Access Scope: GLOBAL", state["system_prompt_content"])

    def test_install_lifecycle(self):
        """Test full install/uninstall via CLI."""
        # 1. Install
        result = self.run_cli(["install", str(self.local_pkg / "smoke-gem")])
        self.assertEqual(result.returncode, 0)
        self.assertTrue((self.installed_pkg / "smoke-gem").exists())
        
        # 2. Uninstall
        result = self.run_cli(["uninstall", "smoke-gem"])
        self.assertEqual(result.returncode, 0)
        self.assertFalse((self.installed_pkg / "smoke-gem").exists())

    def test_security_barrier(self):
        """Verify security checks block invalid paths."""
        result = self.run_cli(["uninstall", "../../etc/passwd"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error", result.stderr)

    def test_config_display(self):
        """Verify the 'config' command shows current settings."""
        result = self.run_cli(["config"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("G_PACKAGE_ROOT", result.stdout)
        self.assertIn(str(self.pkg_root), result.stdout)

if __name__ == "__main__":
    unittest.main()
