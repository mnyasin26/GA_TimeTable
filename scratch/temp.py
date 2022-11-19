import json
import random
from copy import deepcopy


input_file = 'input.json'
# output_file = 'classes/output3.json'

# Baca data json 
def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    return data

def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)

# Masukan data json ke variabel
test = load_data(input_file)

def randomizer(source: list):
    temp = source[random.randrange(0, len(source))]
    return temp

def generate_gen():
    space = {}

    for angkatan in test['Kelas']:
        kelas_temp = {}
        for kelas in test['Kelas'][angkatan]:
            hari_temp = {}
            for hari in test['Waktu']:
                alokasi_waktu = 0
                mapel_temp = {}
                for jam in test['Waktu'][hari]:
                    if (alokasi_waktu == 0):
                        temp_id = {}

                        temp_mapel = randomizer(test['List_Mapel'])
                        temp_guru = randomizer(test['Guru'])
                        alokasi_waktu = int(temp_mapel['Alokasi_Jam'])

                        temp_id['Mapel'] = temp_mapel['Mapel']
                        temp_id['ID'] = temp_mapel['ID']
                        temp_id['Guru'] = temp_guru
                        mapel_temp[temp_mapel['ID']] = temp_id
                        mapel_temp[temp_mapel['ID']]['Slot_waktu'] = []
                    
                    
                    mapel_temp[temp_mapel['ID']]['Slot_waktu'].append(jam)
                    alokasi_waktu = alokasi_waktu - 1
                hari_temp[hari] = mapel_temp
            kelas_temp[kelas] = hari_temp
        space[angkatan] = kelas_temp

    return space

guru = {test['Guru'][i]: {'Mapel':[],'Slot_waktu':[]} for i in range(0, len(test['Guru']))}
for i in guru:
    guru[i]['Slot_waktu'] = {}
    for j in test['Waktu']:
        guru[i]['Slot_waktu'][j] = []
        


mutan = generate_gen()
write_data(mutan, 'test.json')
# for angkatan in mutan:
#     for kelas in mutan[angkatan]:
#         for hari in mutan[angkatan][kelas]:
#             for jam in mutan[angkatan][kelas][hari]:
                
#                 # Koneksi guru ke mapel
#                 guru[mutan[angkatan][kelas][hari][jam]['Guru']]['Mapel'].append(mutan[angkatan][kelas][hari][jam]['ID'])

#                 # Masukkan slot waktu tiap guru
#                 for slot in mutan[angkatan][kelas][hari][jam]['Slot_waktu']:
#                     guru[mutan[angkatan][kelas][hari][jam]['Guru']]['Slot_waktu'][hari].append(slot)
                    
# # Jika ada Guru yang sama di slot waktu yang sama disetiap hari (irisan) (+1)
# for j in guru:
#     for k in guru[j]['Slot_waktu']:
        
#         result = dict((i, guru[j]['Slot_waktu'][k].count(i)) for i in guru[j]['Slot_waktu'][k])
#         # cost += len(guru[j]['Slot_waktu'][k]) - len(result)
#         print(result)
#         # print(j)
#         # print(k)
#         # print(guru[j]['Slot_waktu'][k])

alpha = 0.1

for angkatan in mutan:
    for kelas in mutan[angkatan]:
        for hari in mutan[angkatan][kelas]:
            active_func = round(random.uniform(0.0, 1.0), 2)
            alokasi_waktu = 0
            if active_func <= alpha:
                print(angkatan)
                print(kelas)
                print(hari)
                print(active_func)
                mapel_temp = {}
                for jam in test['Waktu'][hari]:
                    if (alokasi_waktu == 0):
                        temp_id = {}

                        temp_mapel = randomizer(test['List_Mapel'])
                        temp_guru = randomizer(test['Guru'])
                        alokasi_waktu = int(temp_mapel['Alokasi_Jam'])

                        temp_id['Mapel'] = temp_mapel['Mapel']
                        temp_id['ID'] = temp_mapel['ID']
                        temp_id['Guru'] = temp_guru
                        mapel_temp[temp_mapel['ID']] = temp_id
                        mapel_temp[temp_mapel['ID']]['Slot_waktu'] = []
                    
                    
                    mapel_temp[temp_mapel['ID']]['Slot_waktu'].append(jam)
                    alokasi_waktu = alokasi_waktu - 1
                    
                mutan[angkatan][kelas][hari] = mapel_temp

write_data(mutan, 'output.json')