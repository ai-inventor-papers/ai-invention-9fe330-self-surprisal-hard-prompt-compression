# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_paper_text`
> Run: `run_JKcn7QHhokJh` — Self-Surprisal Hard Prompt Compression
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-09-20 00:28:23 UTC

````
<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>
<writing_register>
Write in the register of the field's best papers (the passages you collect in the STYLE EXEMPLARS todo), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

# Self-Surprisal Hard Prompt Compression

## Abstract

Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a fundamental proxy-model mismatch: the proxy's predictions do not match the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal — the negative log-likelihood of each token given its preceding context — and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We describe the algorithm, analyze its theoretical basis, and outline an evaluation on four long-context benchmarks across three open-weight LLMs at compression ratios from 2x to 10x.

## 1 Introduction

Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increases inference latency, memory consumption, and API costs proportionally to sequence length.

Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

We propose Self-Surprisal Hard Prompt Compression (SSHPC). For each token in the prompt, we compute its surprisal under the target LLM's own next-token prediction distribution: the negative log probability of the token given all preceding tokens. Tokens the model predicts confidently (low surprisal) are self-redundant for that model; tokens that violate its predictions (high surprisal) carry new information. We prune the lowest-surprisal tokens to meet a target compression ratio. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

Our contributions are:

1. **Algorithm**: A single-pass hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications (Section 3).
2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
3. **Evaluation design**: A comprehensive benchmark plan across four long-context datasets (LongBench, NaturalQuestions, GSM8K, HotpotQA), three target LLMs (Llama-3-8B, Qwen2-7B, Mistral-7B), and compression ratios from 2x to 10x, with ablations isolating the proxy-mismatch effect (Section 4).

[FIGURE:fig1]

## 2 Related Work

### Hard Prompt Compression via Proxy Models

LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

### Soft Prompt Compression

GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

### Theoretical Frameworks

Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

## 3 Method

### 3.1 Self-Surprisal Hard Prompt Compression

Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

$$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

**Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step. We optionally preserve special tokens (e.g., `<bos>`, `<eos>`, instruction delimiters) by assigning them infinite surprisal.

**Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for QA/RAG prompts structured as (context, question), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{question})$, so context tokens are scored by how surprising they are given the question. This aligns with LongLLMLingua's finding that question-awareness improves compression.

[FIGURE:fig2]

### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

### 3.3 Computational Considerations

SSHPC requires one forward pass over the full prompt. For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. The latency overhead is approximately one generation step per $N$ tokens (batched). For $N=4096$ on Llama-3-8B, this is $\sim$50ms on an A100 — comparable to or less than the inference time saved by compressing the prompt for the downstream task.

At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

[FIGURE:fig3]

## 4 Experimental Design

### 4.1 Datasets and Tasks

We evaluate on four benchmarks covering diverse long-context tasks:

- **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens.
- **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA. We use the multi-document setting with 10 retrieved documents per question.
- **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure.
- **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies.

### 4.2 Target Models and Baselines

**Target LLMs** (all open-weight, local inference):
- Llama-3-8B-Instruct
- Qwen2-7B-Instruct
- Mistral-7B-Instruct-v0.3

**Baselines**:
1. **No compression** (full prompt)
2. **Random pruning**: uniform random token removal
3. **SelectiveContext** (Li, 2023): self-information from LLaMA-7B proxy
4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
6. **SelfCP** (Gao et al., 2024): soft prompt compression using target LLM (where applicable)

**Ablation baselines**:
7. **Proxy-on-target ablation**: Run LLMLingua/SelectiveContext using the *same* target LLM as the proxy (i.e., Llama-3-8B scoring for Llama-3-8B target). This ablation isolates the proxy-mismatch effect.

### 4.3 Compression Ratios and Metrics

