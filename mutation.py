import random


def neighbour(chromosome):
    """
    Returns a mutated chromosome. The mutation is done by searching for all classes that violate some hard constraint
    (with any resource) and randomly choosing one of them. Then, transfer that class in an unoccupied time frame, in
    one of the allowed classrooms for that class. If there exists no such combination of time frame and classroom,
    transfer the class into a random time frame in one of the allowed classrooms.
    :param chromosome: Current timetable
    :return: Mutated timetable
    """
    candidates = []
    # Search for all classes violating hard constraints
    for k in range(len(chromosome[0])):
        for j in range(len(chromosome[2][chromosome[0][k]['Assigned_classroom']])):
            if chromosome[2][chromosome[0][k]['Assigned_classroom']][j] >= 2:
                candidates.append(k)
        for j in range(len(chromosome[1][chromosome[0][k]['Professor']])):
            if chromosome[1][chromosome[0][k]['Professor']][j] >= 2:
                candidates.append(k)
        for group in chromosome[0][k]['Group']:
            for j in range(len(chromosome[3][group])):
                if chromosome[3][group][j] >= 2:
                    candidates.append(k)

    if not candidates:
        i = random.randrange(len(chromosome[0]))
    else:
        i = random.choice(candidates)

    # Remove that class from its time frame and classroom
    for j in range(chromosome[0][i]['Assigned_time'], chromosome[0][i]['Assigned_time'] + int(chromosome[0][i]['Length'])):
        chromosome[1][chromosome[0][i]['Professor']][j] -= 1
        chromosome[2][chromosome[0][i]['Assigned_classroom']][j] -= 1
        for group in chromosome[0][i]['Group']:
            chromosome[3][group][j] -= 1
    chromosome[4][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].remove(
        (chromosome[0][i]['Assigned_time'], chromosome[0][i]['Group']))

    # Find a free time and place
    length = int(chromosome[0][i]['Length'])
    found = False
    pairs = []
    for classroom in chromosome[2]:
        c = 0
        # If class can't be held in this classroom
        if classroom not in chromosome[0][i]['Classroom']:
            continue
        for k in range(len(chromosome[2][classroom])):
            if chromosome[2][classroom][k] == 0 and k % 8 + length <= 8:
                c += 1
                # If we found x consecutive hours where x is length of our class
                if c == length:
                    time = k + 1 - c
                    # Friday 8pm is reserved for free hour
                    if k != 37:
                        pairs.append((time, classroom))
                        found = True
                    c = 0
            else:
                c = 0
    # Find a random time
    if not found:
        classroom = random.choice(chromosome[0][i]['Classroom'])
        day = random.randrange(0, 5)
        # Friday 8pm is reserved for free hour
        if day == 4:
            period = random.randrange(
                0, 7 - int(chromosome[0][i]['Length']))
        else:
            period = random.randrange(
                0, 9 - int(chromosome[0][i]['Length']))
        time = 8 * day + period

        chromosome[0][i]['Assigned_classroom'] = classroom
        chromosome[0][i]['Assigned_time'] = time

    # Set that class to a new time and place
    if found:
        novo = random.choice(pairs)
        chromosome[0][i]['Assigned_classroom'] = novo[1]
        chromosome[0][i]['Assigned_time'] = novo[0]

    for j in range(chromosome[0][i]['Assigned_time'], chromosome[0][i]['Assigned_time'] + int(chromosome[0][i]['Length'])):
        chromosome[1][chromosome[0][i]['Professor']][j] += 1
        chromosome[2][chromosome[0][i]['Assigned_classroom']][j] += 1
        for group in chromosome[0][i]['Group']:
            chromosome[3][group][j] += 1
    chromosome[4][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].append(
        (chromosome[0][i]['Assigned_time'], chromosome[0][i]['Group']))

    return chromosome


def neighbour2(chromosome):
    """
    Returns a mutated chromosome. pick two classes at random and swap their places and assigned times. Besides this,
    check if the two classes are compatible for swapping (if they use the same type of classrooms).
    :param chromosome: Current timetable
    :return: Mutated timetable
    """
    first_index = random.randrange(0, len(chromosome[0]))

    first = chromosome[0][first_index]
    satisfied = False

    c = 0
    # Find two candidates that can be swapped (constraints are type of classroom and length, because of overlapping days)
    while not satisfied:
        # Return the same chromosome after 100 failed attempts
        if c == 100:
            return chromosome
        second_index = random.randrange(0, len(chromosome[0]))

        second = chromosome[0][second_index]
        if first['Assigned_classroom'] in second['Classroom'] and second['Assigned_classroom'] in first['Classroom']\
                and first['Assigned_time'] % 8 + int(second['Length']) <= 8 \
                and second['Assigned_time'] % 8 + int(first['Length']) <= 8:
            if first['Assigned_time'] + int(second['Length']) != 40 and second['Assigned_time'] + int(first['Length']) != 40\
                    and first != second:
                satisfied = True
        c += 1

    # Remove the two classes from their time frames and classrooms
    for j in range(first['Assigned_time'], first['Assigned_time'] + int(first['Length'])):
        chromosome[1][first['Professor']][j] -= 1
        chromosome[2][first['Assigned_classroom']][j] -= 1
        for group in first['Group']:
            chromosome[3][group][j] -= 1
    chromosome[4][first['Subject']][first['Type']].remove(
        (first['Assigned_time'], first['Group']))

    for j in range(second['Assigned_time'], second['Assigned_time'] + int(second['Length'])):
        chromosome[1][second['Professor']][j] -= 1
        chromosome[2][second['Assigned_classroom']][j] -= 1
        for group in second['Group']:
            chromosome[3][group][j] -= 1
    chromosome[4][second['Subject']][second['Type']].remove(
        (second['Assigned_time'], second['Group']))

    # Swap the times and classrooms
    tmp = first['Assigned_time']
    first['Assigned_time'] = second['Assigned_time']
    second['Assigned_time'] = tmp

    tmp_classroom = first['Assigned_classroom']
    first['Assigned_classroom'] = second['Assigned_classroom']
    second['Assigned_classroom'] = tmp_classroom

    # Set the classes to new timse and places
    for j in range(first['Assigned_time'], first['Assigned_time'] + int(first['Length'])):
        chromosome[1][first['Professor']][j] += 1
        chromosome[2][first['Assigned_classroom']][j] += 1
        for group in first['Group']:
            chromosome[3][group][j] += 1
    chromosome[4][first['Subject']][first['Type']].append(
        (first['Assigned_time'], first['Group']))

    for j in range(second['Assigned_time'], second['Assigned_time'] + int(second['Length'])):
        chromosome[1][second['Professor']][j] += 1
        chromosome[2][second['Assigned_classroom']][j] += 1
        for group in second['Group']:
            chromosome[3][group][j] += 1
    chromosome[4][second['Subject']][second['Type']].append(
        (second['Assigned_time'], second['Group']))

    return chromosome
