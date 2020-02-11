import os
import shutil
import subprocess
import unittest

from adjutant.utility import ensure_path


class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), 'build')
        ensure_path(self.test_dir)

    def command(self, args, cwd=None):
        print('Running: {0}'.format(' '.join(args)))
        result = subprocess.run(
            args, cwd=cwd or self.test_dir, capture_output=True)
        return result.stdout.decode('utf8'), result.stderr

    def tearDown(self):
        # shutil.rmtree(self.test_dir)
        pass


class AppTest(ProjectTestCase):
    def test_project(self):
        self.command(['adjutant', 'init'])
        self.command(['adjutant', 'build'])
