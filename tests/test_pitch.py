import math
import tempfile
import unittest
import wave
from pathlib import Path
import numpy as np
from mir.pitch import frame_pitch, analyze

class PitchTests(unittest.TestCase):
    def test_sines(self):
        for rate in (8000,16000,44100):
            t=np.arange(round(rate*.06))/rate
            for hz in (110,220,440,880):
                with self.subTest(rate=rate,hz=hz):
                    p=frame_pitch(.3*np.sin(2*np.pi*hz*t),rate)
                    self.assertIsNotNone(p)
                    self.assertLess(abs(1200*math.log2(p["hz"]/hz)),25)
    def test_harmonic(self):
        t=np.arange(960)/16000
        p=frame_pitch(.15*np.sin(2*np.pi*220*t)+.25*np.sin(2*np.pi*440*t),16000)
        self.assertLess(abs(p["hz"]-220),3)
    def test_silence_and_noise(self):
        self.assertIsNone(frame_pitch(np.zeros(960),16000))
        self.assertIsNone(frame_pitch(np.random.default_rng(7).normal(0,.15,960),16000))
    def test_wav_and_stereo_rejection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"tone.wav"
            for ch in (1,2):
                with wave.open(str(p),"wb") as w:
                    w.setparams((ch,2,16000,0,"NONE","not compressed"))
                    v=(10000*np.sin(2*np.pi*440*np.arange(16000)/16000)).astype("<i2")
                    w.writeframes(np.repeat(v,ch).tobytes())
                if ch==2:
                    with self.assertRaises(ValueError): analyze(p)
                else:
                    r=analyze(p)
                    self.assertEqual(r["transcription"],"NOT_RUN")
                    self.assertTrue(all(abs(x["candidate"]["hz"]-440)<3 for x in r["frames"]))
