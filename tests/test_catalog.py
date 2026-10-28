import copy
import csv
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = build.load_catalog(ROOT)

    def test_unknown_source_is_rejected(self):
        changed = copy.deepcopy(self.data)
        changed["products"][0]["plans"][0]["source_ids"] = ["missing-source"]
        with self.assertRaisesRegex(ValueError, "Unknown source"):
            build.validate_catalog(changed, ROOT)

    def test_second_bitbrowser_paid_plan_is_rejected(self):
        changed = copy.deepcopy(self.data)
        extra = copy.deepcopy(changed["products"][0]["plans"][1])
        extra["id"] = "second-paid-plan"
        changed["products"][0]["plans"].append(extra)
        with self.assertRaisesRegex(ValueError, "one Chinese-site paid plan"):
            build.validate_catalog(changed, ROOT)

    def test_csv_preserves_commas_and_unknown_permissions(self):
        changed = copy.deepcopy(self.data)
        changed["products"][1]["plans"][0]["conditions"] = 'Quoted value: "a,b"; another line\nnext'
        outputs = build.render_outputs(changed, ROOT)
        rows = list(csv.DictReader(io.StringIO(outputs["data/browser-plans.csv"])))
        ads = next(r for r in rows if r["product_id"] == "adspower" and r["id"] == "free")
        self.assertEqual(ads["conditions"], 'Quoted value: "a,b"; another line\nnext')
        self.assertEqual(ads["api"], "unknown")
        original_ads = next(p for p in self.data["products"] if p["id"] == "adspower")
        self.assertEqual(ads["checked_at"], build.get_free(original_ads)["checked_at"])
        exported = json.loads(outputs["data/browser-plans.json"])
        self.assertEqual(len(rows), len(exported["plans"]))

    def test_reader_pages_do_not_publish_internal_notes(self):
        changed = copy.deepcopy(self.data)
        changed["products"][0]["sources"][0]["note"] = "INTERNAL_SOURCE_NOTE"
        free = changed["products"][0]["plans"][0]
        free["confidence"] = "source_conflict"
        free["conflict_note"] = "INTERNAL_CONFLICT_NOTE"
        outputs = build.render_outputs(changed, ROOT)
        for path, text in outputs.items():
            if path.endswith(".md"):
                self.assertNotIn("INTERNAL_SOURCE_NOTE", text)
                self.assertNotIn("INTERNAL_CONFLICT_NOTE", text)

    def test_check_detects_manual_generated_table_edits(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder) / "repo"
            shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("__pycache__"))
            readme = work / "README.md"
            text = readme.read_text()
            begin = text.index("<!-- BEGIN GENERATED:overview -->")
            text = text[:begin] + text[begin:].replace("10 个环境", "999 个环境", 1)
            readme.write_text(text)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--root", str(work), "--check"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("README.md", result.stderr)

    def test_paid_only_browser_is_not_a_free_plan(self):
        octo = next(p for p in self.data['products'] if p['id'] == 'octo-browser')
        self.assertIsNone(build.get_free(octo))
        outputs = build.render_outputs(self.data, ROOT)
        self.assertIn('无长期免费版', outputs['browsers/octo-browser.md'])
        free_block = outputs['guides/best-free-fingerprint-browsers.md'].split('<!-- BEGIN GENERATED:free-comparison -->')[1].split('<!-- END GENERATED:free-comparison -->')[0]
        self.assertNotIn('octo-browser.md', free_block)

    def test_cloud_profiles_and_runtime_are_exported_separately(self):
        outputs = build.render_outputs(self.data, ROOT)
        rows = json.loads(outputs['data/browser-plans.json'])['plans']
        free = next(p for p in rows if p['product_id'] == 'kameleo' and p['id'] == 'free')
        self.assertEqual(free['profile_scope'], 'cloud_browser')
        self.assertEqual(free['profiles'], 100)
        self.assertEqual(free['runtime_minutes'], 300)
        self.assertEqual(free['concurrent_profiles'], 2)

    def test_encoded_links_and_heading_anchors(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            (work/'README.md').write_text('[安装](带%20空格.md#安装与检查)\n[重复](带%20空格.md#test-1)\n')
            (work/'带 空格.md').write_text('# 使用\n\n## 安装与检查\n\n## Test\n\n## Test\n')
            build.validate_links(work)
            (work/'README.md').write_text('[失效](带%20空格.md#不存在)\n')
            with self.assertRaisesRegex(ValueError, 'Broken heading anchor'):
                build.validate_links(work)

    def test_orphan_reader_page_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            (work/'README.md').write_text('# 首页\n')
            (work/'guides').mkdir()
            (work/'guides'/'hidden.md').write_text('# 没有入口的指南\n')
            with self.assertRaisesRegex(ValueError, 'not reachable'):
                build.validate_links(work)


if __name__ == "__main__":
    unittest.main()
