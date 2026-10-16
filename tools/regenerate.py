"""Regenerate artifacts for a build123d model declared by regenerate.toml."""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"
STAGES = ("build", "checks", "views")
MANIFEST = "regenerate.toml"


@dataclass(frozen=True)
class Project:
    name: str
    path: Path
    stages: dict[str, tuple[str, ...]]


def discover() -> dict[str, Project]:
    """Find build123d projects without importing their CAD models."""
    projects = {}
    for manifest in MODELS.rglob(MANIFEST):
        folder = manifest.parent
        data = tomllib.loads(manifest.read_text())
        if data.get("project", {}).get("type") != "build123d":
            raise ValueError(f"{manifest}: project.type must be 'build123d'")
        declared = data.get("stages", {})
        if set(declared) - set(STAGES):
            raise ValueError(f"{manifest}: unknown stages {set(declared) - set(STAGES)}")
        stages = {}
        for stage in STAGES:
            scripts = declared.get(stage, [])
            if not isinstance(scripts, list) or not all(isinstance(s, str) for s in scripts):
                raise ValueError(f"{manifest}: stages.{stage} must be a list of script paths")
            for script in scripts:
                source = (folder / script).resolve()
                if not source.is_relative_to(folder.resolve()) or not source.is_file():
                    raise ValueError(f"{manifest}: missing or outside-project script {script!r}")
            stages[stage] = tuple(scripts)
        name = folder.relative_to(MODELS).as_posix()
        projects[name] = Project(name, folder, stages)
    return projects


def select(name: str, projects: dict[str, Project]) -> Project:
    clean = name.removeprefix("models/").rstrip("/")
    if clean in projects:
        return projects[clean]
    matches = [p for p in projects.values() if p.path.name == clean]
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise ValueError(f"Ambiguous project {name!r}: {', '.join(p.name for p in matches)}")
    raise ValueError(f"Unknown build123d project {name!r}; run 'uv run regen --list'")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", help="build123d project name shown by --list")
    parser.add_argument("--list", action="store_true", help="list build123d projects")
    parser.add_argument("--only", choices=("all", *STAGES), default="all",
                        help="run one artifact stage (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="show commands only")
    args = parser.parse_args(argv)
    try:
        projects = discover()
        if args.list:
            for name in sorted(projects):
                print(name)
            return 0
        if not args.project:
            parser.error("provide a project name or --list")
        project = select(args.project, projects)
        stages = STAGES if args.only == "all" else (args.only,)
        scripts = [(stage, script) for stage in stages for script in project.stages[stage]]
        if not scripts:
            print(f"{project.name}: no {args.only} scripts")
            return 0
        for stage, script in scripts:
            command = (sys.executable, script)
            print(f"[{project.name} / {stage}] "
                  f"(cd {project.path} && {shlex.join(command)})", flush=True)
            if not args.dry_run:
                subprocess.run(command, cwd=project.path,
                               env={**os.environ, "MPLBACKEND": "Agg"}, check=True)
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"regen: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
