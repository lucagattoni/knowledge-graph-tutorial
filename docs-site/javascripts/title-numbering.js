// Put the page's number in front of its title ("1.2 - The LLM era: ..."), taking it from the page's
// entry in the left navigation, where mkdocs_hooks.py numbers the chapters and the sections inside
// them. A page whose nav label has no number (one entry per project) is left as it is, and so is Home.
//
// Done in JS (not in the Markdown) so the source files, their heading anchors and the GitHub
// rendering stay clean: cross-document links across the repository target those anchors. Only the
// title is numbered: many pages number their own headings, and a second number would repeat theirs.
// Uses Material's `document$` so it re-runs on instant navigation; the data flag keeps it idempotent.
document$.subscribe(function () {
  var title = document.querySelector(".md-content h1");
  if (!title || title.dataset.numbered) return;

  // The nav link text starts with the number, e.g. "1.2 LLM era". The trailing dot is optional
  // because a top-level chapter is labelled "3. Decisions", not "3.1 Decisions".
  var active = document.querySelector(".md-sidebar--primary .md-nav__link--active");
  var match = active && active.textContent.trim().match(/^(\d+(?:\.\d+)*)\.?\s/);
  if (!match) return;

  title.dataset.numbered = "1";
  title.insertBefore(document.createTextNode(match[1] + " - "), title.firstChild);
});
