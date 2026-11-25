"""Bounded, monophonic F0 candidate baseline; not vocal separation or verified transcription."""
import argparse
import hashlib
import io
import json
import math
import wave
from pathlib import Path

import numpy as np

MAX_BYTES = 64 * 1024 * 1024
MAX_SECONDS = 60

def frame_pitch(samples, rate):
    x = np.asarray(samples, dtype=np.float64)
    x = x - x.mean()
    rms = float(np.sqrt(np.mean(x*x)))
    if rms < 0.005:
        return None
    lo, hi = math.ceil(rate/1000), min(math.floor(rate/70), len(x)//2)
    if lo >= hi:
        return None
    # Normalized autocorrelation; select first strong local peak to reduce octave errors.
    ac = np.correlate(x, x, mode="full")[len(x)-1:len(x)+hi]
    sums = np.r_[0., np.cumsum(x*x)]
    lags = np.arange(hi+1)
    den = np.sqrt(sums[len(x)-lags] * (sums[-1]-sums[lags]))
    corr = np.divide(ac, den, out=np.zeros_like(ac), where=den>0)
    peaks = [k for k in range(lo+1, hi) if corr[k]>=corr[k-1] and corr[k]>corr[k+1] and corr[k]>=0.8]
    if not peaks:
        return None
    strongest = max(float(corr[k]) for k in peaks)
    k = next(k for k in peaks if corr[k]>=0.95*strongest)
    a,b,c = corr[k-1:k+2]
    denom = a-2*b+c
    delta = float(0.5*(a-c)/denom) if abs(denom)>1e-12 else 0.
    hz = rate/(k+max(-.5,min(.5,delta)))
    return {"hz":round(hz,3),"midi_candidate":round(69+12*math.log2(hz/440),3),
            "periodicity":round(float(corr[k]),4)}

def analyze(path):
    with Path(path).open("rb") as f:
        data=f.read(MAX_BYTES+1)
    if len(data)>MAX_BYTES: raise ValueError("WAV too large")
    with wave.open(io.BytesIO(data),"rb") as w:
        rate,n=w.getframerate(),w.getnframes()
        if w.getnchannels()!=1 or w.getsampwidth()!=2 or w.getcomptype()!="NONE" or not 8000<=rate<=48000 or not 0<n<=rate*MAX_SECONDS:
            raise ValueError("expected <=60s mono PCM16 WAV")
        raw=w.readframes(n)
        if len(raw)!=n*2: raise ValueError("truncated WAV")
    x=np.frombuffer(raw,dtype="<i2").astype(np.float64)/32768
    size,hop=round(rate*.06),round(rate*.03)
    frames=[]
    for start in range(0,len(x)-size+1,hop):
        candidate=frame_pitch(x[start:start+size],rate)
        frames.append({"center_s":round((start+size/2)/rate,6),"candidate":candidate})
    return {"schema_version":"0.1.0","source_sha256":hashlib.sha256(data).hexdigest(),
            "method":"normalized-autocorrelation-baseline","sample_rate_hz":rate,
            "scope":"monophonic candidate only","frames":frames,
            "real_song_accuracy":"NOT_RUN","transcription":"NOT_RUN"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("wav",type=Path); p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        if a.output.resolve()==a.wav.resolve(): raise ValueError("cannot overwrite input")
        report=analyze(a.wav)
        with a.output.open("x",encoding="utf-8") as f: json.dump(report,f,indent=2,allow_nan=False)
    except (ValueError,OSError,wave.Error,EOFError) as e: p.exit(2,f"ERROR: {e}\n")
if __name__=="__main__": main()
