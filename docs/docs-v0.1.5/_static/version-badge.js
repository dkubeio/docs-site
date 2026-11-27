document.addEventListener("DOMContentLoaded", function () {
  function ensureTitleNode(container) {
    if (!container) {
      return null;
    }

    var existingTitle = container.querySelector(":scope > span");
    if (existingTitle) {
      return existingTitle;
    }

    // Shibuya can render nav links as plain text without child spans.
    if (container.childElementCount === 0) {
      var text = (container.textContent || "").trim();
      if (!text) {
        return null;
      }
      container.textContent = "";
      var span = document.createElement("span");
      span.textContent = text;
      container.appendChild(span);
      return span;
    }

    for (var i = 0; i < container.childNodes.length; i += 1) {
      var node = container.childNodes[i];
      if (node.nodeType === Node.TEXT_NODE && node.textContent && node.textContent.trim()) {
        var wrapped = document.createElement("span");
        wrapped.textContent = node.textContent.trim();
        container.replaceChild(wrapped, node);
        return wrapped;
      }
    }

    return null;
  }

  function applyLatestBadgeText() {
    var latestTokenPattern = /\|\s*Latest\b/;
    var containers = document.querySelectorAll(".sy-head .sy-head-links a, .sy-head .sy-head-links button");

    containers.forEach(function (container) {
      if (!container || container.querySelector(".version-latest-badge")) {
        return;
      }

      var titleNode = ensureTitleNode(container);
      if (!titleNode) {
        return;
      }

      var text = (titleNode.textContent || "").trim();
      if (!latestTokenPattern.test(text)) {
        return;
      }

      var label = text.replace(/\s*\|\s*Latest\b\s*/, " ").trim();
      if (!label) {
        return;
      }

      titleNode.textContent = label;
      titleNode.classList.add("version-label");

      var badgeSpan = document.createElement("span");
      badgeSpan.className = "version-latest-badge";
      badgeSpan.textContent = "Latest";

      if (container.querySelector("small")) {
        // Keep title and summary stacked; badge sits to the right, vertically centered.
        container.classList.add("has-latest-badge");
        container.appendChild(badgeSpan);
      } else {
        titleNode.appendChild(document.createTextNode(" "));
        titleNode.appendChild(badgeSpan);
      }
    });
  }

  applyLatestBadgeText();

  // Re-apply when nav DOM mutates (e.g., dropdown nodes are toggled/updated).
  var head = document.querySelector(".sy-head");
  if (head) {
    var observer = new MutationObserver(function () {
      applyLatestBadgeText();
    });
    observer.observe(head, { childList: true, subtree: true });
  }
});
