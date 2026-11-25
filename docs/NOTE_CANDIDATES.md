# Review-only note candidates

`python -m mir.notes pitch.json --output notes.json` groups adjacent quantized monophonic pitch frames (minimum 3, within 35 cents) into candidate MIDI pitches and approximate spans. It is not a MIDI transcription engine: repeated same pitches may merge, vibrato or glides can fragment, silence and noisy evidence can be rejected, and times are frame-grid estimates. Real singing and polyphonic input remain NOT_RUN. Tests use authored pitch sequences; no musical accuracy claim.
