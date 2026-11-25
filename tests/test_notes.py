import unittest
from mir.notes import notes_from_pitch

def record(values):
    return {"schema_version":"0.1.0","method":"normalized-autocorrelation-baseline","source_sha256":"a"*64,"frames":[{"center_s":round(.03+i*.03,6),"candidate":None if v is None else {"midi_candidate":v,"periodicity":.95}} for i,v in enumerate(values)]}

class NotesTests(unittest.TestCase):
    def test_two_notes_and_silence(self):
        r=notes_from_pitch(record([60.02]*4+[None]*2+[64.1]*5))
        self.assertEqual([n["pitch_midi"] for n in r["notes"]],[60,64])
        self.assertAlmostEqual(r["notes"][0]["start_s"],.015)
        self.assertEqual(r["status"],"REVIEW_ONLY")
    def test_short_and_uncertain(self):
        self.assertEqual(notes_from_pitch(record([60]*2+[60.49]*4+[None]))["notes"],[])
    def test_clock_and_corruption(self):
        r=record([60]*4); r["frames"][1]["center_s"]=.2
        with self.assertRaises(ValueError): notes_from_pitch(r)
        r=record([60]*4); r["frames"][0]["candidate"]["periodicity"]=.3
        with self.assertRaises(ValueError): notes_from_pitch(r)
