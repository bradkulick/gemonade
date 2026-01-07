import os
import sys
import json
import shutil
import unittest
import subprocess
from pathlib import Path

# Add project root to sys.path so we can import core.gemonade
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class BaseGemonadeTest(unittest.TestCase):
    def setUp(self):
        """Setup a localized Gemonade environment for each test."""
        # Unique temp directory per test to ensure isolation
        self.test_id = self.id().split('.')[-1]
        self.temp_env = PROJECT_ROOT / "tests" / f"tmp_{self.test_id}"
        if self.temp_env.exists():
            shutil.rmtree(self.temp_env)
        self.temp_env.mkdir(parents=True)
        
        # Scaffold Fake Package Root
        self.pkg_root = self.temp_env / "packages"
        self.local_pkg = self.pkg_root / "local"
        self.installed_pkg = self.pkg_root / "installed"
        self.core_pkg = self.pkg_root / "core"
        
        for d in [self.local_pkg, self.installed_pkg, self.core_pkg]:
            d.mkdir(parents=True)

        # Scaffold Fake Config
        self.config_file = self.temp_env / ".gemonade_config"
        self.knowledge_dir = self.temp_env / "knowledge"
        self.knowledge_dir.mkdir()
        
        with open(self.config_file, 'w') as f:
            f.write(f'G_PACKAGE_ROOT="{self.pkg_root}"\n')
            f.write(f'G_KNOWLEDGE_DIR="{self.knowledge_dir}"\n')
            f.write(f'G_CORE_PERSONA="{PROJECT_ROOT}/core/CORE_PERSONA.md"\n')
            f.write(f'G_SAVER_SCRIPT="{PROJECT_ROOT}/tools/save_session.py"\n')

        # Environment Overrides
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.temp_env)
        
        # Dummy Gem
        self.create_gem(self.local_pkg, "smoke-gem", "Be a dummy.")

    def tearDown(self):
        """Cleanup."""
        if self.temp_env.exists():
            shutil.rmtree(self.temp_env)

    def create_gem(self, root, name, objective):
        gem_dir = root / name
        gem_dir.mkdir(parents=True, exist_ok=True)
        (gem_dir / "gem.json").write_text(json.dumps({
            "name": name, 
            "version": "0.1.0",
            "description": objective
        }))
        (gem_dir / "persona.md").write_text(f"# {name}\n- **Objective:** {objective}")
        (gem_dir / "tools").mkdir(exist_ok=True)
        return gem_dir


    def run_cli(self, args):
        """Helper to run the core CLI via subprocess."""
        cli_path = PROJECT_ROOT / "core" / "gemonade.py"
        cmd = [sys.executable, str(cli_path)] + args
        return subprocess.run(cmd, env=self.env, capture_output=True, text=True)
