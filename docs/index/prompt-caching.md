---
type: index
kind: concept
aliases: [context caching, prefix caching, KV cache reuse]
updated: 20261102 22:49 UTC
---

# Prompt caching

This entry says what prompt caching is, when providers introduced it, and how their rules differ. It also compares lifetimes and prices as the providers' pages stated them on 20261102.

## Definition

Prompt caching reuses the already-processed start of a prompt on later requests. OpenAI's documentation says it "reuses work when requests share the same prompt prefix" and that the cache holds the model's key-value (KV) tensors, not the tokens [4]. Anthropic describes "allowing resuming from specific prefixes in your prompts" [1]. A hit is billed below the normal input price [1][4]. Open-source servers say KV cache reuse (SGLang) or Automatic Prefix Caching (vLLM) [12][13].

## How it changed

- **20231107.** Gim et al. submit Prompt Cache, which stores attention states of recurring text segments for reuse; time to first token falls 8x (GPU) to 60x (CPU) (first-party) [11].
- **2024, launches (first-party).** Google: announced 20240514 as coming in June, launched 20240627 [6][7]. DeepSeek: 20240802, hits at $0.014 per million tokens [10]. Anthropic: beta 20240814, no beta header from 20241217 [2]. OpenAI: 20241001, "discounts and faster processing times" on recent input [5].
- **20250508.** Google adds implicit caching for Gemini 2.5, same 75% discount, and says it pioneered context caching in May 2024 [8].
- **20260219.** Anthropic adds automatic caching: one top-level `cache_control` field [2].
- **20260709.** OpenAI's GPT-5.6 adds explicit cache controls [5]. Google's guide, read 20261102, makes implicit caching the default and does not support explicit caching on Gemini 4 Argon and later [9].

## Where sources disagree

**Same name, different thing.** Gim et al. cache named text segments defined by a schema [11]. Providers match a prefix: DeepSeek counts "only requests with identical prefixes" [10]; OpenAI needs the entire rendered prefix to match [4].

**Prices and lifetimes.** Anthropic: 5 minutes or 1 hour; writes 1.25x or 2x the input price, reads 0.1x (0.05x or 0.025x on some models) [1]; one model's read price was cut to 0.05x on 20261007 [2]. OpenAI, GPT-5.6 and later: 30 minutes or 12 hours; writes 1.25x or 2.5x. Earlier models other than GPT-5.5: no write charge; entries typically stay 5 to 10 minutes idle and up to an hour, or up to 24 hours with extended retention [4]. Google's current rate is unstated in the pages read.

**Anthropic's own figures.** Its announcement page says latency falls "by up to 85%", its release notes 80%. The page header date, 20250814, conflicts with its own 20241217 update note, so dates here come from the release notes [2][3].

## Related

[large language model](./large-language-model.md) · [context window](./context-window.md) · [retrieval-augmented generation](./retrieval-augmented-generation.md) · [PageIndex](../projects/pageindex.md) · [matched-cost comparison (X3)](../experiments/x3-matched-cost-comparison.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Vectorless retrieval: from similarity search to a model reasoning over a document tree](../trends/reasoning-over-structure.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://platform.claude.com/docs/en/build-with-claude/prompt-caching : Anthropic documentation: definition, 5-minute and 1-hour lifetimes, pricing multipliers and footnotes (first-party; read 20261102 22:15 UTC)
2. https://platform.claude.com/docs/en/release-notes/overview : Anthropic API release notes: 14 Aug 2024, 17 Dec 2024, 19 Feb 2026, 7 Oct 2026 (first-party; read 20261102 22:15 UTC)
3. https://claude.com/resources/articles/prompt-caching : Anthropic announcement page, "Prompt caching with Claude", header date 14 August 2025, update note 17 December 2024, "latency by up to 85%" (first-party; read 20261102 22:14 UTC)
4. https://developers.openai.com/api/docs/guides/prompt-caching : OpenAI documentation: definition, KV tensors, prefix matching, GPT-5.6 and earlier-model rules and prices (first-party; read 20261102 22:15 UTC)
5. https://developers.openai.com/api/docs/changelog : OpenAI changelog: 1 Oct 2024 and 9 Jul 2026 entries (first-party; read 20261102 22:16 UTC)
6. https://developers.googleblog.com/en/new-features-for-the-gemini-api-and-google-ai-studio/ : Google, 27 June 2024, context caching launched for Gemini 1.5 Pro and Flash (first-party; read 20261102 22:17 UTC)
7. https://blog.google/innovation-and-ai/technology/developers-tools/gemini-gemma-developer-updates-may-2024/ : Google, 14 May 2024, caching "coming in June" (first-party; read 20261102 22:17 UTC)
8. https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/ : Google, 8 May 2025, implicit caching, 75% discount, "pioneered" claim (first-party; read 20261102 22:16 UTC)
9. https://ai.google.dev/gemini-api/docs/caching.md.txt : Gemini API caching guide as served now: implicit by default, explicit not supported on Gemini 4 (first-party; read 20261102 22:16 UTC)
10. https://api-docs.deepseek.com/news/news0802 : DeepSeek, "Context Caching is Available", 2 Aug 2024 (first-party; read 20261102 22:17 UTC)
11. https://arxiv.org/abs/2311.04934 : Gim et al. (6 authors), "Prompt Cache: Modular Attention Reuse for Low-Latency Inference", v1 20231107, abstract (first-party; read 20261102 22:17 UTC)
12. https://arxiv.org/abs/2312.07104 : Zheng et al. (12 authors), "SGLang", v1 20231212, abstract: RadixAttention "for KV cache reuse" (read 20261102 22:17 UTC)
13. https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/ : vLLM documentation, Automatic Prefix Caching (read 20261102 22:18 UTC)
