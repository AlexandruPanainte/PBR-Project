import nltk
def UpdateGrammar(text,limbaj,limbajTokenizat):
    #Punem textul din fisierul limbaj intr-un string
    with open(limbaj,"r") as string:
        data = string.read().replace("\n"," ")
    #Transformam string-ul intr-un dictionar
    #dataDictionary = eval(str(data))
    # Transformam textul intr-o lista de cuvinte
    cuvinteDinText = text.split()
    string= str(data)
    # Verificam pentru fiecare cuvant din textul dat ca input
    # daca este in lista noastra de cuvinte
    for word in cuvinteDinText:
        # Transformam string-ul intr-o lista de cuvinte
        cuvinte = data.split()
        if word not in cuvinte:
            #Updatam string-ul
            data += " " + word
    # Updatam din nou lista de cuvinte dupa ultima iteratie de la for
    cuvinte = data.split()
    # Dam override la fisierul limbaj cu noul text actualizat
    with open(limbaj, "w") as limbaj:
        limbaj.write(data)
    # Se face tokenizarea textului actualizat
    tokens = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokens)
    # Dam override la fisierul limbajTokenizat cu actualul text tokenizat
    with open(limbajTokenizat, "w") as limbaj:
        limbaj.write(str(tagged))

# Pentru verificarea functionalitatii recomand sa se stearga toate datele din
# limbaj si limbajTokenizat iar apoi sa se apeleze de mai multe ori functia

UpdateGrammar(", , punct ","Limbaj.txt","LimbajTokenizat.txt")
