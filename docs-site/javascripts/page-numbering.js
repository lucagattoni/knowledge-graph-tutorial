// Number a page from its entry in the left navigation, where mkdocs_hooks.py numbers the chapters
// and the sections inside them: the title becomes "1.2 - The LLM era: ...", its sections "1.2.1 - ..."
// and "1.2.2 - ...", their subsections "1.2.2.1 - ...". The same numbers go into the right-hand
// contents list. A page whose nav label has no number (one entry per project) and Home are left as
// they are.
//
// Done in JS (not in the Markdown) so the source files, their heading anchors and the GitHub
// rendering stay clean: cross-document links across the repository target those anchors, and the
// ids are never touched here.
//
// Many pages number their own headings ("1. The arc in one screen", "3.1 From eager ..."). On the
// site those numbers are replaced by the page's own scheme, so a heading never carries two. The
// pattern needs a dot after the digits ("1.", "3.1"), so a heading such as "2026 outlook" is safe.
//
// Uses Material's `document$` so it re-runs on instant navigation; the data flags keep it idempotent.
document$.subscribe(function () {
  var content = document.querySelector(".md-content");
  var title = content && content.querySelector("h1");
  if (!title || title.dataset.numbered) return;

  // The nav link text starts with the number, e.g. "1.2 LLM era". The trailing dot is optional
  // because a top-level chapter is labelled "3. Decisions", not "3.1 Decisions".
  var active = document.querySelector(".md-sidebar--primary .md-nav__link--active");
  var match = active && active.textContent.trim().match(/^(\d+(?:\.\d+)*)\.?\s/);
  if (!match) return;
  var pageNum = match[1];

  var OWN_NUMBER = /^(\s*)(\d+\.\d+(?:\.\d+)*|\d+\.)\s+/;

  // The first non-blank text node a label starts with, looking through the <span> Material wraps
  // around contents-list entries (and the blank text around it); null when the label starts with
  // other markup, such as inline code.
  function leadingText(el) {
    for (var n = el.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3) {
        if (n.data.trim()) return n;
      } else if (n.nodeType === 1 && n.tagName === "SPAN") {
        return leadingText(n);
      } else {
        return null;
      }
    }
    return null;
  }

  function relabel(el, num) {
    if (!el || el.dataset.numbered) return;
    el.dataset.numbered = "1";
    var text = leadingText(el);
    if (text) text.data = text.data.replace(OWN_NUMBER, "$1");
    el.insertBefore(document.createTextNode(num + " - "), el.firstChild);
  }

  function number(heading, num) {
    relabel(heading, num);
    // The same heading in the contents lists. With instant navigation their hrefs are absolute
    // (".../page/#slug"), so match on the "#slug" suffix.
    if (!heading.id) return;
    var id = window.CSS && CSS.escape ? CSS.escape(heading.id) : heading.id;
    document.querySelectorAll('a.md-nav__link[href$="#' + id + '"]').forEach(function (link) {
      relabel(link, num);
    });
  }

  relabel(title, pageNum);

  // Sections and subsections: "1.2.1", "1.2.1.1". A subsection before the first section has no
  // number to hang from and stays as written.
  var h2 = 0, h3 = 0;
  content.querySelectorAll("h2, h3").forEach(function (h) {
    if (h.dataset.numbered) return;
    if (h.tagName === "H2") {
      h2 += 1; h3 = 0;
      number(h, pageNum + "." + h2);
    } else if (h2 > 0) {
      h3 += 1;
      number(h, pageNum + "." + h2 + "." + h3);
    }
  });
});
