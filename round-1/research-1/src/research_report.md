# Prompt Compression Implementation Details Survey

## Summary

This research provides a comprehensive implementation survey of six prompt compression methods: SelectiveContext (Li et al., 2023), LLMLingua (Jiang et al., 2023), LLMLingua-2 (Pan et al., 2024), SelfCP (Gao et al., 2024), ASAP (Zeng et al., 2025), and PIS (Chen et al., 2025). Key findings: (1) SelectiveContext uses self-information I(x) = -log2 P(xt|x<t) computed by a small causal LM (GPT-3 curie or LLaMA-7B), merging tokens into phrases via SpaCy noun-chunk parsing or sentences via NLTK, then retaining units above the p-th percentile (default p=50). (2) LLMLingua employs a coarse-to-fine pipeline: budget controller allocates compression ratios per prompt component (instruction τ_ins=0.85, question τ_que=0.9, demonstrations derived from overall τ), selects demonstrations by descending perplexity, then applies iterative token-level compression (ITPC) with segment size=100, granular control k=2, using GPT-2 or Alpaca-7B as the small model. (3) LLMLingua-2 reframes compression as token classification (preserve/discard) using a Transformer encoder (XLM-RoBERTa-large or mBERT), trained on GPT-4-distilled data from MeetingBank with 5 constraints (only remove words, no reordering, no changes, no abbreviations, no additions). (4) SelfCP uses the frozen target LLM itself as compressor, projecting hidden states through a learnable linear connector into memory tokens, achieving 12x compression with only 17M trainable parameters on Vicuna-7B or BlueLM-7B backbones, supporting three strategies: former, latter, and concatenated compression. (5) ASAP is a CoT-specific method using two stages: anchor-guided pruning (generating a Direct Thought backbone from Q,A pairs) and surprisal-based refining using first-token surprisal S = -log P(first_token|context) to identify cognitive pivots, then distilling via supervised fine-tuning on DeepSeek-R1-Distill models. (6) PIS uses LLM-native attention scores as importance weights, implementing dual-level compression via a 9-layer RL policy network at token level and Russian roulette sampling at sentence level, achieving 38% overhead reduction vs baselines. All methods share the core insight that natural language redundancy can be exploited, but differ in scoring mechanism (perplexity vs self-information vs attention vs RL), granularity (token vs phrase vs sentence vs step), and training requirement (training-free vs distilled vs fine-tuned).

## Research Findings

## Prompt Compression Methods: Implementation Details Survey

This survey documents the exact implementation details for six prompt compression methods, enabling faithful reproduction and comparison.

### 1. SelectiveContext (Li et al., 2023) [1]

**Core Mechanism:** Self-information-based token/phrase/sentence pruning.

**Token Scoring Formula:**
```
I(x_i) = -log2 P(x_i | x_0, x_1, ..., x_{i-1})
```
Self-information is computed by a small causal language model (GPT-3 "curie" variant for OpenAI models, or LLaMA-7B for open models) [1]. The additivity property allows summing token-level self-information to get phrase/sentence-level scores:
```
I(u) = Σ_{i=t}^{t+α} I(x_i)
```

**Lexical Unit Merging:**
- **Token level:** No merging needed
- **Phrase level:** SpaCy's `merge_noun_chunks` for noun phrase boundary detection [1]
- **Sentence level:** NLTK sentence tokenizer [1]
- Verb phrases are NOT merged to avoid overly long units [1]

**Filtering Strategy:** Percentile-based adaptive filtering:
```
I_p = np.percentile([I(u_0), ..., I(u_k)], p)
C' = {u_i | I(u_i) >= I_p}
```
Default percentile p=50 (retain top 50% of lexical units by self-information) [1].

**Forward-Pass Pattern:** Single pass through the small LM to compute all token log-probabilities, then merge and filter. No iteration.