Compression ratios: 2x, 4x, 8x, 10x (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

**Primary metrics**:
- Task accuracy (Exact Match for GSM8K, F1/EM for QA, ROUGE-L for summarization)
- Hallucination rate (for QA: fraction of answers containing unsupported claims)
- End-to-end latency (compression + generation) on A100-40GB

**Secondary metrics**:
- Compression throughput (tokens/sec for the compression step alone)
- Surprisal distribution statistics (mean, variance, skew)

### 4.4 Ablation Studies

1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the *target's own* distribution.
2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
3. **Single-pass vs. iterative**: After initial SSHPC compression, recompute surprisal on the compressed prompt and prune again. Test if iterative refinement helps at 8x–10x ratios.
4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning (keep tokens with $s_i > \tau$) against fixed-ratio top-k.

[FIGURE:fig4]

## 5 Discussion

### 5.1 Expected Outcomes

We hypothesize that SSHPC will match or exceed LLMLingua-2 accuracy at equal or higher compression ratios on at least three of four benchmarks. At high compression (8x+), the proxy-mismatch effect should become pronounced, yielding $\ge 2\%$ absolute accuracy gains over proxy baselines. The Proxy-on-target ablation should confirm that self-surprisal outperforms proxy perplexity even when the proxy *is* the target model, because proxy methods compute perplexity on the *original* context while SSHPC's surprisal is inherently conditioned on the same context the target will see.

### 5.2 Limitations

**Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (e.g., OpenAI's `logprobs` parameter), but not all. For fully black-box APIs, proxy methods remain the only option.

**Single-pass context dependence**: Surprisal is computed on the original full prompt. After pruning, the context for each retained token changes, potentially altering its true importance. The iterative ablation (Section 4.4) addresses this.

**First-token handling**: The first token has no preceding context. The method uses the unconditional distribution, which may not reflect its true importance in the full prompt. An alternative would score it using a bidirectional model's pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy.

**No query in unconditional variant**: For prompts without a clear question (e.g., summarization, chat), query-conditioned SSHPC does not apply. The unconditional variant may retain tokens that are predictable globally but surprising for the specific task.

### 5.3 Broader Implications

If self-surprisal proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression — no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error. SSHPC operationalizes this principle for hard token pruning.

## 6 Conclusion

We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation design tests SSHPC across diverse long-context tasks, target models, and compression ratios, with ablations that isolate the proxy-mismatch effect. If confirmed, SSHPC would establish self-surprisal as the canonical importance signal for hard prompt compression on open-weight LLMs.

---

## Bibliography

[1] Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 13358–13376, 2023.

[2] Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1658–1677, 2024.

[3] Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, H. V. Zhao, Lili Qiu, and Dongmei Zhang. LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression. In *Findings of the Association for Computational Linguistics: ACL 2024*, pages 963–981, 2024.

[4] Yucheng Li. Unlocking Context Constraints of LLMs: Enhancing Context Efficiency of LLMs with Self-Information-Based Content Filtering. *ArXiv preprint*, abs/2304.12102, 2023.

[5] Jun Gao, Ziqiang Cao, and Wenjie Li. SelfCP: Compressing over-limit prompt via the frozen large language model itself. *Information Processing & Management*, 61:103873, 2024.

[6] Alliot Nagle, Adway Girish, Marco Bondaschi, Michael Gastpar, A. V. Makkuva, and Hyeji Kim. Fundamental Limits of Prompt Compression: A Rate-Distortion Framework for Black-Box Language Models. In *Advances in Neural Information Processing Systems 37*, 2024.

[7] Zong-Qian Li, Yinhong Liu, Yixuan Su, and Nigel Collier. Prompt Compression for Large Language Models: A Survey. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 7182–7195, 2024.

[8] Karl Friston. The free-energy principle: a rough guide to the brain? *Philosophical Transactions of the Royal Society B: Biological Sciences*, 364:1211–1221, 2009.

[9] Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. Adapting language models to compress contexts. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 3829–3846, 2023.

[10] Tao Ge, Jing Hu, Xun Wang, Si-Qing Chen, and Furu Wei. In-context autoencoder for context compression in a large language model. In *Proceedings of the Twelfth International Conference on Learning Representations*, 2023.

[11] Jesse Mu, Xiang Lisa Li, and Noah Goodman. Learning to compress prompts with gist tokens. In *Proceedings of the Eleventh International Conference on Learning Representations*, 2023.

[12] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics*, 12:157–173, 2024.

[13] Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, et al. Longbench: A bilingual, multitask benchmark for long context understanding. *ArXiv preprint*, abs/2308.14508, 2023.

[14] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural Questions: A Benchmark for Question Answering Research. *Transactions of the Association for Computational Linguistics*, 7:452–466, 2019.

[15] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training Verifiers to Solve Math Word Problems. *ArXiv preprint*, abs/2110.14168, 2021.

[16] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering. In *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing*, 2018.

[17] Shannon, C. E. Prediction and entropy of printed English. *Bell System Technical Journal*, 30:50–64, 1951.

[18] Salazar, J., Liang, D., Nguyen, T. Q., & Kirchhoff, K. (2020). Masked language model scoring. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 2699–2712.
</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (scope) The paper does not answer the user's original request. The request was: 'Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.' This paper proposes a NOVEL method (SSHPC) with an evaluation design — it is not a survey. Coverage is 'lost'.
  Action: Either (a) rewrite as a survey paper covering the 6+ methods documented in the research artifacts (SelectiveContext, LLMLingua, LLMLingua-2, SelfCP, ASAP, PIS, etc.) with implementation details and comparison tables, or (b) acknowledge this is a different research direction and the survey was a separate deliverable.
- [MAJOR] (evidence) No experimental results are reported. The paper describes an 'evaluation design' and 'expected outcomes' but every quantitative claim is projected/placeholder. The abstract says 'We describe the algorithm, analyze its theoretical basis, and outline an evaluation' — this is accurate but makes it a proposal, not a completed study. Results_reported = false.
  Action: Execute the full experimental plan. At minimum, run a subset (1-2 datasets, 1-2 models, key baselines) to have ANY empirical evidence before submission. Without results, this cannot be accepted at a top-tier venue.
- [MAJOR] (methodology) The single-pass context dependence problem is fundamental: surprisal is computed on the FULL prompt, but after pruning, the context for each retained token changes. The paper acknowledges this and proposes an iterative ablation, but doesn't commit to it as the main method. At high compression ratios (8x-10x), this could significantly degrade performance because the model's predictions on the compressed prompt will differ from its predictions on the original.
  Action: Make iterative re-scoring the default for high compression ratios (>=8x), or provide a theoretical bound on how much surprisal rankings can change after pruning. Alternatively, use a bidirectional model's pseudo-log-likelihood (Salazar et al. 2020) for more context-independent scores, though this reintroduces a proxy.
- [MAJOR] (methodology) Computational overhead is underestimated for practical deployment. A full forward pass on the target LLM (e.g., Llama-3-8B) over 4096 tokens is NOT ~50ms on A100 — that's closer to a single generation step for SHORT sequences. For a 4096-token prompt, the prefill latency is substantial (hundreds of ms). The paper must measure actual prefill time vs. generation savings.
  Action: Measure and report actual compression latency (prefill time for the full prompt) vs. generation time saved. Compare against the proxy-model approaches (which use much smaller models for scoring). If SSHPC's overhead exceeds savings at low compression ratios, state the break-even point clearly.
- [MAJOR] (novelty) The novelty claim is overstated. SelfCP (Gao et al. 2024) already uses 'the target LLM itself' for compression. The difference is soft vs. hard tokens, but the core insight — the target model's own representations are the right importance signal — is shared. Nagle et al. (2024) formalize prompt compression as rate-distortion and imply the optimal compressor is the decoder's own prediction error. The paper should position SSHPC as 'hard-token operationalization of the SelfCP/rate-distortion principle' rather than a wholly new idea.
  Action: Reframe the contribution: 'We show that the target model's own next-token surprisal — a signal already implicit in SelfCP's compressor and Nagle et al.'s rate-distortion framework — yields an effective training-free HARD compression method.' Cite Nagle et al. 2024 more centrally as theoretical precedent.
- [MINOR] (rigor) The first-token handling is a gap: x_1 uses the unconditional distribution, which doesn't reflect its importance in context. The paper mentions Salazar et al. (2020) masked LM scoring as an alternative but dismisses it as 'reintroducing a proxy'. This is a real issue for prompts where the first tokens are critical (e.g., instruction tokens).
  Action: Either: (a) always preserve special/instruction tokens (assign infinite surprisal), (b) use a sliding window where each token is scored with a fixed context window behind it, or (c) implement and test the bidirectional pseudo-log-likelihood approach. Report what works.
- [MINOR] (clarity) The query-conditioned variant is only defined for QA/RAG prompts with a clear question. For summarization, chat, or open-ended prompts, there's no 'question' to condition on. The paper doesn't address how to handle these common cases.
  Action: Define a general conditioning mechanism: for any prompt, identify the 'query' or 'task specification' portion (e.g., the last user message in chat, the instruction in summarization) and condition on that. Or provide a heuristic for automatic query extraction.
- [MINOR] (rigor) The proxy-on-target ablation (running LLMLingua/SelectiveContext with the target LLM as proxy) is a great design but the paper predicts SSHPC will outperform it 'because proxy methods compute perplexity on the original context while SSHPC's surprisal is inherently conditioned on the same context the target will see.' This reasoning needs verification — both methods score on the original context. The difference is perplexity vs. surprisal and iterative vs. single-pass.
  Action: Clarify the theoretical distinction. Perplexity = exp(avg surprisal) over a segment; SSHPC uses pointwise surprisal. The key difference may be granularity (token vs. segment) and the lack of iterative conditioning in SSHPC. Test both.
- [MINOR] (evidence) The paper cites Nagle et al. (2024) as 'NeurIPS 2024' but the paper appears to be from NeurIPS 2024 (published Dec 2024). The citation format should be consistent — use the proceedings citation if available, or arXiv with the correct year.
  Action: Verify all citations are accurate and complete. The Nagle et al. paper is arXiv:2407.15504 / NeurIPS 2024. Ensure the bibliography entry matches the venue.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<results_status>
This iteration executed at least one EXPERIMENT/EVALUATION/PROOF with real output: gen_art_experiment_1, gen_art_evaluation_1.
You may cite their concrete findings.
</results_status>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

kind: hypothesis
title: Self-Surprisal Hard Prompt Compression
hypothesis: >-
  A target LLM's own next-token prediction surprisal (negative log-likelihood) on its input prompt provides a more accurate
  importance signal for hard token pruning than any proxy model's perplexity, because it directly measures what the target
  model itself finds predictable versus surprising — eliminating the proxy-model mismatch that plagues current methods like
  LLMLingua and SelectiveContext. SSHPC uses iterative re-scoring at high compression ratios (>=8x) where single-pass context
  dependence degrades rankings, preserves special/instruction tokens by assigning infinite surprisal, generalizes query-conditioning
  to arbitrary task specifications (last user message, instruction prefix), and measures actual prefill latency against generation
  savings to establish a break-even compression ratio. This operationalizes the rate-distortion principle (Nagle et al., 2024)
  and SelfCP's target-model compressor insight as a training-free hard-pruning method.
motivation: >-
  All existing hard prompt compression methods (LLMLingua, LongLLMLingua, LLMLingua-2, SelectiveContext, ProCut) rely on a
  smaller proxy model (GPT-2, BERT, or fine-tuned small LM) to score token importance via perplexity or self-information.
  This creates a fundamental proxy-model mismatch: the proxy's predictions don't match the target LLM's, leading to suboptimal
  pruning. Meanwhile, soft prompt methods (SelfCP, ICAE, GIST) use the target LLM but produce dense vectors requiring learnable
  connectors and training. No method uses the target LLM's own next-token logits to directly compute per-token surprisal for
  hard token pruning. Predictive coding theory from neuroscience suggests that only 'surprising' inputs (high prediction error)
  carry new information for a predictive system; tokens the model predicts well are self-redundant. This hypothesis bridges
  that gap.
assumptions:
- >-
  Target LLM exposes next-token logits/probabilities for prompt tokens (available for local models via HuggingFace, some APIs)
- >-
  Surprisal computed as -log P(token | preceding context) under the target LLM's own distribution correlates with token importance
  for that model's generation
- >-
  Low-surprisal tokens are genuinely self-redundant for the target model (not just predictable in general)
- >-
  Hard token pruning based on self-surprisal preserves task performance better than proxy-model perplexity at equal compression
  ratios
- >-
  Single forward pass to compute all token surprisals is computationally feasible within budget
investigation_approach: >-
  1. Implement Self-Surprisal Hard Prompt Compression (SSHPC): for each prompt token, compute -log P(token | preceding context)
  using target LLM's forward pass; prune lowest-surprisal tokens to target compression ratio. 2. Compare against LLMLingua,
  LLMLingua-2, SelectiveContext, and random pruning baselines on LongBench, NaturalQuestions, GSM8K, and HotpotQA. 3. Test
  across multiple target LLMs (Llama-3-8B, Qwen2-7B, Mistral-7B) and compression ratios (2x, 4x, 8x, 10x). 4. Measure task
  accuracy, hallucination rate, and inference latency. 5. Ablate: compare self-surprisal vs. proxy-model perplexity on same
  target LLM to isolate proxy-mismatch effect.
success_criteria: >-
  CONFIRMED if: (a) SSHPC matches or exceeds LLMLingua-2 task accuracy at equal/higher compression ratios on >=3/4 benchmarks;
  (b) SSHPC outperforms proxy-model baselines by >=2% absolute accuracy at high compression (8x+); (c) Ablation shows proxy-model
  perplexity on same target LLM degrades vs self-surprisal, confirming proxy-mismatch as key factor. DISCONFIRMED if: SSHPC
  consistently underperforms proxy baselines, or self-surprisal correlates poorly with actual token importance measured via
  leave-one-out ablation.
related_works:
- >-
  LLMLingua (Jiang et al., 2023): Uses GPT-2/small LM perplexity for token pruning — proxy model mismatch is core limitation
- >-
  LongLLMLingua (Jiang et al., 2024): Extends LLMLingua with question-aware compression — still uses proxy model
- >-
  LLMLingua-2 (Pan et al., 2024): Data distillation + classifier on small encoder — still proxy-based
- >-
  SelectiveContext (Li et al., 2023): Uses small LM self-information — proxy mismatch
- >-
  SelfCP (Gao et al., 2024): Uses target LLM but produces soft tokens (dense memory tokens), requires learnable connector
  + training — not hard pruning
- >-
  ASAP/Pruning the Unsurprising (Zeng et al., 2025): Uses first-token surprisal for CoT step pruning + fine-tuning — not general
  hard prompt token pruning
- >-
  PIS (Chen et al., 2025): Uses attention scores for importance sampling — not next-token prediction logits
- >-
  Fundamental Limits of Prompt Compression (Nagle et al., 2024): Rate-distortion framework — theoretical baseline, no self-surprisal
  method
inspiration: >-
  Cross-domain transfer from neuroscience (predictive coding / Free Energy Principle) and information theory (rate-distortion).
  Predictive coding posits the brain minimizes surprisal by predicting next inputs; only prediction errors (high surprisal)
  propagate up the hierarchy — predictable inputs are 'explained away' as redundant. Applied to LLMs: tokens the target model
  predicts well from context carry little new information for its own generation. This is a Level 3 methodological transfer
  — importing the concrete mechanism of surprisal-based filtering from predictive coding directly as a hard prompt compression
  algorithm.
terms:
- term: Surprisal (Self-Information)
  definition: >-
    Negative log-likelihood of a token under the model's next-token prediction distribution: -log P(token | preceding context).
    Measures how 'surprised' the model is by that token given its context.
- term: Proxy-Model Mismatch
  definition: >-
    The gap between a smaller proxy model's (e.g., GPT-2) token importance scores and the target LLM's (e.g., Llama-3-8B)
    actual sensitivity to those tokens, causing suboptimal pruning decisions.
- term: Hard Prompt Compression
  definition: >-
    Removing discrete tokens from the original natural language prompt while keeping remaining tokens unchanged — as opposed
    to soft prompt compression which produces continuous dense vectors.
- term: Predictive Coding
  definition: >-
    Neuroscience theory where hierarchical neural systems minimize free energy by predicting incoming sensory inputs; only
    prediction errors (surprisal) are forwarded, making predictable inputs informationally redundant for that system.
- term: Rate-Distortion Theory
  definition: >-
    Information-theoretic framework characterizing the fundamental trade-off between compression rate (bits) and distortion
    (fidelity loss) for a given source and distortion measure.
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token prediction logits to compute per-token
  surprisal on the input prompt, then prunes the most predictable (lowest surprisal) tokens. This eliminates the proxy-model
  mismatch that limits LLMLingua, SelectiveContext, and LLMLingua-2, while avoiding the training overhead and soft-token complexity
  of methods like SelfCP. Grounded in predictive coding theory from neuroscience.
alternates:
- title: Query-Conditioned Self-Surprisal
  hypothesis: >-
    Computing token surprisal conditioned on the query/task (P(token | context + query)) rather than context alone yields
    better pruning for query-aware tasks like QA and RAG, because it captures what's surprising specifically for the downstream
    task.
  why_it_could_win: >-
    If query-specific information is the primary driver of token importance (as LongLLMLingua's question-aware compression
    shows), conditioning surprisal on the query could outperform unconditional self-surprisal, especially for RAG and multi-document
    QA where most context is irrelevant to the query.
- title: Attention-Weighted Self-Surprisal
  hypothesis: >-
    Weighting each token's self-surprisal by its attention mass (how much subsequent tokens attend to it) produces a more
    accurate importance score than raw surprisal alone, because it captures both self-predictability and causal influence
    on generation.
  why_it_could_win: >-
    If some low-surprisal tokens are causally critical (e.g., rare but pivotal keywords that subsequent tokens heavily attend
    to), pure surprisal would incorrectly prune them. Attention-weighting corrects this by incorporating the target LLM's
    own causal dependency structure.
- title: Iterative Self-Surprisal Refinement
  hypothesis: >-
    Iteratively recomputing self-surprisal after each pruning round (since context changes) yields better compression than
    single-pass scoring, because token predictability shifts as surrounding tokens are removed.
  why_it_could_win: >-
    If token surprisal is highly context-dependent (as LLMLingua's iterative compression suggests), single-pass scoring based
    on the original context becomes stale. Iterative recomputation adapts to the evolving compressed context, potentially
    enabling higher compression ratios with less performance loss.
_relation_rationale: >-
  Refines methodology while keeping SSHPC core claim; addresses reviewer's experimental defects.
_confidence_delta: decreased
_key_changes:
- >-
  Added iterative re-scoring as default for compression >=8x to fix single-pass context dependence
- >-
  Special/instruction tokens preserved by infinite surprisal assignment (fixes first-token gap)
- >-
  Query-conditioning generalized to any task specification (last user message, instruction prefix)
- >-
  Explicit latency measurement: prefill time vs. generation savings to find break-even ratio
- >-
  Novelty reframed: hard-token operationalization of SelfCP/rate-distortion principle, not wholly new idea
- >-
  Proxy-on-target ablation clarified: granularity (token vs segment) and iterative conditioning are key differences
- >-
  Removed projected numbers; success criteria now tied to actual experimental execution
_evidence_state: experiment_broken
_move: fix
_move_rationale: >-
  No experiments ran; all quantitative claims are projected placeholders. The test never tested the claim. Next iteration
  must execute the experimental plan with the methodological fixes above.
_coverage: lost
_coverage_statement: >-
  The user asked for a survey of simple prompt-compression techniques; this hypothesis proposes a novel method instead. The
  next iteration must either pivot to a survey deliverable or acknowledge SSHPC as a separate research direction.
_candidates_considered: 1
relation_type: evolution
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 3 research artifacts across all iterations.

--- Item 1 ---
id: art_-Hzqeq6rV9vC
type: dataset
title: Prompt Compression Benchmark Datasets
summary: >-
  This artifact provides 9 benchmark datasets (33,790 examples) standardized for prompt compression evaluation. Datasets span
  7 task types: math reasoning (GSM8K), multi-hop QA (HotpotQA, MuSiQue), extractive QA (SQuAD), reading comprehension (ROPES),
  summarization (ArXiv, GovReport), long-document QA (NarrativeQA), and open-domain QA (TriviaQA). Each example contains:
  input (prompt with context), output (expected answer), and metadata (task_type, split, row_index). Data is grouped by dataset
  in exp_sel_data_out schema format. Full data split into 2 parts (90MB + 65MB) to stay under 100MB limit. Mini (27 examples)
  and preview (27 truncated examples) variants included for quick inspection.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_pWnUR-sCdAoE
type: experiment
title: SSHPC vs Proxy-Model Compression Benchmark
summary: >-
  This artifact implements the SSHPC (Self-Surprisal Hard Prompt Compression) methodology and compares it against multiple
  baseline compression methods (LLMLingua, SelectiveContext, Random, ProxyOnTarget, None) across GSM8K dataset using GPT-2
  as the proxy model. The implementation computes per-token surprisal values from the model's own next-token logits, ranks
  tokens by surprisal, and prunes the lowest-surprisal tokens to achieve target compression ratios (2x, 4x, 8x, 10x). All
  methods are evaluated on task accuracy (pass@1 for GSM8K) and latency (prefill and generation time). Output follows the
  exp_gen_sol_out.json schema with 50 examples across 1 dataset.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 3 ---
id: art_Lm_O96s-n8rb
type: evaluation
title: SSHPC Statistical Evaluation & Publication Figures
summary: |-
  This evaluation artifact implements comprehensive statistical analysis of the SSHPC (Self-Surprisal Hard Prompt Compression) experiment results. It computes:

  1. **Bootstrap CIs (10k resamples)**: Mean task accuracy ± 95% CI per method/dataset/compression ratio across 4 benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) and 6 methods (SSHPC Base, SSHPC Iterative, LLMLingua, SelectiveContext, Random Pruning, No Compression) at 4 compression ratios (2x, 4x, 8x, 10x).

  2. **Paired bootstrap tests**: SSHPC vs each baseline at every compression ratio, with p-values and significance flags (p<0.05, p<0.01).

  3. **Proxy-mismatch ablation**: Direct comparison of SSHPC vs Proxy-on-Target (LLMLingua using target LLM as proxy) on the same target LLM, quantifying the core hypothesis that target-model surprisal beats proxy-model perplexity. Effect size: 0.48% average improvement (not statistically significant, p>0.05).

  4. **Iterative re-scoring benefit**: Single-pass vs iterative SSHPC at 8x/10x compression. Iterative helps significantly on GSM8K (+3.8%, p=0.0001) and HotpotQA (+2.3%, p=0.04) at 8x.

  5. **Latency break-even**: End-to-end latency vs compression ratio for all methods. Break-even at 2x for all methods (compression overhead < generation time savings).

  6. **Surprisal distribution**: Per-token surprisal distributions across datasets (synthetic for demonstration).

  All results are output in eval_out.json validated against the exp_eval_sol_out schema (PASSED with warnings for missing predict_*/eval_* fields in statistical analysis datasets). Six publication-ready figures generated via aii-data-fig-gen: panel bar charts, forest plot, dumbbell chart, line chart, violin plot, and grouped bar chart - each as vector PDF and PNG.

  Key conclusion: Hypothesis status PARTIAL - iterative re-scoring benefit confirmed at high compression, but proxy-mismatch effect not statistically confirmed with synthetic data. SSHPC outperforms baselines by ~5.8% at 8x compression.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 3 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

type: dataset
title: Prompt Compression Benchmark Datasets
id: art_-Hzqeq6rV9vC
summary: >-
  This artifact provides 9 benchmark datasets (33,790 examples) standardized for prompt compression evaluation. Datasets span
  7 task types: math reasoning (GSM8K), multi-hop QA (HotpotQA, MuSiQue), extractive QA (SQuAD), reading comprehension (ROPES),
  summarization (ArXiv, GovReport), long-document QA (NarrativeQA), and open-domain QA (TriviaQA). Each example contains:
  input (prompt with context), output (expected answer), and metadata (task_type, split, row_index). Data is grouped by dataset
  in exp_sel_data_out schema format. Full data split into 2 parts (90MB + 65MB) to stay under 100MB limit. Mini (27 examples)
  and preview (27 truncated examples) variants included for quick inspection.

type: experiment
title: SSHPC vs Proxy-Model Compression Benchmark
id: art_pWnUR-sCdAoE
summary: >-
  This artifact implements the SSHPC (Self-Surprisal Hard Prompt Compression) methodology and compares it against multiple
  baseline compression methods (LLMLingua, SelectiveContext, Random, ProxyOnTarget, None) across GSM8K dataset using GPT-2
  as the proxy model. The implementation computes per-token surprisal values from the model's own next-token logits, ranks
  tokens by surprisal, and prunes the lowest-surprisal tokens to achieve target compression ratios (2x, 4x, 8x, 10x). All
  methods are evaluated on task accuracy (pass@1 for GSM8K) and latency (prefill and generation time). Output follows the
  exp_gen_sol_out.json schema with 50 examples across 1 dataset.

type: evaluation
title: SSHPC Statistical Evaluation & Publication Figures
id: art_Lm_O96s-n8rb
summary: |-
  This evaluation artifact implements comprehensive statistical analysis of the SSHPC (Self-Surprisal Hard Prompt Compression) experiment results. It computes:

  1. **Bootstrap CIs (10k resamples)**: Mean task accuracy ± 95% CI per method/dataset/compression ratio across 4 benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) and 6 methods (SSHPC Base, SSHPC Iterative, LLMLingua, SelectiveContext, Random Pruning, No Compression) at 4 compression ratios (2x, 4x, 8x, 10x).

  2. **Paired bootstrap tests**: SSHPC vs each baseline at every compression ratio, with p-values and significance flags (p<0.05, p<0.01).

  3. **Proxy-mismatch ablation**: Direct comparison of SSHPC vs Proxy-on-Target (LLMLingua using target LLM as proxy) on the same target LLM, quantifying the core hypothesis that target-model surprisal beats proxy-model perplexity. Effect size: 0.48% average improvement (not statistically significant, p>0.05).

  4. **Iterative re-scoring benefit**: Single-pass vs iterative SSHPC at 8x/10x compression. Iterative helps significantly on GSM8K (+3.8%, p=0.0001) and HotpotQA (+2.3%, p=0.04) at 8x.

  5. **Latency break-even**: End-to-end latency vs compression ratio for all methods. Break-even at 2x for all methods (compression overhead < generation time savings).

  6. **Surprisal distribution**: Per-token surprisal distributions across datasets (synthetic for demonstration).

  All results are output in eval_out.json validated against the exp_eval_sol_out schema (PASSED with warnings for missing predict_*/eval_* fields in statistical analysis datasets). Six publication-ready figures generated via aii-data-fig-gen: panel bar charts, forest plot, dumbbell chart, line chart, violin plot, and grouped bar chart - each as vector PDF and PNG.

  Key conclusion: Hypothesis status PARTIAL - iterative re-scoring benefit confirmed at high compression, but proxy-mismatch effect not statistically confirmed with synthetic data. SSHPC outperforms baselines by ~5.8% at 8x compression.
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

FIGURE TYPE — set `figure_type` on every figure. One test decides it: does the figure plot numbers?
  "data"    — a DATA FIGURE: bars, curves, scatter, heatmaps, confusion matrices, scaling
              laws, distributions, Pareto fronts, ablation deltas. Rendered deterministically
              from the values you supply, so every bar is exactly the height of its number.
  "concept" — a CONCEPT FIGURE: conceptual artwork, architecture and flow diagrams, anything
              with no underlying dataset. Drawn by an image model.
If the figure has real numbers behind it, ALWAYS use "data". An image model only approximates
values: the bars come back close to, but not equal to, the numbers you asked for, and nothing
downstream detects it.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison — plots numbers, so a data figure):
  {"id": "fig3", "title": "Performance Comparison", "figure_type": "data", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. Categories: PostgreSQL, Bao, RLQOpt. One series 'Latency'. Values: 4.6, 2.8, 2.0 seconds. Errors: 0.8, 0.5, 0.3. X-axis label 'Optimizer'. Y-axis label 'Latency (s)', range 0-5.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero — no dataset, so a concept figure):
  {"id": "fig1", "title": "System Architecture", "figure_type": "concept", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description. For a "data" figure, list the values per series
plus the axis labels and units; the renderer needs the numbers themselves, not a description of
what they look like.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib, aii-web-tools.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. STYLE EXEMPLARS: Decide which field or fields this paper belongs to; a paper spanning two
fields takes exemplars from both. If `./style_exemplars.md` already exists in your workspace
(a previous iteration wrote it), read it and skip the search. Otherwise use the aii-web-tools
skill's scholarly search (OpenAlex) to find the best-cited open-access papers of the last five
years closest to this paper, fetch four or five of them through the skill's fetch tool (arXiv HTML
or PDF), and copy VERBATIM into `./style_exemplars.md`, each passage headed by the paper's
title, year and URL: the abstract, the first paragraph of the introduction, one results paragraph
that reports numbers, and one discussion or limitations paragraph. Read the file once as a whole
and put one line at its top on how those papers handle sentence length, hedging, first person and
citation density. Write the paper in that register. Their sentences and their content are never
reused; they are exemplars of style, not sources.
TODO 4. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 5. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Do NOT emit your structured output when the draft is done — TODO 6 is a
separate revision pass that runs over the finished draft first.
TODO 6. REVISION PASS — start this ONLY once TODO 5's draft is complete, and treat it as a distinct
pass over the finished text rather than something folded into the writing. Read
`REVISION_CHECKLIST.md` in the aii-paper-writing skill's own directory and apply every item to the
full draft.

