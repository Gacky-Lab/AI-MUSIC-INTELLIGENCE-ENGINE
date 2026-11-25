import hashlib, math, struct, tempfile, unittest, wave
from pathlib import Path
from mir.analyze import analyze, estimate_pulse

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"test.wav"
    def tearDown(self): self.tmp.cleanup()
    def write(self, values, ch=1,width=2):
        with wave.open(str(self.path),"wb") as w:
            w.setnchannels(ch); w.setsampwidth(width); w.setframerate(8000)
            w.writeframes(struct.pack("<"+"h"*len(values),*values) if width==2 else bytes(values))
    def test_pulse(self):
        self.write([12000 if 160<=i%4000<800 else 0 for i in range(48000)])
        p=analyze(self.path)["pulse"]
        self.assertEqual(p["status"],"CANDIDATE")
        self.assertAlmostEqual(p["pulse_per_minute"],120,delta=3)
    def test_silence(self):
        self.write([0]*8000)
        a=analyze(self.path)
        self.assertIsNone(a["rms_dbfs"]); self.assertIsNone(a["sample_peak_dbfs"])
        self.assertEqual(a["silent_window_fraction"],1)
        self.assertEqual(a["pulse"]["status"],"UNKNOWN")
    def test_stereo(self):
        self.write([10000,-10000]*8000,ch=2)
        self.assertAlmostEqual(analyze(self.path)["rms_dbfs"],20*math.log10(10000/32768))
    def test_invalid_width(self):
        self.write([128]*8000,width=1)
        with self.assertRaises(ValueError): analyze(self.path)
    def test_empty(self):
        self.write([])
        with self.assertRaises(ValueError): analyze(self.path)
    def test_clip_hash(self):
        self.write([-32768,32767,0,0])
        a=analyze(self.path)
        self.assertEqual(a["clipped_samples"],2)
        self.assertEqual(a["sample_peak_dbfs"],0)
        self.assertEqual(a["source_sha256"],hashlib.sha256(self.path.read_bytes()).hexdigest())
        self.assertEqual(a["sample_frames"],4)
    def test_irregular(self):
        e=[0.0]*200
        for i in [2,22,51,70,99,130,155]: e[i]=0.5
        self.assertEqual(estimate_pulse(e,.02)["status"],"UNKNOWN")
    def test_truncated(self):
        self.write([0]*8000)
        self.path.write_bytes(self.path.read_bytes()[:-10])
        with self.assertRaises(ValueError): analyze(self.path)
