from datetime import datetime, timezone
import os
import subprocess

# Resolve current docs version from tag, then commit, then fallback.
def detect_doc_version() -> str:
	# sphinx-multiversion checks out each ref before loading this file.
	try:
		return subprocess.check_output(
			["git", "describe", "--tags", "--exact-match"],
			stderr=subprocess.DEVNULL,
			text=True,
		).strip()
	except Exception:
		try:
			return (
				subprocess.check_output(
					["git", "rev-parse", "--short", "HEAD"],
					stderr=subprocess.DEVNULL,
					text=True,
				)
				.strip()
			)
		except Exception:
			return os.environ.get("DOC_VERSION", "local")


doc_version = detect_doc_version()
version = doc_version
release = doc_version
build_date = datetime.now(timezone.utc).strftime("%d.%m.%Y")

project = "DKubeX Documentation"
author = "DKube"
copyright = (
	f"&copy; 2026, dkube.io. All rights reserved. "
	f"Last updated on: {build_date}. Documentation version: {doc_version}"
)

extensions = [
	"myst_parser",
	"sphinx.ext.githubpages",
	"sphinx_copybutton",
	"sphinx_multiversion",
	"sphinxcontrib.video",
	"sphinx_design",
]

smv_tag_whitelist = r"^.+$"
smv_branch_whitelist = r"^$"
smv_remote_whitelist = r"^origin$"
smv_released_pattern = r"^refs/tags/.*$"
smv_outputdir_format = "docs-{ref.name}"
smv_prefer_remote_refs = True
smv_disable_warnings = True

myst_enable_extensions = [
	"substitution",
	"colon_fence",
]

myst_substitutions = {
	"doc_version": doc_version,
}

# Suppress warning categories common in historical docs tags.
suppress_warnings = [
	"image.not_readable",
	"toc.not_included",
	"myst.xref_missing",
	"misc.highlighting_failure",
]

templates_path = ["_templates"]
# specifications.md is intentionally kept in the repo but excluded from the
# build/nav (retained for later use; folded content now lives on the homepage).
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md", "specifications.md"]

html_theme = "shibuya"
html_title = "DKubeX Documentation"
html_static_path = ["_static"]
html_logo = "_static/DKube_Icon_512x512.svg"
html_theme_options = {
	"logo_target": "index.html",
	"github_url": "https://github.com/dkubeio/docs-site/",
	"youtube_url": "https://www.youtube.com/@DKube_OC",
}

html_css_files = ["custom.css"]
html_js_files = ["footer-dkube-link.js", "version-badge.js"]
html_baseurl = "https://dkubex2.dkube.io/"
html_favicon = "_static/DKube_Icon_512x512.svg"


import re


def _version_parts(name: str):
	"""Extract comparable numeric parts from tags like v2.0.0.2 or 2.0.0."""
	match = re.match(r"^v?(\d+(?:\.\d+)*)", str(name or ""))
	if not match:
		return None
	try:
		return tuple(int(part) for part in match.group(1).split("."))
	except Exception:
		return None


def _version_sort_key(version_item):
	"""Sort released versions first, then semantic tags descending."""
	name = str(version_item.get("name", ""))
	is_released = 1 if version_item.get("is_released") else 0
	parts = _version_parts(name)
	is_semver = 1 if parts is not None else 0
	parts_key = parts if parts is not None else tuple()
	return (is_released, is_semver, parts_key, name)

# Normalize version objects exposed by sphinx-multiversion for templates.
def format_version(app, pagename, templatename, context, doctree):
	"""Normalize version objects to simple template-safe values."""
	if "current_version" in context and context["current_version"]:
		version_obj = context["current_version"]
		if hasattr(version_obj, "name"):
			context["current_version"] = version_obj.name
		else:
			context["current_version"] = str(version_obj)

	current_name = str(context.get("current_version", ""))

	# Normalize versions list for templates that iterate over it.
	if "versions" in context and context["versions"]:
		try:
			formatted_versions = []
			for v in context["versions"]:
				if hasattr(v, "name"):
					formatted_versions.append(
						{
							"name": v.name,
							"url": v.url,
							"is_released": v.is_released,
						}
					)
				else:
					formatted_versions.append(
						{
							"name": str(v),
							"url": "#",
							"is_released": False,
						}
					)

			formatted_versions.sort(key=_version_sort_key, reverse=True)
			latest_name = formatted_versions[0]["name"] if formatted_versions else ""

			for item in formatted_versions:
				item["is_current"] = item["name"] == current_name
				item["is_latest"] = item["name"] == latest_name

			context["current_version_display"] = current_name or latest_name
			context["current_version_is_latest"] = (current_name == latest_name)
			context["versions"] = formatted_versions
		except:
			pass