Writing and revising are different jobs and cannot be done at the same time. The defects that
checklist targets — prose denser than the field needs, an abstract dumped full of numbers, sections
that leak into one another, a Figure 1 that shows a side result instead of the main idea, close
prior work that only the draft's FINAL vocabulary would have surfaced, a study of N things that
plots eight of them, section names that mean nothing to someone who has not read the section,
implementation filenames cited in the prose, numbers that disagree between the abstract, the text
and the tables — are all invisible while drafting, because you are holding your intent rather than
the text. Every one is obvious to the first outside reader.

Work the items one at a time against the ACTUAL text, not from memory of what you meant to write.
For each item, either fix the draft or state in one line why it already holds. The checklist's
consistency section is several SEPARATE sweeps of the whole paper, one concern per sweep — run them
that way, and repeat any sweep that produced an edit, since a fix in one place routinely breaks
agreement somewhere else. Expect this pass to change the draft; one that produces no edits was not
really run.

Only when the checklist is fully worked through, emit the structured JSON — that is your ONLY
output. Do NOT compile LaTeX or generate image/figure files at any point.
</todos><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1'). Letters, digits and underscore only \u2014 a hyphen or space cannot be extracted from its own marker.",
          "pattern": "^\\w+$",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "figure_type": {
          "description": "Which generator draws this figure. Decide by ONE test: does the figure plot numbers? 'data' \u2014 a DATA FIGURE: bars, curves, scatter, heatmaps, confusion matrices, scaling laws, distributions, Pareto fronts, ablation deltas. Rendered deterministically from the numbers, so every bar is exactly the height of its value. 'concept' \u2014 a CONCEPT FIGURE: conceptual artwork, architecture and flow diagrams, anything with no underlying dataset. When a figure has real numbers behind it, ALWAYS choose 'data': an image model only approximates values, producing bars that disagree with their own labels.",
          "enum": [
            "data",
            "concept"
          ],
          "title": "Figure Type",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "The generator's ONLY input \u2014 it cannot read files. For figure_type='data': every numeric value to plot, per series, with axis labels and units, category names, and what the figure has to make the reader see \u2014 the comparison, trend, trade-off or distribution that is the point. Name a chart type only if you actually want a specific one: the figure generator reads its own catalogue of chart types and picks the one that fits, so an enumeration here would only go stale as that catalogue grows. For figure_type='concept': the composition \u2014 what appears where, colours, labels, and what to leave out.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "aspect_ratio": {
          "default": "21:9",
          "description": "Shape of the figure. '21:9' for architecture diagrams / pipelines / flow charts (the paper's hero diagram is usually one of these), '16:9' for side-by-side comparisons and multi-panel results, '4:3' for dense charts, '1:1' for heatmaps / confusion matrices / scatter plots, '3:4' or '9:16' for vertical layouts.",
          "enum": [
            "1:1",
            "4:3",
            "3:2",
            "16:9",
            "21:9",
            "3:4",
            "9:16"
          ],
          "title": "Aspect Ratio",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "figure_type",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-09-20 00:28:23 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-09-20 00:29:43 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: "Writes the PROSE of an AI research paper: abstract, introduction, related work, methods, experiments, discussion and conclusion, with a page budget, the 5-paragraph intro pattern, writing-quality rules, inline [FIGURE:fig_id] markers plus a structured figures array, and a MANDATORY REVISION_CHECKLIST.md pass over every finished draft. Use whenever a paper, abstract, section, or full write-up is being drafted or rewritten for a venue such as NeurIPS, ICML, ICLR or ACL. Triggers: write a paper, paper structure, abstract, introduction, related work, methods, experiments, contributions, figure caption and placement, revision pass, academic prose. NOT for: assembling or compiling .tex (use aii-paper-to-latex), rendering the figure image files (aii-data-fig-gen, aii-concept-fig-gen), fetching BibTeX (use aii-semscholar-bib), or critiquing a finished draft's logic (use amg-paper-verification)."
---

## MANDATORY: the final revision pass

**`REVISION_CHECKLIST.md`, in this skill's own directory, MUST be read and
applied to every finished draft, always, as a separate pass after the writing
is done.** It is not optional, not conditional on how the draft looks, and not
something to fold into the writing itself.

Writing and revising are different jobs and cannot be done in one pass. The
defects that checklist targets — dense prose, a number-dumped abstract, sections
that leak into each other, a Figure 1 that shows a side result, prior work the
final vocabulary would have found, results mentioned but never plotted,
inconsistencies between abstract and tables — are all invisible while drafting,
because the author is holding the intent rather than the text. Every one of them
is obvious to the first outside reader. Reading the checklist before writing
does not substitute: the pass has to run against a finished draft.

So the order is always: write the complete draft → read `REVISION_CHECKLIST.md`
→ work its items against the full text, fixing as you go → only then emit the
output.

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-web-tools · 2026-09-20 00:29:53 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Runs web search, page fetch as markdown, and regex grep over full HTML or PDF text via this skill's own scripts (aii_fast_web_search.py, aii_fast_web_fetch.py) — a free-first keyless search stack with Serper fallback that works even where built-in WebSearch and WebFetch are absent. Use when a query, page, or paper must be searched, read, or mined for an exact quote, number, table value, or methodology sentence, and whenever a lossy summary would lose the detail. Triggers: web search, scholarly search, OpenAlex, Crossref, Serper, fetch a URL as markdown, read a PDF, arXiv, regex grep a page, exact quote, table value, citation check. NOT for: planning a broad multi-source literature review or mass verification campaign — use aii-web-research-tools; NOT for a PDF file already on disk — extraction, form filling, merging and PDF creation are anthropic-pdf; NOT for driving a browser or testing a UI."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — free-first web search (keyless general/scholarly engines,
   Serper fallback), html2text + PyMuPDF for fetch, and regex grep over the full
   document text. They work without any built-in web tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (free-first: general or scholarly)

