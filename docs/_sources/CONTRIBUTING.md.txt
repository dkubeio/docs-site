# Contributing Application Documentation

This repository accepts documentation contributions only under the `applications/` directory.

## Contribution Scope

- Add or update docs only inside `applications/`.
- Each application must have its own subfolder.

## Required Folder Structure

For every application, create this structure first:

```text
applications/
  <your-application>/
    index.md
    images/
```

Example:

```text
applications/
  mortgage-lite/
    index.md
    images/
```

## Image Guidelines

- Store all images for your application inside your application's `images/` folder.
- In every markdown file, the image link path must correctly point to your application's `images/` folder.
- The path is always relative to the markdown file where you add the image link.

Examples:

```markdown
# From applications/my-app/index.md
![Architecture](./images/architecture.png)

# From applications/my-app/guides/setup.md
![Architecture](../images/architecture.png)
```

If the path to `images/` is wrong, the image will not render in the docs.

## Application Homepage Requirements

Your `index.md` is the homepage for your application documentation.

It must:

- Use an appropriate top-level heading for your application.
- You must link to your other documentation pages through a `toctree` on the index.md page.

Sample homepage toctree template:

````markdown
```{toctree}
:maxdepth: 2
:caption: Contents

getting-started
architecture
deployment
api-reference
```
````

Notes:

- List pages without `.md` in `toctree` entries.
- Paths are relative to your `index.md`.

## Update the Applications Toctree

After creating your application folder, you must add your app index to the toctree in `applications/index.md`.

Add one line in the toctree block:

```text
<your-application>/index
```

Example:

```text
securellm/index
```

## Checklist Before Commit

- Application folder exists under `applications/`.
- `index.md` exists in your application folder.
- `images/` folder exists in your application folder.
- All images are stored in your local `images/` folder and linked with correct relative paths.
- Your application `index.md` includes a `toctree` that references your pages.
- `applications/index.md` includes `<your-application>/index`.