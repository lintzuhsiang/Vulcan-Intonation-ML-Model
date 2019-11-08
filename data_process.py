
from python_speech_features import mfcc
from trim_audio import trim_test_file
import soundfile as sf
import random
import os
import numpy as np



# def data_prepossing(data_path):
class Data_process():
    def __init__(self):
        self.window_length = 1.0
        self.test_x = np.zeros((1,99,13))
        self.train_x = np.zeros((1,99,13))
        self.train_y = np.zeros(1)
        self.sample_per_wav = 10

    def train_data(self,data_path):
    
        for filename in os.listdir(os.getcwd()+'/'+data_path+'/'):
            print(filename)
            if filename =='.DS_Store':continue
    
            signal,rate = sf.read(data_path+'/'+filename)
            wav_length = len(signal)/rate  #second
            

            for index in range(self.sample_per_wav): # take ten windows in an audio file
                window_seed = random.uniform(0,abs(wav_length-self.window_length))
                window_range = (window_seed,window_seed+self.window_length)
                window_signal = signal[int(window_range[0]*rate):int(window_range[1]*rate)]
                # if len(window_signal) != 16000: break
                mfcc_feat = mfcc(window_signal)
                mfcc_feat_scale = mfcc_feat / np.linalg.norm(mfcc_feat)
                # result_array=(mfcc_feat-np.min(mfcc_feat))/np.ptp(mfcc_feat)

                mfcc_feat_scale = mfcc_feat_scale[np.newaxis,:]
                self.train_x = np.concatenate((self.train_x,mfcc_feat_scale))

                label = np.append([],int(filename.split('_')[1][0]))
            label = np.repeat(label,self.sample_per_wav)
            # print(label)
            
            self.train_y = np.concatenate((self.train_y,label))
            # print(train_x.shape,train_y.shape)
        np.save('train_x_1.npy',self.train_x)
        np.save('train_y_1.npy',self.train_y)
        return self.train_x,self.train_y


    def test_data(self,data_path):
    
        for filename in os.listdir(os.getcwd()+'/'+data_path+'/'):
            if filename =='.DS_Store':continue
    
            signal,rate = sf.read(data_path+'/'+filename)
            wav_length = len(signal)/rate  #second

            # for index in range(sample_per_wav): # take ten windows in an audio file
            window_seed = random.uniform(0,abs(wav_length-self.window_length))
            window_range = (window_seed,window_seed+self.window_length)
            window_signal = signal[int(window_range[0]*rate):int(window_range[1]*rate)]
        
            mfcc_feat = mfcc(window_signal)
            mfcc_feat_scale = mfcc_feat / np.linalg.norm(mfcc_feat)
            # result_array=(mfcc_feat-np.min(mfcc_feat))/np.ptp(mfcc_feat)
            
            mfcc_feat_scale = mfcc_feat_scale[np.newaxis,:]
            self.test_x = np.concatenate((self.test_x,mfcc_feat_scale))


        return self.test_x[1:]

