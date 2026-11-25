# Monophonic pitch candidate baseline

Separate optional module; the existing Analysis Evidence v0.1.0 is unchanged.

```sh
python -m pip install -r requirements-pitch.txt
python -m mir.pitch mono.wav --output pitch.json
python -m unittest discover -s tests -v
```

60 ms frames / 30 ms hop, normalized autocorrelation, RMS and periodicity rejection; mono PCM16 only, <=60 seconds. Synthetic sine frequencies (110–880 Hz), harmonics, noise, silence and invalid stereo are tested. Periodicity is not calibrated confidence. No polyphonic pitch, source separation, singing accuracy, note segmentation or real-song benchmark claim. Pitch candidates must be reviewed before use.
