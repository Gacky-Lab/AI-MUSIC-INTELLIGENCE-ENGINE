# Creative Deviation Evaluation (CDE) v0.1

**Beyond Acceptance: Distinguishing Creative Discovery from Compromise in AI-Assisted Music Editing**

Gacky-Lab · Independent research proposal · 2026-11-26 (JST)  
**Status: Proposed / Empirically unvalidated (NOT_RUN).**

[One-page research framework (HTML)](CDE_public_research_framework.html) — download and open locally in a browser to view the full layout.

> Not every deviation is a defect. Not every acceptance is a discovery. Not every rejection is a failure.

## Abstract

AI-assisted music editing can alter expressive elements that a creator intended to preserve. Accepting a musical artifact does not necessarily mean that the creator prefers each individual change; rejecting an artifact does not imply that all of its changes are undesirable. CDE proposes an evaluation protocol combining prospective intent records, observed musical changes, artifact-level adoption, controlled restoration comparisons, and delayed preference reassessment. Its aim is to investigate whether otherwise overlooked creative decisions can be recovered as evidence-linked knowledge for subsequent production.

The proposed contribution is the integrated protocol, not a new generation model, similarity metric, selective-undo algorithm, preference elicitation technique or theory of musical taste. No empirical result or priority claim is made.

## 1. Scope and proposed contribution

**Research question:** When an AI-assisted edit changes a musical target that the creator intended to preserve, does the creator prefer the change itself, independently of whether the whole edited artifact was adopted? Does that preference persist under a repeated comparison?

The unit of observation is **creator × artifact/edit episode × target change**. Multiple target changes may belong to one artifact; they are not independent observations. Intent must be recorded before the edit, not reconstructed after listening. A target delegated to the system or left unspecified is not automatically an unintended deviation.

### Five observation fields

| ID | Field | Values / interpretation |
|---|---|---|
| A | Prospective intent | CHANGE / PRESERVE / DELEGATE / UNSPECIFIED |
| B | Observed change | CHANGED / UNCHANGED / UNKNOWN; compare with A |
| C | Artifact adoption (before restoration comparison) | ACCEPT / HOLD / REJECT |
| D | Restoration-comparison preference | EDITED / RESTORED / TIE / UNSURE / MISSING |
| E | Temporal preference pattern | Derived from D at two or more prespecified times; not an independent predictor |

The main matrix applies only to cases with prospectively recorded PRESERVE intent and a verified CHANGED target. Store the original observations; do not force missing or ambiguous cases into the matrix.

### Creative Deviation Matrix

| Artifact adoption | Prefers restored version | Prefers edited version |
|---|---|---|
| ACCEPT | CDE-02 — compromised-adoption candidate | CDE-01 — creative-discovery candidate |
| REJECT | CDE-04 — unintended-loss candidate | CDE-03 — partial-discovery candidate |

CDE-U: HOLD, TIE, UNSURE, missing observation or insufficient evidence; retain the specific reason. The four labels are operational candidates, not psychological diagnoses. A restoration preference does not establish reluctant acceptance, and preference for an edited target does not establish that it is the cause of artifact adoption. Ask the creator why they chose it; keep self-reported reasons separate from observed choices.

### Temporal classification

| Code | Initial preference | Delayed preference |
|---|---|---|
| S1 | EDITED | EDITED |
| S2 | EDITED | RESTORED |
| S3 | RESTORED | EDITED |
| S4 | RESTORED | RESTORED |
| SU | Any other combination | Record raw observations and reason |

S1/S4 indicate agreement across the measured occasions, not permanent preferences. S2/S3 indicate a directional reversal, not necessarily a psychological change caused by time. Repeated exposure, context and order can affect responses. Keep CDE class at the initial comparison and temporal code separately.

### Musical target tags (non-exclusive; not claimed as novel)

Composition (melody, harmony, rhythm); expression (timing, dynamics, vibrato); acoustics (timbre, mix); language (lyrics, pronunciation); context (phrase/section placement); relationships between elements. Specify the actual target, boundaries, units, source and transformation.

## 2. Proposed controlled protocol

1. Obtain consent and rights to use the material. Record the creator's prospective intent, target, and permitted edits before editing.
2. Save the original artifact, actual edited artifact, edit settings and observable changes. Verify whether a PRESERVE target changed within prespecified tolerance. Record artifact adoption before any restoration variant is presented.
3. Construct a restoration comparator that keeps the intended edit while reverting the target change only. For example, both variants contain the same revised lyrics and accompaniment, but differ in a specified vibrato intervention. Verify render controls and document deviations, source hashes, software versions, time boundaries and uncertainty. If the restoration is not feasible, mark NOT_RUN/BLOCKED; if other changes cannot be ruled out, label COMPOSITE and report descriptively outside the target-specific primary analysis.
4. Compare edited and restored variants with randomized/counterbalanced order, condition labels concealed where feasible, matched playback conditions and an explicit tie/unsure option. Record the choice and reasons separately. Creators may recognize familiar material; do not claim double blinding.
5. Reassess the same comparison after a prespecified interval (e.g. 24–48 hours for a pilot), with order randomized again. Record intervening exposure and missing responses. Do not infer that time itself caused a reversal.
6. Derive candidate classes only from eligible observations. Retain contradictions, ties, exclusions and null results. Save any reuse suggestion as a hypothesis, not as a generalizable artistic rule.

For a controlled singing-expression pilot, a two-by-two design crossing the intended edit and target expression may be used where feasible, with a separate check for rendering confounds. A deliberately simulated deviation is labelled SIMULATED, not an observed AI editing failure. Naturally occurring AI deviations require a separate authorized validation study.

