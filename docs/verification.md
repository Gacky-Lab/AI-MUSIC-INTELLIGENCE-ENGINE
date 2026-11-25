# DVP / DVR
| Test | Target | Evidence at authoring |
|---|---|---|
| T01 | Known 120 pulse/min fixture within ±3 pulse/min | CI pending |
| T02 | Silence: null RMS/peak, UNKNOWN pulse | CI pending |
| T03 | Stereo antiphase: no cancellation | CI pending |
| T04 | Unsupported 8-bit/empty input rejected | CI pending |
| T05 | Known clipped samples, source SHA, time origin | CI pending |
| T06 | Irregular pulses: UNKNOWN | CI pending |
| T07 | JSON schema validation against report | Future |
| T08 | Real music beat/pitch/lyrics vs human reference | NOT_RUN |
| T09 | Cross-project adapter and final-master hash mismatch | NOT_RUN |

P0: synthetic fixture, CLI, deterministic evidence. P1: authorized real WAV and annotated onset/beat comparisons; assess alternative tempo hypotheses, false positives, genre coverage. P2: pitch and note candidates with RMVPE/pYIN or other licensed model after evaluation. P3: lyric/phoneme alignment and expression; independently annotated reference and Japanese singing validation. P4: integration with Suno/VOCALOID/MV and controlled comparisons. No commercial-quality or efficacy claims without data.

DVR: This PR is a candidate. Record the exact CI run/commit after execution. Synthetic test results do not establish real-song accuracy.
