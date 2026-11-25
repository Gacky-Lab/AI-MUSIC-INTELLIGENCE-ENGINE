"""Bounded PCM16 WAV evidence extractor; not a beat or pitch detector."""
import argparse, hashlib, json, math, statistics, struct, wave
from pathlib import Path

MAX_BYTES=128*1024*1024
MAX_SECONDS=300
VERSION="0.1.0"

def dbfs(ratio):
    return 20*math.log10(ratio) if ratio>0 else None

def estimate_pulse(energies,window_s):
    onsets=[]
    for i in range(1,len(energies)):
        prev=max(energies[i-1],1e-12)
        cur=energies[i]
        t=i*window_s
        if cur>=10**(-35/20) and cur/prev>=10**(8/20) and (not onsets or t-onsets[-1]>=0.15):
            onsets.append(t)
    intervals=[b-a for a,b in zip(onsets,onsets[1:])]
    estimate=None
    if len(intervals)>=4:
        m=statistics.median(intervals)
        mad=statistics.median(abs(x-m) for x in intervals)
        # Reject missed/double events as well as high typical dispersion.
        if 0.25<=m<=1 and mad<=0.10*m and all(abs(x-m)<=0.20*m for x in intervals):
            estimate=round(60/m,3)
    return {"status":"CANDIDATE" if estimate is not None else "UNKNOWN","pulse_per_minute":estimate,
            "energy_onsets_s":[round(t,6) for t in onsets],"verified_musical_bpm":False}

def analyze(path):
    path=Path(path)
    with path.open("rb") as stream:
        # Bound before decoding; hash and decode the same in-memory snapshot.
        data=stream.read(MAX_BYTES+1)
    if len(data)>MAX_BYTES: raise ValueError("file too large")
    import io
    sha=hashlib.sha256(data).hexdigest()
    with wave.open(io.BytesIO(data),"rb") as w:
        rate,ch,n=w.getframerate(),w.getnchannels(),w.getnframes()
        if w.getsampwidth()!=2 or ch not in (1,2) or not 8000<=rate<=96000 or not 0<n<=rate*MAX_SECONDS or w.getcomptype()!="NONE":
            raise ValueError("expected bounded PCM16 mono/stereo WAV")
        win=max(1,rate//50)
        count=0; total_sq=0; peak=0; clips=0; energies=[]
        remaining=n
        while remaining:
            take=min(win,remaining)
            raw=w.readframes(take)
            if len(raw)!=take*ch*2: raise ValueError("truncated WAV")
            vals=[v[0] for v in struct.iter_unpack("<h",raw)]
            sq=sum(v*v for v in vals)
            total_sq+=sq; count+=len(vals)
            peak=max(peak,max(abs(v) for v in vals))
            clips+=sum(v in (-32768,32767) for v in vals)
            if take==win: energies.append(math.sqrt(sq/len(vals))/32768)
            remaining-=take
    return {"schema_version":VERSION,"source_sha256":sha,"sample_rate_hz":rate,"channels":ch,
            "sample_frames":n,"duration_s":n/rate,"rms_dbfs":dbfs(math.sqrt(total_sq/count)/32768),
            "sample_peak_dbfs":dbfs(peak/32768),"clipped_samples":clips,
            "silent_window_fraction":sum(e<=0.001 for e in energies)/len(energies) if energies else None,
            "window_samples":win,"pulse":estimate_pulse(energies,win/rate),
            "pitch_status":"NOT_RUN","lyrics_status":"NOT_RUN","artistic_acceptance":"NOT_RUN"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("wav",type=Path); p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        if args.output and args.output.resolve()==args.wav.resolve(): raise ValueError("output must not overwrite source")
        result=analyze(args.wav)
        rendered=json.dumps(result,indent=2,allow_nan=False)+"\n"
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            with args.output.open("x",encoding="utf-8") as f: f.write(rendered)
        print(rendered,end="")
    except (ValueError,OSError,wave.Error,EOFError,struct.error) as e:
        p.exit(2,f"ERROR: {e}\n")
if __name__=="__main__": main()