# Post-process generated HTML for any leaked namedtuple repr strings.
def fix_version_html(app, exception):
	"""Replace version namedtuple repr with readable version names in HTML."""
	if exception is not None:
		return
	
	import glob
	import os
	
	# Pattern to match the namedtuple repr: Version(name='...', ...)
	pattern = r"Version\(name='([^']+)'[^)]*\)"
	
	outdir = app.outdir
	for html_file in glob.glob(os.path.join(outdir, "**/*.html"), recursive=True):
		try:
			with open(html_file, "r", encoding="utf-8") as f:
				content = f.read()
			
			# Replace the namedtuple repr with just the version name
			fixed_content = re.sub(pattern, r"\1", content)
			
			if fixed_content != content:
				with open(html_file, "w", encoding="utf-8") as f:
					f.write(fixed_content)
		except Exception as e:
			pass


# Build a clean version list for shibuya's nav dropdown. Connected at a high
# priority so it runs AFTER sphinx-multiversion (default priority), whose
# handler overwrites context["versions"] with its own ascending VersionInfo.
# We read that final value and expose a normalized, newest-first list plus the
# latest tag name, consumed by _templates/components/nav-versions.html.
def prepare_nav_versions(app, pagename, templatename, context, doctree):
	raw = context.get("versions")
	if not raw:
		return

	current = context.get("current_version")
	current_name = getattr(current, "name", None) or (str(current) if current else "")
	# Ensure the button label is the plain tag name, not a namedtuple repr.
	context["current_version"] = current_name

	items = []
	for v in raw:
		# smv Version is a namedtuple ([0]=name, [1]=url); be tolerant of dicts.
		name = getattr(v, "name", None) or (v[0] if not isinstance(v, dict) else v.get("name"))
		url = getattr(v, "url", None) or (v[1] if not isinstance(v, dict) else v.get("url"))
		if name:
			items.append({"name": name, "url": url})

	def _key(item):
		parts = _version_parts(item["name"])
		return (1 if parts is not None else 0, parts or tuple(), item["name"])

	items.sort(key=_key, reverse=True)
	latest_name = items[0]["name"] if items else ""
	for item in items:
		item["is_latest"] = item["name"] == latest_name
		item["is_current"] = item["name"] == current_name

	context["nav_versions"] = items
	context["nav_latest_name"] = latest_name


# Read the first level-1 heading from a markdown file. Used to derive a
# human-readable display title from each application's index.md.
def _read_h1(path):
	try:
		with open(path, "r", encoding="utf-8") as f:
			for line in f:
				stripped = line.strip()
				if stripped.startswith("# "):
					return stripped[2:].strip()
	except Exception:
		pass
	return None


def _format_slug(slug):
	return slug.replace("-", " ").replace("_", " ").title()


# Canonical display names for slugs whose folder name doesn't match the
# brand name. Overrides both the visible list label and the sidebar entry.
APPLICATION_DISPLAY_NAMES = {
	"modelstudio": "ModelStudio",
	"mlflow": "MLflow",
	"ragflow": "RAGFlow",
	"securellm": "SecureLLM",
}


# Preferred order for applications in the list and sidebar. Slugs listed here
# come first in this order; any others (e.g. apps only present in older
# versions) follow alphabetically.
APPLICATION_ORDER = ["workspace", "modelstudio", "securellm", "ragflow", "langflow"]


def _ordered_app_slugs(slugs):
	slugs = list(slugs)
	ordered = [s for s in APPLICATION_ORDER if s in slugs]
	rest = sorted(s for s in slugs if s not in APPLICATION_ORDER)
	return ordered + rest


# Append an auto-generated bulleted list of applications plus a hidden toctree
# to applications/index.md. The visible list keeps the page discoverable for
# end users; the hidden toctree drives the sidebar navigation and document
# structure. New components show up automatically as soon as their index.md
# lands under applications/<slug>/.
def auto_app_toctree(app, docname, source):
	if docname != "applications/index":
		return

	apps_dir = os.path.join(str(app.srcdir), "applications")
	if not os.path.isdir(apps_dir):
		return

	available = [
		entry
		for entry in os.listdir(apps_dir)
		if os.path.isdir(os.path.join(apps_dir, entry))
		and os.path.isfile(os.path.join(apps_dir, entry, "index.md"))
	]

	entries = []
	for entry in _ordered_app_slugs(available):
		index_path = os.path.join(apps_dir, entry, "index.md")
		title = (
			APPLICATION_DISPLAY_NAMES.get(entry)
			or _read_h1(index_path)
			or _format_slug(entry)
		)
		entries.append((entry, title))

	if not entries:
		return

	lines = ["", ""]
	for slug, title in entries:
		lines.append(f"- [{title}](./{slug}/index.md)")
	lines.append("")
	lines.append("```{toctree}")
	lines.append(":hidden:")
	lines.append("")
	for slug, title in entries:
		if APPLICATION_DISPLAY_NAMES.get(slug):
			lines.append(f"{title} <{slug}/index>")
		else:
			lines.append(f"{slug}/index")
	lines.append("```")
	lines.append("")

	source[0] = source[0].rstrip() + "\n" + "\n".join(lines)


# Register context and post-build normalization hooks.
def setup(app):
	app.connect("source-read", auto_app_toctree)
	app.connect("html-page-context", format_version)
	# High priority => runs after sphinx-multiversion's own context handler.
	app.connect("html-page-context", prepare_nav_versions, priority=900)
	app.connect("build-finished", fix_version_html)