**Hyperparameters:**
- Small model: GPT-3 curie (OpenAI) or LLaMA-7B (open)
- Percentile threshold: p=50 (default)
- Granularity: token, phrase, or sentence (configurable)
- Context window: Process in chunks to avoid position bias [1]

**Compute Requirements:** One forward pass of the small LM over the full context. No GPU memory for the target LLM during compression.

### 2. LLMLingua (Jiang et al., 2023) [2]

**Core Mechanism:** Coarse-to-fine compression with budget controller and iterative token-level compression.

**Budget Controller (Algorithm 1):**
- Prompt decomposed into: instruction (x_ins), demonstrations (x_dems), question (x_que)
- Pre-defined compression rates: τ_ins = 0.85, τ_que = 0.90 [2]
- Demonstration compression rate derived: τ_dems = (τ·L - τ_ins·L_ins - τ_que·L_que) / L_dems [2]
- Demonstrations ranked by perplexity (descending), selected until token budget k·τ_dems·L_dems is reached [2]
- Granular control coefficient: k = 2 [2]
- Remaining budget allocated to instruction/question: Δτ = (k·τ_dems·L_dems - L_D) / (L_ins + L_que) [2]

**Iterative Token-Level Prompt Compression (ITPC, Algorithm 2):**
- Divide prompt into segments of size 100 tokens [2]
- For each segment i:
  - Compute conditional probabilities: p(e_s_j) = Π p(e_s_{j,i} | e_s_{<j,i}, x_{<i}) [2]
  - Compute compression threshold γ_i [2]
  - Select tokens above threshold
- Concatenate compressed tokens from all segments [2]

**Token Scoring:** Perplexity-based. Tokens with higher perplexity are more important:
```
PPL = 2^H(S) where H(S) = (1/N) Σ I(x_t)
```
Higher perplexity → more informative → retain [2].

**Forward-Pass Pattern:** Iterative. Process segments sequentially, concatenating compressed output to the context for the next segment to model interdependence [2].

**Hyperparameters:**
- Small model: GPT-2 (137M) or Alpaca-7B (fine-tuned for distribution alignment) [2]
- Segment size: 100 tokens [2]
- Granular control k: 2 [2]
- Instruction compression rate: 0.85 [2]
- Question compression rate: 0.90 [2]
- Target compression ratio: configurable (up to 20x demonstrated) [2]

**Compute Requirements:** Multiple forward passes of the small LM (one per segment). Distribution alignment requires fine-tuning Alpaca-7B on the Alpaca dataset [2].

### 3. LLMLingua-2 (Pan et al., 2024) [3]

**Core Mechanism:** Token classification (preserve/discard) using a Transformer encoder trained via GPT-4 data distillation.

**Architecture:**
- Base model: XLM-RoBERTa-large or multilingual BERT (mBERT) [3]
- Task: Binary token classification — each token labeled as "preserve" or "discard" [3]
- Compression metric: p_preserve (predicted probability of "preserve" label) [3]
- Uses bidirectional context (unlike causal LM approaches) [3]

**Data Distillation from GPT-4:**
- Instruction: "Compress the given text to short expressions, and such that you (GPT-4) can reconstruct it as close as possible to the original" [3]
- 5 strict constraints: (1) ONLY remove unimportant words, (2) Do not reorder, (3) Do not change words, (4) No abbreviations/emojis, (5) No new words/symbols [3]
- Training data: MeetingBank dataset (Hu et al., 2023) [3]
- Quality control: Two filtering metrics for low-quality samples [3]

**Token Scoring:**
```
score(token) = p_preserve(token)  # from classifier output
```
Tokens with p_preserve above a threshold are retained [3].

**Forward-Pass Pattern:** Single forward pass of the encoder over the full prompt. No iteration. 3x-6x faster than entropy-based methods [3].

**Hyperparameters:**
- Model: XLM-RoBERTa-large or mBERT
- Compression ratio: 2x-5x (achieves 14x in some settings) [3]
- Training: Supervised token classification on distilled data [3]
- End-to-end latency improvement: 1.6x-2.9x [3]

