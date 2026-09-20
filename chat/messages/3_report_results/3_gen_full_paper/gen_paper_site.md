# gen_paper_site — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_JKcn7QHhokJh` — Self-Surprisal Hard Prompt Compression
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_paper_site` (sdk_openhands_agent, openai/z-ai/glm-5.3)

### [1] CONFIG · 2026-09-20 03:07:26 UTC

```
Model: Free tier (no preference) | Session: e7be7aca-b10a-4e53-9cd9-2ed746457e1d | Tools: 4 | Permission: acceptEdits
```

### [2] SYSTEM PROMPT · 2026-09-20 03:07:28 UTC

```
<design_philosophy>
You are building ONE web page whose only job is to let a reader understand a research paper faster
than they could by opening the PDF. Every decision on the page is judged against that.

WHAT "FASTER" MEANS HERE
- A reader who leaves after thirty seconds still knows the finding and the number behind it.
- A reader who stays five minutes has the method, the figures and the caveats, in that order.
- Nothing on the page is there because a layout had a slot for it.

ACCURACY IS THE HARD CONSTRAINT
Every number, name and claim comes from the paper as written — you read them out of the LaTeX
source and the run's own data files. You never change a number's precision, never restate a
comparison the paper did not make, and never invent a headline figure to fill a card. A page that
looks excellent and misreports one result is worse than no page, because the PDF beside it says
something else and a reader will find that out.

CRAFT, AND THE LOOK TO AVOID
The failure mode for a generated page is a look every reader now recognises on sight: a
purple-to-blue gradient banner, three identical cards with emoji headings, and body text set in
one weight at one size. Avoid all of it.
- Type carries the design. One system font stack, a real scale with visible jumps between levels
  rather than a creep of similar sizes, long-form text around 17-19px with a measure of 65-75
  characters and generous line height. Weight and size do the emphasis; colour rarely does.
- Colour is restrained. A light, near-white ground, one dark ink for text, one accent used for
  links and the current-section marker and almost nothing else. No gradients as decoration.
- Space does the work that borders and boxes would do badly. Sections separated by real vertical
  rhythm, cards defined by alignment and a single hairline rather than by shadow stacks.
- Structure over ornament: no emoji as section markers, no icon fonts, no badge clutter, no
  animated counters.
- Motion is a courtesy. A short transition on a lightbox or a hover state is welcome; anything
  that moves on scroll, autoplays, or delays the reader is not — and all of it stops under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and says what it is to a screen reader. That is
  part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a browser, read it at a phone width and a desktop
width, tabbed through every control, and found nothing to fix. Not before.
</design_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<subagent-delegation>
You may delegate bounded work to subagents (e.g. the Task tool). Delegate by default rather than doing everything yourself:

- Pick the cheapest capable model available to you for each subagent launch:
- Pass `subagent_type="tier-easy"` (steered toward `cohere/north-mini-code:free`) for a small/fast tier for mechanical work.
- Pass `subagent_type="tier-medium"` (steered toward `cohere/north-mini-code:free`) for a mid tier for implementation or investigation (the default).
- Pass `subagent_type="tier-hard"` (steered toward `google/gemma-4-31b-it:free`) for the strongest tier only for hard reasoning or after a cheaper model has already failed on the same task.
- Give each subagent prompt one focused objective: exact scope, the acceptance check, and the required output format.
- Subagents report back only the result, changed files, verification, and blockers — not narration or full logs.
- Delegations on this backend BLOCK: the tool call does not return until that subagent has finished, so launches are serialized no matter how many you plan. Size each delegation to be worth waiting for, and do cheap work yourself rather than paying the round trip.
- Never fork yourself, and never let a subagent spawn its own subagents.
- You (the orchestrator) decompose, coordinate, and synthesize; do not redo work you already delegated.
- Verify each result with the smallest reliable check.
</subagent-delegation>
```

### [3] SYSTEM-USER prompt · 2026-09-20 03:07:28 UTC

````
<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<paper_text>
title: Self-Surprisal Hard Prompt Compression
abstract: >-
  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score
  token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ
  from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses
  the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its
  preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy
  mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four
  long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines
  by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical
  significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for
  SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring
  rather than self-surprisal alone.
paper_text: |-
  # Self-Surprisal Hard Prompt Compression

  ## Abstract

  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring rather than self-surprisal alone.

  ## 1 Introduction

  Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increase in length raises inference latency, memory consumption, and API costs proportionally to sequence length.

  Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

  Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

  Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

  We propose Self-Surprisal Hard Prompt Compression (SSHPC), which scores tokens by the target LLM's own next-token surprisal and prunes the lowest-surprisal tokens. At high compression ratios (≥8×), iterative re-scoring adapts to the changed context. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

  [FIGURE:fig1_method]

  Our contributions are:

  1. **Algorithm**: A hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications. At high compression (≥8×), iterative re-scoring adapts to the changed context (Section 3).
  2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
  3. **Empirical evaluation**: Experiments on four benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) with Llama-3-8B, comparing SSHPC against LLMLingua, SelectiveContext, LLMLingua-2, random pruning, and a proxy-on-target ablation, at compression ratios 2×–10×. We measure task accuracy and end-to-end latency (Section 4).
  4. **Ablation studies**: Proxy-mismatch isolation, iterative vs. single-pass at high compression, query-conditioned vs. unconditional surprisal, and latency break-even analysis (Section 4.4).

  ## 2 Related Work

  ### 2.1 Hard Prompt Compression via Proxy Models

  LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

  SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

  All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

  Recent work has explored alternatives. ProCut (Xu et al., 2025) segments prompt templates into semantic units and estimates their attribution via an LLM-driven estimator, achieving 78% token reduction in production. Nano-Capsulator (Chuang et al., 2024) paraphrases prompts into concise natural language using a fine-tuned Vicuna-7B. ASAP (Zeng et al., 2025) uses first-token surprisal for chain-of-thought step pruning with fine-tuning. PIS (Chen et al., 2025) uses attention scores for importance sampling. None uses the target LLM's own next-token logits directly for hard token pruning.

  ### 2.2 Soft Prompt Compression

  GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

  SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

  ### 2.3 Theoretical Frameworks

  Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

  Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

  ## 3 Method

  ### 3.1 Self-Surprisal Hard Prompt Compression

  Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

  $$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

  where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

  **Special token preservation.** Instruction delimiters, `<bos>`, `<eos>`, and other structural tokens are assigned infinite surprisal so they are never pruned.

  Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

  **Iterative re-scoring for high compression.** At compression ratios $r \ge 8$, token predictability changes substantially as surrounding tokens are removed. We therefore iterate: after initial pruning, we recompute surprisal on the compressed prompt $\tilde{\mathbf{x}}$ under the same model $M$ and prune again to the target ratio. We use 3 rounds by default. This is the default for $r \ge 8$; for $r < 8$, single-pass is used.

  **Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step.

  **Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for prompts with an identifiable task specification (question in QA, last user message in chat, instruction prefix in summarization), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{task\_spec})$, so context tokens are scored by how surprising they are given the task. This aligns with LongLLMLingua's finding that question-awareness improves compression. (3) *Attention-weighted SSHPC*: each token's surprisal is weighted by its total attention mass received from subsequent tokens in the final layer, capturing both self-predictability and causal influence.

  [FIGURE:fig1_method]

  ### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

  Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

  Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

  If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

  This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

  ### 3.3 Computational Considerations

  SSHPC requires one forward pass over the full prompt (or multiple passes for iterative re-scoring). For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. We measure actual prefill latency on A100-40GB and compare against generation time savings to determine break-even compression ratios.

  At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

  [FIGURE:fig7_surprisal]

  ## 4 Experiments

  ### 4.1 Datasets and Tasks

  We evaluate on four benchmarks covering diverse long-context tasks [ARTIFACT:art_-Hzqeq6rV9vC]:

  - **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure. Metric: Exact Match.
  - **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies. Metric: F1.
  - **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA with 10 retrieved documents per question. Metric: F1.
  - **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens. Metric: F1/EM/ROUGE-L (task-dependent).

  ### 4.2 Target Models and Baselines

  **Target LLM** (local inference via HuggingFace):
  - Llama-3-8B-Instruct

  **Proxy model for baselines**:
  - GPT-2 (124M parameters) for LLMLingua and SelectiveContext

  **Methods compared**:
  1. **No compression** (full prompt)
  2. **Random pruning**: uniform random token removal
  3. **SelectiveContext** (Li, 2023): self-information from GPT-2 proxy
  4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
  5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
  6. **Proxy-on-Target ablation**: LLMLingua using the *same* target LLM (Llama-3-8B) as the proxy. This isolates the proxy-mismatch effect.
  7. **SSHPC Base**: single-pass self-surprisal, special tokens preserved
  8. **SSHPC Query-Conditioned**: surprisal conditioned on task specification
  9. **SSHPC Attention-Weighted**: surprisal weighted by attention mass
  10. **SSHPC Iterative**: single-pass at 2×, 4×; iterative (3 rounds) at 8×, 10×

  ### 4.3 Compression Ratios and Metrics

  Compression ratios: 2×, 4×, 8×, 10× (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

  **Primary metrics**:
  - Task accuracy (Exact Match for GSM8K, F1 for QA, ROUGE-L for summarization)
  - End-to-end latency (compression + generation) on A100-40GB

  **Secondary metrics**:
  - Compression throughput (tokens/sec for the compression step alone)
  - Surprisal distribution statistics

  ### 4.4 Ablation Studies

  1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the target's own distribution with iterative re-scoring.
  2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
  3. **Single-pass vs. iterative**: At 8× and 10×, compare single-pass SSHPC against iterative (3 rounds).
  4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning against fixed-ratio top-k.

  ## 5 Results

  ### 5.1 Main Results

  Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks and compression ratios. SSHPC Iterative is the best-performing method at 8× and 10× on GSM8K (72.9% and 71.1% EM) and HotpotQA (62.5% and 61.4% F1). At 2× and 4×, all methods including SSHPC Base remain close to the no-compression baseline (within 1–2 points). The gap widens at higher compression: at 10×, SSHPC Iterative leads LLMLingua by 7.4 points on GSM8K and 5.9 points on HotpotQA.

  On NaturalQuestions, SSHPC Base and Iterative match SelectiveContext at 2×–4× (68.5–68.6% F1) and pull ahead at 8× (67.1% vs 61.7%). On LongBench, SSHPC Iterative consistently outperforms baselines, reaching 42.8% at 8× vs 40.4% for LLMLingua.

  Random pruning degrades rapidly, confirming that token importance is non-uniform and methods that exploit it are effective.

  [FIGURE:fig2_main]

  ### 5.2 Proxy-Mismatch Ablation

  [FIGURE:fig3_proxy]

  This indicates that the proxy-mismatch effect, while real, is small in isolation. The larger gains of SSHPC Iterative at high compression come from iterative re-scoring adapting to the changed context, not from self-surprisal being inherently superior to target-model perplexity in a single pass.

  ### 5.3 Iterative Re-Scoring Benefit

  Figure 4 shows the iterative benefit at 8× and 10×. On GSM8K, iterative adds +3.8 points at 8× (p = 0.0001) and +2.2 points at 10× (p = 0.003). On HotpotQA, +2.3 points at 8× (p = 0.04) and +1.6 points at 10× (p = 0.08). On NaturalQuestions, +1.1 points at 8× (p = 0.12) and +3.5 points at 10× (p = 0.02). On LongBench, +0.8 points at 8× (p = 0.21) and +1.2 points at 10× (p = 0.15).

  Iterative re-scoring is most beneficial for reasoning-heavy tasks (GSM8K, HotpotQA) where token dependencies are strong and context changes substantially after pruning.

  [FIGURE:fig4_iterative]

  ### 5.4 Query-Conditioned and Attention-Weighted Variants

  Figure 5 compares SSHPC variants at 8×. Query-conditioned SSHPC improves over Base on NaturalQuestions (+1.6 points) and HotpotQA (+2.2 points) where a clear question exists. On GSM8K (no explicit question), it matches Base. Attention-weighted SSHPC improves on GSM8K (+2.6 points) and HotpotQA (+1.9 points) but not on LongBench. The best variant is task-dependent: Iterative dominates on GSM8K and HotpotQA; Query-Conditioned leads on NaturalQuestions.

  [FIGURE:fig5_variants]

  ### 5.5 Latency Break-Even

  Figure 6 shows end-to-end latency vs. compression ratio. For all methods, break-even (compression overhead equals generation time saved) occurs at 2×. At 2×, compression adds ~2.5s prefill but saves ~2.5s generation, yielding net parity. At 4× and above, all methods show net latency reduction. SSHPC Base adds ~5–10ms overhead per 1000 tokens vs. GPT-2-based methods, but this is negligible compared to generation savings at high compression. The break-even ratio of 2× holds across all benchmarks.

  [FIGURE:fig6_latency]

  [ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:art_Lm_O96s-n8rb]

  ## 6 Discussion

  ### 6.1 Summary of Findings

  1. **Self-surprisal works**: SSHPC Base matches or exceeds proxy-based baselines across all benchmarks, with larger margins at high compression.
  2. **Iterative re-scoring is critical at ≥8×**: It provides statistically significant gains on reasoning tasks (GSM8K, HotpotQA) by adapting to the changed context after pruning.
  3. **Proxy mismatch is real but small in isolation**: When the proxy is the target model, SSHPC's single-pass advantage is 0.48% on average and not significant. The practical gains come from iterative re-scoring, which proxy methods do not naturally support because they condition on the *original* context during iterative compression.
  4. **Query conditioning helps when a question exists**: On QA tasks, conditioning surprisal on the question improves pruning decisions.
  5. **Latency break-even at 2×**: All methods including SSHPC become net-positive at 2× compression on A100.

  ### 6.2 Limitations

  **Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (OpenAI's `logprobs`), but not all. For fully black-box APIs, proxy methods remain the only option.

  **Single-pass context dependence**: At high compression, single-pass surprisal computed on the full prompt becomes stale. We address this with iterative re-scoring as the default for r ≥ 8, but this multiplies compression latency by the number of rounds (3× in our experiments).

  **First-token handling**: The first token uses the unconditional distribution, which may not reflect its importance. We mitigate this by always preserving special/instruction tokens via infinite surprisal assignment. An alternative would use bidirectional pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy model.

  **Query-conditioning generality**: Our heuristic for extracting the "task specification" (last user message, question, instruction prefix) works for standard prompt templates but may fail for unusual formats. A more robust approach would use an instruction-following model to identify the task specification automatically.

  **Single target model**: We evaluate only on Llama-3-8B-Instruct. The method should transfer to other open-weight models (Qwen2, Mistral), but the exact break-even ratios and iterative benefits may vary with model architecture and size.

  **Synthetic surprisal distributions**: The surprisal distribution in Figure 7 is synthetic (generated from a log-normal fit to pilot data). Real distributions from Llama-3-8B would provide stronger evidence but require additional computation.

  ### 6.3 Broader Implications

  If self-surprisal with iterative re-scoring proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression—no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error, applied iteratively. SSHPC operationalizes this principle for hard token pruning.

  The negative result on proxy-mismatch (when the proxy *is* the target) is informative: it suggests that LLMLingua's iterative compression already approximates the target model's preferences reasonably well when the proxy is large and aligned. The remaining gap at high compression comes from LLMLingua conditioning on the *original* context during re-scoring, whereas SSHPC re-scores on the *compressed* context, which is what the target will actually see.

  ## 7 Conclusion

  We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token prediction logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation on four long-context benchmarks with Llama-3-8B shows that SSHPC Base outperforms proxy baselines at high compression, and iterative re-scoring (default for r ≥ 8×) provides statistically significant additional gains of 1.8–3.8 points on reasoning tasks. The proxy-mismatch ablation reveals that self-surprisal alone provides only a marginal (0.48%, not significant) advantage over target-model perplexity; the practical gains come from iterative adaptation to the compressed context. Latency break-even occurs at 2× compression for all methods. Future work includes extending to multiple target models, chunked computation for >8k tokens, and automatic task-specification extraction for query conditioning.

  ---

  ## Bibliography

  \bibliography{references}
  \bibliographystyle{plainnat}
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token logits to compute per-token surprisal
  for hard prompt pruning. Evaluated on 4 benchmarks with Llama-3-8B at 2x-10x compression. SSHPC Iterative (with re-scoring
  at >=8x) outperforms proxy baselines by 2-5 points at high compression. Key finding: proxy-mismatch effect is small (0.48%,
  ns) in isolation; gains come from iterative re-scoring adapting to compressed context. Latency break-even at 2x.
</paper_text>

<available_figures>
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig2_main_v0.png [render from fig2_main_v0.pdf first] — "Task Accuracy Across Benchmarks and Compression Ratios" (caption: "Task accuracy (%) across four benchmarks and four compression ratios (2×, 4×, 8×, 10×) for six methods. SSHPC Iterative (solid green) consistently outperforms baselines at high compression. LLMLingua (blue) and SelectiveContext (orange) degrade faster than SSHPC variants. No Compression (black) is the upper bound. Random Pruning (gray) degrades rapidly. Error bars show 95% bootstrap confidence intervals (10,000 resamples).")
- figures/fig3_proxy_v0.png [render from fig3_proxy_v0.pdf first] — "Proxy-Mismatch Ablation: SSHPC vs Proxy-on-Target" (caption: "Accuracy difference (SSHPC Base minus Proxy-on-Target) across 16 dataset–ratio conditions. Positive values favor SSHPC. The average improvement is +0.48% (not statistically significant, p > 0.05). Error bars show standard error (1.5%). Conditions: GSM8K 2×–10×, HotpotQA 2×–10×, NaturalQuestions 2×–10×, LongBench 2×–10×.")
- figures/fig4_iterative_v0.png [render from fig4_iterative_v0.pdf first] — "Iterative Re-Scoring Benefit at High Compression" (caption: "Dumbbell chart comparing single-pass vs iterative (3 rounds) SSHPC at 8× and 10× compression. Iterative re-scoring provides significant gains on GSM8K (+3.8 at 8×, p=0.0001) and HotpotQA (+2.3 at 8×, p=0.04), moderate gains on NaturalQuestions, and smaller non-significant gains on LongBench. Single-pass values are constant at 70% (baseline reference).")
- figures/fig5_variants_v0.png [render from fig5_variants_v0.pdf first] — "SSHPC Variant Comparison at 8× Compression" (caption: "Comparison of four SSHPC variants at 8× compression across four datasets. Iterative (green) leads on GSM8K (72.9%) and HotpotQA (62.5%). Query-Conditioned (orange) leads on NaturalQuestions (67.6%). Attention-Weighted (purple) is competitive on GSM8K (71.7%) and HotpotQA (62.2%). Base (blue) is the single-pass unconditional variant. Error bars show 95% CI.")
- figures/fig6_latency_v0.png [render from fig6_latency_v0.pdf first] — "End-to-End Latency vs Compression Ratio" (caption: "End-to-end latency (compression + generation) vs compression ratio for four methods. Break-even occurs at 2× for all methods. At 2×, latency ~2500ms; at 4×, ~1250ms; at 8×, ~625ms; at 10×, ~500ms. SSHPC Base (green) and Iterative (purple) overlap with LLMLingua (blue) and No Compression (black) within error bands. Shaded bands show standard deviation across datasets.")
- figures/fig7_surprisal_v0.png [render from fig7_surprisal_v0.pdf first] — "Per-Token Surprisal Distribution (Synthetic)" (caption: "Violin plot of per-token surprisal distribution for GSM8K (synthetic data from log-normal fit to pilot runs). Surprisal values range from near 0 to ~16, with a long right tail. Median ~1.5, mean ~3.2. The distribution is highly skewed, confirming that most tokens are predictable (low surprisal) while a few carry high information.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNG files into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [4] HUMAN-USER prompt · 2026-09-20 03:07:28 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```

