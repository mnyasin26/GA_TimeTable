import json
import random
# python3 install prettytable
from prettytable import PrettyTable

# fungsi untuk mengambil data buat gen nantinya, dalam kasus ini gen-nya adalah satu KBM
def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    # for university_class in data['Casovi']:
    #     classroom = university_class['Classroom']
    #     university_class['Classroom'] = data['Classroom'][classroom]

    data = data['Casovi']  # sebenernya kita cuma butuh ini aaaaaa

    return data

# fungsi untuk membuat satu jadwal penuh / satu calon solusi
def generate_chromosome(data):

    # kemungkinan variabel2 yg bawah ini buat nandain jadwal masing2
    professors = {} # jadwal guru ngajar
    # classrooms = {} # jadwal ruangan kepake
    groups = {} # jadwal kelas masuk
    subjects = {} # jadwal mapelnya tu kapan dan kelas yg masuknya apa

    new_data = [] # kromosom -> satu jadwal

    # ini kayaknya buat alokasi awal dari variabel2 penentu cost tadi
    for single_class in data:

        # alokasi penanda jadwal guru, 0 berarti kosong alias gak ngajar
        # nah si penanda ini harus 0 atau 1, gaboleh lebih
        # karena dalam 1 jam pelajaran, si guru cuma boleh ngajar di 1 kelas
        professors[single_class['Professor']] = [0] * 40 # -> dibikin semuanya isi 0 dulu, kyk biasa ges, inisialisasi
        # nb : sebenernya 40 bisa diganti 38 kyknya ges, tp kan biar jaga2 kita jadiin 40 aja karena 5 hari kali 8 jam pelajaran tiap harinya
        # contoh
        # professors['Najma'][0] = 1 -> ini maksudnya di jam pelajaran ke-0 (senin jam 7) itu Najma ada jadwal

        # kita ga make ini jadi abaikan :D tp intinya mah sama kyk di atas
        # for classroom in single_class['Classroom']:
        #     classrooms[classroom] = [0] * 40
        for group in single_class['Group']:
            groups[group] = [0] * 40
        subjects[single_class['Subject']] = {'P': [], 'V': [], 'L': []}

    # yak jadi ini perulangan intinya sih, buat nentuin posisi 1 gen
    # perulangan mencari alokasi waktu untuk tiap 1 gen/KBM klo di kasus kita
    # klo aslinya sih buat nentuin ruangan sama waktu
    for single_class in data:

        # si new_single_class ini itu nanti jadi 1 gen baru
        new_single_class = single_class.copy() 

        # random cari kelas
        # klo di kasus asli kodingan ini, berarti ini tu nyari ruangan yg kosong
        # kyknya di kasus kita mah ga butuh ini, atau bisa sih, jadi random kelasnya
        # ++++ classroom = random.choice(single_class['Classroom'])

        #####! random cari alokasi waktu (jam pelajaran) !######

        # pertama cari hari dulu
        if int(single_class['Length']) == 3:

            day = random.randrange(0, 4)
        else:
            day = random.randrange(0, 5)
            
        # baru cari periode waktunya
        if day == 4: # kalo jumat
            free = [0, 2, 4]
            # period = random.randrange(0, 7 - int(single_class['Length']))
        else:
            # nb : jadi ges, menurut aku kita bisa otak atik di sini klo misal mau ngatasin masalah mapelnya kepotong istirahat
            if int(single_class['Length']) == 3:
                free = [0, 3]
            else:
                free = [6]
            # period = random.randrange(0, 9 - int(single_class['Length']))
            # kan sehari ada 8 jam pelajaran
            # trus kita perlu tau kelas yg ini tuh berapa lama / berapa jam pelajaran, misal 3
            # nah kita bakalan ngerandom antara 0 sampe (9 - 3)
            # jadinya antara 0 sampe 6
            # ya gitu lah intinya, biar 3 periode/jam pelajaran kepake gitu maksudnya

        period = random.choice(free)
        #####! selese !######

        # nah ini mulai ngisi gen-nya ges, tapi kan yg kasus kita mah sebenernya cuma jam pelajarannya doang

        # ++++ new_single_class['Assigned_classroom'] = classroom # ya ini berarti kan kelas yg dirandom tadi tuh, ruangan klo di aslinya
        
        time = 8 * day + period # buat ngitung jam pelajaran-nya, paham lah ya ges
        new_single_class['Assigned_time'] = time # masukin deh

        # nah ini buat nandain yang tadi tuh
        for i in range(time, time + int(single_class['Length'])): # kita tandain di index yang sesuai sama jam pelajaran tadi

            # tandain klo gurunya ngajar di jam itu
            professors[new_single_class['Professor']][i] += 1
            # tandain klo kelasnya (ruangan) kepake
            # ++++ classrooms[classroom][i] += 1
            # tandain klo kelas (yg kyk C1 gitu) lagi ada jam pelajaran
            for group in new_single_class['Group']:
                groups[group][i] += 1

        # ini juga buat nandain jadwal matkulnya
        subjects[new_single_class['Subject']][new_single_class['Type']].append(
            (time, new_single_class['Group']))

        # masukin gen yg dibuat ke kromosom
        # masukin 1 KBM ke jadwal
        new_data.append(new_single_class)

    # mereturn kromosomnyaa
    return (new_data, professors, groups, subjects) # tadinya ada classroom di setelah professors
    # karena ngembaliin banyak data, si kromosom ini nanti bakalan jadi array (atau list ya, atau apalah gatau)
    # chromosome[0] -> jadwal
    # chromosome[1] -> jadwal guru (professors)
    # chromosome[2] -> jadwal kelas (ruangan)
    # chromosome[3] -> jadwal kelas (yg kyk C1)
    # chromosome[4] -> jadwal mapel/matkul

def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)

def sortByTime(e):
    return e['Assigned_time']

def print_table(data):
    len_data = len(data)
    print("Total Data", len_data)
    
    # Manual Printing
    # print("Column Subject:", data[0]['Subject']);
    # print("Column Type:", data[0]['Type']);
    # print("Column Professor:", data[0]['Professor']);
    # print("Column Group:", data[0]['Group'][0]);
    # print("Column Classroom:", data[0]['Classroom'][0]);
    # print("Column Length:", data[0]['Length']);
    # print("Column Assigned_classroom:", data[0]['Assigned_classroom']);
    # print("Column Assigned_time:", data[0]['Assigned_time']);

    # Using PrettyTable
    print("+-----------------------------------------------------------------------------------------------------------+")
    print("|                                       JADWAL PELAJARAN KELAS VII A                                        |")
    tab = PrettyTable()    
    tab.field_names = ["Kelas", "Penempatan Waktu", "Mata Pelajaran", "Guru", "Jumlah Jam"]
    tab.align["Kelas"]              = "c"
    tab.align["Penempatan Waktu"]   = "c"
    tab.align["Mata Pelajaran"]     = "l"
    tab.align["Guru"]               = "l"
    tab.align["Jumlah Jam"]         = "c"
    data.sort(key=sortByTime)
    
    # Looping
    for i in range(len_data):
        if (data[i]['Assigned_classroom'] == "VII A"):
            value = [[data[i]['Classroom'][0], data[i]['Assigned_time'], data[i]['Subject'], data[i]['Professor'], data[i]['Length']]]
            tab.add_rows(value[0:])
    
    # Print Table
    print(tab)
