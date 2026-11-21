import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "scripts" / "gh_arsenal.py"
MCP_SERVER = ROOT / "scripts" / "mcp_server.py"


class TestGitHubAIArsenal(unittest.TestCase):
    def _run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=25,
        )

    def test_stats_has_over_20000_tools(self):
        proc = self._run_cli("stats", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertGreaterEqual(data["mega_index_total"], 20000)
        self.assertGreaterEqual(data["core_elite_tools"], 50)

    def test_doctor_command(self):
        proc = self._run_cli("doctor", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIn("runtimes", data)
        self.assertGreaterEqual(data["mega_index_tools"], 20000)

    def test_mega_offline_search_and_ranking(self):
        proc = self._run_cli("mega", "--query", "mcp postgres", "--limit", "5", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertGreater(data["total_matches"], 0)
        self.assertLessEqual(len(data["tools"]), 5)

    def test_recommend_arabic_and_english(self):
        p_ar = self._run_cli("recommend", "بوت تليجرام وكشط مواقع", "--json")
        self.assertEqual(p_ar.returncode, 0, p_ar.stderr)
        d_ar = json.loads(p_ar.stdout)
        self.assertGreater(len(d_ar["core_matches"]), 0)

        p_en = self._run_cli("recommend", "security audit and reverse engineering", "--json")
        self.assertEqual(p_en.returncode, 0, p_en.stderr)
        d_en = json.loads(p_en.stdout)
        self.assertGreater(len(d_en["core_matches"]), 0)

    def test_stack_command(self):
        proc_list = self._run_cli("stack", "list", "--json")
        self.assertEqual(proc_list.returncode, 0, proc_list.stderr)
        data_list = json.loads(proc_list.stdout)
        self.assertIn("available_stacks", data_list)
        self.assertGreaterEqual(len(data_list["available_stacks"]), 8)

        proc_saas = self._run_cli("stack", "saas-ai", "--json")
        self.assertEqual(proc_saas.returncode, 0, proc_saas.stderr)
        data_saas = json.loads(proc_saas.stdout)
        self.assertEqual(data_saas["id"], "saas-ai")
        self.assertGreater(len(data_saas["components"]), 3)

    def test_audit_repo_offline_fallback(self):
        # Test audit-repo produces structured output
        proc = self._run_cli("audit-repo", "torvalds/linux", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIn("trust_score", data)
        self.assertIn("verdict", data)

    def test_mcp_config_generator(self):
        proc = self._run_cli("mcp-config", "github")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIn("mcpServers", data)
        self.assertIn("github", data["mcpServers"])

    def test_quickstart_and_bookmarks(self):
        proc_q = self._run_cli("quickstart", "unclecode/crawl4ai", "--json")
        self.assertEqual(proc_q.returncode, 0, proc_q.stderr)
        dq = json.loads(proc_q.stdout)
        self.assertEqual(dq["repo"], "unclecode/crawl4ai")

        proc_b = self._run_cli("bookmark", "add", "unclecode/crawl4ai", "--note", "Great LLM Crawler", "--json")
        self.assertEqual(proc_b.returncode, 0, proc_b.stderr)
        proc_l = self._run_cli("bookmark", "list", "--json")
        self.assertEqual(proc_l.returncode, 0, proc_l.stderr)
        dl = json.loads(proc_l.stdout)
        self.assertGreaterEqual(dl["count"], 1)

    def test_analyze_project_and_deep_scan(self):
        proc_az = self._run_cli("analyze", ".", "--json")
        self.assertEqual(proc_az.returncode, 0, proc_az.stderr)
        daz = json.loads(proc_az.stdout)
        self.assertIn("detected_stack", daz)
        self.assertIn("recommended_core_tools", daz)

        proc_sc = self._run_cli("scan", "fazah-arsenal/github-ai-arsenal", "--json")
        self.assertEqual(proc_sc.returncode, 0, proc_sc.stderr)
        dsc = json.loads(proc_sc.stdout)
        self.assertIn("verdict", dsc)
        self.assertIn("files_scanned", dsc)

    def test_give_snippet_and_memory(self):
        proc_m = self._run_cli("memory", "log", "unclecode/crawl4ai", "--task", "web scraping", "--outcome", "success", "--note", "Works great", "--json")
        self.assertEqual(proc_m.returncode, 0, proc_m.stderr)
        proc_g = self._run_cli("give", "web scraping", "--json")
        self.assertEqual(proc_g.returncode, 0, proc_g.stderr)
        dg = json.loads(proc_g.stdout)
        self.assertIn("delivered_tool", dg)
        self.assertIn("security_scan", dg)
        self.assertIn("self_healing", dg)
        self.assertGreaterEqual(len(dg["verified_in_memory"]), 1)

    def test_adaptive_error_learning_and_self_healing(self):
        # 1. Teach Arsenal about a broken tool and its alternative
        proc_l = self._run_cli(
            "memory", "learn", "bogus/broken-scraper",
            "--task", "scraping",
            "--outcome", "failed",
            "--error", "ModuleNotFoundError: No module named 'libxml2'",
            "--fix", "Use unclecode/crawl4ai which is pure python",
            "--alt", "unclecode/crawl4ai",
            "--json"
        )
        self.assertEqual(proc_l.returncode, 0, proc_l.stderr)
        dl = json.loads(proc_l.stdout)
        self.assertEqual(dl["action"], "learned")
        self.assertEqual(dl["entry"]["error_type"], "missing_dependency")
        self.assertGreaterEqual(dl["entry"]["fail_count"], 1)

        # 2. Query recorded mistakes
        proc_mis = self._run_cli("memory", "mistakes", "--json")
        self.assertEqual(proc_mis.returncode, 0, proc_mis.stderr)
        dmis = json.loads(proc_mis.stdout)
        self.assertGreaterEqual(dmis["count"], 1)
        self.assertTrue(any(m["repo"] == "bogus/broken-scraper" for m in dmis["mistakes"]))

        # 3. Test recommendation surfaces the learned fix and penalizes the failing tool
        proc_rec = self._run_cli("recommend", "scraping", "--json")
        self.assertEqual(proc_rec.returncode, 0, proc_rec.stderr)
        drec = json.loads(proc_rec.stdout)
        self.assertIn("learned_replacements", drec)
        self.assertTrue(any(r["failed_repo"] == "bogus/broken-scraper" for r in drec["learned_replacements"]))

    def test_native_mcp_server_stdio(self):
        # Simulate stdio JSON-RPC handshake, tools, resources & prompts listing
        reqs = (
            json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
            + "\n"
            + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
            + "\n"
            + json.dumps({"jsonrpc": "2.0", "id": 3, "method": "resources/list", "params": {}})
            + "\n"
            + json.dumps({"jsonrpc": "2.0", "id": 4, "method": "prompts/list", "params": {}})
            + "\n"
        )
        proc = subprocess.run(
            [sys.executable, str(MCP_SERVER)],
            input=reqs,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [line.strip() for line in proc.stdout.strip().split("\n") if line.strip()]
        self.assertGreaterEqual(len(lines), 4)
        resp1 = json.loads(lines[0])
        expected_ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(resp1.get("result", {}).get("serverInfo", {}).get("version"), expected_ver)
        resp2 = json.loads(lines[1])
        tool_names = [t["name"] for t in resp2.get("result", {}).get("tools", [])]
        self.assertGreaterEqual(len(tool_names), 17)
        self.assertIn("arsenal_give_tool", tool_names)
        self.assertIn("arsenal_get_snippet", tool_names)
        self.assertIn("arsenal_memory", tool_names)
        resp3 = json.loads(lines[2])
        self.assertGreaterEqual(len(resp3.get("result", {}).get("resources", [])), 4)
        resp4 = json.loads(lines[3])
        self.assertGreaterEqual(len(resp4.get("result", {}).get("prompts", [])), 3)

    def test_zero_touch_mcp_auto_link(self):
        proc = self._run_cli("link", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertTrue(data.get("ok"))
        self.assertIn("linked_clients", data)
        self.assertGreaterEqual(len(data["linked_clients"]), 4)
        client_names = [c["client"] for c in data["linked_clients"]]
        self.assertIn("Claude Desktop", client_names)
        self.assertIn("Cursor User", client_names)
        self.assertIn("Current Workspace", client_names)


if __name__ == "__main__":
    unittest.main()
