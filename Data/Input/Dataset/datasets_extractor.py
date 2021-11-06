from xml.etree.ElementTree import ElementTree
from collections import Counter
import os

# Loại bỏ các từ xuất hiện ít hơn 5 lần
def removeWord(lst):
    counted = Counter(lst)
    return {el for el in lst if counted[el] >= 5}


# Chỉ lấy Noun và Adjective do Verb gây nhiễu kết quả
verb_adj = ["NN","NNS","NNP","NNPS","JJ","JJR","JJS"]

# Không lấy tên domain do số lượng từ giống với domain name lớn
domain_name = ["camera","photo","cell","phone","accessories","computers","grocery","food","gourmet"]

# Nhập bộ english.stop bao gồm các từ ngắt câu trong tiếng anh
with open('english_stop.txt') as f:
    english_stop = f.read().splitlines()
    f.close()

#Tên các thư mục domain
domain_folder = ["Camera","Cellphone","Computer","Food"]
# Khởi tạo biến  
err = 0
global_list = []
vocab_all = []
for domain in domain_folder:
    for filename in os.listdir("./"+domain+"/500/"):
        f = "./"+domain+"/500/" + filename
        try:
            with open(f,'r',encoding="iso-8859-5") as file:
                tree = ElementTree()
                tree.parse(file)
                root = tree.getroot()
                # Đi hết các câu trong document
                for num_child in root:
                    vocab_line = []
                    lemma = num_child[1].text.split(" ")
                    vocab = num_child[2].text.lower().replace(".","").replace(",","").replace("-","").replace("%","").replace("\/","").split(" ")
                    for i in range(len(vocab)):
                        # Chỉ lấy các từ phù hợp với tiêu chuẩn đặt ra
                        if lemma[i] in verb_adj and vocab[i] not in domain_name and vocab[i] not in english_stop and vocab[i] != "" and not vocab[i].isnumeric():
                            vocab_line.append(vocab[i])
                            global_list.append(vocab[i])   
                    if (len(vocab_line)>0):
                        vocab_all.append(vocab_line)
                file.close()
        except Exception as e: 
            print(f,end=" ")
            print(e)

    #Loại bỏ các từ xuất hiện <5 lần
    keep_word_list = removeWord(global_list)
    #Tạo dict index
    index_word_dict = {k: v for v, k in enumerate(keep_word_list)}
    #Lưu vocab
    f = open("./"+domain+"/"+domain+".vocab", "w")
    for word in index_word_dict:
        print(str(index_word_dict[word])+":"+word,file=f)
    f.close()
    #Lưu docs
    f = open("./"+domain+"/"+domain+".docs", "w")
    for line in vocab_all:
        check = False
        for word in line:
            if word in keep_word_list:
                print(index_word_dict[word],end=" ",file=f)
                check = True
        if check: 
            print(file=f)
    f.close()