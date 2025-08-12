# turktoken
Turktoken is a simple, tokenizer toolkit for Turkish NLP. Phase 1 ships language-agnostic word-level, subword (BPE), and character-level tokenizers to establish solid baselines. Phase 2 will add Turkish-specific handling—preserving diacritics, normalizing apostrophes, and being smarter around suffix boundaries—for better LLM and search performance.

## Mini roadmap
- Phase 1: Three language-agnostic tokenizers:
  - Character-level tokenizer
  - Word-level tokenizer
  - BPE tokenizer 

- Phase 2: Turkish-aware rules (diacritics, apostrophes), suffix-friendly segmentation, benchmarks and a small web demo.
