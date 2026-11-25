"""Create an original 6s 120 pulse/min synthetic WAV."""
from pathlib import Path
import wave,math,struct
ROOT=Path(__file__).resolve().parents[1]
def main():
    path=ROOT/"out/demo.wav"
    path.parent.mkdir(parents=True,exist_ok=True)
    rate=16000
    data=bytearray()
    for i in range(rate*6):
        phase=(i%(rate//2))/rate
        val=int(16000*math.sin(2*math.pi*440*i/rate)) if 0.02<=phase<0.10 else 0
        data.extend(struct.pack("<h",val))
    with wave.open(str(path),"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(data)
    print(path)
if __name__=="__main__": main()