**Compute Requirements:** One forward pass of a small encoder. Requires pre-training on distilled data. No target LLM needed during compression.

### 4. SelfCP (Gao et al., 2024) [4]

**Core Mechanism:** Uses the frozen target LLM itself as compressor, projecting hidden states into memory tokens via a learnable connector.

**Architecture:**
- Compressor: The target LLM itself (frozen) [4]
- Connector: Learnable linear layer (projection) [4]
- Memory tokens: Dense vectors projected from LLM hidden states [4]
- Total trainable parameters: Only 17M (connector + learnable embedding) [4]
- Backbones: Vicuna-7B or BlueLM-7B [4]

**Compression Strategies:**
1. **Former Compression:** Compress first half, place memory tokens before uncompressed latter half [4]
2. **Latter Compression:** Compress second half, place memory tokens after uncompressed first half [4]
3. **Concatenated Compression:** Compress sub-prompts (e.g., demonstrations) independently into local memory tokens, then concatenate [4]

**Token Scoring:** No explicit token scoring. The LLM's hidden states are compressed into a fixed number of memory tokens via the linear connector. Compression ratio: 12x (12× over-limit prompts substituted with memory tokens) [4].

**Training:**
- Target LLM kept frozen during training [4]
- Connector supervised-tuned under language modeling objective [4]
- Training data: Relatively long texts from public datasets + instruction dataset [4]
- Only the connector and learnable embedding are trained [4]

**Forward-Pass Pattern:** Single forward pass of the frozen LLM on the over-limit portion, then projection through the connector.

**Hyperparameters:**
- Memory token count: Fixed (achieves 12x compression) [4]
- Trainable parameters: 17M [4]
- Backbone: Vicuna-7B or BlueLM-7B [4]

**Compute Requirements:** One forward pass of the target LLM (which is already loaded). Only 17M additional parameters.

### 5. ASAP (Zeng et al., 2025) [5]

**Core Mechanism:** Coarse-to-fine Chain-of-Thought (CoT) compression using anchor-guided pruning and first-token surprisal.

**Stage 1: Anchor-guided Pruning (Coarse):**
- Generate a "Direct Thought" (P) from (Question, Answer) pairs [5]
- P acts as a logical backbone/anchor [5]
- Prune irrelevant branches from the original CoT by alignment with P [5]
- Output: Coarse-grained Pruned CoT (C_coarse) [5]