```bash
# general web (default): keyless engines (ddgs, marginalia); Serper only if they miss
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
# scholarly mode: OpenAlex + Crossref (DOIs, citation counts)
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation" --mode scholarly
```

Returns ranked title / URL / snippet lines. `--mode general` (default) uses
keyless general engines; `--mode scholarly` uses academic APIs. Both fall back
to Serper (paid) only when the free engines miss. Use search first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [5] SKILL-INPUT — aii-semscholar-bib · 2026-09-20 00:30:01 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: "Fetches real BibTeX entries in one batch from Semantic Scholar by DOI, ArXiv ID or title via aii_semscholar_bib__fetch, normalises citation keys to AuthorYYYY, injects DOIs, and writes the result into references.bib, with a mandatory web-search fallback for anything not found. ALWAYS use whenever a bibliography, reference list or .bib file is being built or extended, and whenever a citation needs a verified entry instead of an invented one — never hand-write BibTeX first. Triggers: bibliography, references.bib, bibtex, citation key, DOI, arXiv id, Semantic Scholar, reference list, cite these papers, natbib entries. NOT for: writing the text around the citations (use aii-paper-writing), running bibtex and compiling (use aii-paper-to-latex), judging whether cited work supports the claims (use amg-paper-verification), or open-ended literature search and PDF mining (use aii-web-tools)."
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SYSTEM-USER prompt · 2026-09-20 00:58:58 UTC

