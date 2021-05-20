import nltk
import json
import clips
#Punem textul de input intr-un fisier separat pentru
#a putea fi vazut/modificat in CLIPS
def ProvideText(text,TextInput):
    with open(TextInput,"w")as textInput:
        textInput.write(text)

def UpdateGrammar(text,limbaj,limbajTokenizat,FactsUpdate):
    #Punem textul din fisierul limbaj intr-un string
    with open(limbaj,"r") as string:
        data = string.read().replace("\n"," ")
    #Transformam string-ul intr-un dictionar
    # Transformam textul intr-o lista de cuvinte
    cuvinteDinText = text.split()
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
    #Transformam limbajul tokenizat in fact-uri clips si le adaugam intr-un fisier "Facts"
    with open(FactsUpdate,"w") as string:
        for element in tagged:
            text = "(assert (" + element[0] + " " + element[1]+"))"
            string.write(text + "\n")


def secondFuncitonality(text,limbaj,limbajTokenizat, FactsVerify):
    # Punem textul din fisierul limbaj intr-un string
    with open(limbaj,"r") as string:
        limbajText = string.read().replace("\n"," ")
    # Transformam textul intr-o lista de cuvinte
    verifytext = text.split()

    # Transformam datele din fisierul limbajului intr-o lista de cuvinte
    cuvinte = limbajText.split()
    # Verificam pentru fiecare cuvant din textul dat ca input
    # daca este in lista noastra de cuvinte
    for word in verifytext:
        if word not in cuvinte:
            print("Propozitia data ca input nu poate fi parsata cu limbajul actual.")
            return
    print("Propozitia data ca input poate fi parsata cu limbajul actual si va fi\n"
          "transformata in fact-uri CLIPS")

    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    with open(FactsVerify,"w") as string:
        for element in tagged:
            text = "(assert (" + element[0] + " " + element[1]+"))"
            string.write(text + "\n")
def clipsImplementation():
    env = clips.Environment()

    template_string = """ (deftemplate translation
       (multislot text (type STRING))
       (multislot tokens)
       (multislot output)
       (slot complete (default NO))
    )"""

    env.build(template_string)
    template = env.find_template('translation')

    rule1 = """
    (defrule get_input
       =>
       (printout t "Input: ")
       (bind ?text (readline))
       (assert (translation (text ?text)
                            (tokens (explode$ ?text)))))

    """
    env.build(rule1)

    rule2 = """
    (defrule apply_rule
       ?t <- (translation (tokens $?tokens $?rest)
                          (output $?output))
       (regula ?replacement $?tokens)
       =>
       (modify ?t (tokens $?rest)
                  (output $?output ?replacement))
    )
    """
    env.build(rule2)

    rule3 = """
    (defrule success
       ?t <- (translation (tokens)
                          (complete NO))
       =>
       (modify ?t (complete YES))
    )
    """
    env.build(rule3)

    rule4 = """
    (defrule print_results
       ?t <- (translation (complete ?complete)
                          (tokens $?tokens)
                          (output $?output))
       =>
       (printout t ?complete " " (implode$ (create$ ?output ?tokens)) crlf))
    """
    env.build(rule4)
    for rule4 in env.rules():
        print(rule4)

    env.run()


UpdateGrammar("Test de verificare la misto","Limbaj.txt","LimbajTokenizat.txt","FactsUpdate.txt")
secondFuncitonality("Test de verificare la misto","Limbaj.txt","LimbajTokenizat.txt","FactsVerify.txt")
ProvideText("Test de verificare la misto","TextInput.txt")
clipsImplementation()