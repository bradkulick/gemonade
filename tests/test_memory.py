import unittest
import json
from tests.test_helper import BaseGemonadeTest

class TestGemonadeMemory(BaseGemonadeTest):

    def test_memory_enable_dry_run(self):
        """Verify the memory enable command dry-run logic."""
        result = self.run_cli(["advanced-memory", "enable", "--dry-run"])
        self.assertEqual(result.returncode, 0)
        
        state = json.loads(result.stdout)
        self.assertEqual(state["action"], "enable")
        self.assertEqual(state["status"], "deprecated")

    def test_memory_disable_dry_run(self):
        """Verify the memory disable command dry-run logic."""
        result = self.run_cli(["advanced-memory", "disable", "--dry-run"])
        self.assertEqual(result.returncode, 0)
        
        state = json.loads(result.stdout)
        self.assertEqual(state["action"], "disable")
        self.assertEqual(state["status"], "deprecated")

if __name__ == "__main__":
    unittest.main()
