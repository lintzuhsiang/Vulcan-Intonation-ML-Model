import os 
from pydub import AudioSegment
import sys
# sound = AudioSegment.from_file("trim.wav", format="wav")
# path = os.getcwd()+sys.argv[1]
current_path = os.getcwd()
def detect_silence(sound,threshold=-60.0,chunk=10):
    assert chunk > 0
    trim_ms = 0
    while sound[trim_ms:trim_ms+chunk].dBFS < threshold and trim_ms+ chunk < len(sound):
        trim_ms += chunk
    return trim_ms

def trim_test_file(sound_path):
    trim_ms = 0
    chunk = 400
    print(current_path,sound_path)
    for filename in os.listdir(sound_path):
        if filename =='.DS_Store':continue
        print(sound_path,filename)
        sound = AudioSegment.from_file(sound_path+'/'+filename, format="wav")
        sound = sound.set_frame_rate(16000)
        while(trim_ms+chunk < len(sound)):
            trimmed_sound = sound[trim_ms:trim_ms+chunk]
            if not os.path.exists(sound_path):
                os.mkdirs(sound_path)
            trimmed_sound.export(sound_path+"/trimmed_%s"%trim_ms+".wav",format='wav',bitrate='16k')
            trim_ms += chunk

def trim_audio():
    
    print(sys.argv)
    for filename in os.listdir(sys.argv[1]+"/"+sys.argv[2]):
        if filename ==".DS_Store":break
        print(filename)
        sound = AudioSegment.from_file("./"+sys.argv[1]+"/"+sys.argv[2]+"/"+filename, format="wav")
        sound = sound.set_frame_rate(16000)

        start_trim = detect_silence(sound)
        end_trim = detect_silence(sound.reverse())

        trimmed_sound = sound[start_trim:len(sound)-end_trim]
        if not os.isdir(sys.argv[3]):
            os.mkdir("./"+sys.argv[1]+"/"+sys.argv[3])
        
            
        trimmed_sound.export("./"+sys.argv[1]+"/"+sys.argv[3]+"/"+filename,format='wav',bitrate='16k')

def trim_audio2():
    print("please input audio dir, create emotion video dir and trim chunk.")
    print("intonation data 2, Sad, trimmed Sad 400")
    print(sys.argv)
    # for filename in os.listdir(sys.argv[1]):
    filename = sys.argv[2]
    # if filename ==".DS_Store":break
    print(filename)
    trim_ms = 0
    chunk = int(sys.argv[3])
    sound = AudioSegment.from_file("./"+sys.argv[1]+"/"+filename+'.wav', format="wav")
    sound = sound.set_frame_rate(16000)

    start_trim = detect_silence(sound)
    end_trim = detect_silence(sound.reverse())

    trimmed_sound = sound[start_trim:len(sound)-end_trim]
    if not os.path.isdir(sys.argv[2]):
        os.mkdir("./"+sys.argv[1]+"/"+sys.argv[2])
    
    while(trim_ms+chunk < len(sound)):
        trimmed_sound = sound[trim_ms:trim_ms+chunk]
        trimmed_sound.export("./"+sys.argv[1]+"/"+sys.argv[2]+"/trimmed_%s_%s"%(filename,trim_ms)+".wav",format='wav',bitrate='16k')
        trim_ms += chunk

if __name__ == '__main__':
    trim_audio2()
    # trim_test_file(sys.argv[1])