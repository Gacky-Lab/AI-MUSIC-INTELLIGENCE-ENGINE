"""Group monophonic pitch frames into review-only note candidates."""
import argparse
import json
import math
from pathlib import Path

def notes_from_pitch(report):
    if report.get("schema_version")!="0.1.0" or report.get("method")!="normalized-autocorrelation-baseline":
        raise ValueError("unsupported pitch evidence")
    frames=report.get("frames")
    if not isinstance(frames,list) or len(frames)>2000: raise ValueError("invalid frame count")
    notes=[]; active=None; previous=None
    def finish():
        nonlocal active
        if active and active["frames"]>=3:
            notes.append({"pitch_midi":active["pitch"],"start_s":round(max(0,active["first"]-.015),6),
                          "end_s":round(active["last"]+.015,6),"voiced_frames":active["frames"]})
        active=None
    for f in frames:
        t=f.get("center_s")
        if type(t) not in (float,int) or not math.isfinite(t) or not 0<=t<=60 or (previous is not None and abs(t-previous-.03)>.0002):
            raise ValueError("invalid frame clock")
        previous=t
        c=f.get("candidate")
        if c is None: finish(); continue
        p=c.get("midi_candidate"); q=c.get("periodicity")
        if type(p) not in (float,int) or not math.isfinite(p) or not 0<=p<=127 or type(q) not in (float,int) or not math.isfinite(q) or not .8<=q<=1.001:
            raise ValueError("invalid pitch evidence")
        pitch=round(p)
        if abs(p-pitch)>.35: finish(); continue
        if active is None or active["pitch"]!=pitch:
            finish(); active={"pitch":pitch,"first":t,"last":t,"frames":1}
        else:
            active["last"]=t; active["frames"]+=1
    finish()
    source=report.get("source_sha256")
    if not isinstance(source,str) or len(source)!=64 or any(c not in "0123456789abcdef" for c in source): raise ValueError("invalid source hash")
    return {"schema_version":"0.1.0","source_sha256":source,"status":"REVIEW_ONLY","method":"quantized-monophonic-pitch-runs","notes":notes,"real_song_accuracy":"NOT_RUN","lyrics_alignment":"NOT_RUN"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("pitch",type=Path); p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        if a.pitch.stat().st_size>1024*1024: raise ValueError("pitch file too large")
        r=notes_from_pitch(json.loads(a.pitch.read_text(encoding="utf-8")))
        with a.output.open("x",encoding="utf-8") as f: json.dump(r,f,indent=2,allow_nan=False)
    except (ValueError,OSError,TypeError,AttributeError) as e: p.exit(2,f"ERROR: {e}\n")
if __name__=="__main__": main()
