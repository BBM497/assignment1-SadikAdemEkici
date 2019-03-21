import random


class model:
    def __init__(self, name, unigram, bigram, trigram, bigram_generate, trigram_generate):
        self.name = name
        self.unigram = unigram
        self.bigram = bigram
        self.trigram = trigram
        self.bigram_generate = bigram_generate
        self.trigram_generate = trigram_generate


def unigram(name, list):
    dict = {}
    for author in list:
        if author.name == name:
            for j in author.list:
                if j in dict.keys():
                    dict[j] += 1
                else:
                    dict[j] = 1
    return dict


def bigram(name, list):
    dict = {}
    generate_dict = {}
    for author in list:
        if author.name == name:
            for j in range(len(author.list)-1):
                key = author.list[j] + " " + author.list[j+1]
                if key in dict.keys():
                    dict[key] += 1
                    if author.list[j] in generate_dict.keys():
                        if author.list[j + 1] in generate_dict[author.list[j]].keys():
                            generate_dict[author.list[j]][author.list[j + 1]] += 1
                        else:
                            generate_dict[author.list[j]][author.list[j + 1]] = 1
                    else:
                        generate_dict[author.list[j]] = {}
                        if author.list[j+1] in generate_dict[author.list[j]].keys():
                            generate_dict[author.list[j]][author.list[j+1]] += 1
                        else:
                            generate_dict[author.list[j]][author.list[j + 1]] = 1
                else:
                    dict[key] = 1
                    if author.list[j] in generate_dict.keys():
                        if author.list[j + 1] in generate_dict[author.list[j]].keys():
                            generate_dict[author.list[j]][author.list[j + 1]] += 1
                        else:
                            generate_dict[author.list[j]][author.list[j + 1]] = 1
                    else:
                        generate_dict[author.list[j]] = {}
                        if author.list[j+1] in generate_dict[author.list[j]].keys():
                            generate_dict[author.list[j]][author.list[j+1]] += 1
                        else:
                            generate_dict[author.list[j]][author.list[j + 1]] = 1

    return dict, generate_dict


def trigram(name, list):
    dict = {}
    generate_dict = {}

    for author in list:
        if author.name == name:
            for j in range(len(author.list)-2):
                key = author.list[j] + " " + author.list[j+1] + " " + author.list[j+2]
                generate_key = author.list[j] + " "+ author.list[j+1]
                if key in dict.keys():
                    dict[key] += 1
                    if generate_key in generate_dict.keys():
                        if author.list[j+2] in generate_dict[generate_key].keys():
                            generate_dict[generate_key][author.list[j+2]] += 1
                        else:
                            generate_dict[generate_key][author.list[j+2]] = 1
                    else:
                        generate_dict[generate_key] = {author.list[j+2]: 1}
                else:
                    dict[key] = 1
                    if generate_key in generate_dict.keys():
                        if author.list[j+2] in generate_dict[generate_key].keys():
                            generate_dict[generate_key][author.list[j+2]] += 1
                        else:
                            generate_dict[generate_key][author.list[j+2]] = 1
                    else:
                        generate_dict[generate_key] = {author.list[j+2]: 1}

    return dict, generate_dict


def probabilty(word, count_dict, total_size):
    if word in count_dict.keys():
        return count_dict[word]/total_size
    else:
        return 0


def create_unigram_generate_dict(dict, sizeofngram_models):
    generate_dictionary = {}
    value = 0
    for word in dict.keys():
        generate_dictionary[word] = [value, dict[word] / sizeofngram_models + value]
        value += dict[word] / sizeofngram_models
    return generate_dictionary


def unigram_generator(dict, sizeofngram_models):
    generate_dict = create_unigram_generate_dict(dict, sizeofngram_models)
    new_essay = ""
    control = 0
    for i in range(30):
        select = random.random()
        for word in generate_dict:
            if select >= generate_dict[word][0] and select < generate_dict[word][1]:
                if "token" in word or '.' in word or '!' in word or '?' in word:
                    new_essay += word
                    control = 1
                    break
                new_essay += word + " "
        if control == 1:
            break
    return new_essay


def bigram_generator(dict):
    new_essay = ""
    iteration = 0
    while(1):
        if iteration > 30 or "token" in new_essay or '.' in new_essay or '!' in new_essay or '?' in new_essay:
            break
        number = 0
        generator_dict = {}
        if iteration == 0:
            word = "<s>"
            if word in dict.keys():
                generator_dict = dict[word].copy()
                for k in dict[word].keys():
                    generator_dict[k] = [number, number + dict[word][k] / sum(dict[word].values())]
                    number += dict[word][k] / sum(dict[word].values())
            select = random.random()
            for word2 in generator_dict.keys():
                if select >= generator_dict[word2][0] and select < generator_dict[word2][1]:
                    new_essay += word + " " + word2
                    iteration += 2

        else:
            word = new_essay.split(" ")[len(new_essay.split(" ")) - 1]
            if word in dict.keys():
                generator_dict = dict[word].copy()
                for k in dict[word].keys():
                    generator_dict[k] = [number, number + dict[word][k] / sum(dict[word].values())]
                    number += dict[word][k] / sum(dict[word].values())
            select = random.random()
            for word2 in generator_dict.keys():
                if select >= generator_dict[word2][0] and select < generator_dict[word2][1]:
                    new_essay += " " + word2
                    iteration += 1

    return new_essay

def trigram_generator(dict):
    new_essay = ""
    iteration = 0
    while (1):
        if iteration > 30 or "token" in new_essay or '.' in new_essay or '!' in new_essay or '?' in new_essay:
            break
        number = 0
        if iteration == 0:
            word = "<s> <s>"
            generator_dict = {}
            if word in dict.keys():
                for k in dict[word].keys():
                    generator_dict[k] = [number, number + dict[word][k] / sum(dict[word].values())]
                    number += dict[word][k] / sum(dict[word].values())
            select = random.random()
            for word2 in generator_dict.keys():
                if select >= generator_dict[word2][0] and select < generator_dict[word2][1]:

                    new_essay += word + " " + word2
                    iteration = len(new_essay.split(" "))
                    break


        else:
            a = new_essay.split(" ")
            word = a[- 2] + " " +a[- 1]
            if word in dict.keys():
                generator_dict = {}
                for k in dict[word].keys():
                    generator_dict[k] = [number, number + dict[word][k] / sum(dict[word].values())]
                    number += dict[word][k] / sum(dict[word].values())


            select = random.random()
            for word2 in generator_dict.keys():
                if select >= generator_dict[word2][0] and select < generator_dict[word2][1]:
                     new_essay += " " + word2
                     iteration = len(new_essay.split(" "))
                     break

    return new_essay

