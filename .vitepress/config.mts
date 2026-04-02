import { readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";
import { defineConfig } from "vitepress";

// Auto-generate sidebar groups from docs/components/* directory structure
function generateSidebar() {
  const componentsDir = join("docs", "components");
  const items: any[] = [];

  // Index page
  items.push({ text: "Home", link: "/" });

  if (!readdirSync(".").includes(componentsDir)) {
    return items;
  }

  const componentDirs = readdirSync(componentsDir).filter((dir) => {
    const fullPath = join(componentsDir, dir);
    return statSync(fullPath).isDirectory();
  });

  if (componentDirs.length > 0) {
    const groups: any[] = [];

    for (const dir of componentDirs.sort()) {
      const dirPath = join(componentsDir, dir);
      const files = readdirSync(dirPath).filter(
        (f) =>
          statSync(join(dirPath, f)).isFile() && extname(f) === ".md"
      );

      if (files.length === 0) continue;

      // Human-readable name from directory name
      const title = dir
        .split(/[-_]/)
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(" ");

      const children = files.sort().map((f) => ({
        text: f
          .replace(/\.md$/, "")
          .split(/[-_]/)
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" "),
        link: `/components/${dir}/${f.replace(/\.md$/, "")}`,
      }));

      // Check for subdirectories
      const subDirs = readdirSync(dirPath).filter((f) => {
        const fullPath = join(dirPath, f);
        return statSync(fullPath).isDirectory();
      });

      for (const subDir of subDirs.sort()) {
        const subPath = join(dirPath, subDir);
        const subFiles = readdirSync(subPath).filter(
          (f) =>
            statSync(join(subPath, f)).isFile() && extname(f) === ".md"
        );

        if (subFiles.length > 0) {
          const subTitle = subDir
            .split(/[-_]/)
            .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
            .join(" ");

          children.push({
            text: subTitle,
            collapsed: true,
            items: subFiles.sort().map((f) => ({
              text: f
                .replace(/\.md$/, "")
                .split(/[-_]/)
                .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
                .join(" "),
              link: `/components/${dir}/${subDir}/${f.replace(/\.md$/, "")}`,
            })),
          });
        }
      }

      groups.push({ text: title, collapsed: true, items: children });
    }

    items.push({ text: "Components", items: groups });
  }

  return items;
}

export default defineConfig({
  title: "Docs",
  description: "Component Documentation Site",
  base: "/",
  outDir: "_site",

  head: [
    ["link", { rel: "icon", href: "/favicon.ico" }],
  ],

  // Auto-generated sidebar
  themeConfig: {
    logo: "/logo.svg",

    nav: [
      { text: "Home", link: "/" },
      { text: "Components", link: "/components/" },
    ],

    sidebar: generateSidebar(),

    socialLinks: [
      { icon: "github", link: "https://github.com/your-org/docs-site" },
    ],

    search: {
      provider: "local",
    },

    footer: {
      message: "Built with VitePress",
    },
  },
});
