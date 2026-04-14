from datetime import datetime, timezone

# Single-version docs configuration.
doc_version = "v2.0.1"
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
]

myst_enable_extensions = [
	"substitution",
]

myst_substitutions = {
	"doc_version": doc_version,
}

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
	"nav_links": [
		{
			"title": f"Version: {doc_version} | Latest",
			"url": "../docs/index.html",
			"resource": True,
			"children": [],
		},
	],
}

html_css_files = ["custom.css"]
html_js_files = ["version-badge.js", "footer-dkube-link.js"]
html_baseurl = "https://dkubex2.dkube.io/"
html_favicon = "_static/DKube_Icon_512x512.svg"