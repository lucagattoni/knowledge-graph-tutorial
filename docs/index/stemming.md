---
type: index
kind: concept
aliases: [suffix stripping]
updated: 20261102 21:26 UTC
---

# Stemming

Stemming reduces the different forms of a word to one stem, so that a search for one form finds the others. This entry gives the definition, the two classic algorithms, the Snowball project and a disagreement about whether stemming helps.

## Definition

Lovins (1968) defines a stemming algorithm as "a procedure to reduce all words with the same stem to a common form", usually by stripping derivational and inflectional suffixes [1]. Porter (1980) gives the reason in [information retrieval](./information-retrieval.md): terms with a common stem usually have similar meanings, so conflating them tends to improve performance and shrinks the term list [2]. Manning, Raghavan and Schütze call stemming "a crude heuristic process that chops off the ends of words", against lemmatization, which uses a vocabulary and morphological analysis [5].

## How it changed

- **1968.** Lovins publishes a context-sensitive, longest-match stemming algorithm for English, built for a library information transfer system [1]. Era: [The advent](../history/advent.md).
- **198007.** Porter publishes "An algorithm for suffix stripping" in *Program* 14(3), under 400 lines of BCPL; on a 10,000-word vocabulary it leaves 6,370 stems, a cut of about one third (first-party) [2]. Sanderson and Croft say he developed it in the late 1970s and that it still influences stemmer design [3]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **By 2012.** Sanderson and Croft note that web query logs enabled "more accurate stemming" [3].
- **2014.** Martin Porter retires from Snowball, his language for stemmers, and the community maintains it [4]. His page calls the original Porter stemmer "frozen" and recommends the Snowball English stemmer [6].
- **2025 and 2026.** Snowball 3.0.0 appears in 202505 and 3.2.0 in 202610, with new stemmers and a Zig backend [4].

## Where sources disagree

- **Does it help?** Porter says performance "will be improved" frequently [2]; Sanderson and Croft say stemming "was found to produce a level of improvement" [3]. Manning et al. say it "tends not to improve English information retrieval performance in aggregate", raising recall and harming precision [5]; the same page says Porter's algorithm has "repeatedly been shown to be empirically very effective" [5]. Which fits current systems is **unstated**.
- **Aim.** Porter says suffixes are removed "not as a linguistic exercise" [2]; Snowball says it conflates words of the same meaning and treats over-stemming as worse than under-stemming [4].

## Related

[information retrieval](./information-retrieval.md), [Boolean retrieval](./boolean-retrieval.md), [ranked retrieval](./ranked-retrieval.md), [tf-idf](./tf-idf.md), [BM25](./bm25.md), [hybrid search](./hybrid-search.md), [TREC](./trec.md), [token](./token.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [Knowledge systems: boom and bust](../history/knowledge-systems.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://aclanthology.org/www.mt-archive.info/MT-1968-Lovins.pdf : Lovins, "Development of a Stemming Algorithm", Mechanical Translation and Computational Linguistics 11(1-2), March and June 1968: abstract, introduction (read 20261102 21:04 UTC)
2. https://tartarus.org/martin/PorterStemmer/def.txt : Porter, "An algorithm for suffix stripping", Program 14(3), 130-137, July 1980 (author's text): introduction, vocabulary result (first-party; read 20261102 21:03 UTC)
3. https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1066 : Sanderson and Croft, "The History of Information Retrieval Research", Proc. IEEE 100, 2012: stemming, Porter, query logs (read 20261102 21:04 UTC)
4. https://snowballstem.org/ : Snowball home page: what stemming is, Porter's retirement in 2014, major events May 2025 to October 2026 (first-party; read 20261102 21:03 UTC)
5. https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html : Manning, Raghavan, Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008, section "Stemming and lemmatization" (read 20261102 21:05 UTC through the Internet Archive copy https://web.archive.org/web/2024/https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html, because the original host was unreachable; year and authors from the book's companion page, same archive, read 20261102 21:05 UTC)
6. https://tartarus.org/martin/PorterStemmer/ : Porter stemmer page: status "frozen", Snowball English recommended (first-party; read 20261102 21:03 UTC)