**Stage 2: Surprisal-based Refining (Fine):**
- For each reasoning step s_i in C_coarse, compute first-token surprisal:
```
S(s_i) = -log P(first_token(s_i) | context_before_s_i)
```
- High-surprisal steps are retained (cognitive pivots like "But", "Wait", "Perhaps") [5]
- Low-surprisal steps are pruned (predictable fillers like "So", "Then") [5]
- Output: Fine-grained Pruned CoT (C') [5]

**Key Insight:** Empirical analysis of 10M tokens from DeepSeek-R1-Distill-Qwen-32B shows first tokens have significantly higher entropy (90th percentile = 1.97) than body tokens (90th percentile = 1.62) [5]. High-entropy first tokens correspond to cognitive pivots: exploration ("Alternative", "Another"), causality ("Because", "Since"), self-correction ("Perhaps", "What") [5].

**Training:**
- Supervised fine-tuning on pruned CoTs [5]
- Loss: Standard negative log-likelihood: L = -Σ Σ log P_θ(r_{i,j} | Q_i, r_{i,<j}) [5]
- Models: DeepSeek-R1-Distill-Qwen-7B and DeepSeek-R1-Distill-Llama-8B [5]

**Hyperparameters:**
- Surprisal threshold: Iterative filtering (remove lowest-surprisal steps until target length) [5]
- Target models: DeepSeek-R1-Distill variants [5]
- Results: 23.5% token reduction, 43.5% latency reduction on LiveCodeBench [5]

**Compute Requirements:** Two stages — anchor generation (one LLM call) + surprisal computation (one pass to get first-token log-probs) + fine-tuning.

### 6. PIS (Chen et al., 2025) [6]

**Core Mechanism:** Dual-level importance sampling using LLM-native attention scores.

**Theoretical Foundation:**
- Attention scores α_{t,i} = exp(⟨Q_t, K_i⟩/√d) / Σ_j exp(⟨Q_t, K_j⟩/√d) interpreted as importance weights [6]
- Formalized via measure theory: LLM generation as sampling over text space (Ω, F, P) [6]
- Importance weight: w(ω) = p*(ω) / p_θ(ω) [6]

**Token-Level Compression:**
- Quantify saliency using attention scores from LLM hidden states [6]
- Adaptive pruning via a lightweight 9-layer RL policy network [6]
- The RL network learns which tokens to keep based on attention patterns [6]

**Sentence-Level Compression:**
- Russian roulette sampling strategy for sentence-level importance sampling [6]
- Probabilistic redundancy reduction across semantic units [6]

**Token Scoring:**
```
Importance(token_i) = f(attention_scores(token_i))
```
Where f is learned by the 9-layer RL network [6].

**Forward-Pass Pattern:** Compute attention scores from LLM (one forward pass), then the RL network makes pruning decisions.

**Hyperparameters:**
- RL network: 9 layers [6]
- Dual-level: Token + Sentence [6]
- Results: 15% performance improvement at equivalent compression ratios, 38% overhead reduction vs baselines, 5% accuracy improvement on downstream tasks [6]

**Compute Requirements:** One forward pass of the LLM to get attention scores + one pass of the small RL network. No external generative model needed.

### Comparison Table

| Method | Scoring | Granularity | Training | Small Model | Passes | Max Ratio |
|--------|---------|-------------|----------|-------------|--------|-----------|
| SelectiveContext | Self-information (-log P) | Token/Phrase/Sentence | None | GPT-3 curie / LLaMA-7B | 1 | ~2x |
| LLMLingua | Perplexity | Token (iterative) | Optional (alignment) | GPT-2 / Alpaca-7B | Multiple (per segment) | 20x |
| LLMLingua-2 | Classifier p_preserve | Token | Yes (distilled) | XLM-RoBERTa-large / mBERT | 1 | 14x |
| SelfCP | Hidden state projection | Segment (soft tokens) | Yes (connector only) | Target LLM (frozen) | 1 | 12x |
| ASAP | First-token surprisal | CoT step | Yes (fine-tune) | Target LLM | 2 (anchor + surprisal) | ~5x |
| PIS | Attention + RL | Token + Sentence | Yes (RL) | 9-layer RL network | 1 | Variable |

### Reusable Components for SSHPC Implementation

1. **Self-information computation** (SelectiveContext/LLMLingua): Core building block for surprisal-based methods
2. **Segment-based processing** (LLMLingua): Pattern for handling long contexts in chunks
3. **Percentile-based filtering** (SelectiveContext): Adaptive thresholding without fixed cutoffs
4. **Token classification** (LLMLingua-2): Alternative to scoring — binary preserve/discard
5. **Frozen LLM as compressor** (SelfCP): Architecture for self-compression without external models
6. **First-token analysis** (ASAP): Novel feature for step-level importance
7. **Attention-based importance** (PIS): Direct use of LLM internals for scoring
8. **Dual-level compression** (PIS): Coarse-to-fine pattern applicable across methods

### Cross-Study Observations

Survey studies confirm that these methods span two main paradigms: hard prompt methods (filtering/paraphrasing) and soft prompt methods (attention modification, PEFT, modality integration) [7]. Empirical characterization across standardized benchmarks finds that extractive compression often outperforms token pruning, enabling up to 10x compression with minimal accuracy degradation [8]. However, token pruning methods like LLMLingua remain competitive on aggregation-style tasks requiring pieces of knowledge from all segments [8].

## Sources

[1] [Compressing Context to Enhance Inference Efficiency of Large Language Models (SelectiveContext)](https://arxiv.org/pdf/2310.06201) (Yucheng Li, Bo Dong, Chenghua Lin, Frank Guerin; 2023) — Original SelectiveContext paper introducing self-information-based pruning at token/phrase/sentence levels using percentile-based filtering with SpaCy and NLTK for lexical unit merging.

[2] [LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models](https://arxiv.org/pdf/2310.05736) (Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, Lili Qiu; 2023) — LLMLingua paper introducing coarse-to-fine compression with budget controller, iterative token-level compression (ITPC), and distribution alignment. Key hyperparameters: segment size=100, k=2, τ_ins=0.85, τ_que=0.9.

[3] [LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression](https://arxiv.org/pdf/2403.12968) (Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, H. Vicky Zhao, Lili Qiu, Dongmei Zhang; 2024) — LLMLingua-2 paper introducing token classification approach using XLM-RoBERTa-large/mBERT trained on GPT-4-distilled data from MeetingBank with 5 strict compression constraints.

[4] [SelfCP: Compressing Over-Limit Prompt via the Frozen Large Language Model Itself](https://arxiv.org/pdf/2405.17052) (Jun Gao, Ziqiang Cao, Wenjie Li; 2024) — SelfCP paper introducing self-compression using the frozen target LLM as compressor with a learnable linear connector (17M params) to project hidden states into memory tokens, achieving 12x compression.

[5] [Pruning the Unsurprising: Efficient LLM Reasoning via First-Token Surprisal (ASAP)](https://arxiv.org/pdf/2508.05988) (Wenhao Zeng, Yaoning Wang, Chao Hu, Yuling Shi, Chengcheng Wan, Hongyu Zhang, Xiaodong Gu; 2025) — ASAP paper introducing two-stage CoT compression: anchor-guided pruning using Direct Thought backbone, then first-token surprisal to identify cognitive pivots. Validated on DeepSeek-R1-Distill models.

[6] [PIS: Linking Importance Sampling and Attention Mechanisms for Efficient Prompt Compression](https://arxiv.org/pdf/2504.16574) (Lizhe Chen, Binjia Zhou, Yuyao Ge, Jiayi Chen, Shiguang Ni; 2025) — PIS paper introducing dual-level compression using LLM-native attention scores as importance weights, implemented via a 9-layer RL network at token level and Russian roulette sampling at sentence level.

[7] [Prompt Compression for Large Language Models: A Survey](https://arxiv.org/html/2410.12388v2) (Zongqian Li, Yinhong Liu, Yixuan Su, Nigel Collier; 2024) — Comprehensive survey categorizing prompt compression into hard prompt methods (filtering, paraphrasing) and soft prompt methods (attention modification, PEFT, modality integration), with detailed comparison of architectures.

[8] [Characterizing Prompt Compression Methods for Long Context Inference](https://arxiv.org/html/2407.08892v1) (Siddharth Jha, Lutfi Eren Erdogan, Sehoon Kim, Kurt Keutzer, Amir Gholami; 2024) — Empirical characterization study comparing token pruning, extractive compression, and abstractive compression across standardized benchmarks, finding extractive compression often outperforms token pruning.

## Verification

Numbered citations resolve to unique listed sources. Passage checks test text occurrence, not claim truth or entailment. Author/year metadata and locators are not independently verified. Details: `research_verification.json`.

No optional exact passages supplied; no passage checks performed.

## Follow-up Questions

- How do the compression quality trade-offs change when applying these methods to multimodal prompts (text + images) rather than pure text?
- What is the optimal segment size for iterative compression methods like LLMLingua across different context lengths and model families — is 100 tokens universally optimal?
- Can the first-token surprisal insight from ASAP be generalized to non-CoT prompts (e.g., RAG contexts, conversation history) where 'steps' are not explicitly delineated?

---
*Generated by AI Inventor Pipeline*