````
YOUR PREVIOUS SESSION WAS INTERRUPTED: A single operation exceeded the 1800s message timeout. Each individual operation must complete within 1800s. Do NOT mock, skip, or compromise your execution — still do the real work. Try to make operations run faster if possible. If a command genuinely takes longer than 1800s, split it into sequential parts that each complete within the time limit.

Last messages before interruption:
  - [agent_think]: Now I need to move the method detail from the Introduction to the Method section, leaving only a forward reference.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md",
  "file_text": null,
  "old_str": "We propose Self-Surprisal Hard Prompt Compression (SSHPC). For each token in the prompt, we
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
The file /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md has been edited. Here's the result of running `cat -n` on a snippet of /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_tex
  - [agent_think]: Now let me check the rest of the paper for any issues with numbers consistency, nonreferential "this/that", etc. Let me also verify the numbers match between the text and the figure specs.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": [
    135,
    180
  ]
}
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md:
   135	### 4.4 Ablation Studies
   136	
   137	1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target a
  - [agent_think]: Let me check the numbers in the Results section against the figure specs to ensure consistency.

From fig1_main_results_spec.json (fig2_main in my paper):
- GSM8K: SSHPC Iterative at 8x = 72.89999999999999 ≈ 72.9%, at 10x = 71.09 ≈ 71.1%
- HotpotQA: SSHPC Iterative at 8x = 62.53999999999999 ≈ 62.5%,
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": [
    180,
    230
  ]
}
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
NOTE: We only show up to 221 since there're only 221 lines in this file.
Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md:
   180	[ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:ar
  - [agent_think]: Now let me do the consistency passes. Let me check a few things:

1. Numbers in text vs figures - need to verify they match
2. Figure references - make sure they're correct
3. Nonreferential "this/that" - check
4. Tense consistency - should be past tense for what we did
5. Cross-references - Section
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md",
  "file_text": null,
  "old_str": "**Synthetic surprisal distributions**: The surprisal distribution in Figure 5 is synthetic 
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
The file /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md has been edited. Here's the result of running `cat -n` on a snippet of /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_tex
  - [agent_think]: Now let me check the consistency of numbers across the paper. Let me verify the numbers match between the text and the figure specs
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": [
    144,
    180
  ]
}
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md:
   144	### 5.1 Main Results
   145	
   146	Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks a
  - [agent_think]: Let me check the paper for non-referential "this/that/these/it" and other issues. Let me also verify that all figure references match the figures array in paper_text.json. I notice:

- Figure 2 in text = fig2_main in JSON ✓
- Figure 3 in text = fig3_proxy in JSON ✓
- Figure 4 in text = fig4_iterativ
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "grep -n \"\\bthis\\b\\|\\bthat\\b\\|\\bthese\\b\\|\\bthose\\b\" /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md | head -30",
  "is_input": false,
  "timeout": null,
  "reset": false
}
  - [agent_tool_result] terminal: Tool: terminal
Result:
5:Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading
  - [agent_think]: Let me check if any of these "this" instances are non-referential (i.e., don't have a clear antecedent). Looking at the results:

- Line 5: "This creates a proxy-model mismatch" - "This" refers to "proxy model's predictions differ from target LLM's" - OK
- Line 9: "This increase in length" - "This" 
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "grep -n \"etc\\.\\|for various reasons\" /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/paper_draft.md",
  "is_input": false,
  "timeout": null,
  "reset": false
}

CONTINUE FOLLOWING THESE INSTRUCTIONS:

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>
<writing_register>
Write in the register of the field's best papers (the passages you collect in the STYLE EXEMPLARS todo), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

# Self-Surprisal Hard Prompt Compression

## Abstract

Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a fundamental proxy-model mismatch: the proxy's predictions do not match the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal — the negative log-likelihood of each token given its preceding context — and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We describe the algorithm, analyze its theoretical basis, and outline an evaluation on four long-context benchmarks across three open-weight LLMs at compression ratios from 2x to 10x.

## 1 Introduction

Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increases inference latency, memory consumption, and API costs proportionally to sequence length.

Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

We propose Self-Surprisal Hard Prompt Compression (SSHPC). For each token in the prompt, we compute its surprisal under the target LLM's own next-token prediction distribution: the negative log probability of the token given all preceding tokens. Tokens the model predicts confidently (low surprisal) are self-redundant for that model; tokens that violate its predictions (high surprisal) carry new information. We prune the lowest-surprisal tokens to meet a target compression ratio. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

Our contributions are:

1. **Algorithm**: A single-pass hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications (Section 3).
2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
3. **Evaluation design**: A comprehensive benchmark plan across four long-context datasets (LongBench, NaturalQuestions, GSM8K, HotpotQA), three target LLMs (Llama-3-8B, Qwen2-7B, Mistral-7B), and compression ratios from 2x to 10x, with ablations isolating the proxy-mismatch effect (Section 4).

[FIGURE:fig1]

## 2 Related Work

### Hard Prompt Compression via Proxy Models

LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

### Soft Prompt Compression

GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

### Theoretical Frameworks

Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

## 3 Method

### 3.1 Self-Surprisal Hard Prompt Compression

Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

$$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

**Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step. We optionally preserve special tokens (e.g., `<bos>`, `<eos>`, instruction delimiters) by assigning them infinite surprisal.

**Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for QA/RAG prompts structured as (context, question), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{question})$, so context tokens are scored by how surprising they are given the question. This aligns with LongLLMLingua's finding that question-awareness improves compression.

[FIGURE:fig2]

### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

### 3.3 Computational Considerations

SSHPC requires one forward pass over the full prompt. For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. The latency overhead is approximately one generation step per $N$ tokens (batched). For $N=4096$ on Llama-3-8B, this is $\sim$50ms on an A100 — comparable to or less than the inference time saved by compressing the prompt for the downstream task.

At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

[FIGURE:fig3]

## 4 Experimental Design

### 4.1 Datasets and Tasks

We evaluate on four benchmarks covering diverse long-context tasks:

- **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens.
- **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA. We use the multi-document setting with 10 retrieved documents per question.
- **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure.
- **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies.

### 4.2 Target Models and Baselines

**Target LLMs** (all open-weight, local inference):
- Llama-3-8B-Instruct
- Qwen2-7B-Instruct
- Mistral-7B-Instruct-v0.3

**Baselines**:
1. **No compression** (full prompt)
2. **Random pruning**: uniform random token removal
3. **SelectiveContext** (Li, 2023): self-information from LLaMA-7B proxy
4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
6. **SelfCP** (Gao et al., 2024): soft prompt compression using target LLM (where applicable)

**Ablation baselines**:
7. **Proxy-on-target ablation**: Run LLMLingua/SelectiveContext using the *same* target LLM as the proxy (i.e., Llama-3-8B scoring for Llama-3-8B target). This ablation isolates the proxy-mismatch effect.

### 4.3 Compression Ratios and Metrics

