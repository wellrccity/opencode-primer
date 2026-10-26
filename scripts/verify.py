#!/usr/bin/env python3
"""Repository verification for opencode-primer (work package W8).

Standard library only, Python 3.9+, cross-platform, no network access.
Every check prints one PASS or FAIL line. Exit code 0 only when all pass.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILL_IDS = (
    "anti-slop-docs",
    "brainstorm-grill",
    "browser-control",
    "caveman-mode",
    "code-review",
    "create-skill",
    "execution-focus",
    "git-safe",
    "mandatory-verification",
    "meta-goal",
    "professional-workflow",
    "session-handoff",
    "systematic-debugging",
    "tdd-plan",
    "understand-code",
    "web-research",
)

REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".gitignore",
    ".editorconfig",
    ".gitattributes",
    ".github/workflows/verify.yml",
    "config/opencode.json",
    "config/opencode.example.json",
    "config/cli.json",
    "config/AGENTS.md",
    "agents/reviewer.md",
    "agents/planner.md",
    "agents/team-worker.md",
    "agents/team-worker-free.md",
    "agents/team-reviewer.md",
    "agents/team-worker-paid.md",
    "commands/team-build.md",
    "commands/verify.md",
    "commands/review.md",
    "commands/plan.md",
    "commands/grill.md",
    "commands/tdd.md",
    "commands/handoff.md",
    "commands/map.md",
    "plugins/meta-goal/index.js",
    "plugins/meta-goal/package.json",
    "scripts/install.ps1",
    "scripts/install.sh",
    "scripts/verify.py",
    "docs/INSTALL.md",
    "docs/CONFIGURATION.md",
    "docs/SKILLS.md",
    "docs/MIGRATION.md",
) + tuple("skills/%s/SKILL.md" % skill for skill in SKILL_IDS)

TEXT_EXTS = {
    ".md",
    ".json",
    ".js",
    ".py",
    ".sh",
    ".ps1",
    ".yml",
    ".yaml",
    ".editorconfig",
    ".gitattributes",
}
TEXT_NAMES = {".editorconfig", ".gitattributes"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}

README_HEADINGS = (
    "What's inside",
    "Requirements",
    "Quick start",
    "Repository layout",
    "Skills",
    "Agents",
    "Commands",
    "Configuration",
    "Verification",
    "Publishing to GitHub",
    "License",
)

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$")

# Whole Portuguese words that must not appear outside docs/MIGRATION.md.
PORTUGUESE_RE = re.compile(
    r"(?i)\b(?:nao|voce|arquivo|tarefa|codigo|revisao|fluxo|proximo|"
    r"mudanca|verificacao|saida|caminho|segredo|pasta)\b"
)

SECRET_PATTERNS = (
    ("sk- key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")),
    ("ghp_ token", re.compile(r"\bghp_[A-Za-z0-9]{10,}")),
    ("AKIA key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("service account file", re.compile(r"service\.json")),
)
SECRET_ASSIGN_RE = re.compile(
    r"""(?i)\b(?:password|api[_-]?key)\b["']?[ \t]*[:=][ \t]*["']?([^\s"',;]+)"""
)
PLACEHOLDER_PREFIXES = ("{env:", "{file:", "$", "%", "<", "[")
PLACEHOLDER_VALUES = {"", "null", "true", "false", "none"}

PATH_PATTERNS = (
    ("absolute Windows user path", re.compile(r"C:\\Users\\")),
    ("absolute POSIX home path", re.compile(r"/home/[A-Za-z0-9._-]+/")),
    ("temporary tunnel host", re.compile(r"trycloudflare\.com")),
)

# AGENTS.md is the build specification: it quotes the forbidden words, the
# credential filename, and the path prefix as rules, so content scans skip it.
CONTENT_SCAN_SKIP = {"docs/MIGRATION.md", "scripts/verify.py", "AGENTS.md"}


class Checker:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []

    def check(self, name, ok, detail=""):
        if ok:
            self.passed += 1
            print("PASS %s" % name)
        else:
            self.failed += 1
            self.failures.append(name)
            suffix = (" - " + detail) if detail else ""
            print("FAIL %s%s" % (name, suffix))
        return ok


def iter_files():
    for path in sorted(ROOT.rglob("*")):
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_file():
            yield path


def is_text_file(path):
    return path.suffix.lower() in TEXT_EXTS or path.name in TEXT_NAMES


def iter_texts():
    for path in iter_files():
        if not is_text_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        yield path.relative_to(ROOT).as_posix(), text


def read_text(path):
    try:
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeDecodeError) as exc:
        return None, str(exc)


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data = {}
    current = None
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            current = match.group(1)
            data[current] = match.group(2).strip()
        elif current and (
            line.startswith((" ", "\t")) or line.lstrip().startswith("-")
        ):
            data[current] = (data[current] + " " + line.strip()).strip()
        else:
            return None
    return data if closed else None


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def skill_dirs():
    base = ROOT / "skills"
    if not base.is_dir():
        return []
    return sorted(path for path in base.iterdir() if path.is_dir())


def summarize(items, limit=6):
    items = list(items)
    detail = ", ".join(items[:limit])
    if len(items) > limit:
        detail += ", ..."
    return detail


def check_required_files(chk):
    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).is_file()]
    chk.check(
        "required files exist",
        not missing,
        "%d missing: %s" % (len(missing), summarize(missing)) if missing else "",
    )


def check_no_empty_files(chk):
    empty = []
    for path in iter_files():
        try:
            if path.stat().st_size == 0:
                empty.append(path.relative_to(ROOT).as_posix())
        except OSError as exc:
            empty.append("%s (%s)" % (path.relative_to(ROOT).as_posix(), exc))
    chk.check("no empty files", not empty, summarize(empty))


def check_config_json(chk):
    base = ROOT / "config"
    paths = sorted(base.glob("*.json")) if base.is_dir() else []
    bad = []
    for path in paths:
        text, err = read_text(path)
        if text is None:
            bad.append("%s: %s" % (path.name, err))
            continue
        try:
            json.loads(text)
        except ValueError as exc:
            bad.append("%s: %s" % (path.name, exc))
    ok = bool(paths) and not bad
    detail = summarize(bad) if bad else ("no config/*.json found" if not paths else "")
    chk.check("config JSON files parse", ok, detail)


def check_example_mcp_disabled(chk):
    name = "example MCP servers use disabled"
    path = ROOT / "config" / "opencode.example.json"
    if not path.is_file():
        chk.check(name, False, "config/opencode.example.json missing")
        return
    text, err = read_text(path)
    if text is None:
        chk.check(name, False, err)
        return
    try:
        data = json.loads(text)
    except ValueError as exc:
        chk.check(name, False, str(exc))
        return
    mcp = data.get("mcp") if isinstance(data, dict) else None
    servers = mcp.get("servers") if isinstance(mcp, dict) else None
    if not isinstance(servers, dict) or not servers:
        chk.check(name, False, "mcp.servers missing or empty")
        return
    bad = []
    for server_name, server in servers.items():
        if not isinstance(server, dict):
            bad.append("%s: not an object" % server_name)
            continue
        if server.get("disabled") is not True:
            bad.append("%s: disabled is not true" % server_name)
        if "enabled" in server:
            bad.append("%s: enabled key present" % server_name)
    chk.check(name, not bad, summarize(bad))


def check_schema(chk):
    path = ROOT / "config" / "opencode.json"
    if not path.is_file():
        chk.check(
            "config/opencode.json has $schema", False, "config/opencode.json missing"
        )
        return
    text, err = read_text(path)
    if text is None:
        chk.check("config/opencode.json has $schema", False, err)
        return
    try:
        data = json.loads(text)
    except ValueError as exc:
        chk.check("config/opencode.json has $schema", False, str(exc))
        return
    schema = data.get("$schema") if isinstance(data, dict) else None
    ok = isinstance(schema, str) and bool(schema.strip())
    chk.check(
        "config/opencode.json has $schema", ok, "" if ok else "missing or empty $schema"
    )


def check_skill_set(chk):
    names = sorted(path.name for path in skill_dirs())
    expected = sorted(SKILL_IDS)
    if names == expected:
        chk.check("skill directories match the 16 IDs", True)
        return
    missing = sorted(set(expected) - set(names))
    extra = sorted(set(names) - set(expected))
    parts = []
    if missing:
        parts.append("missing: " + ", ".join(missing))
    if extra:
        parts.append("unexpected: " + ", ".join(extra))
    chk.check("skill directories match the 16 IDs", False, "; ".join(parts))


def check_skill_contents(chk):
    dirs = skill_dirs()
    bad = []
    for directory in dirs:
        entries = sorted(
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*")
            if path.is_file()
        )
        if entries != ["SKILL.md"]:
            bad.append("%s: [%s]" % (directory.name, ", ".join(entries)))
    ok = bool(dirs) and not bad
    detail = (
        summarize(bad) if bad else ("" if dirs else "skills/ has no skill directories")
    )
    chk.check("each skill directory contains only SKILL.md", ok, detail)


def check_skill_frontmatter(chk):
    dirs = skill_dirs()
    bad = []
    for directory in dirs:
        path = directory / "SKILL.md"
        if not path.is_file():
            bad.append("%s: SKILL.md missing" % directory.name)
            continue
        text, err = read_text(path)
        if text is None:
            bad.append("%s: %s" % (directory.name, err))
            continue
        data = parse_frontmatter(text)
        if data is None:
            bad.append("%s: invalid frontmatter" % directory.name)
            continue
        name = unquote(data.get("name", ""))
        description = unquote(data.get("description", ""))
        if name != directory.name:
            bad.append("%s: name is %r" % (directory.name, name))
        elif not SKILL_NAME_RE.match(name):
            bad.append("%s: name does not match kebab-case rule" % directory.name)
        if not 20 <= len(description) <= 400:
            bad.append("%s: description length %d" % (directory.name, len(description)))
    ok = bool(dirs) and not bad
    chk.check("skill frontmatter is valid", ok, summarize(bad) if bad else "")


def check_commands(chk):
    base = ROOT / "commands"
    paths = sorted(base.glob("*.md")) if base.is_dir() else []
    bad = []
    for path in paths:
        text, err = read_text(path)
        data = parse_frontmatter(text) if text is not None else None
        if data is None:
            bad.append("%s: invalid or missing frontmatter" % path.name)
            continue
        if not unquote(data.get("description", "")):
            bad.append("%s: description missing" % path.name)
    ok = bool(paths) and not bad
    detail = summarize(bad) if bad else ("" if paths else "no commands/*.md found")
    chk.check("commands have description frontmatter", ok, detail)


def check_agents(chk):
    base = ROOT / "agents"
    paths = sorted(base.glob("*.md")) if base.is_dir() else []
    bad = []
    for path in paths:
        text, err = read_text(path)
        data = parse_frontmatter(text) if text is not None else None
        if data is None:
            bad.append("%s: invalid or missing frontmatter" % path.name)
            continue
        missing = [
            key
            for key in ("description", "mode", "steps")
            if not unquote(data.get(key, ""))
        ]
        if missing:
            bad.append("%s: missing %s" % (path.name, ", ".join(missing)))
    ok = bool(paths) and not bad
    detail = summarize(bad) if bad else ("" if paths else "no agents/*.md found")
    chk.check("agents have description, mode, steps", ok, detail)


def check_text_encoding(chk):
    bad = []
    for path in iter_files():
        if not is_text_file(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            raw = path.read_bytes()
        except OSError as exc:
            bad.append("%s: %s" % (rel, exc))
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            bad.append("%s: not UTF-8 (%s)" % (rel, exc))
            continue
        if rel == "docs/MIGRATION.md":
            continue
        try:
            text.encode("ascii")
        except UnicodeEncodeError:
            bad.append("%s: non-ASCII" % rel)
    chk.check("text files are UTF-8 and ASCII", not bad, summarize(bad))


def check_portuguese(chk):
    hits = []
    for rel, text in iter_texts():
        if rel in CONTENT_SCAN_SKIP:
            continue
        match = PORTUGUESE_RE.search(text)
        if match:
            hits.append("%s: %s" % (rel, match.group(0)))
    chk.check(
        "no Portuguese words outside docs/MIGRATION.md", not hits, summarize(hits)
    )


def check_secrets(chk):
    hits = []
    for rel, text in iter_texts():
        if rel in CONTENT_SCAN_SKIP:
            continue
        found = False
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append("%s: %s" % (rel, label))
                found = True
                break
        if found:
            continue
        for match in SECRET_ASSIGN_RE.finditer(text):
            value = match.group(1).strip()
            lowered = value.lower()
            if lowered in PLACEHOLDER_VALUES or value.startswith(PLACEHOLDER_PREFIXES):
                continue
            hits.append("%s: literal credential value" % rel)
            break
    chk.check("no committed secrets", not hits, summarize(hits))


def check_paths(chk):
    hits = []
    for rel, text in iter_texts():
        if rel in CONTENT_SCAN_SKIP:
            continue
        for label, pattern in PATH_PATTERNS:
            if pattern.search(text):
                hits.append("%s: %s" % (rel, label))
                break
    chk.check("no machine-specific paths or tunnel hosts", not hits, summarize(hits))


def check_readme(chk):
    path = ROOT / "README.md"
    if not path.is_file():
        chk.check("README has the required headings", False, "README.md missing")
        return
    text, err = read_text(path)
    if text is None:
        chk.check("README has the required headings", False, err)
        return
    missing = []
    for heading in README_HEADINGS:
        pattern = re.compile(
            r"^##[ \t]+" + re.escape(heading) + r"[ \t]*$", re.MULTILINE
        )
        if not pattern.search(text):
            missing.append(heading)
    chk.check(
        "README has the required headings",
        not missing,
        "missing: " + summarize(missing),
    )


def check_skills_doc(chk):
    path = ROOT / "docs" / "SKILLS.md"
    if not path.is_file():
        chk.check(
            "docs/SKILLS.md references every skill ID", False, "docs/SKILLS.md missing"
        )
        return
    text, err = read_text(path)
    if text is None:
        chk.check("docs/SKILLS.md references every skill ID", False, err)
        return
    missing = [skill for skill in SKILL_IDS if skill not in text]
    chk.check(
        "docs/SKILLS.md references every skill ID",
        not missing,
        "missing: " + summarize(missing),
    )


def check_installers(chk):
    bad = []
    for rel in ("scripts/install.ps1", "scripts/install.sh"):
        path = ROOT / rel
        text, _ = read_text(path) if path.is_file() else (None, None)
        if text is None or "OPENCODE_CONFIG_DIR" not in text:
            bad.append(rel)
    chk.check(
        "installers honor OPENCODE_CONFIG_DIR", not bad, "missing: " + summarize(bad)
    )


def check_node_syntax(chk):
    name = "node --check plugins/meta-goal/index.js"
    node = shutil.which("node")
    target = ROOT / "plugins" / "meta-goal" / "index.js"
    if node is None:
        chk.check(name, True, "skipped: node not installed")
        return
    if not target.is_file():
        chk.check(name, True, "skipped: file missing")
        return
    try:
        proc = subprocess.run(
            [node, "--check", str(target)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        chk.check(name, False, str(exc))
        return
    output = (proc.stderr or proc.stdout or "").strip().replace("\n", " ")
    chk.check(name, proc.returncode == 0, output[:200])


def main():
    chk = Checker()
    check_required_files(chk)
    check_no_empty_files(chk)
    check_config_json(chk)
    check_example_mcp_disabled(chk)
    check_schema(chk)
    check_skill_set(chk)
    check_skill_contents(chk)
    check_skill_frontmatter(chk)
    check_commands(chk)
    check_agents(chk)
    check_text_encoding(chk)
    check_portuguese(chk)
    check_secrets(chk)
    check_paths(chk)
    check_readme(chk)
    check_skills_doc(chk)
    check_installers(chk)
    check_node_syntax(chk)

    total = chk.passed + chk.failed
    print("")
    if chk.failed:
        print(
            "Summary: %d checks, %d passed, %d failed" % (total, chk.passed, chk.failed)
        )
        print("Failed: " + ", ".join(chk.failures))
        return 1
    print("Summary: %d checks, %d passed, 0 failed" % (total, chk.passed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
