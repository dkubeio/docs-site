document.addEventListener("DOMContentLoaded", function () {
  var footer = document.querySelector(".sy-foot-copyright");
  if (!footer) {
    return;
  }

  var nodes = footer.querySelectorAll("p, span, div");
  var dkubeIoLink = '<a href="https://www.dkube.io" target="_blank" rel="noopener noreferrer">dkube.io</a>';
  var dkubeLabelLink = '<a href="https://www.dkube.io" target="_blank" rel="noopener noreferrer">DKube</a>';

  nodes.forEach(function (node) {
    if (!node.innerHTML) {
      return;
    }

    var updatedHtml = node.innerHTML;
    updatedHtml = updatedHtml.replace(/\bdkube\.io\b/gi, dkubeIoLink);
    updatedHtml = updatedHtml.replace(/\bDKube\b/g, dkubeLabelLink);

    if (updatedHtml !== node.innerHTML) {
      node.innerHTML = updatedHtml;
    }
  });
});
