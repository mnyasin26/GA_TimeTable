# jadi ada 2 fungsi buat ngitung cost, tapi nantinya mah hasil 2 fungsi ini ditambah

# fungsi untuk menghitung cost dari : adanya tabrakan tiap gen dan soft constraint yg tadi ada di doc, pokoknya tentang urutan apalah, kita ga make
def cost(chromosome):
    """
    Cost function for all hard constraints and soft constraint regarding preferred order. All parameters are empirical.
    :param chromosome: Timetable for which we are calculating the cost function.
    :return: Value of cost
    """
    prof_cost = 0
    classrooms_cost = 0
    groups_cost = 0
    subjects_cost = 0

    # Traverse all classes for hard constraints
    # mengecek hard constraint dari kromosom dengan memeriksa tiap gen
    for single_class in chromosome[0]:

        time = single_class['Assigned_time'] # jam pelajaran
        # contohnya jam pelajaran ke-0 ya ges, senin pagi
        class_len = single_class['Length']
        # contohnya 3 jam pelajaran

        # Check hard constraint violation in classes time frame
        # mengecek adanya tabrakan atau tidak
        for i in range(time, time + int(class_len)):
            # klo dari contoh tadi, berarti perulangan ini bakalan ngecek 3 kali, yaitu di jam pelajaran 0, 1, 2

            # mengecek jadwal guru
            if chromosome[1][single_class['Professor']][i] > 1:
                # klo lebih dari 1 itu berarti dalam 1 waktu si guru ngajar lebih dari 1 kelas, kan nabrak tuh
                # berarti tambah costnya
                prof_cost += 1

            # sama tapi buat ruangan
            if chromosome[2][single_class['Assigned_classroom']][i] > 1:
                classrooms_cost += 1

            # sama tapi buat kelas (misal C1)
            for group in single_class['Group']:
                if chromosome[3][group][i] > 1:
                    groups_cost += 1

    # Traverse all classes for soft constraint regarding preferred order

    # mengecek soft constraint dari kromosom dengan memeriksa tiap gen
    # tapi kita kyknya ga make
    for single_class in chromosome[4]:
        for lab in chromosome[4][single_class]['L']:
            for practice in chromosome[4][single_class]['V']:
                for grupa in lab[1]:
                    # If lab is before practical
                    if grupa in practice[1] and lab[0] < practice[0]:
                        subjects_cost += 0.0025
            for lecture in chromosome[4][single_class]['P']:
                for grupa in lab[1]:
                    # If lab is before lecture
                    if grupa in lecture[1] and lab[0] < lecture[0]:
                        subjects_cost += 0.0025
        for practice in chromosome[4][single_class]['V']:
            for lecture in chromosome[4][single_class]['P']:
                for grupa in practice[1]:
                    # If practical is before lecture
                    if grupa in lecture[1] and practice[0] < lecture[0]:
                        subjects_cost += 0.0025

    return prof_cost + classrooms_cost + groups_cost + round(subjects_cost, 4)

# fungsi untuk menghitung cost dari : idleness kelas (C1) dan guru
def cost2(chromosome):
    """
    Cost function for all hard constraints and all soft constraints. All parameters are empirical.
    :param chromosome: Timetable for which we are calculating the cost function.
    :return: Value of cost
    """
    groups_empty = 0
    prof_empty = 0
    load_groups = 0
    load_prof = 0

    # Call function for calculating cost for hard constratins and soft constraint regarding preferred order
    original_cost = cost(chromosome)

    # Calculating idleness and load for groups
    for group in chromosome[3]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(8):
                time = day * 8 + hour
                if chromosome[3][group][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        groups_empty += (time - last_seen - 1) / 500
                    last_seen = time
            if current_load > 6:
                load_groups += 0.005

    # Calculating idleness and load for professors
    for prof in chromosome[1]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(8):
                time = day * 8 + hour
                if chromosome[1][prof][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        prof_empty += (time - last_seen - 1) / 2000
                    last_seen = time
            if current_load > 6:
                load_prof += 0.0025

    return original_cost + round(groups_empty, 3) + round(prof_empty, 5) + round(load_prof, 3) + round(load_groups, 4)
