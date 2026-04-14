from datetime import datetime, timezone
import os
import subprocess

# Multi-version docs configuration (tags-only).
def detect_doc_version() -> str:
	# In sphinx-multiversion builds, each ref is checked out before conf.py loads.
	# Prefer exact tag name when available; otherwise use short commit id.
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

# Historical tags can contain content that triggers non-critical warnings.
# Suppress these categories to keep multiversion builds stable and readable.
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
html_js_files = ["footer-dkube-link.js"]
html_baseurl = "https://dkubex2.dkube.io/"
html_favicon = "_static/DKube_Icon_512x512.svg"


import re

def format_version(app, pagename, templatename, context, doctree):
	"""Convert version namedtuple to its name attribute for template rendering."""
	if "current_version" in context and context["current_version"]:
		version_obj = context["current_version"]
		# If it's a namedtuple/object with 'name' attribute, extract it
		if hasattr(version_obj, "name"):
			context["current_version"] = version_obj.name
		else:
			context["current_version"] = str(version_obj)
	
	# Also format versions list if it exists
	if "versions" in context and context["versions"]:
		try:
			formatted_versions = []
			for v in context["versions"]:
				if hasattr(v, "name"):
					formatted_versions.append({"name": v.name, "url": v.url, "is_released": v.is_released})
				else:
					formatted_versions.append(v)
			context["versions"] = formatted_versions
		except:
			pass


def fix_version_html(app, exception):
	"""Post-process HTML files to fix version namedtuple representations."""
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


def setup(app):
	app.connect("html-page-context", format_version)
	app.connect("build-finished", fix_version_html)