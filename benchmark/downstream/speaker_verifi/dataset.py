# -*- coding: utf-8 -*- #
"""*********************************************************************************************"""
#   FileName     [ dataset.py ]
#   Synopsis     [ the speaeker_verifi dataset ]
#   Author       [ S3PRL ]
#   Copyright    [ Copyleft(c), Speech Lab, NTU, Taiwan ]
"""*********************************************************************************************"""


###############
# IMPORTATION #
###############
import os
import random
#-------------#
import numpy as np
import pandas as pd
#-------------#
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data.dataset import Dataset
#-------------#
import os
import torch
import random
import torchaudio
from tqdm import tqdm
from pathlib import Path
from os.path import join, getsize
from joblib import Parallel, delayed
from torch.utils.data import Dataset
from librosa.util import find_files


# Voxceleb 1 + 2 
# preprocessing need seperate folder to dev, train, test
class SpeakerVerifi_train(Dataset):
    def __init__(self, directory_path,max_timestep=16000*5,utter_sample=5):

        self.root = directory_path
        self.all_speakers = [f.path for f in os.scandir(self.root) if f.is_dir()]
        self.utter_number = utter_sample
        self.necessary_dict = self.processing()
        self.dataset = self.necessary_dict['spk_paths'] 
        self.max_timestep = max_timestep
        

    def processing(self):
        
        speaker_num = len(self.all_speakers)
        return {"spk_paths":self.all_speakers,"total_spk_num":speaker_num,"pair_table":None}
    
    def __len__(self):
        return self.necessary_dict['total_spk_num']


    def __getitem__(self, idx):
        
        path = random.sample(find_files(self.dataset[idx], ext=['wav']), self.utter_number)

        x_list = []
        length_list = []

        for i in range(len(path)):
            wav, sr = torchaudio.load(path[i])
            wav = wav.squeeze(0)
            length = wav.shape[0]

            if length > self.max_timestep:
                length = self.max_timestep
                start = random.randint(0,length - self.max_timestep)
                wav = wav[start:start+self.max_timestep]

            x_list.append(wav)
            length_list.append(torch.tensor(length).long())

        return x_list, length_list
    
    def collate_fn(self,data_sample):

        wavs = []
        lengths = []
        indexes = []

        for samples in data_sample:
            wavs.extend(samples[0])
            lengths.extend(samples[1])

        return wavs, lengths, -1


class SpeakerVerifi_dev(Dataset):
    def __init__(self, directory_path, max_timestep, meta_data=None):

        self.root = directory_path
        self.meta_data = meta_data
        self.necessary_dict = self.processing()
        self.max_timestep = max_timestep
        self.dataset = self.necessary_dict['pair_table'] 
        
    def processing(self):
        pair_table = []
        usage_list = open(self.meta_data, "r").readlines()
        for pair in usage_list:
            list_pair = pair.split()
            pair_1= os.path.join(self.root, list_pair[1])
            pair_2= os.path.join(self.root, list_pair[2])
            one_pair = [list_pair[0],pair_1,pair_2 ]
            pair_table.append(one_pair)
        return {"spk_paths":None,"total_spk_num":None,"pair_table":pair_table}

    def __len__(self):
        return len(self.necessary_dict['pair_table'])

    def __getitem__(self, idx):
        y_label, x1_path, x2_path = self.dataset[idx]
        wav1, _ = torchaudio.load(x1_path)
        wav2, _ = torchaudio.load(x2_path)

        wav1 = wav1.squeeze(0)
        wav2 = wav2.squeeze(0)

        length1 = wav1.shape[0]

        if length1 > self.max_timestep:
            length1 = self.max_timestep
            start = random.randint(0,length1 - self.max_timestep)
            wav1 = wav1[start:start+self.max_timestep]

        length2 = wav2.shape[0]

        if length2 > self.max_timestep:
            length2 = self.max_timestep
            start = random.randint(0,length2 - self.max_timestep)
            wav2 = wav1[start:start+self.max_timestep]


        return wav1, wav2, \
        torch.tensor(length1), torch.tensor(length2), \
        torch.tensor(int(y_label[0])),
    
    def collate_fn(self, data_sample):
        wavs1 = []
        wavs2 = []
        lengths1 = []
        lengths2 = []
        ylabels = []

        for samples in data_sample:
            wavs1.append(samples[0])
            wavs2.append(samples[1])
            lengths1.append(samples[2])
            lengths2.append(samples[3])
            ylabels.append(samples[4])

        all_wavs = []
        all_wavs.extend(wavs1)
        all_wavs.extend(wavs2)

        all_lengths = []
        all_lengths.extend(lengths1)
        all_lengths.extend(lengths2)

        return all_wavs, all_lengths, ylabels



class SpeakerVerifi_test(Dataset):
    def __init__(self, directory_path,meta_data=None):

        self.root = directory_path
        self.meta_data = meta_data
        self.necessary_dict = self.processing()
        self.dataset = self.necessary_dict['pair_table'] 
        
    def processing(self):
        pair_table = []
        usage_list = open(self.meta_data, "r").readlines()
        for pair in usage_list:
            list_pair = pair.split()
            pair_1= os.path.join(self.root, list_pair[1])
            pair_2= os.path.join(self.root, list_pair[2])
            one_pair = [list_pair[0],pair_1,pair_2 ]
            pair_table.append(one_pair)
        return {"spk_paths":None,"total_spk_num":None,"pair_table":pair_table}

    def __len__(self):
        return len(self.necessary_dict['pair_table'])

    def __getitem__(self, idx):
        y_label, x1_path, x2_path = self.dataset[idx]
        wav1, _ = torchaudio.load(x1_path)
        wav2, _ = torchaudio.load(x2_path)

        wav1 = wav1.squeeze(0)
        wav2 = wav2.squeeze(0)

        length1 = wav1.shape[0]
        length2 = wav2.shape[0]

        return wav1, wav2, \
        torch.tensor(length1), torch.tensor(length2), \
        torch.tensor(int(y_label[0])),
    
    def collate_fn(self, data_sample):
        wavs1 = []
        wavs2 = []
        lengths1 = []
        lengths2 = []
        ylabels = []

        for samples in data_sample:
            wavs1.append(samples[0])
            wavs2.append(samples[1])
            lengths1.append(samples[2])
            lengths2.append(samples[3])
            ylabels.append(samples[4])

        all_wavs = []
        all_wavs.extend(wavs1)
        all_wavs.extend(wavs2)

        all_lengths = []
        all_lengths.extend(lengths1)
        all_lengths.extend(lengths2)

        return all_wavs, all_lengths, ylabels

