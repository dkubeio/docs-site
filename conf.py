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
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

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


# Register context and post-build normalization hooks.
def setup(app):
	app.connect("html-page-context", format_version)
	app.connect("build-finished", fix_version_html)