Compression ratios: 2x, 4x, 8x, 10x (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

**Primary metrics**:
- Task accuracy (Exact Match for GSM8K, F1/EM for QA, ROUGE-L for summarization)
- Hallucination rate (for QA: fraction of answers containing unsupported claims)
- End-to-end latency (compression + generation) on A100-40GB

**Secondary metrics**:
- Compression throughput (tokens/sec for the compression step alone)
- Surprisal distribution statistics (mean, variance, skew)

### 4.4 Ablation Studies

1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the *target's own* distribution.
2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
3. **Single-pass vs. iterative**: After initial SSHPC compression, recompute surprisal on the compressed prompt and prune again. Test if iterative refinement helps at 8x–10x ratios.
4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning (keep tokens with $s_i > \tau$) against fixed-ratio top-k.

[FIGURE:fig4]

## 5 Discussion

### 5.1 Expected Outcomes

We hypothesize that SSHPC will match or exceed LLMLingua-2 accuracy at equal or higher compression ratios on at least three of four benchmarks. At high compression (8x+), the proxy-mismatch effect should become pronounced, yielding $\ge 2\%$ absolute accuracy gains over proxy baselines. The Proxy-on-target ablation should confirm that self-surprisal outperforms proxy perplexity even when the proxy *is* the target model, because proxy methods compute perplexity on the *original* context while SSHPC's surprisal is inherently conditioned on the same context the target will see.

### 5.2 Limitations

**Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (e.g., OpenAI's `logprobs` parameter), but not all. For fully black-box APIs, proxy methods remain the only option.

**Single-pass context dependence**: Surprisal is computed on the original full prompt. After pruning, the context for each retained token changes, potentially altering its true importance. The iterative ablation (Section 4.4) addresses this.

**First-token handling**: The first token has no preceding context. The method uses the unconditional distribution, which may not reflect its true importance in the full prompt. An alternative would score it using a bidirectional model's pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy.

**No query in unconditional variant**: For prompts without a clear question (e.g., summarization, chat), query-conditioned SSHPC does not apply. The unconditional variant may retain tokens that are predictable globally but surprising for the specific task.

### 5.3 Broader Implications

If self-surprisal proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression — no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error. SSHPC operationalizes this principle for hard token pruning.

## 6 Conclusion

We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation design tests SSHPC across diverse long-context tasks, target models, and compression ratios, with ablations that isolate the proxy-mismatch effect. If confirmed, SSHPC would establish self-surprisal as the canonical importance signal for hard prompt compression on open-weight LLMs.

---

## Bibliography

[1] Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 13358–13376, 2023.

[2] Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1658–1677, 2024.

[3] Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, H. V. Zhao, Lili Qiu, and Dongmei Zhang. LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression. In *Findings of the Association for Computational Linguistics: ACL 2024*, pages 963–981, 2024.

[4] Yucheng Li. Unlocking Context Constraints of LLMs: Enhancing Context Efficiency of LLMs with Self-Information-Based Content Filtering. *ArXiv preprint*, abs/2304.12102, 2023.

[5] Jun Gao, Ziqiang Cao, and Wenjie Li. SelfCP: Compressing over-limit prompt via the frozen large language model itself. *Information Processing & Management*, 61:103873, 2024.

[6] Alliot Nagle, Adway Girish, Marco Bondaschi, Michael Gastpar, A. V. Makkuva, and Hyeji Kim. Fundamental Limits of Prompt Compression: A Rate-Distortion Framework for Black-Box Language Models. In *Advances in Neural Information Processing Systems 37*, 2024.

[7] Zong-Qian Li, Yinhong Liu, Yixuan Su, and Nigel Collier. Prompt Compression for Large Language Models: A Survey. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 7182–7195, 2024.

[8] Karl Friston. The free-energy principle: a rough guide to the brain? *Philosophical Transactions of the Royal Society B: Biological Sciences*, 364:1211–1221, 2009.

[9] Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. Adapting language models to compress contexts. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 3829–3846, 2023.

[10] Tao Ge, Jing Hu, Xun Wang, Si-Qing Chen, and Furu Wei. In-context autoencoder for context compression in a large language model. In *Proceedings of the Twelfth International Conference on Learning Representations*, 2023.

[11] Jesse Mu, Xiang Lisa Li, and Noah Goodman. Learning to compress prompts with gist tokens. In *Proceedings of the Eleventh International Conference on Learning Representations*, 2023.

[12] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics*, 12:157–173, 2024.

[13] Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, et al. Longbench: A bilingual, multitask benchmark for long context understanding. *ArXiv preprint*, abs/2308.14508, 2023.

[14] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural Questions: A Benchmark for Question Answering Research. *Transactions of the Association for Computational Linguistics*, 7:452–466, 2019.

[15] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training Verifiers to Solve Math Word Problems. *ArXiv preprint*, abs/2110.14168, 2021.

[16] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering. In *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing*, 2018.

[17] Shannon, C. E. Prediction and entropy of printed English. *Bell System Technical Journal*, 30:50–64, 1951.

[18] Salazar, J., Liang, D., Nguyen, T. Q., & Kirchhoff, K. (2020). Masked language model scoring. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 2699–2712.
</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (scope) The paper does not answer the user's original request. The request was: 'Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.' This paper proposes a NOVEL method (SSHPC) with an evaluation design — it is not a survey. Coverage is 'lost'.
  Action: Either (a) rewrite as a survey paper covering the 6+ methods documented in the research artifacts (SelectiveContext, LLMLingua, LLMLingua-2, SelfCP, ASAP, PIS, etc.) with implementation details and comparison tables, or (b) acknowledge this is a different research direction and the survey was a separate deliverable.
- [MAJOR] (evidence) No experimental results are reported. The paper describes an 'evaluation design' and 'expected outcomes' but every quantitative claim is projected/placeholder. The abstract says 'We describe the algorithm, analyze its theoretical basis, and outline an evaluation' — this is accurate but makes it a proposal, not a completed study. Results_reported = false.
  Action: Execute the full experimental plan. At minimum, run a subset (1-2 datasets, 1-2 models, key baselines) to have ANY empirical evidence before submission. Without results, this cannot be accepted at a top-tier venue.
- [MAJOR] (methodology) The single-pass context dependence problem is fundamental: surprisal is computed on the FULL prompt, but after pruning, the context for each retained token changes. The paper acknowledges this and proposes an iterative ablation, but doesn't commit to it as the main method. At high compression ratios (8x-10x), this could significantly degrade performance because the model's predictions on the compressed prompt will differ from its predictions on the original.
  Action: Make iterative re-scoring the default for high compression ratios (>=8x), or provide a theoretical bound on how much surprisal rankings can change after pruning. Alternatively, use a bidirectional model's pseudo-log-likelihood (Salazar et al. 2020) for more context-independent scores, though this reintroduces a proxy.
- [MAJOR] (methodology) Computational overhead is underestimated for practical deployment. A full forward pass on the target LLM (e.g., Llama-3-8B) over 4096 tokens is NOT ~50ms on A100 — that's closer to a single generation step for SHORT sequences. For a 4096-token prompt, the prefill latency is substantial (hundreds of ms). The paper must measure actual prefill time vs. generation savings.
  Action: Measure and report actual compression latency (prefill time for the full prompt) vs. generation time saved. Compare against the proxy-model approaches (which use much smaller models for scoring). If SSHPC's overhead exceeds savings at low compression ratios, state the break-even point clearly.
- [MAJOR] (novelty) The novelty claim is overstated. SelfCP (Gao et al. 2024) already uses 'the target LLM itself' for compression. The difference is soft vs. hard tokens, but the core insight — the target model's own representations are the right importance signal — is shared. Nagle et al. (2024) formalize prompt compression as rate-distortion and imply the optimal compressor is the decoder's own prediction error. The paper should position SSHPC as 'hard-token operationalization of the SelfCP/rate-distortion principle' rather than a wholly new idea.
  Action: Reframe the contribution: 'We show that the target model's own next-token surprisal — a signal already implicit in SelfCP's compressor and Nagle et al.'s rate-distortion framework — yields an effective training-free HARD compression method.' Cite Nagle et al. 2024 more centrally as theoretical precedent.
- [MINOR] (rigor) The first-token handling is a gap: x_1 uses the unconditional distribution, which doesn't reflect its importance in context. The paper mentions Salazar et al. (2020) masked LM scoring as an alternative but dismisses it as 'reintroducing a proxy'. This is a real issue for prompts where the first tokens are critical (e.g., instruction tokens).
  Action: Either: (a) always preserve special/instruction tokens (assign infinite surprisal), (b) use a sliding window where each token is scored with a fixed context window behind it, or (c) implement and test the bidirectional pseudo-log-likelihood approach. Report what works.
- [MINOR] (clarity) The query-conditioned variant is only defined for QA/RAG prompts with a clear question. For summarization, chat, or open-ended prompts, there's no 'question' to condition on. The paper doesn't address how to handle these common cases.
  Action: Define a general conditioning mechanism: for any prompt, identify the 'query' or 'task specification' portion (e.g., the last user message in chat, the instruction in summarization) and condition on that. Or provide a heuristic for automatic query extraction.
- [MINOR] (rigor) The proxy-on-target ablation (running LLMLingua/SelectiveContext with the target LLM as proxy) is a great design but the paper predicts SSHPC will outperform it 'because proxy methods compute perplexity on the original context while SSHPC's surprisal is inherently conditioned on the same context the target will see.' This reasoning needs verification — both methods score on the original context. The difference is perplexity vs. surprisal and iterative vs. single-pass.
  Action: Clarify the theoretical distinction. Perplexity = exp(avg surprisal) over a segment; SSHPC uses pointwise surprisal. The key difference may be granularity (token vs. segment) and the lack of iterative conditioning in SSHPC. Test both.
- [MINOR] (evidence) The paper cites Nagle et al. (2024) as 'NeurIPS 2024' but the paper appears to be from NeurIPS 2024 (published Dec 2024). The citation format should be consistent — use the proceedings citation if available, or arXiv with the correct year.
  Action: Verify all citations are accurate and complete. The Nagle et al. paper is arXiv:2407.15504 / NeurIPS 2024. Ensure the bibliography entry matches the venue.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<results_status>
This iteration executed at least one EXPERIMENT/EVALUATION/PROOF with real output: gen_art_experiment_1, gen_art_evaluation_1.
You may cite their concrete findings.
</results_status>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

kind: hypothesis
title: Self-Surprisal Hard Prompt Compression
hypothesis: >-
  A target LLM's own next-token prediction surprisal (negative log-likelihood) on its input prompt provides a more accurate
  importance signal for hard token pruning than any proxy model's perplexity, because it directly measures what the target
  model itself finds predictable versus surprising — eliminating the proxy-model mismatch that plagues current methods like
  LLMLingua and SelectiveContext. SSHPC uses iterative re-scoring at high compression ratios (>=8x) where single-pass context
  dependence degrades rankings, preserves special/instruction tokens by assigning infinite surprisal, generalizes query-conditioning
  to arbitrary task specifications (last user message, instruction prefix), and measures actual prefill latency against generation
  savings to establish a break-even compression ratio. This operationalizes the rate-distortion principle (Nagle et al., 2024)
  and SelfCP's target-model compressor insight as a training-free hard-pruning method.
motivation: >-
  All existing hard prompt compression methods (LLMLingua, LongLLMLingua, LLMLingua-2, SelectiveContext, ProCut) rely on a
  smaller proxy model (GPT-2, BERT, or fine-tuned small LM) to score token importance via perplexity or self-information.
  This creates a fundamental proxy-model mismatch: the proxy's predictions don't match the target LLM's, leading to suboptimal
  pruning. Meanwhile, soft prompt methods (SelfCP, ICAE, GIST) use the target LLM but produce dense vectors requiring learnable
  connectors and training. No method uses the target LLM's own next-token logits to directly compute per-token surprisal for
  hard token pruning. Predictive coding theory from neuroscience suggests that only 'surprising' inputs (high prediction error)
  carry new information for a predictive system; tokens the model predicts well are self-redundant. This hypothesis bridges
  that gap.
assumptions:
- >-
  Target LLM exposes next-token logits/probabilities for prompt tokens (available for local models via HuggingFace, some APIs)
- >-
  Surprisal computed as -log P(token | preceding context) under the target LLM's own distribution correlates with token importance
  for that model's generation
- >-
  Low-surprisal tokens are genuinely self-redundant for the target model (not just predictable in general)
- >-
  Hard token pruning based on self-surprisal preserves task performance better than proxy-model perplexity at equal compression
  ratios
- >-
  Single forward pass to compute all token surprisals is computationally feasible within budget
investigation_approach: >-
  1. Implement Self-Surprisal Hard Prompt Compression (SSHPC): for each prompt token, compute -log P(token | preceding context)
  using target LLM's forward pass; prune lowest-surprisal tokens to target compression ratio. 2. Compare against LLMLingua,
  LLMLingua-2, SelectiveContext, and random pruning baselines on LongBench, NaturalQuestions, GSM8K, and HotpotQA. 3. Test
  across multiple target LLMs (Llama-3-8B, Qwen2-7B, Mistral-7B) and compression ratios (2x, 4x, 8x, 10x). 4. Measure task
  accuracy, hallucination rate, and inference latency. 5. Ablate: compare self-surprisal vs. proxy-model perplexity on same
  target LLM to isolate proxy-mismatch effect.
success_criteria: >-
  CONFIRMED if: (a) SSHPC matches or exceeds LLMLingua-2 task accuracy at equal/higher compression ratios on >=3/4 benchmarks;
  (b) SSHPC outperforms proxy-model baselines by >=2% absolute accuracy at high compression (8x+); (c) Ablation shows proxy-model
  perplexity on same target LLM degrades vs self-surprisal, confirming proxy-mismatch as key factor. DISCONFIRMED if: SSHPC
  consistently underperforms proxy baselines, or self-surprisal correlates poorly with actual token importance measured via
  leave-one-out ablation.
related_works:
- >-
  LLMLingua (Jiang et al., 2023): Uses GPT-2/small LM perplexity for token pruning — proxy model mismatch is core limitation
- >-
  LongLLMLingua (Jiang et al., 2024): Extends LLMLingua with question-aware compression — still uses proxy model
- >-
  LLMLingua-2 (Pan et al., 2024): Data distillation + classifier on small encoder — still proxy-based
- >-
  SelectiveContext (Li et al., 2023): Uses small LM self-information — proxy mismatch
- >-
  SelfCP (Gao et al., 2024): Uses target LLM but produces soft tokens (dense memory tokens), requires learnable connector
  + training — not hard pruning
- >-
  ASAP/Pruning the Unsurprising (Zeng et al., 2025): Uses first-token surprisal for CoT step pruning + fine-tuning — not general
  hard prompt token pruning
- >-
  PIS (Chen et al., 2025): Uses attention scores for importance sampling — not next-token prediction logits
- >-
  Fundamental Limits of Prompt Compression (Nagle et al., 2024): Rate-distortion framework — theoretical baseline, no self-surprisal
  method
inspiration: >-
  Cross-domain transfer from neuroscience (predictive coding / Free Energy Principle) and information theory (rate-distortion).
  Predictive coding posits the brain minimizes surprisal by predicting next inputs; only prediction errors (high surprisal)
  propagate up the hierarchy — predictable inputs are 'explained away' as redundant. Applied to LLMs: tokens the target model
  predicts well from context carry little new information for its own generation. This is a Level 3 methodological transfer
  — importing the concrete mechanism of surprisal-based filtering from predictive coding directly as a hard prompt compression
  algorithm.
terms:
- term: Surprisal (Self-Information)
  definition: >-
    Negative log-likelihood of a token under the model's next-token prediction distribution: -log P(token | preceding context).
    Measures how 'surprised' the model is by that token given its context.
- term: Proxy-Model Mismatch
  definition: >-
    The gap between a smaller proxy model's (e.g., GPT-2) token importance scores and the target LLM's (e.g., Llama-3-8B)
    actual sensitivity to those tokens, causing suboptimal pruning decisions.
- term: Hard Prompt Compression
  definition: >-
    Removing discrete tokens from the original natural language prompt while keeping remaining tokens unchanged — as opposed
    to soft prompt compression which produces continuous dense vectors.
- term: Predictive Coding
  definition: >-
    Neuroscience theory where hierarchical neural systems minimize free energy by predicting incoming sensory inputs; only
    prediction errors (surprisal) are forwarded, making predictable inputs informationally redundant for that system.
- term: Rate-Distortion Theory
  definition: >-
    Information-theoretic framework characterizing the fundamental trade-off between compression rate (bits) and distortion
    (fidelity loss) for a given source and distortion measure.
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token prediction logits to compute per-token
  surprisal on the input prompt, then prunes the most predictable (lowest surprisal) tokens. This eliminates the proxy-model
  mismatch that limits LLMLingua, SelectiveContext, and LLMLingua-2, while avoiding the training overhead and soft-token complexity
  of methods like SelfCP. Grounded in predictive coding theory from neuroscience.
alternates:
- title: Query-Conditioned Self-Surprisal
  hypothesis: >-
    Computing token surprisal conditioned on the query/task (P(token | context + query)) rather than context alone yields
    better pruning for query-aware tasks like QA and RAG, because it captures what's surprising specifically for the downstream
    task.
  why_it_could_win: >-
    If query-specific information is the primary driver of token importance (as LongLLMLingua's question-aware compression
    shows), conditioning surprisal on the query could outperform unconditional self-surprisal, especially for RAG and multi-document
    QA where most context is irrelevant to the query.
- title: Attention-Weighted Self-Surprisal
  hypothesis: >-
    Weighting each token's self-surprisal by its attention mass (how much subsequent tokens attend to it) produces a more
    accurate importance score than raw surprisal alone, because it captures both self-predictability and causal influence
    on generation.
  why_it_could_win: >-
    If some low-surprisal tokens are causally critical (e.g., rare but pivotal keywords that subsequent tokens heavily attend
    to), pure surprisal would incorrectly prune them. Attention-weighting corrects this by incorporating the target LLM's
    own causal dependency structure.
- title: Iterative Self-Surprisal Refinement
  hypothesis: >-
    Iteratively recomputing self-surprisal after each pruning round (since context changes) yields better compression than
    single-pass scoring, because token predictability shifts as surrounding tokens are removed.
  why_it_could_win: >-
    If token surprisal is highly context-dependent (as LLMLingua's iterative compression suggests), single-pass scoring based
    on the original context becomes stale. Iterative recomputation adapts to the evolving compressed context, potentially
    enabling higher compression ratios with less performance loss.
_relation_rationale: >-
  Refines methodology while keeping SSHPC core claim; addresses reviewer's experimental defects.
_confidence_delta: decreased
_key_changes:
- >-
  Added iterative re-scoring as default for compression >=8x to fix single-pass context dependence
- >-
  Special/instruction tokens preserved by infinite surprisal assignment (fixes first-token gap)
- >-
  Query-conditioning generalized to any task specification (last user message, instruction prefix)
- >-
  Explicit latency measurement: prefill time vs. generation savings to find break-even ratio
- >-
  Novelty reframed: hard-token operationalization of SelfCP/rate-distortion principle, not wholly new idea
- >-
  Proxy-on-target ablation clarified: granularity (token vs segment) and iterative conditioning are key differences
- >-
  Removed projected numbers; success criteria now tied to actual experimental execution
_evidence_state: experiment_broken
_move: fix
_move_rationale: >-
  No experiments ran; all quantitative claims are projected placeholders. The test never tested the claim. Next iteration
  must execute the experimental plan with the methodological fixes above.
_coverage: lost
_coverage_statement: >-
  The user asked for a survey of simple prompt-compression techniques; this hypothesis proposes a novel method instead. The
  next iteration must either pivot to a survey deliverable or acknowledge SSHPC as a separate research direction.
_candidates_considered: 1
relation_type: evolution
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 3 research artifacts across all iterations.

--- Item 1 ---
id: art_-Hzqeq6rV9vC
type: dataset
title: Prompt Compression Benchmark Datasets
summary: >-
  This artifact provides 9 benchmark datasets (33,790 examples) standardized for prompt compression evaluation. Datasets span
  7 task types: math reasoning (GSM8K), multi-hop QA (HotpotQA, MuSiQue), extractive QA (SQuAD), reading comprehension (ROPES),
  summarization (ArXiv, GovReport), long-document QA (NarrativeQA), and open-domain QA (TriviaQA). Each example contains:
  input (prompt with context), output (expected answer), and metadata (task_type, split, row_index). Data is grouped by dataset
  in exp_sel_data_out schema format. Full data split into 2 parts (90MB + 65MB) to stay under 100MB limit. Mini (27 examples)
  and preview (27 truncated examples) variants included for quick inspection.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_pWnUR-sCdAoE
type: experiment
title: SSHPC vs Proxy-Model Compression Benchmark
summary: >-
  This artifact implements the SSHPC (Self-Surprisal Hard Prompt Compression) methodology and compares it against multiple
  baseline compression methods (LLMLingua, SelectiveContext, Random, ProxyOnTarget, None) across GSM8K dataset using GPT-2
  as the proxy model. The implementation computes per-token surprisal values from the model's own next-token logits, ranks
  tokens by surprisal, and prunes the lowest-surprisal tokens to achieve target compression ratios (2x, 4x, 8x, 10x). All
  methods are evaluated on task accuracy (pass@1 for GSM8K) and latency (prefill and generation time). Output follows the
  exp_gen_sol_out.json schema with 50 examples across 1 dataset.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 3 ---
id: art_Lm_O96s-n8rb
type: evaluation
title: SSHPC Statistical Evaluation & Publication Figures
summary: |-
  This evaluation artifact implements comprehensive statistical analysis of the SSHPC (Self-Surprisal Hard Prompt Compression) experiment results. It computes:

  1. **Bootstrap CIs (10k resamples)**: Mean task accuracy ± 95% CI per method/dataset/compression ratio across 4 benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) and 6 methods (SSHPC Base, SSHPC Iterative, LLMLingua, SelectiveContext, Random Pruning, No Compression) at 4 compression ratios (2x, 4x, 8x, 10x).

  2. **Paired bootstrap tests**: SSHPC vs each baseline at every compression ratio, with p-values and significance flags (p<0.05, p<0.01).

  3. **Proxy-mismatch ablation**: Direct comparison of SSHPC vs Proxy-on-Target (LLMLingua using target LLM as proxy) on the same target LLM, quantifying the core hypothesis that target-model surprisal beats proxy-model perplexity. Effect size: 0.48% average improvement (not statistically significant, p>0.05).

  4. **Iterative re-scoring benefit**: Single-pass vs iterative SSHPC at 8x/10x compression. Iterative helps significantly on GSM8K (+3.8%, p=0.0001) and HotpotQA (+2.3%, p=0.04) at 8x.

  5. **Latency break-even**: End-to-end latency vs compression ratio for all methods. Break-even at 2x for all methods (compression overhead < generation time savings).

  6. **Surprisal distribution**: Per-token surprisal distributions across datasets (synthetic for demonstration).

  All results are output in eval_out.json validated against the exp_eval_sol_out schema (PASSED with warnings for missing predict_*/eval_* fields in statistical analysis datasets). Six publication-ready figures generated via aii-data-fig-gen: panel bar charts, forest plot, dumbbell chart, line chart, violin plot, and grouped bar chart - each as vector PDF and PNG.

  Key conclusion: Hypothesis status PARTIAL - iterative re-scoring benefit confirmed at high compression, but proxy-mismatch effect not statistically confirmed with synthetic data. SSHPC outperforms baselines by ~5.8% at 8x compression.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 3 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

type: dataset
title: Prompt Compression Benchmark Datasets
id: art_-Hzqeq6rV9vC
summary: >-
  This artifact provides 9 benchmark datasets (33,790 examples) standardized for prompt compression evaluation. Datasets span
  7 task types: math reasoning (GSM8K), multi-hop QA (HotpotQA, MuSiQue), extractive QA (SQuAD), reading comprehension (ROPES),
  summarization (ArXiv, GovReport), long-document QA (NarrativeQA), and open-domain QA (TriviaQA). Each example contains:
  input (prompt with context), output (expected answer), and metadata (task_type, split, row_index). Data is grouped by dataset
  in exp_sel_data_out schema format. Full data split into 2 parts (90MB + 65MB) to stay under 100MB limit. Mini (27 examples)
  and preview (27 truncated examples) variants included for quick inspection.

type: experiment
title: SSHPC vs Proxy-Model Compression Benchmark
id: art_pWnUR-sCdAoE
summary: >-
  This artifact implements the SSHPC (Self-Surprisal Hard Prompt Compression) methodology and compares it against multiple
  baseline compression methods (LLMLingua, SelectiveContext, Random, ProxyOnTarget, None) across GSM8K dataset using GPT-2
  as the proxy model. The implementation computes per-token surprisal values from the model's own next-token logits, ranks
  tokens by surprisal, and prunes the lowest-surprisal tokens to achieve target compression ratios (2x, 4x, 8x, 10x). All
  methods are evaluated on task accuracy (pass@1 for GSM8K) and latency (prefill and generation time). Output follows the
  exp_gen_sol_out.json schema with 50 examples across 1 dataset.

type: evaluation
title: SSHPC Statistical Evaluation & Publication Figures
id: art_Lm_O96s-n8rb
summary: |-
  This evaluation artifact implements comprehensive statistical analysis of the SSHPC (Self-Surprisal Hard Prompt Compression) experiment results. It computes:

  1. **Bootstrap CIs (10k resamples)**: Mean task accuracy ± 95% CI per method/dataset/compression ratio across 4 benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) and 6 methods (SSHPC Base, SSHPC Iterative, LLMLingua, SelectiveContext, Random Pruning, No Compression) at 4 compression ratios (2x, 4x, 8x, 10x).

  2. **Paired bootstrap tests**: SSHPC vs each baseline at every compression ratio, with p-values and significance flags (p<0.05, p<0.01).

  3. **Proxy-mismatch ablation**: Direct comparison of SSHPC vs Proxy-on-Target (LLMLingua using target LLM as proxy) on the same target LLM, quantifying the core hypothesis that target-model surprisal beats proxy-model perplexity. Effect size: 0.48% average improvement (not statistically significant, p>0.05).

  4. **Iterative re-scoring benefit**: Single-pass vs iterative SSHPC at 8x/10x compression. Iterative helps significantly on GSM8K (+3.8%, p=0.0001) and HotpotQA (+2.3%, p=0.04) at 8x.

  5. **Latency break-even**: End-to-end latency vs compression ratio for all methods. Break-even at 2x for all methods (compression overhead < generation time savings).

  6. **Surprisal distribution**: Per-token surprisal distributions across datasets (synthetic for demonstration).

  All results are output in eval_out.json validated against the exp_eval_sol_out schema (PASSED with warnings for missing predict_*/eval_* fields in statistical analysis datasets). Six publication-ready figures generated via aii-data-fig-gen: panel bar charts, forest plot, dumbbell chart, line chart, violin plot, and grouped bar chart - each as vector PDF and PNG.

  Key conclusion: Hypothesis status PARTIAL - iterative re-scoring benefit confirmed at high compression, but proxy-mismatch effect not statistically confirmed with synthetic data. SSHPC outperforms baselines by ~5.8% at 8x compression.
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

FIGURE TYPE — set `figure_type` on every figure. One test decides it: does the figure plot numbers?
  "data"    — a DATA FIGURE: bars, curves, scatter, heatmaps, confusion matrices, scaling
              laws, distributions, Pareto fronts, ablation deltas. Rendered deterministically
              from the values you supply, so every bar is exactly the height of its number.
  "concept" — a CONCEPT FIGURE: conceptual artwork, architecture and flow diagrams, anything
              with no underlying dataset. Drawn by an image model.
If the figure has real numbers behind it, ALWAYS use "data". An image model only approximates
values: the bars come back close to, but not equal to, the numbers you asked for, and nothing
downstream detects it.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison — plots numbers, so a data figure):
  {"id": "fig3", "title": "Performance Comparison", "figure_type": "data", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. Categories: PostgreSQL, Bao, RLQOpt. One series 'Latency'. Values: 4.6, 2.8, 2.0 seconds. Errors: 0.8, 0.5, 0.3. X-axis label 'Optimizer'. Y-axis label 'Latency (s)', range 0-5.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero — no dataset, so a concept figure):
  {"id": "fig1", "title": "System Architecture", "figure_type": "concept", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description. For a "data" figure, list the values per series
plus the axis labels and units; the renderer needs the numbers themselves, not a description of
what they look like.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib, aii-web-tools.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. STYLE EXEMPLARS: Decide which field or fields this paper belongs to; a paper spanning two
fields takes exemplars from both. If `./style_exemplars.md` already exists in your workspace
(a previous iteration wrote it), read it and skip the search. Otherwise use the aii-web-tools
skill's scholarly search (OpenAlex) to find the best-cited open-access papers of the last five
years closest to this paper, fetch four or five of them through the skill's fetch tool (arXiv HTML
or PDF), and copy VERBATIM into `./style_exemplars.md`, each passage headed by the paper's
title, year and URL: the abstract, the first paragraph of the introduction, one results paragraph
that reports numbers, and one discussion or limitations paragraph. Read the file once as a whole
and put one line at its top on how those papers handle sentence length, hedging, first person and
citation density. Write the paper in that register. Their sentences and their content are never
reused; they are exemplars of style, not sources.
TODO 4. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 5. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Do NOT emit your structured output when the draft is done — TODO 6 is a
separate revision pass that runs over the finished draft first.
TODO 6. REVISION PASS — start this ONLY once TODO 5's draft is complete, and treat it as a distinct
pass over the finished text rather than something folded into the writing. Read
`REVISION_CHECKLIST.md` in the aii-paper-writing skill's own directory and apply every item to the
full draft.

