import string
import numpy as np
import math


def read_files(number, essay_name):
    essay = open("data\\" + str(essay_name) + ".txt", "r")
    essay.readline().rstrip(" \n")
    essay = essay.readline().rstrip("\n").lower()
    for punction in string.punctuation:
        if punction == '.' or punction == '!' or punction == "?":
            if number == 1:
                essay = essay.replace(punction, " " + punction)
            elif number == 2:
                essay = essay.replace(punction, " token " + str(punction) + " <s>")
            else:
                essay = essay.replace(punction, " token token " + str(punction) + " <s> <s>")
        elif punction == "<" or punction == ">":
            continue
        else:
            essay = essay.replace(punction, " ")

    new = essay.split(" ")
    if number == 2:
        new = ["<s>"] + new
    if number == 3:
        new = ["<s>"] + ["<s>"] + new
    new = [k for k in new if k]
    return new


def unigram_test(test_uni, dict, size_dict):
    total_prob = 0
    for word in test_uni:
        if word in dict:
            total_prob += math.log((dict[word]+1) / (len(dict.keys())+size_dict), 2)
        else:
            total_prob += math.log(1 / (len(dict.keys())+size_dict), 2)
    return np.power(2, -total_prob / (len(test_uni)))


def bigram_test(test_bi, bi_dict, size_dict, uni_dict):
    total_prob = 0

    for i in range(len(test_bi) - 1):
        word = test_bi[i] + " " + test_bi[i+1]
        if word in bi_dict:
            try:
                total_prob += math.log((bi_dict[word] + 1) / (size_dict + uni_dict[test_bi[i]]), 2)
            except:
                total_prob += math.log((bi_dict[word] + 1) / size_dict, 2)
        else:
            try:
                total_prob += math.log(1 / (size_dict + uni_dict[test_bi[i]]), 2)
            except:
                total_prob += math.log(1 / size_dict, 2)
    return np.power(2, -total_prob / (len(test_bi) - 1))


def trigram_test(test_tri, bi_dict, size_tri_dict, tri_dict):
    total_prob = 0
    for i in range(len(test_tri) - 2):
        word = test_tri[i] + " " + test_tri[i+1] + " " + test_tri[i+2]
        if word in tri_dict:
            try:
                total_prob += math.log((tri_dict[word] + 1) / (size_tri_dict + bi_dict[test_tri[i] + " " + test_tri[i+1]]), 2)
            except:
                total_prob += math.log((tri_dict[word] + 1) / size_tri_dict, 2)
        else:
            try:
                total_prob += math.log(1 / (size_tri_dict + bi_dict[test_tri[i] + " " + test_tri[i+1]]), 2)
            except:
                total_prob += math.log(1 / size_tri_dict, 2)
    return np.power(2, -total_prob / (len(test_tri) - 2))


def main(test_list, hamiton_uni_dict, hamilton_bi_dict, hamilton_tri_dict, madison_uni_dict, madison_bi_dict, madison_tri_dict):
    dictionary = {1:"unigram", 2: "bigram", 3:"trigram"}
    for k in test_list:
        for i in range(1, 4):

            if i == 1:
                list = read_files(i, k)
                prob_ha = unigram_test(list, hamiton_uni_dict, sum(hamiton_uni_dict.values()))
                prob_ma = unigram_test(list, madison_uni_dict, sum(madison_uni_dict.values()))

            elif i == 2:
                list = read_files(i, k)
                prob_ha = bigram_test(list, hamilton_bi_dict, len(hamilton_bi_dict.keys()), hamiton_uni_dict)
                prob_ma = bigram_test(list, madison_bi_dict, len(madison_bi_dict.keys()), madison_uni_dict)

            else:
                list = read_files(i, k)
                prob_ha = trigram_test(list, hamilton_bi_dict, len(hamilton_tri_dict.keys()), hamilton_tri_dict)
                prob_ma = trigram_test(list, madison_bi_dict, len(madison_tri_dict.keys()), madison_tri_dict)


            if np.abs(prob_ha) > np.abs(prob_ma):
                print("hamilton: ", np.abs(prob_ha), "****WINNER**** madison: ", np.abs(prob_ma), dictionary[i], " for ==>>>> text ", k)
            else:
                print("****WINNER**** hamilton: ", np.abs(prob_ha), " madison: ", np.abs(prob_ma), dictionary[i], " for ==>>>> text ", k)
        print("*****************************************************************************")