## 3. Questions, outcomes and analysis plan

- H1: artifact adoption and target-level preference can diverge (CDE-02 or CDE-03).
- H2: restoration comparison adds information beyond adoption-only records; compare with an adoption-only baseline.
- H3: target preference can differ between the initial and delayed sessions.
- H4 (later study): CDE records may support later production decisions better than ordinary edit histories, under matched review time and editing budget. Evaluate on held-out creative tasks; no transfer claim from an individual case.

Primary descriptive outcome: proportion of eligible, decisive initial comparisons in CDE-02 or CDE-03; report numerator and denominator. Secondary outcomes: restoration preference among accepted cases (CDE-02 / [CDE-01 + CDE-02]); edited preference among rejected cases (CDE-03 / [CDE-03 + CDE-04]); agreement and directional reversal among valid paired decisive responses. Use neutral observed-rate names, not a measured psychological compromise/discovery rate. Report ties, holds, missing responses, control failures and coverage separately. If a denominator is zero, report undefined. Cluster by creator and artifact when estimating uncertainty; a small individual pilot is exploratory and does not support population inference. Prespecify sampling, tolerances, analysis and stopping rules before a confirmatory study. No acceptance threshold or artistic score is defined.

## 4. Related work and originality boundaries

| Work | Established contribution relevant to CDE | Boundary of proposed CDE contribution |
|---|---|---|
| Louie et al., [Novice-AI Music Co-Creation via AI-Steering Tools for Deep Generative Models](https://doi.org/10.1145/3313831.3376739), CHI 2020 (Cococo) | Interactive steering and auditioning generated alternatives | CDE asks about preference for an unintended change separately from whole-artifact adoption. |
| Kim et al., [Amuse: Human-AI Collaborative Songwriting with Multimodal Inspirations](https://gclef-cmu.org/research/2025kimamuse/), CHI 2025 | Creative songwriting support through multimodal inspiration | CDE proposes a prospective intention record and restoration-based evaluation, not an inspiration tool. |
| Vishe et al., [Evaluating Music Context Preservation: A Multi-facet Framework for Music Editing Systems](https://arxiv.org/abs/2512.14629v2), 2025–2026 (MuseCPEval) | Measuring preservation of musical facets during editing | CDE treats verified change as evidence, not as a substitute for the creator's choice. |
| Cervera et al., [SMEBench](https://arxiv.org/abs/2610.36715), 2026 preprint | Controlled symbolic edits and matched renders for benchmarking music editing | CDE uses controlled comparisons to study creative decisions, not to benchmark editing fidelity alone. |
| Madison & Schiölde, [Repeated Listening Increases the Liking for Music Regardless of Its Complexity](https://doi.org/10.3389/fnins.2017.00147), 2017 | Repeated listening can alter music liking | CDE records delayed target-level preference; it does not claim the exposure effect as a discovery. |

These selected references are a starting point, not a systematic review or patent clearance. Selective undo, human-AI co-creation, pairwise comparison, preference learning and repeated listening are established methods. The proposed original contribution is their operational combination around prospective preservation intent, artifact adoption and restoration-comparison preference, with delayed reassessment. The selected public literature reviewed motivates the question; it does not prove that no equivalent protocol exists. Academic novelty and usefulness remain to be tested.

## 5. Integration and evidence boundaries

This is a research-only directory in AI-MUSIC-INTELLIGENCE-ENGINE. Existing MIR evidence (see [contract](../../docs/evidence_contract.md)) is referenced by source hash, never overwritten. It does not decide artistic quality. Upstream editing requirements and approved manifests remain the responsibility of their existing production projects; existing study-plan and render controls are reused where appropriate rather than duplicated. This proposal adds no runtime dependency, paid call, model training, automated artistic approval, or cross-repository API. No affiliation with product providers is implied.

CDE records could later link creative choices to controlled comparison audio, intent, edit provenance, observations and a clearly labelled reuse hypothesis. No schema or execution pipeline is claimed implemented in v0.1.

## 6. Rights, reproducibility and status

Use only original or explicitly authorized music, lyrics and voices; review applicable service terms before any research use of third-party outputs. Do not upload private audio, personal listening responses, licensed voicebanks or credentials. Record informed consent, retention and sharing permissions before human studies. Public examples must be synthetic or permission-cleared. Initial validation is offline and does not consume paid service credits.

| Milestone | Status |
|---|---|
| Research proposal and public one-page framework | DOCUMENTED |
| Controlled audio stimuli / actual AI deviations | NOT_RUN |
| Creator listening data and delayed assessment | NOT_RUN |
| Empirical effect estimates and replication | NOT_RUN |
| Knowledge reuse / cross-project integration | NOT_RUN |

**Human-led creativity. Evidence-driven understanding.**

---

## 日本語概要

CDEは、AI音楽編集で意図せず変化した表現に対して、作品全体の採否と個別変化の選好を分離する研究提案です。保持を希望した対象が変化した場合、意図した編集を維持しながら対象だけを復元した比較音源を用意し、創作者がどちらを選ぶか、後日も同じ判断をするかを調べます。

採用曲にも戻したい変化があり、不採用曲にも残したい表現があるかもしれません。これを創作上の発見・妥協の候補として整理します。心理的な理由は本人の回答と区別して記録し、統制不能や判定不能を無理に分類しません。単独効果や他楽曲への転用可能性は未検証です。

[公開用ワンページ（HTML）](CDE_public_research_framework.html) をダウンロードしブラウザで開くと図版を閲覧できます。研究は特定サービスに依存せず、自作・許諾済み素材を対象とします。世界初、実証済み、企業との共同研究を主張するものではありません。
