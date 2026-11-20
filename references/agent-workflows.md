# Battle-Tested GitHub AI Agent Workflows

Load and apply these engineering workflows from top GitHub AI projects when solving complex user tasks.

## 1. Aider Repo-Map & Surgical Editing (`Aider-AI/aider`)
1. Map the project structure before modifying anything (`list files`, identify entry points and dependencies).
2. Read exact target line ranges before editing.
3. Prefer minimal, surgical diff/patch edits over rewriting entire files blindly.
4. Always verify syntax/tests (`py_compile`, `pytest`, `npm test`) after the final edit.

## 2. Fabric Structured Analysis (`danielmiessler/fabric`)
When analyzing code, docs, or security architectures, structure output cleanly:
- **Summary**: 2–3 sentences stating purpose and architecture.
- **Key Findings / Risks**: Concrete evidence with file/line references.
- **Actionable Patch Plan**: Exact steps or ready-to-apply code.

## 3. Multi-Agent Swarm Decomposition (`crewAIInc/crewAI` & `langchain-ai/langgraph`)
For large end-to-end builds, execute in 3 explicit phases (or spawn 3 subagents):
1. **Architect & GitHub Scout**: Inspect workspace, find existing GitHub tools/libraries via `gh_arsenal.py`, design file layout.
2. **Lead Developer**: Implement complete runnable code with zero placeholders.
3. **Security & QA Auditor**: Run tests, check for hardcoded secrets (`gitleaks` patterns), edge cases, and runtime errors.

## 4. Ralph Autonomous Goal Loop (`deepseek-ai/deepseek-harness`)
For tasks requiring guaranteed completion:
1. Define clear, verifiable acceptance criteria up front.
2. Execute -> Test -> Inspect Failure -> Patch -> Re-test iteratively.
3. Never declare completion until the final verification command passes cleanly.

## 5. Live GitHub Tool Acquisition (`github-ai-arsenal`)
Before writing a complex utility from scratch:
1. Run `python scripts/gh_arsenal.py recommend "<task>"` to check the curated 38-tool catalog.
2. If not in the catalog, run `python scripts/gh_arsenal.py search "<keywords>"` to query GitHub live.
3. Inspect the top candidate via `inspect` or `fetch` before pulling or installing.
