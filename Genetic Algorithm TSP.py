import random as rand
import pandas as pd


# Input Data
def data_input(dataset):
    df = pd.read_csv(dataset)
    data_set = dict()
    node = []
    counter_x = 0
    for loop in range(len(df['Node'])):
        node.append(str(counter_x + 1))
        counter_x += 1
    for x in range(0, len(node)):
        for y in range(0, len(node)):
            for ptf in range(len(df['Node'])):
                data_set[tuple([x + 1, y + 1])] = df[node[x]][y]
    data_set = {k: v for k, v in data_set.items() if v}
    return data_set, len(node)


# Inisialisasi
def inisialisasi(popsize, node):
    chromosome = list()
    while len(chromosome) != popsize:
        tmp = list()
        while len(tmp) != node:
            indeks = rand.randint(1, node)
            if indeks not in tmp:
                tmp.append(indeks)
            else:
                continue
        if tmp not in chromosome:
            chromosome.append(tmp)
    return chromosome


# Crossover
def xover(chromosome, popsize, xover_rate, point_cut):
    offspring = []
    offspring_amount = round(popsize * xover_rate)
    y = chromosome.copy()
    while len(offspring) != offspring_amount:
        induk_list = []
        while len(induk_list) != 2:
            indeks = rand.randint(0, popsize - 1)
            induk_list.append(y[indeks])
        xover_res = []
        for x in range(0, point_cut):
            xover_res.append(induk_list[0][x])
        for z in induk_list[1]:
            if z not in xover_res:
                xover_res.append(z)
        offspring.append(xover_res)
    return offspring


# Mutasi
def mutation(chromosome, popsize, mutate_rate, exp1, exp2):
    offspring = []
    offspring_amount = round(popsize * mutate_rate)
    cromosom = [x for x in chromosome]
    while len(offspring) != offspring_amount:
        indeks = rand.randint(0, popsize - 1)
        tmp_list = list()
        res = list()
        for x in cromosom[indeks]:
            tmp_list.append(x)
        for z in range(0, len(tmp_list)):
            if z == exp1 - 1:
                res.append(tmp_list[exp2 - 1])
            elif z == exp2 - 1:
                res.append(tmp_list[exp1 - 1])
            else:
                res.append(tmp_list[z])
        offspring.append(res)
    return offspring


# Evaluasi
def evaluasi(chromosome, krossover, mutation_result):
    dict_pop = dict()
    counter = 1
    for x_chromo in chromosome:
        dict_pop[counter] = x_chromo
        counter += 1
    for y_xover in krossover:
        dict_pop[counter] = y_xover
        counter += 1
    for z_mutation in mutation_result:
        dict_pop[counter] = z_mutation
        counter += 1
    return dict_pop


# Seleksi
def seleksi(new_pop, dist, pop_number, node):
    bobot = dict()
    fitness = dict()
    new_population = list()
    bobot_optimal = list()
    fitness_optimal = list()
    for key, value in new_pop.items():
        tmp = 0
        for kunci, nilai in dist.items():
            for loop in range(0, node):
                if loop + 1 != node:
                    if tuple([value[loop], value[loop + 1]]) == kunci:
                        tmp += nilai
                if loop + 1 == node:
                    if tuple([value[loop], value[0]]) == kunci:
                        tmp += nilai
        bobot[key] = tmp
        fitness[key] = 1000 / tmp
    while len(new_population) != pop_number:
        indeks = max(fitness.values())
        fitness_optimal.append(indeks)
        indeks = max(fitness, key=fitness.get)
        new_population.append(new_pop[indeks])
        bobot_optimal.append(bobot[indeks])
        fitness.pop(indeks)
    return new_population, bobot_optimal, fitness_optimal


# Main Method
def main():
    print("Input:")
    print("\n-Initialization Input: ")
    generation = int(input("> Generation (Integer): "))
    pop_size = int(input("> Population size (Integer): "))
    jarak, node = data_input("Data_Node_Jarak.csv")
    kromosom = inisialisasi(pop_size, node)
    print("\n-Reproduction Input:")
    print("\n--Crossover Phase (Cut point pick integer from 0 to {})--".format(node))
    cr = float(input("> Crossover rate: "))
    cut_point = int(input("> Cut point crossover: "))
    crossover = xover(kromosom, pop_size, cr, cut_point)
    print("\n--Mutation Phase (Exchange point pick integer from 1 to {})--".format(node))
    mr = float(input("> Mutation rate: "))
    xp1 = int(input("> Exchange Point 1: "))
    xp2 = int(input("> Exchange Point 2: "))
    while (xp1 and xp2) == 0 or xp1 == xp2:
        if xp1 == xp2:
            print("\n<<Exchange point can't be the same>>")
            xp1 = int(input("> Exchange point 1: "))
            xp2 = int(input("> Exchange point 2: "))
        if (xp1 and xp2) == 0:
            print("\n<<Exchange point can't be 0>>")
            xp1 = int(input("> Exchange point 1: "))
            xp2 = int(input("> Exchange point 2: "))
    res_mutation = mutation(kromosom, pop_size, mr, xp1, xp2)
    evaluated = evaluasi(kromosom, crossover, res_mutation)
    new_kromosom, bobot, fitness = seleksi(evaluated, jarak, pop_size, node)
    counter = 1
    while counter != generation and kromosom != new_kromosom:
        kromosom = new_kromosom
        crossover = xover(kromosom, pop_size, cr, cut_point)
        res_mutation = mutation(kromosom, pop_size, mr, xp1, xp2)
        evaluated = evaluasi(kromosom, crossover, res_mutation)
        new_kromosom, bobot, fitness = seleksi(evaluated, jarak, pop_size, node)
        counter += 1
    print("\nEnd Result:")
    hasil_akhir = pd.DataFrame({'Chromosome': new_kromosom, 'Distance (In KM)': bobot, 'Fitness (1000/Jarak)': fitness})
    print(hasil_akhir.to_string())


main()