### [5] RETRY (attempt 1) · 2026-09-20 03:09:39 UTC

```
Agent result indicates failure (attempt 1/6): Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed746457e1d

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [6] RETRY (attempt 2) · 2026-09-20 03:09:39 UTC

```
Agent retry... (attempt 2/6): Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed746457e1d

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [7] CONFIG · 2026-09-20 03:09:40 UTC

```
Model: Free tier (no preference) | Session: 0b75a215-b011-44c1-ae88-41510d92b879 | Tools: 4 | Permission: acceptEdits
```

### [8] SYSTEM PROMPT · 2026-09-20 03:09:42 UTC

```
<design_philosophy>
You are building ONE web page whose only job is to let a reader understand a research paper faster
than they could by opening the PDF. Every decision on the page is judged against that.

WHAT "FASTER" MEANS HERE
- A reader who leaves after thirty seconds still knows the finding and the number behind it.
- A reader who stays five minutes has the method, the figures and the caveats, in that order.
- Nothing on the page is there because a layout had a slot for it.

ACCURACY IS THE HARD CONSTRAINT
Every number, name and claim comes from the paper as written — you read them out of the LaTeX
source and the run's own data files. You never change a number's precision, never restate a
comparison the paper did not make, and never invent a headline figure to fill a card. A page that
looks excellent and misreports one result is worse than no page, because the PDF beside it says
something else and a reader will find that out.

CRAFT, AND THE LOOK TO AVOID
The failure mode for a generated page is a look every reader now recognises on sight: a
purple-to-blue gradient banner, three identical cards with emoji headings, and body text set in
one weight at one size. Avoid all of it.
- Type carries the design. One system font stack, a real scale with visible jumps between levels
  rather than a creep of similar sizes, long-form text around 17-19px with a measure of 65-75
  characters and generous line height. Weight and size do the emphasis; colour rarely does.
- Colour is restrained. A light, near-white ground, one dark ink for text, one accent used for
  links and the current-section marker and almost nothing else. No gradients as decoration.
- Space does the work that borders and boxes would do badly. Sections separated by real vertical
  rhythm, cards defined by alignment and a single hairline rather than by shadow stacks.
- Structure over ornament: no emoji as section markers, no icon fonts, no badge clutter, no
  animated counters.
- Motion is a courtesy. A short transition on a lightbox or a hover state is welcome; anything
  that moves on scroll, autoplays, or delays the reader is not — and all of it stops under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and says what it is to a screen reader. That is
  part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a browser, read it at a phone width and a desktop
width, tabbed through every control, and found nothing to fix. Not before.
</design_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<subagent-delegation>
You may delegate bounded work to subagents (e.g. the Task tool). Delegate by default rather than doing everything yourself:

- Pick the cheapest capable model available to you for each subagent launch:
- Pass `subagent_type="tier-easy"` (steered toward `cohere/north-mini-code:free`) for a small/fast tier for mechanical work.
- Pass `subagent_type="tier-medium"` (steered toward `cohere/north-mini-code:free`) for a mid tier for implementation or investigation (the default).
- Pass `subagent_type="tier-hard"` (steered toward `google/gemma-4-31b-it:free`) for the strongest tier only for hard reasoning or after a cheaper model has already failed on the same task.
- Give each subagent prompt one focused objective: exact scope, the acceptance check, and the required output format.
- Subagents report back only the result, changed files, verification, and blockers — not narration or full logs.
- Delegations on this backend BLOCK: the tool call does not return until that subagent has finished, so launches are serialized no matter how many you plan. Size each delegation to be worth waiting for, and do cheap work yourself rather than paying the round trip.
- Never fork yourself, and never let a subagent spawn its own subagents.
- You (the orchestrator) decompose, coordinate, and synthesize; do not redo work you already delegated.
- Verify each result with the smallest reliable check.
</subagent-delegation>
```

### [9] SYSTEM-USER prompt · 2026-09-20 03:09:42 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed746457e1d

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
Last actions before failure:
  - [agent_system_user_prompt]: <task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize indepe
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<paper_text>
title: Self-Surprisal Hard Prompt Compression
abstract: >-
  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score
  token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ
  from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses
  the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its
  preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy
  mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four
  long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines
  by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical
  significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for
  SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring
  rather than self-surprisal alone.
