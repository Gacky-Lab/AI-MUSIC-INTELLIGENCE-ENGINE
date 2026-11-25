# AMIE-SRS-001 v0.1
## Purpose
Provide reusable, independently measured signal evidence to the four creative-production projects. The analyzer is not the acceptance authority for artistic quality. The final master hash is the binding identity; source audio and re-rendered master are different artifacts.

| ID | Requirement |
|---|---|
| MIR-01 | Validate bounded uncompressed PCM16 WAV; reject malformed, empty or unsupported inputs. |
| MIR-02 | Report decoded sample frames, rate, channels, duration, SHA-256. |
| MIR-03 | Report channel-preserving RMS, sample peak, clipping count and silent-window fraction; document threshold. |
| MIR-04 | Return energy onset candidates and pulse-rate estimate only when sufficient regular evidence exists; otherwise UNKNOWN. |
| MIR-05 | Distinguish synthetic evidence from real-song verification; no automatic musical acceptance. |
| MIR-06 | Versioned JSON contract, deterministic analysis, input identity, offline CI. |
| MIR-07 | Later independent pitch/beat/transcription evidence, uncertainty, reference comparisons. |
| MIR-08 | Later adapters for Suno, VOCALOID and Video IR without rewriting upstream APIs. |

## Architecture
PCM decode -> per-channel-preserving energy windows -> features -> conservative onset/pulse candidate -> versioned evidence. Future pluggable MIR, DSP, transcription and forced alignment engines must report algorithm/model version, units, time origin and confidence limitations.

## Boundaries
No trained model in P0. No LUFS, true peak, source separation, phonemes, singing expression or lyric alignment in P0. Pulse-rate is not a musical beat grid. Never substitute this analyzer for existing Suno independent QA until equivalence is tested; upstream adapters must check master SHA and analysis version. Human approval remains external.
