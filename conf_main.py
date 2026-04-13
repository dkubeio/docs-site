from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def version_key(version: str):
    return tuple(int(part) for part in version.lstrip("vV").split("."))


def version_url(version: str, latest: str):
    if version == latest:
        return "../docs/index.html"
    return f"../docs-{version}/index.html"


def discover_versions(repo_root: Path):
    discovered_versions = []
    for directory in repo_root.glob("raw-v*"):
        if directory.is_dir():
            discovered_versions.append(directory.name.replace("raw-", "", 1))

    return sorted(discovered_versions, key=version_key)


def build_conf(doc_version: str, conf_file: str) -> dict[str, Any]:
    repo_root = Path(conf_file).resolve().parent.parent
    build_date = datetime.now(timezone.utc).strftime("%d.%m.%Y")

    versions = discover_versions(repo_root)
    if not versions:
        versions = [doc_version]

    documentation_versions = [{"version": version} for version in versions]
    latest_version = max((item["version"] for item in documentation_versions), key=version_key)

    default_current_url = f"../docs-{doc_version}/index.html"
    current_version_url = next(
        (
            version_url(item["version"], latest_version)
            for item in documentation_versions
            if item["version"] == doc_version
        ),
        default_current_url,
    )

    version_links = []
    for item in documentation_versions:
        version = item["version"]
        if version == doc_version:
            continue

        version_links.append(
            {
                "title": f"{version} | Latest" if version == latest_version else version,
                "url": version_url(version, latest_version),
                "summary": "Latest stable release" if version == latest_version else "Previous release",
                "resource": True,
            }
        )

    return {
        "project": "DKubeX 2.0 Documentation",
        "author": "DKube",
        "doc_version": doc_version,
        "copyright": (
            f"&copy; 2026, dkube.io. All rights reserved. "
            f"Last updated on: {build_date}. Documentation version: {doc_version}"
        ),
        "extensions": [
            "myst_parser",
            "sphinx.ext.githubpages",
            "sphinx_copybutton",
        ],
        "myst_enable_extensions": [
            "substitution",
        ],
        "myst_substitutions": {
            "doc_version": doc_version,
        },
        "templates_path": ["_templates"],
        "exclude_patterns": ["_build", "Thumbs.db", ".DS_Store"],
        "html_theme": "shibuya",
        "html_title": "DKubeX 2.0 Documentation",
        "html_static_path": ["_static"],
        "html_logo": "_static/DKube_Icon_512x512.svg",
        "html_theme_options": {
            "logo_target": "index.html",
            "github_url": "https://github.com/deepro713/product-docs-test/",
            "youtube_url": "https://www.youtube.com/@DKube_OC",
            "nav_links": [
                {
                    "title": (
                        f"Version: {doc_version} | Latest"
                        if doc_version == latest_version
                        else f"Version: {doc_version}"
                    ),
                    "url": current_version_url,
                    "resource": True,
                    "children": version_links,
                },
            ],
        },
        "html_css_files": ["custom.css"],
        "html_js_files": ["version-badge.js", "footer-dkube-link.js"],
        "html_baseurl": "https://docs-test.dkube.io/",
        "html_favicon": "_static/DKube_Icon_512x512.svg",
    }