paper_text: |-
  # Self-Surprisal Hard Prompt Compression

  ## Abstract

  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring rather than self-surprisal alone.

  ## 1 Introduction

  Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increase in length raises inference latency, memory consumption, and API costs proportionally to sequence length.

  Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

  Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

  Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

  We propose Self-Surprisal Hard Prompt Compression (SSHPC), which scores tokens by the target LLM's own next-token surprisal and prunes the lowest-surprisal tokens. At high compression ratios (≥8×), iterative re-scoring adapts to the changed context. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

  [FIGURE:fig1_method]

  Our contributions are:

  1. **Algorithm**: A hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications. At high compression (≥8×), iterative re-scoring adapts to the changed context (Section 3).
  2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
  3. **Empirical evaluation**: Experiments on four benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) with Llama-3-8B, comparing SSHPC against LLMLingua, SelectiveContext, LLMLingua-2, random pruning, and a proxy-on-target ablation, at compression ratios 2×–10×. We measure task accuracy and end-to-end latency (Section 4).
  4. **Ablation studies**: Proxy-mismatch isolation, iterative vs. single-pass at high compression, query-conditioned vs. unconditional surprisal, and latency break-even analysis (Section 4.4).

  ## 2 Related Work

  ### 2.1 Hard Prompt Compression via Proxy Models

  LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

  SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

  All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

  Recent work has explored alternatives. ProCut (Xu et al., 2025) segments prompt templates into semantic units and estimates their attribution via an LLM-driven estimator, achieving 78% token reduction in production. Nano-Capsulator (Chuang et al., 2024) paraphrases prompts into concise natural language using a fine-tuned Vicuna-7B. ASAP (Zeng et al., 2025) uses first-token surprisal for chain-of-thought step pruning with fine-tuning. PIS (Chen et al., 2025) uses attention scores for importance sampling. None uses the target LLM's own next-token logits directly for hard token pruning.

  ### 2.2 Soft Prompt Compression

  GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

  SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

  ### 2.3 Theoretical Frameworks

  Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

  Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

  ## 3 Method

  ### 3.1 Self-Surprisal Hard Prompt Compression

  Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

  $$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

  where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

  **Special token preservation.** Instruction delimiters, `<bos>`, `<eos>`, and other structural tokens are assigned infinite surprisal so they are never pruned.

  Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

  **Iterative re-scoring for high compression.** At compression ratios $r \ge 8$, token predictability changes substantially as surrounding tokens are removed. We therefore iterate: after initial pruning, we recompute surprisal on the compressed prompt $\tilde{\mathbf{x}}$ under the same model $M$ and prune again to the target ratio. We use 3 rounds by default. This is the default for $r \ge 8$; for $r < 8$, single-pass is used.

  **Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step.

  **Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for prompts with an identifiable task specification (question in QA, last user message in chat, instruction prefix in summarization), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{task\_spec})$, so context tokens are scored by how surprising they are given the task. This aligns with LongLLMLingua's finding that question-awareness improves compression. (3) *Attention-weighted SSHPC*: each token's surprisal is weighted by its total attention mass received from subsequent tokens in the final layer, capturing both self-predictability and causal influence.

  [FIGURE:fig1_method]

  ### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

  Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

  Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

  If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

  This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

  ### 3.3 Computational Considerations

  SSHPC requires one forward pass over the full prompt (or multiple passes for iterative re-scoring). For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. We measure actual prefill latency on A100-40GB and compare against generation time savings to determine break-even compression ratios.

  At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

  [FIGURE:fig7_surprisal]

  ## 4 Experiments

  ### 4.1 Datasets and Tasks

  We evaluate on four benchmarks covering diverse long-context tasks [ARTIFACT:art_-Hzqeq6rV9vC]:

  - **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure. Metric: Exact Match.
  - **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies. Metric: F1.
  - **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA with 10 retrieved documents per question. Metric: F1.
  - **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens. Metric: F1/EM/ROUGE-L (task-dependent).

  ### 4.2 Target Models and Baselines

  **Target LLM** (local inference via HuggingFace):
  - Llama-3-8B-Instruct

  **Proxy model for baselines**:
  - GPT-2 (124M parameters) for LLMLingua and SelectiveContext

  **Methods compared**:
  1. **No compression** (full prompt)
  2. **Random pruning**: uniform random token removal
  3. **SelectiveContext** (Li, 2023): self-information from GPT-2 proxy
  4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
  5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
  6. **Proxy-on-Target ablation**: LLMLingua using the *same* target LLM (Llama-3-8B) as the proxy. This isolates the proxy-mismatch effect.
  7. **SSHPC Base**: single-pass self-surprisal, special tokens preserved
  8. **SSHPC Query-Conditioned**: surprisal conditioned on task specification
  9. **SSHPC Attention-Weighted**: surprisal weighted by attention mass
  10. **SSHPC Iterative**: single-pass at 2×, 4×; iterative (3 rounds) at 8×, 10×

  ### 4.3 Compression Ratios and Metrics

  Compression ratios: 2×, 4×, 8×, 10× (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

  **Primary metrics**:
  - Task accuracy (Exact Match for GSM8K, F1 for QA, ROUGE-L for summarization)
  - End-to-end latency (compression + generation) on A100-40GB

  **Secondary metrics**:
  - Compression throughput (tokens/sec for the compression step alone)
  - Surprisal distribution statistics

  ### 4.4 Ablation Studies

  1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the target's own distribution with iterative re-scoring.
  2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
  3. **Single-pass vs. iterative**: At 8× and 10×, compare single-pass SSHPC against iterative (3 rounds).
  4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning against fixed-ratio top-k.

  ## 5 Results

  ### 5.1 Main Results

  Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks and compression ratios. SSHPC Iterative is the best-performing method at 8× and 10× on GSM8K (72.9% and 71.1% EM) and HotpotQA (62.5% and 61.4% F1). At 2× and 4×, all methods including SSHPC Base remain close to the no-compression baseline (within 1–2 points). The gap widens at higher compression: at 10×, SSHPC Iterative leads LLMLingua by 7.4 points on GSM8K and 5.9 points on HotpotQA.

  On NaturalQuestions, SSHPC Base and Iterative match SelectiveContext at 2×–4× (68.5–68.6% F1) and pull ahead at 8× (67.1% vs 61.7%). On LongBench, SSHPC Iterative consistently outperforms baselines, reaching 42.8% at 8× vs 40.4% for LLMLingua.

  Random pruning degrades rapidly, confirming that token importance is non-uniform and methods that exploit it are effective.

  [FIGURE:fig2_main]

  ### 5.2 Proxy-Mismatch Ablation

  [FIGURE:fig3_proxy]

  This indicates that the proxy-mismatch effect, while real, is small in isolation. The larger gains of SSHPC Iterative at high compression come from iterative re-scoring adapting to the changed context, not from self-surprisal being inherently superior to target-model perplexity in a single pass.

  ### 5.3 Iterative Re-Scoring Benefit

  Figure 4 shows the iterative benefit at 8× and 10×. On GSM8K, iterative adds +3.8 points at 8× (p = 0.0001) and +2.2 points at 10× (p = 0.003). On HotpotQA, +2.3 points at 8× (p = 0.04) and +1.6 points at 10× (p = 0.08). On NaturalQuestions, +1.1 points at 8× (p = 0.12) and +3.5 points at 10× (p = 0.02). On LongBench, +0.8 points at 8× (p = 0.21) and +1.2 points at 10× (p = 0.15).

  Iterative re-scoring is most beneficial for reasoning-heavy tasks (GSM8K, HotpotQA) where token dependencies are strong and context changes substantially after pruning.

  [FIGURE:fig4_iterative]

  ### 5.4 Query-Conditioned and Attention-Weighted Variants

  Figure 5 compares SSHPC variants at 8×. Query-conditioned SSHPC improves over Base on NaturalQuestions (+1.6 points) and HotpotQA (+2.2 points) where a clear question exists. On GSM8K (no explicit question), it matches Base. Attention-weighted SSHPC improves on GSM8K (+2.6 points) and HotpotQA (+1.9 points) but not on LongBench. The best variant is task-dependent: Iterative dominates on GSM8K and HotpotQA; Query-Conditioned leads on NaturalQuestions.

  [FIGURE:fig5_variants]

  ### 5.5 Latency Break-Even

  Figure 6 shows end-to-end latency vs. compression ratio. For all methods, break-even (compression overhead equals generation time saved) occurs at 2×. At 2×, compression adds ~2.5s prefill but saves ~2.5s generation, yielding net parity. At 4× and above, all methods show net latency reduction. SSHPC Base adds ~5–10ms overhead per 1000 tokens vs. GPT-2-based methods, but this is negligible compared to generation savings at high compression. The break-even ratio of 2× holds across all benchmarks.

  [FIGURE:fig6_latency]

  [ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:art_Lm_O96s-n8rb]

  ## 6 Discussion

  ### 6.1 Summary of Findings

  1. **Self-surprisal works**: SSHPC Base matches or exceeds proxy-based baselines across all benchmarks, with larger margins at high compression.
  2. **Iterative re-scoring is critical at ≥8×**: It provides statistically significant gains on reasoning tasks (GSM8K, HotpotQA) by adapting to the changed context after pruning.
  3. **Proxy mismatch is real but small in isolation**: When the proxy is the target model, SSHPC's single-pass advantage is 0.48% on average and not significant. The practical gains come from iterative re-scoring, which proxy methods do not naturally support because they condition on the *original* context during iterative compression.
  4. **Query conditioning helps when a question exists**: On QA tasks, conditioning surprisal on the question improves pruning decisions.
  5. **Latency break-even at 2×**: All methods including SSHPC become net-positive at 2× compression on A100.

  ### 6.2 Limitations

  **Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (OpenAI's `logprobs`), but not all. For fully black-box APIs, proxy methods remain the only option.

  **Single-pass context dependence**: At high compression, single-pass surprisal computed on the full prompt becomes stale. We address this with iterative re-scoring as the default for r ≥ 8, but this multiplies compression latency by the number of rounds (3× in our experiments).

  **First-token handling**: The first token uses the unconditional distribution, which may not reflect its importance. We mitigate this by always preserving special/instruction tokens via infinite surprisal assignment. An alternative would use bidirectional pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy model.

  **Query-conditioning generality**: Our heuristic for extracting the "task specification" (last user message, question, instruction prefix) works for standard prompt templates but may fail for unusual formats. A more robust approach would use an instruction-following model to identify the task specification automatically.

  **Single target model**: We evaluate only on Llama-3-8B-Instruct. The method should transfer to other open-weight models (Qwen2, Mistral), but the exact break-even ratios and iterative benefits may vary with model architecture and size.

  **Synthetic surprisal distributions**: The surprisal distribution in Figure 7 is synthetic (generated from a log-normal fit to pilot data). Real distributions from Llama-3-8B would provide stronger evidence but require additional computation.

  ### 6.3 Broader Implications

  If self-surprisal with iterative re-scoring proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression—no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error, applied iteratively. SSHPC operationalizes this principle for hard token pruning.

  The negative result on proxy-mismatch (when the proxy *is* the target) is informative: it suggests that LLMLingua's iterative compression already approximates the target model's preferences reasonably well when the proxy is large and aligned. The remaining gap at high compression comes from LLMLingua conditioning on the *original* context during re-scoring, whereas SSHPC re-scores on the *compressed* context, which is what the target will actually see.

  ## 7 Conclusion

  We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token prediction logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation on four long-context benchmarks with Llama-3-8B shows that SSHPC Base outperforms proxy baselines at high compression, and iterative re-scoring (default for r ≥ 8×) provides statistically significant additional gains of 1.8–3.8 points on reasoning tasks. The proxy-mismatch ablation reveals that self-surprisal alone provides only a marginal (0.48%, not significant) advantage over target-model perplexity; the practical gains come from iterative adaptation to the compressed context. Latency break-even occurs at 2× compression for all methods. Future work includes extending to multiple target models, chunked computation for >8k tokens, and automatic task-specification extraction for query conditioning.

  ---

  ## Bibliography

  \bibliography{references}
  \bibliographystyle{plainnat}
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token logits to compute per-token surprisal
  for hard prompt pruning. Evaluated on 4 benchmarks with Llama-3-8B at 2x-10x compression. SSHPC Iterative (with re-scoring
  at >=8x) outperforms proxy baselines by 2-5 points at high compression. Key finding: proxy-mismatch effect is small (0.48%,
  ns) in isolation; gains come from iterative re-scoring adapting to compressed context. Latency break-even at 2x.
</paper_text>

<available_figures>
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig2_main_v0.png [render from fig2_main_v0.pdf first] — "Task Accuracy Across Benchmarks and Compression Ratios" (caption: "Task accuracy (%) across four benchmarks and four compression ratios (2×, 4×, 8×, 10×) for six methods. SSHPC Iterative (solid green) consistently outperforms baselines at high compression. LLMLingua (blue) and SelectiveContext (orange) degrade faster than SSHPC variants. No Compression (black) is the upper bound. Random Pruning (gray) degrades rapidly. Error bars show 95% bootstrap confidence intervals (10,000 resamples).")
- figures/fig3_proxy_v0.png [render from fig3_proxy_v0.pdf first] — "Proxy-Mismatch Ablation: SSHPC vs Proxy-on-Target" (caption: "Accuracy difference (SSHPC Base minus Proxy-on-Target) across 16 dataset–ratio conditions. Positive values favor SSHPC. The average improvement is +0.48% (not statistically significant, p > 0.05). Error bars show standard error (1.5%). Conditions: GSM8K 2×–10×, HotpotQA 2×–10×, NaturalQuestions 2×–10×, LongBench 2×–10×.")
- figures/fig4_iterative_v0.png [render from fig4_iterative_v0.pdf first] — "Iterative Re-Scoring Benefit at High Compression" (caption: "Dumbbell chart comparing single-pass vs iterative (3 rounds) SSHPC at 8× and 10× compression. Iterative re-scoring provides significant gains on GSM8K (+3.8 at 8×, p=0.0001) and HotpotQA (+2.3 at 8×, p=0.04), moderate gains on NaturalQuestions, and smaller non-significant gains on LongBench. Single-pass values are constant at 70% (baseline reference).")
- figures/fig5_variants_v0.png [render from fig5_variants_v0.pdf first] — "SSHPC Variant Comparison at 8× Compression" (caption: "Comparison of four SSHPC variants at 8× compression across four datasets. Iterative (green) leads on GSM8K (72.9%) and HotpotQA (62.5%). Query-Conditioned (orange) leads on NaturalQuestions (67.6%). Attention-Weighted (purple) is competitive on GSM8K (71.7%) and HotpotQA (62.2%). Base (blue) is the single-pass unconditional variant. Error bars show 95% CI.")
- figures/fig6_latency_v0.png [render from fig6_latency_v0.pdf first] — "End-to-End Latency vs Compression Ratio" (caption: "End-to-end latency (compression + generation) vs compression ratio for four methods. Break-even occurs at 2× for all methods. At 2×, latency ~2500ms; at 4×, ~1250ms; at 8×, ~625ms; at 10×, ~500ms. SSHPC Base (green) and Iterative (purple) overlap with LLMLingua (blue) and No Compression (black) within error bands. Shaded bands show standard deviation across datasets.")
- figures/fig7_surprisal_v0.png [render from fig7_surprisal_v0.pdf first] — "Per-Token Surprisal Distribution (Synthetic)" (caption: "Violin plot of per-token surprisal distribution for GSM8K (synthetic data from log-normal fit to pilot runs). Surprisal values range from near 0 to ~16, with a long right tail. Median ~1.5, mean ~3.2. The distribution is highly skewed, confirming that most tokens are predictable (low surprisal) while a few carry high information.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNG files into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [10] HUMAN-USER prompt · 2026-09-20 03:09:42 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```

### [11] RETRY (attempt 2) · 2026-09-20 03:11:18 UTC

```
Agent result indicates failure (attempt 2/6): Conversation run failed for id=0b75a215-b011-44c1-ae88-41510d92b879: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/0b75a215b01144c1ae8841510d92b879

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [12] RETRY (attempt 3) · 2026-09-20 03:11:18 UTC

```
Agent retry... (attempt 3/6): Conversation run failed for id=0b75a215-b011-44c1-ae88-41510d92b879: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/0b75a215b01144c1ae8841510d92b879

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [13] CONFIG · 2026-09-20 03:11:18 UTC

```
Model: Free tier (no preference) | Session: 107b816b-b5bf-43d1-8c15-c777e1aa5aab | Tools: 4 | Permission: acceptEdits
```

### [14] SYSTEM PROMPT · 2026-09-20 03:11:20 UTC

```
<design_philosophy>
You are building ONE web page whose only job is to let a reader understand a research paper faster
than they could by opening the PDF. Every decision on the page is judged against that.

WHAT "FASTER" MEANS HERE
- A reader who leaves after thirty seconds still knows the finding and the number behind it.
- A reader who stays five minutes has the method, the figures and the caveats, in that order.
- Nothing on the page is there because a layout had a slot for it.

ACCURACY IS THE HARD CONSTRAINT
Every number, name and claim comes from the paper as written — you read them out of the LaTeX
source and the run's own data files. You never change a number's precision, never restate a
comparison the paper did not make, and never invent a headline figure to fill a card. A page that
looks excellent and misreports one result is worse than no page, because the PDF beside it says
something else and a reader will find that out.

CRAFT, AND THE LOOK TO AVOID
The failure mode for a generated page is a look every reader now recognises on sight: a
purple-to-blue gradient banner, three identical cards with emoji headings, and body text set in
one weight at one size. Avoid all of it.
- Type carries the design. One system font stack, a real scale with visible jumps between levels
  rather than a creep of similar sizes, long-form text around 17-19px with a measure of 65-75
  characters and generous line height. Weight and size do the emphasis; colour rarely does.
- Colour is restrained. A light, near-white ground, one dark ink for text, one accent used for
  links and the current-section marker and almost nothing else. No gradients as decoration.
- Space does the work that borders and boxes would do badly. Sections separated by real vertical
  rhythm, cards defined by alignment and a single hairline rather than by shadow stacks.
- Structure over ornament: no emoji as section markers, no icon fonts, no badge clutter, no
  animated counters.
- Motion is a courtesy. A short transition on a lightbox or a hover state is welcome; anything
  that moves on scroll, autoplays, or delays the reader is not — and all of it stops under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and says what it is to a screen reader. That is
  part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a browser, read it at a phone width and a desktop
width, tabbed through every control, and found nothing to fix. Not before.
</design_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<subagent-delegation>
You may delegate bounded work to subagents (e.g. the Task tool). Delegate by default rather than doing everything yourself:

- Pick the cheapest capable model available to you for each subagent launch:
- Pass `subagent_type="tier-easy"` (steered toward `cohere/north-mini-code:free`) for a small/fast tier for mechanical work.
- Pass `subagent_type="tier-medium"` (steered toward `cohere/north-mini-code:free`) for a mid tier for implementation or investigation (the default).
- Pass `subagent_type="tier-hard"` (steered toward `google/gemma-4-31b-it:free`) for the strongest tier only for hard reasoning or after a cheaper model has already failed on the same task.
- Give each subagent prompt one focused objective: exact scope, the acceptance check, and the required output format.
- Subagents report back only the result, changed files, verification, and blockers — not narration or full logs.
- Delegations on this backend BLOCK: the tool call does not return until that subagent has finished, so launches are serialized no matter how many you plan. Size each delegation to be worth waiting for, and do cheap work yourself rather than paying the round trip.
- Never fork yourself, and never let a subagent spawn its own subagents.
- You (the orchestrator) decompose, coordinate, and synthesize; do not redo work you already delegated.
- Verify each result with the smallest reliable check.
</subagent-delegation>
```

### [15] SYSTEM-USER prompt · 2026-09-20 03:11:20 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=0b75a215-b011-44c1-ae88-41510d92b879: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/0b75a215b01144c1ae8841510d92b879

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
Last actions before failure:
  - [agent_system_user_prompt]: <task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize indepe
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<paper_text>
title: Self-Surprisal Hard Prompt Compression
abstract: >-
  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score
  token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ
  from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses
  the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its
  preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy
  mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four
  long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines
  by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical
  significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for
  SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring
  rather than self-surprisal alone.
paper_text: |-
  # Self-Surprisal Hard Prompt Compression

  ## Abstract

  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring rather than self-surprisal alone.

  ## 1 Introduction

  Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increase in length raises inference latency, memory consumption, and API costs proportionally to sequence length.

  Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

  Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

  Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

  We propose Self-Surprisal Hard Prompt Compression (SSHPC), which scores tokens by the target LLM's own next-token surprisal and prunes the lowest-surprisal tokens. At high compression ratios (≥8×), iterative re-scoring adapts to the changed context. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

  [FIGURE:fig1_method]

  Our contributions are:

  1. **Algorithm**: A hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications. At high compression (≥8×), iterative re-scoring adapts to the changed context (Section 3).
  2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
  3. **Empirical evaluation**: Experiments on four benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) with Llama-3-8B, comparing SSHPC against LLMLingua, SelectiveContext, LLMLingua-2, random pruning, and a proxy-on-target ablation, at compression ratios 2×–10×. We measure task accuracy and end-to-end latency (Section 4).
  4. **Ablation studies**: Proxy-mismatch isolation, iterative vs. single-pass at high compression, query-conditioned vs. unconditional surprisal, and latency break-even analysis (Section 4.4).

  ## 2 Related Work

  ### 2.1 Hard Prompt Compression via Proxy Models

  LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

  SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

  All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

  Recent work has explored alternatives. ProCut (Xu et al., 2025) segments prompt templates into semantic units and estimates their attribution via an LLM-driven estimator, achieving 78% token reduction in production. Nano-Capsulator (Chuang et al., 2024) paraphrases prompts into concise natural language using a fine-tuned Vicuna-7B. ASAP (Zeng et al., 2025) uses first-token surprisal for chain-of-thought step pruning with fine-tuning. PIS (Chen et al., 2025) uses attention scores for importance sampling. None uses the target LLM's own next-token logits directly for hard token pruning.

  ### 2.2 Soft Prompt Compression

  GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

  SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

  ### 2.3 Theoretical Frameworks

  Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

  Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

  ## 3 Method

  ### 3.1 Self-Surprisal Hard Prompt Compression

  Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

  $$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

  where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

  **Special token preservation.** Instruction delimiters, `<bos>`, `<eos>`, and other structural tokens are assigned infinite surprisal so they are never pruned.

  Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

  **Iterative re-scoring for high compression.** At compression ratios $r \ge 8$, token predictability changes substantially as surrounding tokens are removed. We therefore iterate: after initial pruning, we recompute surprisal on the compressed prompt $\tilde{\mathbf{x}}$ under the same model $M$ and prune again to the target ratio. We use 3 rounds by default. This is the default for $r \ge 8$; for $r < 8$, single-pass is used.

  **Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step.

  **Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for prompts with an identifiable task specification (question in QA, last user message in chat, instruction prefix in summarization), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{task\_spec})$, so context tokens are scored by how surprising they are given the task. This aligns with LongLLMLingua's finding that question-awareness improves compression. (3) *Attention-weighted SSHPC*: each token's surprisal is weighted by its total attention mass received from subsequent tokens in the final layer, capturing both self-predictability and causal influence.

  [FIGURE:fig1_method]

  ### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

  Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

  Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

  If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

  This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

  ### 3.3 Computational Considerations

  SSHPC requires one forward pass over the full prompt (or multiple passes for iterative re-scoring). For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. We measure actual prefill latency on A100-40GB and compare against generation time savings to determine break-even compression ratios.

  At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

  [FIGURE:fig7_surprisal]

  ## 4 Experiments

  ### 4.1 Datasets and Tasks

  We evaluate on four benchmarks covering diverse long-context tasks [ARTIFACT:art_-Hzqeq6rV9vC]:

  - **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure. Metric: Exact Match.
  - **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies. Metric: F1.
  - **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA with 10 retrieved documents per question. Metric: F1.
  - **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens. Metric: F1/EM/ROUGE-L (task-dependent).

  ### 4.2 Target Models and Baselines

  **Target LLM** (local inference via HuggingFace):
  - Llama-3-8B-Instruct

  **Proxy model for baselines**:
  - GPT-2 (124M parameters) for LLMLingua and SelectiveContext

  **Methods compared**:
  1. **No compression** (full prompt)
  2. **Random pruning**: uniform random token removal
  3. **SelectiveContext** (Li, 2023): self-information from GPT-2 proxy
  4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
  5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
  6. **Proxy-on-Target ablation**: LLMLingua using the *same* target LLM (Llama-3-8B) as the proxy. This isolates the proxy-mismatch effect.
  7. **SSHPC Base**: single-pass self-surprisal, special tokens preserved
  8. **SSHPC Query-Conditioned**: surprisal conditioned on task specification
  9. **SSHPC Attention-Weighted**: surprisal weighted by attention mass
  10. **SSHPC Iterative**: single-pass at 2×, 4×; iterative (3 rounds) at 8×, 10×

  ### 4.3 Compression Ratios and Metrics

  Compression ratios: 2×, 4×, 8×, 10× (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

  **Primary metrics**:
  - Task accuracy (Exact Match for GSM8K, F1 for QA, ROUGE-L for summarization)
  - End-to-end latency (compression + generation) on A100-40GB

  **Secondary metrics**:
  - Compression throughput (tokens/sec for the compression step alone)
  - Surprisal distribution statistics

  ### 4.4 Ablation Studies

  1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the target's own distribution with iterative re-scoring.
  2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
  3. **Single-pass vs. iterative**: At 8× and 10×, compare single-pass SSHPC against iterative (3 rounds).
  4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning against fixed-ratio top-k.

  ## 5 Results

  ### 5.1 Main Results

  Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks and compression ratios. SSHPC Iterative is the best-performing method at 8× and 10× on GSM8K (72.9% and 71.1% EM) and HotpotQA (62.5% and 61.4% F1). At 2× and 4×, all methods including SSHPC Base remain close to the no-compression baseline (within 1–2 points). The gap widens at higher compression: at 10×, SSHPC Iterative leads LLMLingua by 7.4 points on GSM8K and 5.9 points on HotpotQA.

  On NaturalQuestions, SSHPC Base and Iterative match SelectiveContext at 2×–4× (68.5–68.6% F1) and pull ahead at 8× (67.1% vs 61.7%). On LongBench, SSHPC Iterative consistently outperforms baselines, reaching 42.8% at 8× vs 40.4% for LLMLingua.

  Random pruning degrades rapidly, confirming that token importance is non-uniform and methods that exploit it are effective.

  [FIGURE:fig2_main]

  ### 5.2 Proxy-Mismatch Ablation

  [FIGURE:fig3_proxy]

  This indicates that the proxy-mismatch effect, while real, is small in isolation. The larger gains of SSHPC Iterative at high compression come from iterative re-scoring adapting to the changed context, not from self-surprisal being inherently superior to target-model perplexity in a single pass.

  ### 5.3 Iterative Re-Scoring Benefit

  Figure 4 shows the iterative benefit at 8× and 10×. On GSM8K, iterative adds +3.8 points at 8× (p = 0.0001) and +2.2 points at 10× (p = 0.003). On HotpotQA, +2.3 points at 8× (p = 0.04) and +1.6 points at 10× (p = 0.08). On NaturalQuestions, +1.1 points at 8× (p = 0.12) and +3.5 points at 10× (p = 0.02). On LongBench, +0.8 points at 8× (p = 0.21) and +1.2 points at 10× (p = 0.15).

  Iterative re-scoring is most beneficial for reasoning-heavy tasks (GSM8K, HotpotQA) where token dependencies are strong and context changes substantially after pruning.

  [FIGURE:fig4_iterative]

  ### 5.4 Query-Conditioned and Attention-Weighted Variants

  Figure 5 compares SSHPC variants at 8×. Query-conditioned SSHPC improves over Base on NaturalQuestions (+1.6 points) and HotpotQA (+2.2 points) where a clear question exists. On GSM8K (no explicit question), it matches Base. Attention-weighted SSHPC improves on GSM8K (+2.6 points) and HotpotQA (+1.9 points) but not on LongBench. The best variant is task-dependent: Iterative dominates on GSM8K and HotpotQA; Query-Conditioned leads on NaturalQuestions.

  [FIGURE:fig5_variants]

  ### 5.5 Latency Break-Even

  Figure 6 shows end-to-end latency vs. compression ratio. For all methods, break-even (compression overhead equals generation time saved) occurs at 2×. At 2×, compression adds ~2.5s prefill but saves ~2.5s generation, yielding net parity. At 4× and above, all methods show net latency reduction. SSHPC Base adds ~5–10ms overhead per 1000 tokens vs. GPT-2-based methods, but this is negligible compared to generation savings at high compression. The break-even ratio of 2× holds across all benchmarks.

  [FIGURE:fig6_latency]

  [ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:art_Lm_O96s-n8rb]

  ## 6 Discussion

  ### 6.1 Summary of Findings

  1. **Self-surprisal works**: SSHPC Base matches or exceeds proxy-based baselines across all benchmarks, with larger margins at high compression.
  2. **Iterative re-scoring is critical at ≥8×**: It provides statistically significant gains on reasoning tasks (GSM8K, HotpotQA) by adapting to the changed context after pruning.
  3. **Proxy mismatch is real but small in isolation**: When the proxy is the target model, SSHPC's single-pass advantage is 0.48% on average and not significant. The practical gains come from iterative re-scoring, which proxy methods do not naturally support because they condition on the *original* context during iterative compression.
  4. **Query conditioning helps when a question exists**: On QA tasks, conditioning surprisal on the question improves pruning decisions.
  5. **Latency break-even at 2×**: All methods including SSHPC become net-positive at 2× compression on A100.

  ### 6.2 Limitations

  **Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (OpenAI's `logprobs`), but not all. For fully black-box APIs, proxy methods remain the only option.

  **Single-pass context dependence**: At high compression, single-pass surprisal computed on the full prompt becomes stale. We address this with iterative re-scoring as the default for r ≥ 8, but this multiplies compression latency by the number of rounds (3× in our experiments).

  **First-token handling**: The first token uses the unconditional distribution, which may not reflect its importance. We mitigate this by always preserving special/instruction tokens via infinite surprisal assignment. An alternative would use bidirectional pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy model.

  **Query-conditioning generality**: Our heuristic for extracting the "task specification" (last user message, question, instruction prefix) works for standard prompt templates but may fail for unusual formats. A more robust approach would use an instruction-following model to identify the task specification automatically.

  **Single target model**: We evaluate only on Llama-3-8B-Instruct. The method should transfer to other open-weight models (Qwen2, Mistral), but the exact break-even ratios and iterative benefits may vary with model architecture and size.

  **Synthetic surprisal distributions**: The surprisal distribution in Figure 7 is synthetic (generated from a log-normal fit to pilot data). Real distributions from Llama-3-8B would provide stronger evidence but require additional computation.

  ### 6.3 Broader Implications

  If self-surprisal with iterative re-scoring proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression—no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error, applied iteratively. SSHPC operationalizes this principle for hard token pruning.

  The negative result on proxy-mismatch (when the proxy *is* the target) is informative: it suggests that LLMLingua's iterative compression already approximates the target model's preferences reasonably well when the proxy is large and aligned. The remaining gap at high compression comes from LLMLingua conditioning on the *original* context during re-scoring, whereas SSHPC re-scores on the *compressed* context, which is what the target will actually see.

  ## 7 Conclusion

  We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token prediction logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation on four long-context benchmarks with Llama-3-8B shows that SSHPC Base outperforms proxy baselines at high compression, and iterative re-scoring (default for r ≥ 8×) provides statistically significant additional gains of 1.8–3.8 points on reasoning tasks. The proxy-mismatch ablation reveals that self-surprisal alone provides only a marginal (0.48%, not significant) advantage over target-model perplexity; the practical gains come from iterative adaptation to the compressed context. Latency break-even occurs at 2× compression for all methods. Future work includes extending to multiple target models, chunked computation for >8k tokens, and automatic task-specification extraction for query conditioning.

  ---

  ## Bibliography

  \bibliography{references}
  \bibliographystyle{plainnat}
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token logits to compute per-token surprisal
  for hard prompt pruning. Evaluated on 4 benchmarks with Llama-3-8B at 2x-10x compression. SSHPC Iterative (with re-scoring
  at >=8x) outperforms proxy baselines by 2-5 points at high compression. Key finding: proxy-mismatch effect is small (0.48%,
  ns) in isolation; gains come from iterative re-scoring adapting to compressed context. Latency break-even at 2x.
</paper_text>

<available_figures>
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig2_main_v0.png [render from fig2_main_v0.pdf first] — "Task Accuracy Across Benchmarks and Compression Ratios" (caption: "Task accuracy (%) across four benchmarks and four compression ratios (2×, 4×, 8×, 10×) for six methods. SSHPC Iterative (solid green) consistently outperforms baselines at high compression. LLMLingua (blue) and SelectiveContext (orange) degrade faster than SSHPC variants. No Compression (black) is the upper bound. Random Pruning (gray) degrades rapidly. Error bars show 95% bootstrap confidence intervals (10,000 resamples).")
- figures/fig3_proxy_v0.png [render from fig3_proxy_v0.pdf first] — "Proxy-Mismatch Ablation: SSHPC vs Proxy-on-Target" (caption: "Accuracy difference (SSHPC Base minus Proxy-on-Target) across 16 dataset–ratio conditions. Positive values favor SSHPC. The average improvement is +0.48% (not statistically significant, p > 0.05). Error bars show standard error (1.5%). Conditions: GSM8K 2×–10×, HotpotQA 2×–10×, NaturalQuestions 2×–10×, LongBench 2×–10×.")
- figures/fig4_iterative_v0.png [render from fig4_iterative_v0.pdf first] — "Iterative Re-Scoring Benefit at High Compression" (caption: "Dumbbell chart comparing single-pass vs iterative (3 rounds) SSHPC at 8× and 10× compression. Iterative re-scoring provides significant gains on GSM8K (+3.8 at 8×, p=0.0001) and HotpotQA (+2.3 at 8×, p=0.04), moderate gains on NaturalQuestions, and smaller non-significant gains on LongBench. Single-pass values are constant at 70% (baseline reference).")
- figures/fig5_variants_v0.png [render from fig5_variants_v0.pdf first] — "SSHPC Variant Comparison at 8× Compression" (caption: "Comparison of four SSHPC variants at 8× compression across four datasets. Iterative (green) leads on GSM8K (72.9%) and HotpotQA (62.5%). Query-Conditioned (orange) leads on NaturalQuestions (67.6%). Attention-Weighted (purple) is competitive on GSM8K (71.7%) and HotpotQA (62.2%). Base (blue) is the single-pass unconditional variant. Error bars show 95% CI.")
- figures/fig6_latency_v0.png [render from fig6_latency_v0.pdf first] — "End-to-End Latency vs Compression Ratio" (caption: "End-to-end latency (compression + generation) vs compression ratio for four methods. Break-even occurs at 2× for all methods. At 2×, latency ~2500ms; at 4×, ~1250ms; at 8×, ~625ms; at 10×, ~500ms. SSHPC Base (green) and Iterative (purple) overlap with LLMLingua (blue) and No Compression (black) within error bands. Shaded bands show standard deviation across datasets.")
- figures/fig7_surprisal_v0.png [render from fig7_surprisal_v0.pdf first] — "Per-Token Surprisal Distribution (Synthetic)" (caption: "Violin plot of per-token surprisal distribution for GSM8K (synthetic data from log-normal fit to pilot runs). Surprisal values range from near 0 to ~16, with a long right tail. Median ~1.5, mean ~3.2. The distribution is highly skewed, confirming that most tokens are predictable (low surprisal) while a few carry high information.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNG files into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [16] HUMAN-USER prompt · 2026-09-20 03:11:20 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```

### [17] RETRY (attempt 3) · 2026-09-20 03:12:03 UTC

```
Agent result indicates failure (attempt 3/6): Conversation run failed for id=107b816b-b5bf-43d1-8c15-c777e1aa5aab: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/107b816bb5bf43d18c15c777e1aa5aab

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [18] RETRY (attempt 4) · 2026-09-20 03:12:04 UTC

```
Agent retry... (attempt 4/6): Conversation run failed for id=107b816b-b5bf-43d1-8c15-c777e1aa5aab: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/107b816bb5bf43d18c15c777e1aa5aab

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [19] CONFIG · 2026-09-20 03:12:04 UTC

```
Model: Free tier (no preference) | Session: 90d8e9c0-17d3-48cf-b63f-6b33869fbfe7 | Tools: 4 | Permission: acceptEdits
```

### [20] SYSTEM PROMPT · 2026-09-20 03:12:06 UTC

```
<design_philosophy>
You are building ONE web page whose only job is to let a reader understand a research paper faster
than they could by opening the PDF. Every decision on the page is judged against that.

WHAT "FASTER" MEANS HERE
- A reader who leaves after thirty seconds still knows the finding and the number behind it.
- A reader who stays five minutes has the method, the figures and the caveats, in that order.
- Nothing on the page is there because a layout had a slot for it.

ACCURACY IS THE HARD CONSTRAINT
Every number, name and claim comes from the paper as written — you read them out of the LaTeX
source and the run's own data files. You never change a number's precision, never restate a
comparison the paper did not make, and never invent a headline figure to fill a card. A page that
looks excellent and misreports one result is worse than no page, because the PDF beside it says
something else and a reader will find that out.

CRAFT, AND THE LOOK TO AVOID
The failure mode for a generated page is a look every reader now recognises on sight: a
purple-to-blue gradient banner, three identical cards with emoji headings, and body text set in
one weight at one size. Avoid all of it.
- Type carries the design. One system font stack, a real scale with visible jumps between levels
  rather than a creep of similar sizes, long-form text around 17-19px with a measure of 65-75
  characters and generous line height. Weight and size do the emphasis; colour rarely does.
- Colour is restrained. A light, near-white ground, one dark ink for text, one accent used for
  links and the current-section marker and almost nothing else. No gradients as decoration.
- Space does the work that borders and boxes would do badly. Sections separated by real vertical
  rhythm, cards defined by alignment and a single hairline rather than by shadow stacks.
- Structure over ornament: no emoji as section markers, no icon fonts, no badge clutter, no
  animated counters.
- Motion is a courtesy. A short transition on a lightbox or a hover state is welcome; anything
  that moves on scroll, autoplays, or delays the reader is not — and all of it stops under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and says what it is to a screen reader. That is
  part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a browser, read it at a phone width and a desktop
width, tabbed through every control, and found nothing to fix. Not before.
</design_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<subagent-delegation>
You may delegate bounded work to subagents (e.g. the Task tool). Delegate by default rather than doing everything yourself:

- Pick the cheapest capable model available to you for each subagent launch:
- Pass `subagent_type="tier-easy"` (steered toward `cohere/north-mini-code:free`) for a small/fast tier for mechanical work.
- Pass `subagent_type="tier-medium"` (steered toward `cohere/north-mini-code:free`) for a mid tier for implementation or investigation (the default).
- Pass `subagent_type="tier-hard"` (steered toward `google/gemma-4-31b-it:free`) for the strongest tier only for hard reasoning or after a cheaper model has already failed on the same task.
- Give each subagent prompt one focused objective: exact scope, the acceptance check, and the required output format.
- Subagents report back only the result, changed files, verification, and blockers — not narration or full logs.
- Delegations on this backend BLOCK: the tool call does not return until that subagent has finished, so launches are serialized no matter how many you plan. Size each delegation to be worth waiting for, and do cheap work yourself rather than paying the round trip.
- Never fork yourself, and never let a subagent spawn its own subagents.
- You (the orchestrator) decompose, coordinate, and synthesize; do not redo work you already delegated.
- Verify each result with the smallest reliable check.
</subagent-delegation>
```

### [21] SYSTEM-USER prompt · 2026-09-20 03:12:06 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=107b816b-b5bf-43d1-8c15-c777e1aa5aab: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/107b816bb5bf43d18c15c777e1aa5aab

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
Last actions before failure:
  - [agent_system_user_prompt]: <task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize indepe
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=0b75a215-b011-44c1-ae88-41510d92b879: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/0b75a215b01144c1ae88415
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<paper_text>
title: Self-Surprisal Hard Prompt Compression
abstract: >-
  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score
  token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ
  from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses
  the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its
  preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy
  mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four
  long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines
  by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical
  significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for
  SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring
  rather than self-surprisal alone.
paper_text: |-
  # Self-Surprisal Hard Prompt Compression

  ## Abstract

  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring rather than self-surprisal alone.

  ## 1 Introduction

  Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increase in length raises inference latency, memory consumption, and API costs proportionally to sequence length.

  Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

  Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

  Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

  We propose Self-Surprisal Hard Prompt Compression (SSHPC), which scores tokens by the target LLM's own next-token surprisal and prunes the lowest-surprisal tokens. At high compression ratios (≥8×), iterative re-scoring adapts to the changed context. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

  [FIGURE:fig1_method]

  Our contributions are:

  1. **Algorithm**: A hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications. At high compression (≥8×), iterative re-scoring adapts to the changed context (Section 3).
  2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
  3. **Empirical evaluation**: Experiments on four benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) with Llama-3-8B, comparing SSHPC against LLMLingua, SelectiveContext, LLMLingua-2, random pruning, and a proxy-on-target ablation, at compression ratios 2×–10×. We measure task accuracy and end-to-end latency (Section 4).
  4. **Ablation studies**: Proxy-mismatch isolation, iterative vs. single-pass at high compression, query-conditioned vs. unconditional surprisal, and latency break-even analysis (Section 4.4).

  ## 2 Related Work

  ### 2.1 Hard Prompt Compression via Proxy Models

  LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

  SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

  All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

  Recent work has explored alternatives. ProCut (Xu et al., 2025) segments prompt templates into semantic units and estimates their attribution via an LLM-driven estimator, achieving 78% token reduction in production. Nano-Capsulator (Chuang et al., 2024) paraphrases prompts into concise natural language using a fine-tuned Vicuna-7B. ASAP (Zeng et al., 2025) uses first-token surprisal for chain-of-thought step pruning with fine-tuning. PIS (Chen et al., 2025) uses attention scores for importance sampling. None uses the target LLM's own next-token logits directly for hard token pruning.

  ### 2.2 Soft Prompt Compression

  GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

  SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

  ### 2.3 Theoretical Frameworks

  Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

  Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

  ## 3 Method

  ### 3.1 Self-Surprisal Hard Prompt Compression

  Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

  $$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

  where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

  **Special token preservation.** Instruction delimiters, `<bos>`, `<eos>`, and other structural tokens are assigned infinite surprisal so they are never pruned.

  Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

  **Iterative re-scoring for high compression.** At compression ratios $r \ge 8$, token predictability changes substantially as surrounding tokens are removed. We therefore iterate: after initial pruning, we recompute surprisal on the compressed prompt $\tilde{\mathbf{x}}$ under the same model $M$ and prune again to the target ratio. We use 3 rounds by default. This is the default for $r \ge 8$; for $r < 8$, single-pass is used.

  **Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step.

  **Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for prompts with an identifiable task specification (question in QA, last user message in chat, instruction prefix in summarization), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{task\_spec})$, so context tokens are scored by how surprising they are given the task. This aligns with LongLLMLingua's finding that question-awareness improves compression. (3) *Attention-weighted SSHPC*: each token's surprisal is weighted by its total attention mass received from subsequent tokens in the final layer, capturing both self-predictability and causal influence.

  [FIGURE:fig1_method]

  ### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

  Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

  Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

  If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

  This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

  ### 3.3 Computational Considerations

  SSHPC requires one forward pass over the full prompt (or multiple passes for iterative re-scoring). For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. We measure actual prefill latency on A100-40GB and compare against generation time savings to determine break-even compression ratios.

  At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

  [FIGURE:fig7_surprisal]

  ## 4 Experiments

  ### 4.1 Datasets and Tasks

  We evaluate on four benchmarks covering diverse long-context tasks [ARTIFACT:art_-Hzqeq6rV9vC]:

  - **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure. Metric: Exact Match.
  - **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies. Metric: F1.
  - **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA with 10 retrieved documents per question. Metric: F1.
  - **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens. Metric: F1/EM/ROUGE-L (task-dependent).

  ### 4.2 Target Models and Baselines

  **Target LLM** (local inference via HuggingFace):
  - Llama-3-8B-Instruct

  **Proxy model for baselines**:
  - GPT-2 (124M parameters) for LLMLingua and SelectiveContext

  **Methods compared**:
  1. **No compression** (full prompt)
  2. **Random pruning**: uniform random token removal
  3. **SelectiveContext** (Li, 2023): self-information from GPT-2 proxy
  4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
  5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
  6. **Proxy-on-Target ablation**: LLMLingua using the *same* target LLM (Llama-3-8B) as the proxy. This isolates the proxy-mismatch effect.
  7. **SSHPC Base**: single-pass self-surprisal, special tokens preserved
  8. **SSHPC Query-Conditioned**: surprisal conditioned on task specification
  9. **SSHPC Attention-Weighted**: surprisal weighted by attention mass
  10. **SSHPC Iterative**: single-pass at 2×, 4×; iterative (3 rounds) at 8×, 10×

  ### 4.3 Compression Ratios and Metrics

  Compression ratios: 2×, 4×, 8×, 10× (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

  **Primary metrics**:
  - Task accuracy (Exact Match for GSM8K, F1 for QA, ROUGE-L for summarization)
  - End-to-end latency (compression + generation) on A100-40GB

  **Secondary metrics**:
  - Compression throughput (tokens/sec for the compression step alone)
  - Surprisal distribution statistics

  ### 4.4 Ablation Studies

  1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the target's own distribution with iterative re-scoring.
  2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
  3. **Single-pass vs. iterative**: At 8× and 10×, compare single-pass SSHPC against iterative (3 rounds).
  4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning against fixed-ratio top-k.

  ## 5 Results

  ### 5.1 Main Results

  Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks and compression ratios. SSHPC Iterative is the best-performing method at 8× and 10× on GSM8K (72.9% and 71.1% EM) and HotpotQA (62.5% and 61.4% F1). At 2× and 4×, all methods including SSHPC Base remain close to the no-compression baseline (within 1–2 points). The gap widens at higher compression: at 10×, SSHPC Iterative leads LLMLingua by 7.4 points on GSM8K and 5.9 points on HotpotQA.

  On NaturalQuestions, SSHPC Base and Iterative match SelectiveContext at 2×–4× (68.5–68.6% F1) and pull ahead at 8× (67.1% vs 61.7%). On LongBench, SSHPC Iterative consistently outperforms baselines, reaching 42.8% at 8× vs 40.4% for LLMLingua.

  Random pruning degrades rapidly, confirming that token importance is non-uniform and methods that exploit it are effective.

  [FIGURE:fig2_main]

  ### 5.2 Proxy-Mismatch Ablation

  [FIGURE:fig3_proxy]

  This indicates that the proxy-mismatch effect, while real, is small in isolation. The larger gains of SSHPC Iterative at high compression come from iterative re-scoring adapting to the changed context, not from self-surprisal being inherently superior to target-model perplexity in a single pass.

  ### 5.3 Iterative Re-Scoring Benefit

  Figure 4 shows the iterative benefit at 8× and 10×. On GSM8K, iterative adds +3.8 points at 8× (p = 0.0001) and +2.2 points at 10× (p = 0.003). On HotpotQA, +2.3 points at 8× (p = 0.04) and +1.6 points at 10× (p = 0.08). On NaturalQuestions, +1.1 points at 8× (p = 0.12) and +3.5 points at 10× (p = 0.02). On LongBench, +0.8 points at 8× (p = 0.21) and +1.2 points at 10× (p = 0.15).

  Iterative re-scoring is most beneficial for reasoning-heavy tasks (GSM8K, HotpotQA) where token dependencies are strong and context changes substantially after pruning.

  [FIGURE:fig4_iterative]

  ### 5.4 Query-Conditioned and Attention-Weighted Variants

  Figure 5 compares SSHPC variants at 8×. Query-conditioned SSHPC improves over Base on NaturalQuestions (+1.6 points) and HotpotQA (+2.2 points) where a clear question exists. On GSM8K (no explicit question), it matches Base. Attention-weighted SSHPC improves on GSM8K (+2.6 points) and HotpotQA (+1.9 points) but not on LongBench. The best variant is task-dependent: Iterative dominates on GSM8K and HotpotQA; Query-Conditioned leads on NaturalQuestions.

  [FIGURE:fig5_variants]

  ### 5.5 Latency Break-Even

  Figure 6 shows end-to-end latency vs. compression ratio. For all methods, break-even (compression overhead equals generation time saved) occurs at 2×. At 2×, compression adds ~2.5s prefill but saves ~2.5s generation, yielding net parity. At 4× and above, all methods show net latency reduction. SSHPC Base adds ~5–10ms overhead per 1000 tokens vs. GPT-2-based methods, but this is negligible compared to generation savings at high compression. The break-even ratio of 2× holds across all benchmarks.

  [FIGURE:fig6_latency]

  [ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:art_Lm_O96s-n8rb]

  ## 6 Discussion

  ### 6.1 Summary of Findings

  1. **Self-surprisal works**: SSHPC Base matches or exceeds proxy-based baselines across all benchmarks, with larger margins at high compression.
  2. **Iterative re-scoring is critical at ≥8×**: It provides statistically significant gains on reasoning tasks (GSM8K, HotpotQA) by adapting to the changed context after pruning.
  3. **Proxy mismatch is real but small in isolation**: When the proxy is the target model, SSHPC's single-pass advantage is 0.48% on average and not significant. The practical gains come from iterative re-scoring, which proxy methods do not naturally support because they condition on the *original* context during iterative compression.
  4. **Query conditioning helps when a question exists**: On QA tasks, conditioning surprisal on the question improves pruning decisions.
  5. **Latency break-even at 2×**: All methods including SSHPC become net-positive at 2× compression on A100.

  ### 6.2 Limitations

  **Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (OpenAI's `logprobs`), but not all. For fully black-box APIs, proxy methods remain the only option.

  **Single-pass context dependence**: At high compression, single-pass surprisal computed on the full prompt becomes stale. We address this with iterative re-scoring as the default for r ≥ 8, but this multiplies compression latency by the number of rounds (3× in our experiments).

  **First-token handling**: The first token uses the unconditional distribution, which may not reflect its importance. We mitigate this by always preserving special/instruction tokens via infinite surprisal assignment. An alternative would use bidirectional pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy model.

  **Query-conditioning generality**: Our heuristic for extracting the "task specification" (last user message, question, instruction prefix) works for standard prompt templates but may fail for unusual formats. A more robust approach would use an instruction-following model to identify the task specification automatically.

  **Single target model**: We evaluate only on Llama-3-8B-Instruct. The method should transfer to other open-weight models (Qwen2, Mistral), but the exact break-even ratios and iterative benefits may vary with model architecture and size.

  **Synthetic surprisal distributions**: The surprisal distribution in Figure 7 is synthetic (generated from a log-normal fit to pilot data). Real distributions from Llama-3-8B would provide stronger evidence but require additional computation.

  ### 6.3 Broader Implications

  If self-surprisal with iterative re-scoring proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression—no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error, applied iteratively. SSHPC operationalizes this principle for hard token pruning.

  The negative result on proxy-mismatch (when the proxy *is* the target) is informative: it suggests that LLMLingua's iterative compression already approximates the target model's preferences reasonably well when the proxy is large and aligned. The remaining gap at high compression comes from LLMLingua conditioning on the *original* context during re-scoring, whereas SSHPC re-scores on the *compressed* context, which is what the target will actually see.

  ## 7 Conclusion

  We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token prediction logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation on four long-context benchmarks with Llama-3-8B shows that SSHPC Base outperforms proxy baselines at high compression, and iterative re-scoring (default for r ≥ 8×) provides statistically significant additional gains of 1.8–3.8 points on reasoning tasks. The proxy-mismatch ablation reveals that self-surprisal alone provides only a marginal (0.48%, not significant) advantage over target-model perplexity; the practical gains come from iterative adaptation to the compressed context. Latency break-even occurs at 2× compression for all methods. Future work includes extending to multiple target models, chunked computation for >8k tokens, and automatic task-specification extraction for query conditioning.

  ---

  ## Bibliography

  \bibliography{references}
  \bibliographystyle{plainnat}
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token logits to compute per-token surprisal
  for hard prompt pruning. Evaluated on 4 benchmarks with Llama-3-8B at 2x-10x compression. SSHPC Iterative (with re-scoring
  at >=8x) outperforms proxy baselines by 2-5 points at high compression. Key finding: proxy-mismatch effect is small (0.48%,
  ns) in isolation; gains come from iterative re-scoring adapting to compressed context. Latency break-even at 2x.
</paper_text>

<available_figures>
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig2_main_v0.png [render from fig2_main_v0.pdf first] — "Task Accuracy Across Benchmarks and Compression Ratios" (caption: "Task accuracy (%) across four benchmarks and four compression ratios (2×, 4×, 8×, 10×) for six methods. SSHPC Iterative (solid green) consistently outperforms baselines at high compression. LLMLingua (blue) and SelectiveContext (orange) degrade faster than SSHPC variants. No Compression (black) is the upper bound. Random Pruning (gray) degrades rapidly. Error bars show 95% bootstrap confidence intervals (10,000 resamples).")
- figures/fig3_proxy_v0.png [render from fig3_proxy_v0.pdf first] — "Proxy-Mismatch Ablation: SSHPC vs Proxy-on-Target" (caption: "Accuracy difference (SSHPC Base minus Proxy-on-Target) across 16 dataset–ratio conditions. Positive values favor SSHPC. The average improvement is +0.48% (not statistically significant, p > 0.05). Error bars show standard error (1.5%). Conditions: GSM8K 2×–10×, HotpotQA 2×–10×, NaturalQuestions 2×–10×, LongBench 2×–10×.")
- figures/fig4_iterative_v0.png [render from fig4_iterative_v0.pdf first] — "Iterative Re-Scoring Benefit at High Compression" (caption: "Dumbbell chart comparing single-pass vs iterative (3 rounds) SSHPC at 8× and 10× compression. Iterative re-scoring provides significant gains on GSM8K (+3.8 at 8×, p=0.0001) and HotpotQA (+2.3 at 8×, p=0.04), moderate gains on NaturalQuestions, and smaller non-significant gains on LongBench. Single-pass values are constant at 70% (baseline reference).")
- figures/fig5_variants_v0.png [render from fig5_variants_v0.pdf first] — "SSHPC Variant Comparison at 8× Compression" (caption: "Comparison of four SSHPC variants at 8× compression across four datasets. Iterative (green) leads on GSM8K (72.9%) and HotpotQA (62.5%). Query-Conditioned (orange) leads on NaturalQuestions (67.6%). Attention-Weighted (purple) is competitive on GSM8K (71.7%) and HotpotQA (62.2%). Base (blue) is the single-pass unconditional variant. Error bars show 95% CI.")
- figures/fig6_latency_v0.png [render from fig6_latency_v0.pdf first] — "End-to-End Latency vs Compression Ratio" (caption: "End-to-end latency (compression + generation) vs compression ratio for four methods. Break-even occurs at 2× for all methods. At 2×, latency ~2500ms; at 4×, ~1250ms; at 8×, ~625ms; at 10×, ~500ms. SSHPC Base (green) and Iterative (purple) overlap with LLMLingua (blue) and No Compression (black) within error bands. Shaded bands show standard deviation across datasets.")
- figures/fig7_surprisal_v0.png [render from fig7_surprisal_v0.pdf first] — "Per-Token Surprisal Distribution (Synthetic)" (caption: "Violin plot of per-token surprisal distribution for GSM8K (synthetic data from log-normal fit to pilot runs). Surprisal values range from near 0 to ~16, with a long right tail. Median ~1.5, mean ~3.2. The distribution is highly skewed, confirming that most tokens are predictable (low surprisal) while a few carry high information.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNG files into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [22] HUMAN-USER prompt · 2026-09-20 03:12:06 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```

### [23] RETRY (attempt 4) · 2026-09-20 03:13:24 UTC

```
Agent result indicates failure (attempt 4/6): Conversation run failed for id=90d8e9c0-17d3-48cf-b63f-6b33869fbfe7: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/90d8e9c017d348cfb63f6b33869fbfe7

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [24] RETRY (attempt 5) · 2026-09-20 03:13:24 UTC

```
Agent retry... (attempt 5/6): Conversation run failed for id=90d8e9c0-17d3-48cf-b63f-6b33869fbfe7: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/90d8e9c017d348cfb63f6b33869fbfe7

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [25] CONFIG · 2026-09-20 03:13:24 UTC

```
Model: Free tier (no preference) | Session: 9884d036-d35d-480a-a32f-f89efed04ce4 | Tools: 4 | Permission: acceptEdits
```

### [26] SYSTEM PROMPT · 2026-09-20 03:13:26 UTC

```
<design_philosophy>
You are building ONE web page whose only job is to let a reader understand a research paper faster
than they could by opening the PDF. Every decision on the page is judged against that.

WHAT "FASTER" MEANS HERE
- A reader who leaves after thirty seconds still knows the finding and the number behind it.
- A reader who stays five minutes has the method, the figures and the caveats, in that order.
- Nothing on the page is there because a layout had a slot for it.

ACCURACY IS THE HARD CONSTRAINT
Every number, name and claim comes from the paper as written — you read them out of the LaTeX
source and the run's own data files. You never change a number's precision, never restate a
comparison the paper did not make, and never invent a headline figure to fill a card. A page that
looks excellent and misreports one result is worse than no page, because the PDF beside it says
something else and a reader will find that out.

CRAFT, AND THE LOOK TO AVOID
The failure mode for a generated page is a look every reader now recognises on sight: a
purple-to-blue gradient banner, three identical cards with emoji headings, and body text set in
one weight at one size. Avoid all of it.
- Type carries the design. One system font stack, a real scale with visible jumps between levels
  rather than a creep of similar sizes, long-form text around 17-19px with a measure of 65-75
  characters and generous line height. Weight and size do the emphasis; colour rarely does.
- Colour is restrained. A light, near-white ground, one dark ink for text, one accent used for
  links and the current-section marker and almost nothing else. No gradients as decoration.
- Space does the work that borders and boxes would do badly. Sections separated by real vertical
  rhythm, cards defined by alignment and a single hairline rather than by shadow stacks.
- Structure over ornament: no emoji as section markers, no icon fonts, no badge clutter, no
  animated counters.
- Motion is a courtesy. A short transition on a lightbox or a hover state is welcome; anything
  that moves on scroll, autoplays, or delays the reader is not — and all of it stops under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and says what it is to a screen reader. That is
  part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a browser, read it at a phone width and a desktop
width, tabbed through every control, and found nothing to fix. Not before.
</design_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<subagent-delegation>
You may delegate bounded work to subagents (e.g. the Task tool). Delegate by default rather than doing everything yourself:

- Pick the cheapest capable model available to you for each subagent launch:
- Pass `subagent_type="tier-easy"` (steered toward `cohere/north-mini-code:free`) for a small/fast tier for mechanical work.
- Pass `subagent_type="tier-medium"` (steered toward `cohere/north-mini-code:free`) for a mid tier for implementation or investigation (the default).
- Pass `subagent_type="tier-hard"` (steered toward `google/gemma-4-31b-it:free`) for the strongest tier only for hard reasoning or after a cheaper model has already failed on the same task.
- Give each subagent prompt one focused objective: exact scope, the acceptance check, and the required output format.
- Subagents report back only the result, changed files, verification, and blockers — not narration or full logs.
- Delegations on this backend BLOCK: the tool call does not return until that subagent has finished, so launches are serialized no matter how many you plan. Size each delegation to be worth waiting for, and do cheap work yourself rather than paying the round trip.
- Never fork yourself, and never let a subagent spawn its own subagents.
- You (the orchestrator) decompose, coordinate, and synthesize; do not redo work you already delegated.
- Verify each result with the smallest reliable check.
</subagent-delegation>
```

### [27] SYSTEM-USER prompt · 2026-09-20 03:13:26 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=90d8e9c0-17d3-48cf-b63f-6b33869fbfe7: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/90d8e9c017d348cfb63f6b33869fbfe7

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
Last actions before failure:
  - [agent_system_user_prompt]: <task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize indepe
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=0b75a215-b011-44c1-ae88-41510d92b879: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/0b75a215b01144c1ae88415
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=107b816b-b5bf-43d1-8c15-c777e1aa5aab: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/107b816bb5bf43d18c15c77
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<paper_text>
title: Self-Surprisal Hard Prompt Compression
abstract: >-
  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score
  token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ
  from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses
  the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its
  preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy
  mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four
  long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines
  by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical
  significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for
  SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring
  rather than self-surprisal alone.
paper_text: |-
  # Self-Surprisal Hard Prompt Compression

  ## Abstract

  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring rather than self-surprisal alone.

  ## 1 Introduction

  Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increase in length raises inference latency, memory consumption, and API costs proportionally to sequence length.

  Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

  Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

  Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

  We propose Self-Surprisal Hard Prompt Compression (SSHPC), which scores tokens by the target LLM's own next-token surprisal and prunes the lowest-surprisal tokens. At high compression ratios (≥8×), iterative re-scoring adapts to the changed context. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

  [FIGURE:fig1_method]

  Our contributions are:

  1. **Algorithm**: A hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications. At high compression (≥8×), iterative re-scoring adapts to the changed context (Section 3).
  2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
  3. **Empirical evaluation**: Experiments on four benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) with Llama-3-8B, comparing SSHPC against LLMLingua, SelectiveContext, LLMLingua-2, random pruning, and a proxy-on-target ablation, at compression ratios 2×–10×. We measure task accuracy and end-to-end latency (Section 4).
  4. **Ablation studies**: Proxy-mismatch isolation, iterative vs. single-pass at high compression, query-conditioned vs. unconditional surprisal, and latency break-even analysis (Section 4.4).

  ## 2 Related Work

  ### 2.1 Hard Prompt Compression via Proxy Models

  LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

  SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

  All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

  Recent work has explored alternatives. ProCut (Xu et al., 2025) segments prompt templates into semantic units and estimates their attribution via an LLM-driven estimator, achieving 78% token reduction in production. Nano-Capsulator (Chuang et al., 2024) paraphrases prompts into concise natural language using a fine-tuned Vicuna-7B. ASAP (Zeng et al., 2025) uses first-token surprisal for chain-of-thought step pruning with fine-tuning. PIS (Chen et al., 2025) uses attention scores for importance sampling. None uses the target LLM's own next-token logits directly for hard token pruning.

  ### 2.2 Soft Prompt Compression

  GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

  SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

  ### 2.3 Theoretical Frameworks

  Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

  Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

  ## 3 Method

  ### 3.1 Self-Surprisal Hard Prompt Compression

  Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

  $$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

  where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

  **Special token preservation.** Instruction delimiters, `<bos>`, `<eos>`, and other structural tokens are assigned infinite surprisal so they are never pruned.

  Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

  **Iterative re-scoring for high compression.** At compression ratios $r \ge 8$, token predictability changes substantially as surrounding tokens are removed. We therefore iterate: after initial pruning, we recompute surprisal on the compressed prompt $\tilde{\mathbf{x}}$ under the same model $M$ and prune again to the target ratio. We use 3 rounds by default. This is the default for $r \ge 8$; for $r < 8$, single-pass is used.

  **Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step.

  **Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for prompts with an identifiable task specification (question in QA, last user message in chat, instruction prefix in summarization), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{task\_spec})$, so context tokens are scored by how surprising they are given the task. This aligns with LongLLMLingua's finding that question-awareness improves compression. (3) *Attention-weighted SSHPC*: each token's surprisal is weighted by its total attention mass received from subsequent tokens in the final layer, capturing both self-predictability and causal influence.

  [FIGURE:fig1_method]

  ### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

  Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

  Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

  If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

  This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

  ### 3.3 Computational Considerations

  SSHPC requires one forward pass over the full prompt (or multiple passes for iterative re-scoring). For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. We measure actual prefill latency on A100-40GB and compare against generation time savings to determine break-even compression ratios.

  At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

  [FIGURE:fig7_surprisal]

  ## 4 Experiments

  ### 4.1 Datasets and Tasks

  We evaluate on four benchmarks covering diverse long-context tasks [ARTIFACT:art_-Hzqeq6rV9vC]:

  - **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure. Metric: Exact Match.
  - **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies. Metric: F1.
  - **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA with 10 retrieved documents per question. Metric: F1.
  - **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens. Metric: F1/EM/ROUGE-L (task-dependent).

  ### 4.2 Target Models and Baselines

  **Target LLM** (local inference via HuggingFace):
  - Llama-3-8B-Instruct

  **Proxy model for baselines**:
  - GPT-2 (124M parameters) for LLMLingua and SelectiveContext

  **Methods compared**:
  1. **No compression** (full prompt)
  2. **Random pruning**: uniform random token removal
  3. **SelectiveContext** (Li, 2023): self-information from GPT-2 proxy
  4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
  5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
  6. **Proxy-on-Target ablation**: LLMLingua using the *same* target LLM (Llama-3-8B) as the proxy. This isolates the proxy-mismatch effect.
  7. **SSHPC Base**: single-pass self-surprisal, special tokens preserved
  8. **SSHPC Query-Conditioned**: surprisal conditioned on task specification
  9. **SSHPC Attention-Weighted**: surprisal weighted by attention mass
  10. **SSHPC Iterative**: single-pass at 2×, 4×; iterative (3 rounds) at 8×, 10×

  ### 4.3 Compression Ratios and Metrics

  Compression ratios: 2×, 4×, 8×, 10× (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

  **Primary metrics**:
  - Task accuracy (Exact Match for GSM8K, F1 for QA, ROUGE-L for summarization)
  - End-to-end latency (compression + generation) on A100-40GB

  **Secondary metrics**:
  - Compression throughput (tokens/sec for the compression step alone)
  - Surprisal distribution statistics

  ### 4.4 Ablation Studies

  1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the target's own distribution with iterative re-scoring.
  2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
  3. **Single-pass vs. iterative**: At 8× and 10×, compare single-pass SSHPC against iterative (3 rounds).
  4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning against fixed-ratio top-k.

  ## 5 Results

  ### 5.1 Main Results

  Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks and compression ratios. SSHPC Iterative is the best-performing method at 8× and 10× on GSM8K (72.9% and 71.1% EM) and HotpotQA (62.5% and 61.4% F1). At 2× and 4×, all methods including SSHPC Base remain close to the no-compression baseline (within 1–2 points). The gap widens at higher compression: at 10×, SSHPC Iterative leads LLMLingua by 7.4 points on GSM8K and 5.9 points on HotpotQA.

  On NaturalQuestions, SSHPC Base and Iterative match SelectiveContext at 2×–4× (68.5–68.6% F1) and pull ahead at 8× (67.1% vs 61.7%). On LongBench, SSHPC Iterative consistently outperforms baselines, reaching 42.8% at 8× vs 40.4% for LLMLingua.

  Random pruning degrades rapidly, confirming that token importance is non-uniform and methods that exploit it are effective.

  [FIGURE:fig2_main]

  ### 5.2 Proxy-Mismatch Ablation

  [FIGURE:fig3_proxy]

  This indicates that the proxy-mismatch effect, while real, is small in isolation. The larger gains of SSHPC Iterative at high compression come from iterative re-scoring adapting to the changed context, not from self-surprisal being inherently superior to target-model perplexity in a single pass.

  ### 5.3 Iterative Re-Scoring Benefit

  Figure 4 shows the iterative benefit at 8× and 10×. On GSM8K, iterative adds +3.8 points at 8× (p = 0.0001) and +2.2 points at 10× (p = 0.003). On HotpotQA, +2.3 points at 8× (p = 0.04) and +1.6 points at 10× (p = 0.08). On NaturalQuestions, +1.1 points at 8× (p = 0.12) and +3.5 points at 10× (p = 0.02). On LongBench, +0.8 points at 8× (p = 0.21) and +1.2 points at 10× (p = 0.15).

  Iterative re-scoring is most beneficial for reasoning-heavy tasks (GSM8K, HotpotQA) where token dependencies are strong and context changes substantially after pruning.

  [FIGURE:fig4_iterative]

  ### 5.4 Query-Conditioned and Attention-Weighted Variants

  Figure 5 compares SSHPC variants at 8×. Query-conditioned SSHPC improves over Base on NaturalQuestions (+1.6 points) and HotpotQA (+2.2 points) where a clear question exists. On GSM8K (no explicit question), it matches Base. Attention-weighted SSHPC improves on GSM8K (+2.6 points) and HotpotQA (+1.9 points) but not on LongBench. The best variant is task-dependent: Iterative dominates on GSM8K and HotpotQA; Query-Conditioned leads on NaturalQuestions.

  [FIGURE:fig5_variants]

  ### 5.5 Latency Break-Even

  Figure 6 shows end-to-end latency vs. compression ratio. For all methods, break-even (compression overhead equals generation time saved) occurs at 2×. At 2×, compression adds ~2.5s prefill but saves ~2.5s generation, yielding net parity. At 4× and above, all methods show net latency reduction. SSHPC Base adds ~5–10ms overhead per 1000 tokens vs. GPT-2-based methods, but this is negligible compared to generation savings at high compression. The break-even ratio of 2× holds across all benchmarks.

  [FIGURE:fig6_latency]

  [ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:art_Lm_O96s-n8rb]

  ## 6 Discussion

  ### 6.1 Summary of Findings

  1. **Self-surprisal works**: SSHPC Base matches or exceeds proxy-based baselines across all benchmarks, with larger margins at high compression.
  2. **Iterative re-scoring is critical at ≥8×**: It provides statistically significant gains on reasoning tasks (GSM8K, HotpotQA) by adapting to the changed context after pruning.
  3. **Proxy mismatch is real but small in isolation**: When the proxy is the target model, SSHPC's single-pass advantage is 0.48% on average and not significant. The practical gains come from iterative re-scoring, which proxy methods do not naturally support because they condition on the *original* context during iterative compression.
  4. **Query conditioning helps when a question exists**: On QA tasks, conditioning surprisal on the question improves pruning decisions.
  5. **Latency break-even at 2×**: All methods including SSHPC become net-positive at 2× compression on A100.

  ### 6.2 Limitations

  **Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (OpenAI's `logprobs`), but not all. For fully black-box APIs, proxy methods remain the only option.

  **Single-pass context dependence**: At high compression, single-pass surprisal computed on the full prompt becomes stale. We address this with iterative re-scoring as the default for r ≥ 8, but this multiplies compression latency by the number of rounds (3× in our experiments).

  **First-token handling**: The first token uses the unconditional distribution, which may not reflect its importance. We mitigate this by always preserving special/instruction tokens via infinite surprisal assignment. An alternative would use bidirectional pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy model.

  **Query-conditioning generality**: Our heuristic for extracting the "task specification" (last user message, question, instruction prefix) works for standard prompt templates but may fail for unusual formats. A more robust approach would use an instruction-following model to identify the task specification automatically.

  **Single target model**: We evaluate only on Llama-3-8B-Instruct. The method should transfer to other open-weight models (Qwen2, Mistral), but the exact break-even ratios and iterative benefits may vary with model architecture and size.

  **Synthetic surprisal distributions**: The surprisal distribution in Figure 7 is synthetic (generated from a log-normal fit to pilot data). Real distributions from Llama-3-8B would provide stronger evidence but require additional computation.

  ### 6.3 Broader Implications

  If self-surprisal with iterative re-scoring proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression—no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error, applied iteratively. SSHPC operationalizes this principle for hard token pruning.

  The negative result on proxy-mismatch (when the proxy *is* the target) is informative: it suggests that LLMLingua's iterative compression already approximates the target model's preferences reasonably well when the proxy is large and aligned. The remaining gap at high compression comes from LLMLingua conditioning on the *original* context during re-scoring, whereas SSHPC re-scores on the *compressed* context, which is what the target will actually see.

  ## 7 Conclusion

  We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token prediction logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation on four long-context benchmarks with Llama-3-8B shows that SSHPC Base outperforms proxy baselines at high compression, and iterative re-scoring (default for r ≥ 8×) provides statistically significant additional gains of 1.8–3.8 points on reasoning tasks. The proxy-mismatch ablation reveals that self-surprisal alone provides only a marginal (0.48%, not significant) advantage over target-model perplexity; the practical gains come from iterative adaptation to the compressed context. Latency break-even occurs at 2× compression for all methods. Future work includes extending to multiple target models, chunked computation for >8k tokens, and automatic task-specification extraction for query conditioning.

  ---

  ## Bibliography

  \bibliography{references}
  \bibliographystyle{plainnat}
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token logits to compute per-token surprisal
  for hard prompt pruning. Evaluated on 4 benchmarks with Llama-3-8B at 2x-10x compression. SSHPC Iterative (with re-scoring
  at >=8x) outperforms proxy baselines by 2-5 points at high compression. Key finding: proxy-mismatch effect is small (0.48%,
  ns) in isolation; gains come from iterative re-scoring adapting to compressed context. Latency break-even at 2x.
</paper_text>

<available_figures>
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig2_main_v0.png [render from fig2_main_v0.pdf first] — "Task Accuracy Across Benchmarks and Compression Ratios" (caption: "Task accuracy (%) across four benchmarks and four compression ratios (2×, 4×, 8×, 10×) for six methods. SSHPC Iterative (solid green) consistently outperforms baselines at high compression. LLMLingua (blue) and SelectiveContext (orange) degrade faster than SSHPC variants. No Compression (black) is the upper bound. Random Pruning (gray) degrades rapidly. Error bars show 95% bootstrap confidence intervals (10,000 resamples).")
- figures/fig3_proxy_v0.png [render from fig3_proxy_v0.pdf first] — "Proxy-Mismatch Ablation: SSHPC vs Proxy-on-Target" (caption: "Accuracy difference (SSHPC Base minus Proxy-on-Target) across 16 dataset–ratio conditions. Positive values favor SSHPC. The average improvement is +0.48% (not statistically significant, p > 0.05). Error bars show standard error (1.5%). Conditions: GSM8K 2×–10×, HotpotQA 2×–10×, NaturalQuestions 2×–10×, LongBench 2×–10×.")
- figures/fig4_iterative_v0.png [render from fig4_iterative_v0.pdf first] — "Iterative Re-Scoring Benefit at High Compression" (caption: "Dumbbell chart comparing single-pass vs iterative (3 rounds) SSHPC at 8× and 10× compression. Iterative re-scoring provides significant gains on GSM8K (+3.8 at 8×, p=0.0001) and HotpotQA (+2.3 at 8×, p=0.04), moderate gains on NaturalQuestions, and smaller non-significant gains on LongBench. Single-pass values are constant at 70% (baseline reference).")
- figures/fig5_variants_v0.png [render from fig5_variants_v0.pdf first] — "SSHPC Variant Comparison at 8× Compression" (caption: "Comparison of four SSHPC variants at 8× compression across four datasets. Iterative (green) leads on GSM8K (72.9%) and HotpotQA (62.5%). Query-Conditioned (orange) leads on NaturalQuestions (67.6%). Attention-Weighted (purple) is competitive on GSM8K (71.7%) and HotpotQA (62.2%). Base (blue) is the single-pass unconditional variant. Error bars show 95% CI.")
- figures/fig6_latency_v0.png [render from fig6_latency_v0.pdf first] — "End-to-End Latency vs Compression Ratio" (caption: "End-to-end latency (compression + generation) vs compression ratio for four methods. Break-even occurs at 2× for all methods. At 2×, latency ~2500ms; at 4×, ~1250ms; at 8×, ~625ms; at 10×, ~500ms. SSHPC Base (green) and Iterative (purple) overlap with LLMLingua (blue) and No Compression (black) within error bands. Shaded bands show standard deviation across datasets.")
- figures/fig7_surprisal_v0.png [render from fig7_surprisal_v0.pdf first] — "Per-Token Surprisal Distribution (Synthetic)" (caption: "Violin plot of per-token surprisal distribution for GSM8K (synthetic data from log-normal fit to pilot runs). Surprisal values range from near 0 to ~16, with a long right tail. Median ~1.5, mean ~3.2. The distribution is highly skewed, confirming that most tokens are predictable (low surprisal) while a few carry high information.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNG files into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [28] HUMAN-USER prompt · 2026-09-20 03:13:26 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```

### [29] RETRY (attempt 5) · 2026-09-20 03:14:43 UTC

```
Agent result indicates failure (attempt 5/6): Conversation run failed for id=9884d036-d35d-480a-a32f-f89efed04ce4: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/9884d036d35d480aa32ff89efed04ce4

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [30] RETRY (attempt 6) · 2026-09-20 03:14:43 UTC

```
Agent retry... (attempt 6/6): Conversation run failed for id=9884d036-d35d-480a-a32f-f89efed04ce4: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/9884d036d35d480aa32ff89efed04ce4

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
```

### [31] CONFIG · 2026-09-20 03:14:43 UTC

```
Model: Free tier (no preference) | Session: d14a7336-1625-438b-8052-09696c7fa2de | Tools: 4 | Permission: acceptEdits
```

### [32] SYSTEM PROMPT · 2026-09-20 03:14:45 UTC

```
<design_philosophy>
You are building ONE web page whose only job is to let a reader understand a research paper faster
than they could by opening the PDF. Every decision on the page is judged against that.

WHAT "FASTER" MEANS HERE
- A reader who leaves after thirty seconds still knows the finding and the number behind it.
- A reader who stays five minutes has the method, the figures and the caveats, in that order.
- Nothing on the page is there because a layout had a slot for it.

ACCURACY IS THE HARD CONSTRAINT
Every number, name and claim comes from the paper as written — you read them out of the LaTeX
source and the run's own data files. You never change a number's precision, never restate a
comparison the paper did not make, and never invent a headline figure to fill a card. A page that
looks excellent and misreports one result is worse than no page, because the PDF beside it says
something else and a reader will find that out.

CRAFT, AND THE LOOK TO AVOID
The failure mode for a generated page is a look every reader now recognises on sight: a
purple-to-blue gradient banner, three identical cards with emoji headings, and body text set in
one weight at one size. Avoid all of it.
- Type carries the design. One system font stack, a real scale with visible jumps between levels
  rather than a creep of similar sizes, long-form text around 17-19px with a measure of 65-75
  characters and generous line height. Weight and size do the emphasis; colour rarely does.
- Colour is restrained. A light, near-white ground, one dark ink for text, one accent used for
  links and the current-section marker and almost nothing else. No gradients as decoration.
- Space does the work that borders and boxes would do badly. Sections separated by real vertical
  rhythm, cards defined by alignment and a single hairline rather than by shadow stacks.
- Structure over ornament: no emoji as section markers, no icon fonts, no badge clutter, no
  animated counters.
- Motion is a courtesy. A short transition on a lightbox or a hover state is welcome; anything
  that moves on scroll, autoplays, or delays the reader is not — and all of it stops under
  prefers-reduced-motion.
- Every interactive element works with a keyboard and says what it is to a screen reader. That is
  part of the craft, not a checklist bolted on at the end.

FINISH IT
The page is done when you have opened it in a browser, read it at a phone width and a desktop
width, tabbed through every control, and found nothing to fix. Not before.
</design_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<subagent-delegation>
You may delegate bounded work to subagents (e.g. the Task tool). Delegate by default rather than doing everything yourself:

- Pick the cheapest capable model available to you for each subagent launch:
- Pass `subagent_type="tier-easy"` (steered toward `cohere/north-mini-code:free`) for a small/fast tier for mechanical work.
- Pass `subagent_type="tier-medium"` (steered toward `cohere/north-mini-code:free`) for a mid tier for implementation or investigation (the default).
- Pass `subagent_type="tier-hard"` (steered toward `google/gemma-4-31b-it:free`) for the strongest tier only for hard reasoning or after a cheaper model has already failed on the same task.
- Give each subagent prompt one focused objective: exact scope, the acceptance check, and the required output format.
- Subagents report back only the result, changed files, verification, and blockers — not narration or full logs.
- Delegations on this backend BLOCK: the tool call does not return until that subagent has finished, so launches are serialized no matter how many you plan. Size each delegation to be worth waiting for, and do cheap work yourself rather than paying the round trip.
- Never fork yourself, and never let a subagent spawn its own subagents.
- You (the orchestrator) decompose, coordinate, and synthesize; do not redo work you already delegated.
- Verify each result with the smallest reliable check.
</subagent-delegation>
```

### [33] SYSTEM-USER prompt · 2026-09-20 03:14:45 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=9884d036-d35d-480a-a32f-f89efed04ce4: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/9884d036d35d480aa32ff89efed04ce4

To help debug this issue, please file a bug report at:
  https://github.com/OpenHands/software-agent-sdk/issues/new
and attach the conversation logs from the directory above.
Last actions before failure:
  - [agent_system_user_prompt]: <task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize indepe
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=e7be7aca-b10a-4e53-9cd9-2ed746457e1d: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/e7be7acab10a4e539cd92ed
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=0b75a215-b011-44c1-ae88-41510d92b879: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/0b75a215b01144c1ae88415
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=107b816b-b5bf-43d1-8c15-c777e1aa5aab: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/107b816bb5bf43d18c15c77
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: Conversation run failed for id=90d8e9c0-17d3-48cf-b63f-6b33869fbfe7: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Conversation logs are stored at: /ai-inventor/aii_data/runs/run_JKcn7QHhokJh/.oh_sessions/90d8e9c017d348cfb63f6b3
  - [agent_human_user_prompt]: Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
  - [status_public_warning]: Conversation error [AttributeError]: 'PromptTokensDetailsWrapper' object has no attribute 'cache_creation_tokens'

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

<paper_text>
title: Self-Surprisal Hard Prompt Compression
abstract: >-
  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score
  token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ
  from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses
  the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its
  preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy
  mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four
  long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines
  by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical
  significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for
  SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring
  rather than self-surprisal alone.
paper_text: |-
  # Self-Surprisal Hard Prompt Compression

  ## Abstract

  Hard prompt compression methods such as LLMLingua, SelectiveContext, and LLMLingua-2 rely on a smaller proxy model to score token importance via perplexity or self-information. This creates a proxy-model mismatch: the proxy's predictions differ from the target LLM's, leading to suboptimal pruning. We propose Self-Surprisal Hard Prompt Compression (SSHPC), which uses the target LLM's own next-token logits to compute per-token surprisal—the negative log-likelihood of each token given its preceding context—and prunes the lowest-surprisal tokens. Grounded in predictive coding theory, this eliminates the proxy mismatch while avoiding the training overhead and soft-token complexity of methods like SelfCP. We evaluate SSHPC on four long-context benchmarks using Llama-3-8B across compression ratios from 2× to 10×. SSHPC Base outperforms proxy baselines by several percentage points at high compression. Iterative re-scoring adds further gains on reasoning tasks with statistical significance. Latency break-even occurs at 2× compression. A proxy-mismatch ablation shows a small average improvement for SSHPC that is not statistically significant, indicating the gains at high compression come primarily from iterative re-scoring rather than self-surprisal alone.

  ## 1 Introduction

  Large language models have become central to applications ranging from retrieval-augmented generation to multi-step reasoning. As these systems incorporate chain-of-thought prompting, in-context learning, and retrieved documents, prompt lengths routinely exceed thousands of tokens. This increase in length raises inference latency, memory consumption, and API costs proportionally to sequence length.

  Existing hard prompt compression methods address this by removing tokens deemed unimportant. LLMLingua and SelectiveContext compute token-level perplexity or self-information using a small proxy model such as GPT-2 or LLaMA-7B, then discard tokens with low scores. LLMLingua-2 distills a classifier from a proxy model's outputs. All three share the same limitation: the proxy model's internal representations and prediction distributions differ from the target LLM's, so its importance scores are systematically misaligned with what the target model actually finds surprising or predictable. This proxy-model mismatch causes suboptimal pruning, especially at high compression ratios where each retained token must carry maximal information for the target model.

  Soft prompt methods such as GIST, ICAE, AutoCompressor, and SelfCP use the target LLM itself but produce dense continuous vectors that require learnable connectors and supervised training on long-context data. They do not preserve the original discrete token sequence, limiting compatibility with black-box APIs and introducing additional engineering complexity.

  Why has self-surprisal not been used for hard pruning? Two practical barriers exist. First, many API-only models do not expose per-token logits for prompt tokens. Second, computing a full forward pass over a long prompt to obtain logits for every position adds latency that may offset compression gains. Recent open-weight models (Llama-3, Qwen2, Mistral) and efficient batched inference have reduced both barriers, making self-surprisal computationally feasible and directly accessible.

  We propose Self-Surprisal Hard Prompt Compression (SSHPC), which scores tokens by the target LLM's own next-token surprisal and prunes the lowest-surprisal tokens. At high compression ratios (≥8×), iterative re-scoring adapts to the changed context. This uses the target model's own predictive coding machinery as the importance signal, eliminating the proxy mismatch entirely.

  [FIGURE:fig1_method]

  Our contributions are:

  1. **Algorithm**: A hard prompt compression method that scores tokens by the target LLM's own next-token surprisal, requiring no proxy model, no training, and no architectural modifications. At high compression (≥8×), iterative re-scoring adapts to the changed context (Section 3).
  2. **Theoretical grounding**: A connection to predictive coding and the free-energy principle, formalizing why self-surprisal is the correct importance signal for a given target model (Section 3.2).
  3. **Empirical evaluation**: Experiments on four benchmarks (GSM8K, HotpotQA, NaturalQuestions, LongBench) with Llama-3-8B, comparing SSHPC against LLMLingua, SelectiveContext, LLMLingua-2, random pruning, and a proxy-on-target ablation, at compression ratios 2×–10×. We measure task accuracy and end-to-end latency (Section 4).
  4. **Ablation studies**: Proxy-mismatch isolation, iterative vs. single-pass at high compression, query-conditioned vs. unconditional surprisal, and latency break-even analysis (Section 4.4).

  ## 2 Related Work

  ### 2.1 Hard Prompt Compression via Proxy Models

  LLMLingua (Jiang et al., 2023) introduced a coarse-to-fine framework using a small language model (GPT-2 or Alpaca-7B) to compute token perplexity. A budget controller allocates different compression ratios to instructions, demonstrations, and questions, followed by iterative token-level compression that conditions on previously retained tokens. LongLLMLingua (Jiang et al., 2024) extends this with question-aware compression and document reordering to address position bias in long contexts. LLMLingua-2 (Pan et al., 2024) replaces the iterative process with a data distillation pipeline: a small Transformer encoder (XLM-RoBERTa-large) is trained to classify tokens as keep/discard using labels derived from the proxy model's perplexity scores.

  SelectiveContext (Li, 2023) computes self-information (negative log probability) of noun phrases identified by spaCy dependency parsing, then filters phrases below a threshold. Like LLMLingua, it relies on a small LM's probability estimates rather than the target model's.

  All these methods suffer from proxy-model mismatch. The small LM's vocabulary, architecture, and training distribution differ from the target LLM's, so its perplexity rankings correlate imperfectly with the target's actual sensitivity to token removal. Jiang et al. (2023) mitigate this via instruction tuning the proxy on target-LLM outputs, but alignment remains incomplete.

  Recent work has explored alternatives. ProCut (Xu et al., 2025) segments prompt templates into semantic units and estimates their attribution via an LLM-driven estimator, achieving 78% token reduction in production. Nano-Capsulator (Chuang et al., 2024) paraphrases prompts into concise natural language using a fine-tuned Vicuna-7B. ASAP (Zeng et al., 2025) uses first-token surprisal for chain-of-thought step pruning with fine-tuning. PIS (Chen et al., 2025) uses attention scores for importance sampling. None uses the target LLM's own next-token logits directly for hard token pruning.

  ### 2.2 Soft Prompt Compression

  GIST (Mu et al., 2023) appends trainable "gist tokens" that attend to the full prompt; subsequent generation attends only to gist tokens. AutoCompressor (Chevalier et al., 2023) recursively compresses prompt segments into soft tokens. ICAE (Ge et al., 2023) uses a LoRA-adapted LLM as encoder to compress contexts into virtual tokens, with the frozen LLM as decoder. These methods require fine-tuning the encoder or the full model, and the compressed representations are model-specific dense vectors unusable with black-box APIs.

  SelfCP (Gao et al., 2024) uses the target LLM itself as both compressor and generator. The compressor processes over-limit prompt segments, and a learned linear connector projects the final hidden states into "memory tokens" understood by the generator. Only the connector (17M parameters) is trained; the LLM stays frozen. SelfCP achieves 12× compression but still produces soft tokens and requires training the connector on long-context data.

  ### 2.3 Theoretical Frameworks

  Nagle et al. (2024) formalize prompt compression as a rate-distortion problem for black-box LLMs. They derive the distortion-rate function as a linear program and show a large gap between existing heuristics and the optimal strategy. Their analysis highlights the importance of query-aware compression but does not propose a self-surprisal method.

  Predictive coding (Friston, 2009) posits that hierarchical neural systems minimize free energy by predicting incoming inputs; only prediction errors (surprisal) propagate upward. Applied to LLMs: tokens the model predicts well from context are "explained away" as redundant for that model's generation. This provides a principled justification for self-surprisal as the importance signal.

  ## 3 Method

  ### 3.1 Self-Surprisal Hard Prompt Compression

  Let the target LLM be $M$ with vocabulary $\mathcal{V}$ and context window $L$. Given a prompt $\mathbf{x} = (x_1, x_2, \dots, x_N)$ with $N \le L$, we compute the surprisal of each token under $M$'s next-token distribution:

  $$s_i = -\log P_M(x_i \mid x_{<i}) \quad \text{for } i = 1, \dots, N$$

  where $x_{<i} = (x_1, \dots, x_{i-1})$ and $P_M$ is $M$'s next-token probability distribution (obtained via a forward pass with causal masking). For the first token $x_1$, we use the unconditional distribution $P_M(x_1)$.

  **Special token preservation.** Instruction delimiters, `<bos>`, `<eos>`, and other structural tokens are assigned infinite surprisal so they are never pruned.

  Given a target compression ratio $r \ge 1$ (i.e., retain $N/r$ tokens), we select the top-$k = \lfloor N/r \rfloor$ tokens with highest surprisal scores, preserving their original relative order. The compressed prompt $\tilde{\mathbf{x}}$ is the subsequence of these tokens.

  **Iterative re-scoring for high compression.** At compression ratios $r \ge 8$, token predictability changes substantially as surrounding tokens are removed. We therefore iterate: after initial pruning, we recompute surprisal on the compressed prompt $\tilde{\mathbf{x}}$ under the same model $M$ and prune again to the target ratio. We use 3 rounds by default. This is the default for $r \ge 8$; for $r < 8$, single-pass is used.

  **Implementation details.** We obtain all $s_i$ in a single forward pass by feeding the full prompt to $M$ and reading the logits at each position. For models with grouped-query attention, we use standard causal masking. The computation is $\mathcal{O}(N \cdot d)$ where $d$ is model dimension, comparable to one generation step.

  **Variants.** (1) *Unconditional SSHPC*: surprisal computed on the prompt alone as above. (2) *Query-conditioned SSHPC*: for prompts with an identifiable task specification (question in QA, last user message in chat, instruction prefix in summarization), we compute $s_i = -\log P_M(x_i \mid x_{<i}, \text{task\_spec})$, so context tokens are scored by how surprising they are given the task. This aligns with LongLLMLingua's finding that question-awareness improves compression. (3) *Attention-weighted SSHPC*: each token's surprisal is weighted by its total attention mass received from subsequent tokens in the final layer, capturing both self-predictability and causal influence.

  [FIGURE:fig1_method]

  ### 3.2 Theoretical Motivation: Predictive Coding and Self-Surprisal

  Predictive coding (Friston, 2009) frames perception as hierarchical Bayesian inference: each level predicts the activity of the level below, and only the prediction error (surprisal) is forwarded. In an LLM, the next-token prediction head implements exactly this: at each layer, the residual stream carries a prediction of the next token; the difference between prediction and actual input is the surprisal.

  Formally, let the prompt $\mathbf{x}$ be generated by a stochastic process. The target LLM $M$ defines a conditional distribution $P_M(x_i \mid x_{<i})$. The pointwise mutual information between $x_i$ and $x_{<i}$ under $M$ is $\log \frac{P_M(x_i \mid x_{<i})}{P_M(x_i)}$. Its expectation over $P_M$ is the conditional entropy; the pointwise quantity $-\log P_M(x_i \mid x_{<i})$ is the self-information or surprisal.

  If $s_i$ is low, $M$ already "expects" $x_i$ given $x_{<i}$; removing $x_i$ does not change $M$'s internal state significantly because the prediction was already accurate. If $s_i$ is high, $x_i$ carries information $M$ did not predict; removing it forces $M$ to generate from a context that diverges from what it would have seen. Thus self-surprisal directly measures each token's causal contribution to $M$'s subsequent computation.

  This differs from proxy-model perplexity: a proxy model $M'$ computes $-\log P_{M'}(x_i \mid x_{<i})$, which measures how surprising $x_i$ is to $M'$, not to $M$. The mismatch $P_M \ne P_{M'}$ is the root cause of suboptimal pruning.

  ### 3.3 Computational Considerations

  SSHPC requires one forward pass over the full prompt (or multiple passes for iterative re-scoring). For a prompt of length $N$, the forward pass computes all $N$ surprisal values simultaneously using the model's KV cache. We measure actual prefill latency on A100-40GB and compare against generation time savings to determine break-even compression ratios.

  At very long contexts ($N > 8192$), we can chunk the prompt and compute surprisal within each chunk, or use a sliding window. We leave chunked computation to future work.

  [FIGURE:fig7_surprisal]

  ## 4 Experiments

  ### 4.1 Datasets and Tasks

  We evaluate on four benchmarks covering diverse long-context tasks [ARTIFACT:art_-Hzqeq6rV9vC]:

  - **GSM8K** (Cobbe et al., 2021): Multi-step mathematical reasoning with chain-of-thought prompts. Tests whether compression preserves reasoning structure. Metric: Exact Match.
  - **HotpotQA** (Yang et al., 2018): Multi-hop reasoning over multiple documents. Tests whether compression preserves cross-document dependencies. Metric: F1.
  - **NaturalQuestions** (Kwiatkowski et al., 2019): Multi-document open-domain QA with 10 retrieved documents per question. Metric: F1.
  - **LongBench** (Bai et al., 2023): Bilingual multi-task benchmark including single-doc QA, multi-doc QA, summarization, few-shot learning, and code completion. Context lengths 5k–15k tokens. Metric: F1/EM/ROUGE-L (task-dependent).

  ### 4.2 Target Models and Baselines

  **Target LLM** (local inference via HuggingFace):
  - Llama-3-8B-Instruct

  **Proxy model for baselines**:
  - GPT-2 (124M parameters) for LLMLingua and SelectiveContext

  **Methods compared**:
  1. **No compression** (full prompt)
  2. **Random pruning**: uniform random token removal
  3. **SelectiveContext** (Li, 2023): self-information from GPT-2 proxy
  4. **LLMLingua** (Jiang et al., 2023): proxy-model perplexity with iterative compression
  5. **LLMLingua-2** (Pan et al., 2024): distilled classifier from proxy model
  6. **Proxy-on-Target ablation**: LLMLingua using the *same* target LLM (Llama-3-8B) as the proxy. This isolates the proxy-mismatch effect.
  7. **SSHPC Base**: single-pass self-surprisal, special tokens preserved
  8. **SSHPC Query-Conditioned**: surprisal conditioned on task specification
  9. **SSHPC Attention-Weighted**: surprisal weighted by attention mass
  10. **SSHPC Iterative**: single-pass at 2×, 4×; iterative (3 rounds) at 8×, 10×

  ### 4.3 Compression Ratios and Metrics

  Compression ratios: 2×, 4×, 8×, 10× (i.e., retain 50%, 25%, 12.5%, 10% of tokens).

  **Primary metrics**:
  - Task accuracy (Exact Match for GSM8K, F1 for QA, ROUGE-L for summarization)
  - End-to-end latency (compression + generation) on A100-40GB

  **Secondary metrics**:
  - Compression throughput (tokens/sec for the compression step alone)
  - Surprisal distribution statistics

  ### 4.4 Ablation Studies

  1. **Proxy mismatch isolation**: Compare SSHPC against Proxy-on-Target ablation. If SSHPC outperforms, the gain is not merely from using a larger proxy but from using the target's own distribution with iterative re-scoring.
  2. **Unconditional vs. query-conditioned**: On NaturalQuestions and HotpotQA, compare SSHPC with and without question conditioning.
  3. **Single-pass vs. iterative**: At 8× and 10×, compare single-pass SSHPC against iterative (3 rounds).
  4. **Surprisal threshold vs. top-k**: Compare fixed-threshold pruning against fixed-ratio top-k.

  ## 5 Results

  ### 5.1 Main Results

  Table 1 (summarized in Figure 2) shows task accuracy across all benchmarks and compression ratios. SSHPC Iterative is the best-performing method at 8× and 10× on GSM8K (72.9% and 71.1% EM) and HotpotQA (62.5% and 61.4% F1). At 2× and 4×, all methods including SSHPC Base remain close to the no-compression baseline (within 1–2 points). The gap widens at higher compression: at 10×, SSHPC Iterative leads LLMLingua by 7.4 points on GSM8K and 5.9 points on HotpotQA.

  On NaturalQuestions, SSHPC Base and Iterative match SelectiveContext at 2×–4× (68.5–68.6% F1) and pull ahead at 8× (67.1% vs 61.7%). On LongBench, SSHPC Iterative consistently outperforms baselines, reaching 42.8% at 8× vs 40.4% for LLMLingua.

  Random pruning degrades rapidly, confirming that token importance is non-uniform and methods that exploit it are effective.

  [FIGURE:fig2_main]

  ### 5.2 Proxy-Mismatch Ablation

  [FIGURE:fig3_proxy]

  This indicates that the proxy-mismatch effect, while real, is small in isolation. The larger gains of SSHPC Iterative at high compression come from iterative re-scoring adapting to the changed context, not from self-surprisal being inherently superior to target-model perplexity in a single pass.

  ### 5.3 Iterative Re-Scoring Benefit

  Figure 4 shows the iterative benefit at 8× and 10×. On GSM8K, iterative adds +3.8 points at 8× (p = 0.0001) and +2.2 points at 10× (p = 0.003). On HotpotQA, +2.3 points at 8× (p = 0.04) and +1.6 points at 10× (p = 0.08). On NaturalQuestions, +1.1 points at 8× (p = 0.12) and +3.5 points at 10× (p = 0.02). On LongBench, +0.8 points at 8× (p = 0.21) and +1.2 points at 10× (p = 0.15).

  Iterative re-scoring is most beneficial for reasoning-heavy tasks (GSM8K, HotpotQA) where token dependencies are strong and context changes substantially after pruning.

  [FIGURE:fig4_iterative]

  ### 5.4 Query-Conditioned and Attention-Weighted Variants

  Figure 5 compares SSHPC variants at 8×. Query-conditioned SSHPC improves over Base on NaturalQuestions (+1.6 points) and HotpotQA (+2.2 points) where a clear question exists. On GSM8K (no explicit question), it matches Base. Attention-weighted SSHPC improves on GSM8K (+2.6 points) and HotpotQA (+1.9 points) but not on LongBench. The best variant is task-dependent: Iterative dominates on GSM8K and HotpotQA; Query-Conditioned leads on NaturalQuestions.

  [FIGURE:fig5_variants]

  ### 5.5 Latency Break-Even

  Figure 6 shows end-to-end latency vs. compression ratio. For all methods, break-even (compression overhead equals generation time saved) occurs at 2×. At 2×, compression adds ~2.5s prefill but saves ~2.5s generation, yielding net parity. At 4× and above, all methods show net latency reduction. SSHPC Base adds ~5–10ms overhead per 1000 tokens vs. GPT-2-based methods, but this is negligible compared to generation savings at high compression. The break-even ratio of 2× holds across all benchmarks.

  [FIGURE:fig6_latency]

  [ARTIFACT:art_pWnUR-sCdAoE][ARTIFACT:art_Lm_O96s-n8rb]

  ## 6 Discussion

  ### 6.1 Summary of Findings

  1. **Self-surprisal works**: SSHPC Base matches or exceeds proxy-based baselines across all benchmarks, with larger margins at high compression.
  2. **Iterative re-scoring is critical at ≥8×**: It provides statistically significant gains on reasoning tasks (GSM8K, HotpotQA) by adapting to the changed context after pruning.
  3. **Proxy mismatch is real but small in isolation**: When the proxy is the target model, SSHPC's single-pass advantage is 0.48% on average and not significant. The practical gains come from iterative re-scoring, which proxy methods do not naturally support because they condition on the *original* context during iterative compression.
  4. **Query conditioning helps when a question exists**: On QA tasks, conditioning surprisal on the question improves pruning decisions.
  5. **Latency break-even at 2×**: All methods including SSHPC become net-positive at 2× compression on A100.

  ### 6.2 Limitations

  **Logit access requirement**: SSHPC requires access to the target LLM's next-token logits for prompt tokens. This is available for local models (HuggingFace, vLLM) and some APIs (OpenAI's `logprobs`), but not all. For fully black-box APIs, proxy methods remain the only option.

  **Single-pass context dependence**: At high compression, single-pass surprisal computed on the full prompt becomes stale. We address this with iterative re-scoring as the default for r ≥ 8, but this multiplies compression latency by the number of rounds (3× in our experiments).

  **First-token handling**: The first token uses the unconditional distribution, which may not reflect its importance. We mitigate this by always preserving special/instruction tokens via infinite surprisal assignment. An alternative would use bidirectional pseudo-log-likelihood (Salazar et al., 2020), but this reintroduces a proxy model.

  **Query-conditioning generality**: Our heuristic for extracting the "task specification" (last user message, question, instruction prefix) works for standard prompt templates but may fail for unusual formats. A more robust approach would use an instruction-following model to identify the task specification automatically.

  **Single target model**: We evaluate only on Llama-3-8B-Instruct. The method should transfer to other open-weight models (Qwen2, Mistral), but the exact break-even ratios and iterative benefits may vary with model architecture and size.

  **Synthetic surprisal distributions**: The surprisal distribution in Figure 7 is synthetic (generated from a log-normal fit to pilot data). Real distributions from Llama-3-8B would provide stronger evidence but require additional computation.

  ### 6.3 Broader Implications

  If self-surprisal with iterative re-scoring proves effective, it suggests that the target LLM's own predictive coding machinery is a sufficient importance signal for compression—no external model, no training, no distillation. This aligns with the rate-distortion framework of Nagle et al. (2024): the optimal compressor for a given decoder is the decoder's own prediction error, applied iteratively. SSHPC operationalizes this principle for hard token pruning.

  The negative result on proxy-mismatch (when the proxy *is* the target) is informative: it suggests that LLMLingua's iterative compression already approximates the target model's preferences reasonably well when the proxy is large and aligned. The remaining gap at high compression comes from LLMLingua conditioning on the *original* context during re-scoring, whereas SSHPC re-scores on the *compressed* context, which is what the target will actually see.

  ## 7 Conclusion

  We proposed Self-Surprisal Hard Prompt Compression (SSHPC), a training-free hard prompt compression method that uses the target LLM's own next-token prediction logits to score token importance. By eliminating the proxy-model mismatch inherent in LLMLingua, SelectiveContext, and LLMLingua-2, and avoiding the soft-token complexity and training overhead of SelfCP, GIST, and ICAE, SSHPC offers a minimal, principled alternative grounded in predictive coding theory. Our evaluation on four long-context benchmarks with Llama-3-8B shows that SSHPC Base outperforms proxy baselines at high compression, and iterative re-scoring (default for r ≥ 8×) provides statistically significant additional gains of 1.8–3.8 points on reasoning tasks. The proxy-mismatch ablation reveals that self-surprisal alone provides only a marginal (0.48%, not significant) advantage over target-model perplexity; the practical gains come from iterative adaptation to the compressed context. Latency break-even occurs at 2× compression for all methods. Future work includes extending to multiple target models, chunked computation for >8k tokens, and automatic task-specification extraction for query conditioning.

  ---

  ## Bibliography

  \bibliography{references}
  \bibliographystyle{plainnat}
summary: >-
  Self-Surprisal Hard Prompt Compression (SSHPC) uses the target LLM's own next-token logits to compute per-token surprisal
  for hard prompt pruning. Evaluated on 4 benchmarks with Llama-3-8B at 2x-10x compression. SSHPC Iterative (with re-scoring
  at >=8x) outperforms proxy baselines by 2-5 points at high compression. Key finding: proxy-mismatch effect is small (0.48%,
  ns) in isolation; gains come from iterative re-scoring adapting to compressed context. Latency break-even at 2x.
</paper_text>

<available_figures>
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig2_main_v0.png [render from fig2_main_v0.pdf first] — "Task Accuracy Across Benchmarks and Compression Ratios" (caption: "Task accuracy (%) across four benchmarks and four compression ratios (2×, 4×, 8×, 10×) for six methods. SSHPC Iterative (solid green) consistently outperforms baselines at high compression. LLMLingua (blue) and SelectiveContext (orange) degrade faster than SSHPC variants. No Compression (black) is the upper bound. Random Pruning (gray) degrades rapidly. Error bars show 95% bootstrap confidence intervals (10,000 resamples).")
- figures/fig3_proxy_v0.png [render from fig3_proxy_v0.pdf first] — "Proxy-Mismatch Ablation: SSHPC vs Proxy-on-Target" (caption: "Accuracy difference (SSHPC Base minus Proxy-on-Target) across 16 dataset–ratio conditions. Positive values favor SSHPC. The average improvement is +0.48% (not statistically significant, p > 0.05). Error bars show standard error (1.5%). Conditions: GSM8K 2×–10×, HotpotQA 2×–10×, NaturalQuestions 2×–10×, LongBench 2×–10×.")
- figures/fig4_iterative_v0.png [render from fig4_iterative_v0.pdf first] — "Iterative Re-Scoring Benefit at High Compression" (caption: "Dumbbell chart comparing single-pass vs iterative (3 rounds) SSHPC at 8× and 10× compression. Iterative re-scoring provides significant gains on GSM8K (+3.8 at 8×, p=0.0001) and HotpotQA (+2.3 at 8×, p=0.04), moderate gains on NaturalQuestions, and smaller non-significant gains on LongBench. Single-pass values are constant at 70% (baseline reference).")
- figures/fig5_variants_v0.png [render from fig5_variants_v0.pdf first] — "SSHPC Variant Comparison at 8× Compression" (caption: "Comparison of four SSHPC variants at 8× compression across four datasets. Iterative (green) leads on GSM8K (72.9%) and HotpotQA (62.5%). Query-Conditioned (orange) leads on NaturalQuestions (67.6%). Attention-Weighted (purple) is competitive on GSM8K (71.7%) and HotpotQA (62.2%). Base (blue) is the single-pass unconditional variant. Error bars show 95% CI.")
- figures/fig6_latency_v0.png [render from fig6_latency_v0.pdf first] — "End-to-End Latency vs Compression Ratio" (caption: "End-to-end latency (compression + generation) vs compression ratio for four methods. Break-even occurs at 2× for all methods. At 2×, latency ~2500ms; at 4×, ~1250ms; at 8×, ~625ms; at 10×, ~500ms. SSHPC Base (green) and Iterative (purple) overlap with LLMLingua (blue) and No Compression (black) within error bands. Shaded bands show standard deviation across datasets.")
- figures/fig7_surprisal_v0.png [render from fig7_surprisal_v0.pdf first] — "Per-Token Surprisal Distribution (Synthetic)" (caption: "Violin plot of per-token surprisal distribution for GSM8K (synthetic data from log-normal fit to pilot runs). Surprisal values range from near 0 to ~16, with a long right tail. Median ~1.5, mean ~3.2. The distribution is highly skewed, confirming that most tokens are predictable (low surprisal) while a few carry high information.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNG files into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-9fe330-self-surprisal-hard-prompt-compression

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_JKcn7QHhokJh/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [34] HUMAN-USER prompt · 2026-09-20 03:14:45 UTC

```
Survey simple prompt-compression techniques that shrink LLM context length without hurting task accuracy.
```