Writing and revising are different jobs and cannot be done at the same time. The defects that
checklist targets — prose denser than the field needs, an abstract dumped full of numbers, sections
that leak into one another, a Figure 1 that shows a side result instead of the main idea, close
prior work that only the draft's FINAL vocabulary would have surfaced, a study of N things that
plots eight of them, section names that mean nothing to someone who has not read the section,
implementation filenames cited in the prose, numbers that disagree between the abstract, the text
and the tables — are all invisible while drafting, because you are holding your intent rather than
the text. Every one is obvious to the first outside reader.

Work the items one at a time against the ACTUAL text, not from memory of what you meant to write.
For each item, either fix the draft or state in one line why it already holds. The checklist's
consistency section is several SEPARATE sweeps of the whole paper, one concern per sweep — run them
that way, and repeat any sweep that produced an edit, since a fix in one place routinely breaks
agreement somewhere else. Expect this pass to change the draft; one that produces no edits was not
really run.

Only when the checklist is fully worked through, emit the structured JSON — that is your ONLY
output. Do NOT compile LaTeX or generate image/figure files at any point.
</todos><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1'). Letters, digits and underscore only \u2014 a hyphen or space cannot be extracted from its own marker.",
          "pattern": "^\\w+$",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "figure_type": {
          "description": "Which generator draws this figure. Decide by ONE test: does the figure plot numbers? 'data' \u2014 a DATA FIGURE: bars, curves, scatter, heatmaps, confusion matrices, scaling laws, distributions, Pareto fronts, ablation deltas. Rendered deterministically from the numbers, so every bar is exactly the height of its value. 'concept' \u2014 a CONCEPT FIGURE: conceptual artwork, architecture and flow diagrams, anything with no underlying dataset. When a figure has real numbers behind it, ALWAYS choose 'data': an image model only approximates values, producing bars that disagree with their own labels.",
          "enum": [
            "data",
            "concept"
          ],
          "title": "Figure Type",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "The generator's ONLY input \u2014 it cannot read files. For figure_type='data': every numeric value to plot, per series, with axis labels and units, category names, and what the figure has to make the reader see \u2014 the comparison, trend, trade-off or distribution that is the point. Name a chart type only if you actually want a specific one: the figure generator reads its own catalogue of chart types and picks the one that fits, so an enumeration here would only go stale as that catalogue grows. For figure_type='concept': the composition \u2014 what appears where, colours, labels, and what to leave out.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "aspect_ratio": {
          "default": "21:9",
          "description": "Shape of the figure. '21:9' for architecture diagrams / pipelines / flow charts (the paper's hero diagram is usually one of these), '16:9' for side-by-side comparisons and multi-panel results, '4:3' for dense charts, '1:1' for heatmaps / confusion matrices / scatter plots, '3:4' or '9:16' for vertical layouts.",
          "enum": [
            "1:1",
            "4:3",
            "3:2",
            "16:9",
            "21:9",
            "3:4",
            "9:16"
          ],
          "title": "Aspect Ratio",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "figure_type",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.

Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
````

### [7] SYSTEM-USER prompt · 2026-09-20 01:26:23 UTC

```
<validation-feedback>
Attempt 1 failed validation.

The output file `.sdk_openhands_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.sdk_openhands_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```
