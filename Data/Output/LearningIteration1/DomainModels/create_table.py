import os
import xlsxwriter

domain_folder = ["Camera","Cellphone","Computer","Food"]

for domain in domain_folder:
    workbook = xlsxwriter.Workbook("./"+domain+"/"+domain+"_twords_with_twdist.xlsx")
    worksheet = workbook.add_worksheet()

    with open("./"+domain+"/"+domain+".twdist",'r') as twdist:
        topic_word_distribution = [line.split() for line in twdist]

    with open("./"+domain+"/"+domain+".twords",'r') as twords:
        top_word = [line.split() for line in twords]

    with open("./"+domain+"/"+domain+".vocab",'r') as vocab:
        vocabulary=vocab.read().splitlines()

    top_word.remove(top_word[0])
    top_word = list(zip(*top_word[::-1]))
    for i in range(len(top_word)):
        top_word[i] = top_word[i][::-1]

    for i in range(len(vocabulary)):
        vocabulary[i] = vocabulary[i].split(':')[1]



    final = []
    for i in range(len(top_word)):
        tmp = []
        for j in range(len(top_word[0])):
            tmp.append([top_word[i][j],topic_word_distribution[i][vocabulary.index(top_word[i][j])]])
        final.append(tmp)
    # print(final)


    i=0
    while (i<30):
        worksheet.merge_range(0,i,0,i+1,'Topic ' + str(i//2))
        i += 2
    for i in range(0,30,2):
        for j in range(len(final[0])):
            worksheet.write(j+1,i,final[i//2][j][0])
            worksheet.write(j+1,i+1,final[i//2][j][1])
    workbook.close()
