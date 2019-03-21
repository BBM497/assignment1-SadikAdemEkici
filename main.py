import string
import text
import ngram
import test

def read_files(essay_list, number, essay_name):
    for i in range(1, 87):
        if i in essay_name:
            essay = open("data\\" + str(i) + ".txt", "r")
            author = essay.readline().rstrip(" \n")
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
            book = text.Text(author, essay, new)
            essay_list.append(book)


def main():
    essay_name = [1, 6, 7, 8, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29, 10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
    test_essays = [1, 9, 11, 12, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 62, 63]
    uni_essay_list = []
    bi_essay_list = []
    tri_essay_list = []

    read_files(uni_essay_list, 1, essay_name)
    read_files(bi_essay_list, 2, essay_name)
    read_files(tri_essay_list, 3, essay_name)

    hamilton = ngram.model("HAMILTON", {}, {}, {}, {}, {})
    madison = ngram.model("HAMILTON", {}, {}, {}, {}, {})

    hamilton.unigram = ngram.unigram("HAMILTON", uni_essay_list)
    madison.unigram = ngram.unigram("MADISON", uni_essay_list)

    hamilton.bigram, hamilton.bigram_generate= ngram.bigram("HAMILTON", bi_essay_list)
    madison.bigram, madison.bigram_generate = ngram.bigram("MADISON", bi_essay_list)

    hamilton.trigram, hamilton.trigram_generate = ngram.trigram("HAMILTON", tri_essay_list)
    madison.trigram, madison.trigram_generate = ngram.trigram("MADISON", tri_essay_list)
    for i in range(2):
        hamilton_generate_uni_essay = ngram.unigram_generator(hamilton.unigram, sum(hamilton.unigram.values()))
        hamilton_generate_bi_essay = ngram.bigram_generator(hamilton.bigram_generate.copy())
        hamilton_generate_tri_essay = ngram.trigram_generator(hamilton.trigram_generate.copy())

        madison_generate_uni_essay = ngram.unigram_generator(madison.unigram, sum(madison.unigram.values()))
        madison_generate_bi_essay = ngram.bigram_generator(madison.bigram_generate.copy())
        madison_generate_tri_essay = ngram.trigram_generator(madison.trigram_generate.copy())

        print("********************************** HAMILTON UNIGRAM ESSAY :**************************************")
        print(hamilton_generate_uni_essay)
        print("HAMILTON: ",test.unigram_test(hamilton_generate_uni_essay.split(" "), hamilton.unigram, sum(hamilton.unigram.values())))
        print("MADISON: ",test.unigram_test(hamilton_generate_uni_essay.split(" "), madison.unigram, sum(madison.unigram.values())), "\n")
        print("********************************** HAMILTON BIGRAM ESSAY :**************************************")
        print(hamilton_generate_bi_essay)
        print("HAMILTON: ", test.bigram_test(hamilton_generate_bi_essay.split(" "), hamilton.bigram, len(hamilton.bigram.keys()), hamilton.unigram))
        print("MADISON: ", test.bigram_test(hamilton_generate_bi_essay.split(" "), madison.bigram, len(madison.bigram.keys()), madison.unigram), "\n")

        print("********************************** HAMILTON TRIGRAM ESSAY :**************************************")
        print(hamilton_generate_tri_essay)
        print("HAMILTON", test.trigram_test(hamilton_generate_tri_essay.split(" "), hamilton.bigram, len(hamilton.trigram.keys()), hamilton.trigram))
        print("MADISON", test.trigram_test(hamilton_generate_tri_essay.split(" "), madison.bigram, len(madison.trigram.keys()), madison.trigram), "\n")

        print("********************************** MADISON UNIGRAM ESSAY :**************************************")
        print(madison_generate_uni_essay)
        print("HAMILTON: ",test.unigram_test(madison_generate_uni_essay.split(" "), hamilton.unigram, sum(hamilton.unigram.values())))
        print("MADISON: ",test.unigram_test(madison_generate_uni_essay.split(" "), madison.unigram, sum(madison.unigram.values())), "\n")

        print("********************************** MADISON BIGRAM ESSAY :**************************************")
        print(madison_generate_bi_essay,"\n")
        print("HAMILTON: ", test.bigram_test(madison_generate_bi_essay.split(" "), hamilton.bigram, len(hamilton.bigram.keys()), hamilton.unigram))
        print("MADISON: ", test.bigram_test(madison_generate_bi_essay.split(" "), madison.bigram, len(madison.bigram.keys()), madison.unigram), "\n")

        print("********************************** MADISON TRIGRAM ESSAY :**************************************")
        print(madison_generate_tri_essay)
        print("HAMILTON", test.trigram_test(madison_generate_tri_essay.split(" "), hamilton.bigram, len(hamilton.trigram.keys()), hamilton.trigram))
        print("MADISON", test.trigram_test(madison_generate_tri_essay.split(" "), madison.bigram, len(madison.trigram.keys()), madison.trigram), "\n")

    test.main(test_essays, hamilton.unigram, hamilton.bigram, hamilton.trigram, madison.unigram, madison.bigram, madison.trigram)


main()

