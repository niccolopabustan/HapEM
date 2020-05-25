# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:21:44 2019

@author: Niccolo Pabustan
@co-author: Gian Pabustan
"""

def create_genotype_population(filename):
    G = []
    temp_G = []
    row_count = 0

    file = open(filename, "r")
    for line in file: 
        h = line.split(" ")     
        temp_G.append(h)
        row_count += 1   
    
    for g in range(len(temp_G)):
        for s in range(len(temp_G[g])-1, len(temp_G[g])):
            if temp_G[g][s] == '0\n':
                temp_G[g][s] = '0'
            elif temp_G[g][s] == '1\n': 
                temp_G[g][s] = '1'
            elif temp_G[g][s] == '2\n':
                temp_G[g][s] = '2'
    
    for col in range(len(temp_G[0])):
        temp_g = []
        
        for row in range(len(temp_G)):
            temp_g.append(temp_G[row][col])
        G.append(temp_g)
    return G

def possible_haplotype_pairs(given_g):    
    g = []
    num1s = 0
    num_phases = 0
    p = []
    h1 = []
    h2 = []
    flip_count = 0
    x = 1
    
    for i in given_g: 
        if i == '1':
            num1s += 1
    if num1s != 0:
        num_phases = 2**(num1s-1)
        for current_hap in range(num_phases):
            p = []
            h1 = []
            h2 = []
            
            for snp in given_g: 
                if snp == '2':
                    h1.append(1)
                    h2.append(1)
                elif snp == '0':
                    h1.append(0)
                    h2.append(0)
                elif snp == '1':
                    h1.append('x')
                    h2.append('x')
            p.append(h1)
            p.append(h2)
            g.append(p)    
    
        for i in range(num1s):
            flip_count = int(num_phases/(2**i))
            x = 1
            for j in range(num_phases):
                for s in range(len(g[j][0])):
                    if g[j][0][s] == 'x': 
                        g[j][0][s] = x
                        g[j][1][s] = 1-x
                        flip_count -= 1         
                        if flip_count == 0:
                            flip_count = num_phases/(2**i)
                            if x==0: x = 1
                            else: x = 0            
                        break
        return g    
    
    
    else: 
        g = []
        p = []
        h1 = []
        h2 = []
        
        for snp in given_g: 
            if snp == '2':
                h1.append(1)
                h2.append(1)
            elif snp == '0':
                h1.append(0)
                h2.append(0)
        p = [h1, h2]
        g.append(p)
        
        
        return g
    



#number of windows function ///////////////////////////////////////////
def get_number_of_windows(number_of_snps, window_size):
    number_of_full_windows = int(number_of_snps / window_size)    
    if number_of_snps % window_size != 0:
        return number_of_full_windows + 1
    else:
        return number_of_full_windows
    

    
    
# Create genotype window function /////////////////////////////////////////////////////////////////////////////
def create_genotype_window(given_G, window_iteration, window_size, number_of_snps):
    
    G_window = []
    g_window = []
    start_index = window_iteration * window_size
    remainder = num_of_snps % window_size
    
    #check if last window
    if ((window_iteration == (get_number_of_windows(number_of_snps, window_size)-1)) and (remainder != 0)):
        window_size = remainder
    
    #continuing code if last window or not
    for g in range(len(given_G)):
        g_window = []
        for s in range(window_size):
            g_window.append(given_G[g][start_index + s])       
        G_window.append(g_window)
    return G_window

# Creating unique haplotype list 
def create_unique_haplotype_list(given_Ggphs_window):
    unique_hap_list = []
    all_hap_list = []


    for g in given_Ggphs_window: 
        for phase in g: 
            for haplotype in phase: 
                g_string = tuple(haplotype)
                all_hap_list.append(g_string)
    
#    for g in given_Ggphs_window:
#        for phase in g:
#            for haplotype in phase:
#                g_string = ""
#                for snp in haplotype: 
#                    g_string = g_string + str(snp)
#                all_hap_list.append(g_string)

    for hap in all_hap_list: 
        if hap not in unique_hap_list: 
            unique_hap_list.append(hap)

    return unique_hap_list

# placing haploid results to final solution ////////////////////////////////////////////////
def update_final_solution(final_sol, hap_pair_solution):
    new_sol = []
    
    #copy what is on final_sol onto new_sol
    temp_g = []
    h1 = []
    h2 = []
#    print("\tlen(final_sol) =", len(final_sol))

    for g in range(len(hap_pair_solution)):        
        temp_g = []
        h1 = []
        h2 = []
        for s in range(len(final_sol[0][0])):
            h1.append(final_sol[g][0][s])
            h2.append(final_sol[g][1][s])
            
        for s in range(len(hap_pair_solution[0][0])):
            h1.append(hap_pair_solution[g][0][s])
            h2.append(hap_pair_solution[g][1][s])
            
        temp_g.append(h1)
        temp_g.append(h2)
        new_sol.append(temp_g)
                
    return new_sol
def update_final_solution5(final_sol, hap_pair_solution): 
    for s in range(len(hap_pair_solution[0][0])): 
        for g in range(len(hap_pair_solution)): 

            final_sol[g].append(hap_pair_solution[g][0][s])
            final_sol[g].append(hap_pair_solution[g][1][s])
    
    return final_sol


def update_final_solution4(final_sol, hap_pair_solution):
    new_sol = []    
    temp_g = []
    h1 = []
    h2 = []
#    print("\tlen(final_sol) =", len(final_sol))

    for g in range(len(hap_pair_solution)):        
        temp_g = []
        h1 = final_sol[g][0]
        h2 = final_sol[g][1]
#        for s in range(len(final_sol[0][0])):
#            h1.append(final_sol[g][0][s])
#            h2.append(final_sol[g][1][s])
            
        for s in range(len(hap_pair_solution[0][0])):
            h1.append(hap_pair_solution[g][0][s])
            h2.append(hap_pair_solution[g][1][s])
            
        temp_g.append(h1)
        temp_g.append(h2)
        new_sol.append(temp_g)
                
    return new_sol
        
#final_solution data prep ////////////////////////////////
def allocate_data_for_final_solution2(final_solution, number_of_genotypes):
    
    
    for g in range(number_of_genotypes):
        single_genotype_space = []
        
        final_solution.append(single_genotype_space)

    return final_solution


#EM ITERATE FUNCTIONS///////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
def EM_iterate2(given_Ggphs):
    hap_pair_solutions = []
    phase_probs = []
    haplotype_probs = []
    em_iteration = 4
    
    phase_probs = initiate_phase_probs(given_Ggphs)
    haplotype_probs = initiate_haplotype_probs(given_Ggphs)


#    print("COMMENCING EM OPERATION:")
    for em_it in range(em_iteration):
#        print("\nEM iteration:", em_it)
        haplotype_probs = create_new_hap_probs(given_Ggphs, phase_probs)
#        print("hap probs:\n",haplotype_probs)
        phase_probs = create_new_phase_probs(given_Ggphs, haplotype_probs)
#        print("phase probs:\n",phase_probs)

#    phase_probs = [[0.838, 0.054, 0.054, 0.054],[0.4,0.6],[1.0]]
    #appending most probable haplotypes onto hap_pair_solutions
    for g in range(len(phase_probs)):
        temp_g = []
        h1 = []
        h2 = []
        greatest_value = 0       
        phase_winner = 0
        
        #getting phase location of highest probable phase
        for p in range(len(phase_probs[g])):
#            current_prob = phase_probs[g][p]
            if phase_probs[g][p] > greatest_value:
                greatest_value = phase_probs[g][p]
                phase_winner = p
#        print("\tphase location:", phase_winner)      
        #appending phase onto hap_pair_solutions
        h1 = given_Ggphs[g][phase_winner][0]
        h2 = given_Ggphs[g][phase_winner][1]
        temp_g.append(h1)
        temp_g.append(h2)       
        hap_pair_solutions.append(temp_g)
            
        
    return hap_pair_solutions

def initiate_phase_probs(given_Ggphs):
    phase_probs = []
    temp_g = []
    phase_prob = 0   
    
    for g in range(len(given_Ggphs)):
        temp_g = []
        
        for p in range(len(given_Ggphs[g])):
            phase_prob = 1/len(given_Ggphs[g])        
#            print("phase prob for genotype", g, "phase", p, "is", phase_prob)
            temp_g.append(phase_prob)            
        phase_probs.append(temp_g)
#    print(phase_probs)
    return phase_probs

def initiate_haplotype_probs(given_Ggphs):
    haplotype_probs= []
    num_of_unique_haps = 0
    hap_prob = 0
    temp_g = []
    temp_p = []
    h1 = 0
    h2 = 0
    
    num_of_unique_haps = get_number_of_unique_haps(given_Ggphs)
    hap_prob = 1/num_of_unique_haps
    
#    print("\tnumber of unique haplotypes:", num_of_unique_haps)
#    print("\tProbability:", hap_prob)
    
    for g in range(len(given_Ggphs)):
        temp_g = []
        temp_p = []
        h1 = hap_prob
        h2 = hap_prob
        for p in range(len(given_Ggphs[g])):
            temp_p = [h1, h2]
            temp_g.append(temp_p)
        haplotype_probs.append(temp_g)   
#    print(haplotype_probs)
    return haplotype_probs

def get_number_of_unique_haps(given_Ggphs):
    haps_list = []
    unique_list = []
    for g in given_Ggphs:
        for phase in g:
            for haplotype in phase:
                g_string = ""
                for snp in haplotype: 
                    g_string = g_string + str(snp)
                haps_list.append(g_string)
    for h in haps_list:
        if h not in unique_list: 
            unique_list.append(h)
    return len(unique_list)

def create_new_hap_probs(given_Ggphs, phase_probs):
    haplotype_probs = []
    numerator = 0
    denomenator = 2 * len(given_Ggphs)
    temp_g = []
    temp_p = []
    hap_prob = 0
    
    for g in range(len(given_Ggphs)):
        temp_g = []
            
        for p in range(len(given_Ggphs[g])):
            temp_p = []
            
            #print("\t", phase_probs[g][p])
            for h in range(len(given_Ggphs[g][p])):
                #print("\t", given_Ggphs[g][p][h])
                
                numerator = get_phase_prob_summation(given_Ggphs, phase_probs, given_Ggphs[g][p][h])
                
                hap_prob = numerator / denomenator
                
                
                temp_p.append(hap_prob)
            temp_g.append(temp_p)
        haplotype_probs.append(temp_g)
        
    
    
    
    return haplotype_probs

def get_phase_prob_summation(given_Ggphs, phase_probs, current_haplotype):
    phase_prob_sum = 0
    
    for g in range(len(given_Ggphs)):
        for p in range(len(given_Ggphs[g])):
            for h in range(len(given_Ggphs[g][p])):
                if given_Ggphs[g][p][h] == current_haplotype:
                    #print("found a match:", given_Ggphs[g][p][h], current_haplotype)
                    phase_prob_sum += phase_probs[g][p]
                    
    #print("phase sum =", phase_prob_sum)
    return phase_prob_sum

def create_new_phase_probs(given_Ggphs, haplotype_probs):
    phase_probs = []
    numerator = 0 
    denomenator = 1
    temp_g = []
    phase_prob = 0
    
    for g in range(len(given_Ggphs)):
#        print("probs at genotype:", g)
        temp_g = []
        denomenator = get_haplotype_prob_summation(given_Ggphs, haplotype_probs, g)
        for p in range(len(given_Ggphs[g])):
            
#            print("\t\thaplotype 1 prob =", haplotype_probs[g][p][0])
#            print("\t\thaplotype 2 prob =", haplotype_probs[g][p][1])
            
            numerator = haplotype_probs[g][p][0] * haplotype_probs[g][p][1]
            
            phase_prob = numerator / denomenator 
            temp_g.append(phase_prob)
            
        phase_probs.append(temp_g)
            
    
    
    
    
    return phase_probs

def get_haplotype_prob_summation(given_Ggphs, haplotype_probs, genotype_index):
    hap_prob_sum = 0
    temp_hap_product = 0
    
    for p in range(len(given_Ggphs[genotype_index])):
#        print("\t\tgenotype", genotype_index, "phase", p, "haplotype 0 prob =", haplotype_probs[genotype_index][p][0])
#        print("\t\tgenotype", genotype_index, "phase", p, "haplotype 1 prob =", haplotype_probs[genotype_index][p][1])
        
        temp_hap_product = haplotype_probs[genotype_index][p][0] * haplotype_probs[genotype_index][p][1]
        hap_prob_sum += temp_hap_product
                
    if hap_prob_sum == 0:
        return 1
    else: 
        return hap_prob_sum


#MAIN /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# #/////TEST FILE
# G = []
# final_sol = []
# num_of_snps = 0
# num_of_genotypes = 0
# num_of_windows = 0
# w_size = 5
# path = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/"
# example_path = "easy_test.txt"
# filename = path + example_path
# result_filename = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/easy_data_sol.txt"

# G = create_genotype_population(filename)
# num_of_snps = len(G[0])
# num_of_genotypes = len(G)
# print("num of snps:", num_of_snps)
# print("num of genotypes:", num_of_genotypes)
# final_sol = allocate_data_for_final_solution2(final_sol, num_of_genotypes)
# num_of_windows = get_number_of_windows(num_of_snps, w_size)

# for win_it in range(num_of_windows):
#     G_window = []
#     Ggphs_window = []
#     hap_pair_solutions = []
    
#     G_window = create_genotype_window(G, win_it, w_size, num_of_snps)

#     for g in G_window: 
#         Ggphs_window.append(possible_haplotype_pairs(g))
        
# #    print(Ggphs_window)


# #testing final_sol updating function / place to put em_iterate////////////////////////////////////

#     hap_pair_solutions = EM_iterate2(Ggphs_window)
# #    print("hap sol length:", len(hap_pair_solutions))
# #    print("hap sol width:", len(hap_pair_solutions[0][0]))

# #    print("hap_pair_solutions:", hap_pair_solutions)
    
# #    print("\tlength of hap_pair_solutions:", len(hap_pair_solutions))
# #    print("\tlength of snp_solutions:", len(hap_pair_solutions[0][0]))
 
    
# #//////////////////////////////////////////////////////////////////////////////////////////////////
#     final_sol = update_final_solution5(final_sol, hap_pair_solutions)
# #    print(final_sol)
#    # print("\tlength of snp in final_sol:", len(final_sol[0][0]))
#     print("UPDATED final solution on window:", win_it+1, "/", num_of_windows, "\n")
    

    
    
# #print(final_sol)
# print("END RESULTS:")
# print("number of genotypes:", len(final_sol))
# #print("number of snps per genotype:", len(final_sol[0][0]))


# f = open(result_filename, "w")
# number_of_rows = 0
# for s in range(num_of_snps):
#     row = ""
#     for g in range(num_of_genotypes):
#         row = row + str(final_sol[g][s*2]) + " " + str(final_sol[g][s*2+1]) + " "
#     row = row[0:-1] + "\n"
#     f.write(row)
#     number_of_rows += 1
# print("This file has", number_of_rows, "rows")
# f.close()

# exit()
import time
import sys
sys.argv[0]
sys.argv[1]
sys.argv[2]
#start = time.time()
#end = time.time()
#print(end - start)
#/////// 1ST FILE
start = time.time()
G = []
final_sol = []
num_of_snps = 0
num_of_genotypes = 0
num_of_windows = 0
w_size = 5
#path = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/"
#example_path = "example_data_1.txt"
file_name = sys.argv[1]
result_filename = sys.argv[2]
#path = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/904413224/"
#print(sys.argv)

print(file_name)
print("here")

print(result_filename)
#"/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/example_data_1_mysolution.txt"

G = create_genotype_population(file_name)
num_of_snps = len(G[0])
num_of_genotypes = len(G)
print("num of snps:", num_of_snps)
print("num of genotypes:", num_of_genotypes)
final_sol = allocate_data_for_final_solution2(final_sol, num_of_genotypes)
num_of_windows = get_number_of_windows(num_of_snps, w_size)

for win_it in range(num_of_windows):
    G_window = []
    Ggphs_window = []
    hap_pair_solutions = []
    
    G_window = create_genotype_window(G, win_it, w_size, num_of_snps)

    for g in G_window: 
        Ggphs_window.append(possible_haplotype_pairs(g))
        
#    print(Ggphs_window)


#testing final_sol updating function / place to put em_iterate////////////////////////////////////

    hap_pair_solutions = EM_iterate2(Ggphs_window)
#    print("hap sol length:", len(hap_pair_solutions))
#    print("hap sol width:", len(hap_pair_solutions[0][0]))

#    print("hap_pair_solutions:", hap_pair_solutions)
    
#    print("\tlength of hap_pair_solutions:", len(hap_pair_solutions))
#    print("\tlength of snp_solutions:", len(hap_pair_solutions[0][0]))

    
#//////////////////////////////////////////////////////////////////////////////////////////////////
    final_sol = update_final_solution5(final_sol, hap_pair_solutions)
#    print(final_sol)
    #print("\tlength of snp in final_sol:", len(final_sol[0][0]))
    print("UPDATED final solution on window:", win_it+1, "/", num_of_windows, "\n")
    

    
    
#print(final_sol)
print("END RESULTS:")
print("number of genotypes:", len(final_sol))
#print("number of snps per genotype:", len(final_sol[0][0]))


f = open(result_filename, "w")
number_of_rows = 0
for s in range(num_of_snps):
    row = ""
    for g in range(num_of_genotypes):
        row = row + str(final_sol[g][s*2]) + " " + str(final_sol[g][s*2+1]) + " "
    row = row[0:-1] + "\n"
    f.write(row)
    number_of_rows += 1
print("This file has", number_of_rows, "rows")
f.close()
end = time.time()
time1=(end-start)
time1 = time1/60
print("run-time: ",time1)
# #//////// 2ND FILE
# start = time.time()
# G = []
# final_sol = []
# num_of_snps = 0
# num_of_genotypes = 0
# num_of_windows = 0
# w_size = 5
# path = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/"
# example_path = "example_data_2.txt"
# filename = path + example_path
# result_filename = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/example_data_2_mysolution.txt"

# G = create_genotype_population(filename)
# num_of_snps = len(G[0])
# num_of_genotypes = len(G)
# print("num of snps:", num_of_snps)
# print("num of genotypes:", num_of_genotypes)
# final_sol = allocate_data_for_final_solution2(final_sol, num_of_genotypes)
# num_of_windows = get_number_of_windows(num_of_snps, w_size)

# for win_it in range(num_of_windows):
#     G_window = []
#     Ggphs_window = []
#     hap_pair_solutions = []
    
#     G_window = create_genotype_window(G, win_it, w_size, num_of_snps)

#     for g in G_window: 
#         Ggphs_window.append(possible_haplotype_pairs(g))
        
# #    print(Ggphs_window)


# #testing final_sol updating function / place to put em_iterate////////////////////////////////////

#     hap_pair_solutions = EM_iterate2(Ggphs_window)
# #    print("hap sol length:", len(hap_pair_solutions))
# #    print("hap sol width:", len(hap_pair_solutions[0][0]))

# #    print("hap_pair_solutions:", hap_pair_solutions)
    
# #    print("\tlength of hap_pair_solutions:", len(hap_pair_solutions))
# #    print("\tlength of snp_solutions:", len(hap_pair_solutions[0][0]))
 
    
# #//////////////////////////////////////////////////////////////////////////////////////////////////
#     final_sol = update_final_solution5(final_sol, hap_pair_solutions)
# #    print(final_sol)
#    # print("\tlength of snp in final_sol:", len(final_sol[0][0]))
#     print("UPDATED final solution on window:", win_it+1, "/", num_of_windows, "\n")
    

    
    
# #print(final_sol)
# print("END RESULTS:")
# print("number of genotypes:", len(final_sol))
# #print("number of snps per genotype:", len(final_sol[0][0]))


# f = open(result_filename, "w")
# number_of_rows = 0
# for s in range(num_of_snps):
#     row = ""
#     for g in range(num_of_genotypes):
#         row = row + str(final_sol[g][s*2]) + " " + str(final_sol[g][s*2+1]) + " "
#     row = row[0:-1] + "\n"
#     f.write(row)
#     number_of_rows += 1
# print("This file has", number_of_rows, "rows")
# f.close()
# end = time.time()
# time2=(end-start)
# time2 = time2/60

# #//////// 3RD FILE
# start = time.time()
# G = []
# final_sol = []
# num_of_snps = 0
# num_of_genotypes = 0
# num_of_windows = 0
# w_size = 5
# path = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/"
# example_path = "example_data_3.txt"
# filename = path + example_path
# result_filename = "/Users/Tristan/Documents/CM124-Winter2019-programmnig-assignment/example_data_3_mysolution.txt"

# G = create_genotype_population(filename)
# num_of_snps = len(G[0])
# num_of_genotypes = len(G)
# print("num of snps:", num_of_snps)
# print("num of genotypes:", num_of_genotypes)
# final_sol = allocate_data_for_final_solution2(final_sol, num_of_genotypes)
# num_of_windows = get_number_of_windows(num_of_snps, w_size)

# for win_it in range(num_of_windows):
#     G_window = []
#     Ggphs_window = []
#     hap_pair_solutions = []
    
#     G_window = create_genotype_window(G, win_it, w_size, num_of_snps)

#     for g in G_window: 
#         Ggphs_window.append(possible_haplotype_pairs(g))
        
# #    print(Ggphs_window)


# #testing final_sol updating function / place to put em_iterate////////////////////////////////////

#     hap_pair_solutions = EM_iterate2(Ggphs_window)
# #    print("hap sol length:", len(hap_pair_solutions))
# #    print("hap sol width:", len(hap_pair_solutions[0][0]))

# #    print("hap_pair_solutions:", hap_pair_solutions)
    
# #    print("\tlength of hap_pair_solutions:", len(hap_pair_solutions))
# #    print("\tlength of snp_solutions:", len(hap_pair_solutions[0][0]))
 
    
# #//////////////////////////////////////////////////////////////////////////////////////////////////
#     final_sol = update_final_solution5(final_sol, hap_pair_solutions)
# #    print(final_sol)
#    # print("\tlength of snp in final_sol:", len(final_sol[0][0]))
#     print("UPDATED final solution on window:", win_it+1, "/", num_of_windows, "\n")
    

    
    
# #print(final_sol)
# print("END RESULTS:")
# print("number of genotypes:", len(final_sol))
# #print("number of snps per genotype:", len(final_sol[0][0]))


# f = open(result_filename, "w")
# number_of_rows = 0
# for s in range(num_of_snps):
#     row = ""
#     for g in range(num_of_genotypes):
#         row = row + str(final_sol[g][s*2]) + " " + str(final_sol[g][s*2+1]) + " "
#     row = row[0:-1] + "\n"
#     f.write(row)
#     number_of_rows += 1
# print("This file has", number_of_rows, "rows")
# f.close()

# end = time.time()
# time3=(end-start)
# time3 = time3/60

# print("time1: ", time1, " minutes")
# print("time2: ", time2, " minutes")
# print("time3: ", time3, " minutes")