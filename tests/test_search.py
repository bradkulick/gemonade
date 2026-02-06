import unittest
import subprocess
from pathlib import Path
from tests.test_helper import BaseGemonadeTest, PROJECT_ROOT

class TestGemonadeSearch(BaseGemonadeTest):

    def test_search_invocation(self):
        """Verify search command executes (integration test)."""
        # We search for a dummy term. 
        # Even if it hits the network and fails, it should catch the exception and print error, 
        # exiting cleanly or with code 1, but not crashing with traceback.
        
        result = self.run_cli(["search", "gemonade-test-query"])
        
        # We expect the core to handle it.
        # It might output "Searching..."
        self.assertIn("Searching", result.stdout)
        
        # It shouldn't crash with a Python traceback
        self.assertNotIn("Traceback", result.stderr)

if __name__ == "__main__":
    unittest.main()