import requests
from bs4 import BeautifulSoup as bs
import time, json

outputFile = open("/home/orashar/Documents/outputQuestions.txt", "a+")



def getQuestionsFromUrl(url):
    parentDict = {}
    print("reading ", url)
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    print("collecting data from : ", url)
    divP = soup.find("div", {"class": "article-detail"})
    allh2 = divP.findAll("h2")
    titleh2 = allh2[0]
    print(f"inside {titleh2.text}")
    childDict = {}
    parentDict["title"] = titleh2.text

    next = titleh2
    i = 0
    qText = ""
    year = ""
    while True:
        try:
            next = next.next_sibling
            while next.name == None or next.name not in ["p", "h2","ol"]:
                next = next.next_sibling
            #print(next)
            if next.name == 'p':
                if next.text[:1].isdigit():
                    if qText != "":
                        i += 1
                        questionDict = {}
                        qText = qText.replace(qText.split(" ")[0], "Q.")
                        questionDict["question"] = qText
                        tagsDict = [titleh2.text, year, "UPSC"]
                        questionDict["tags"] = tagsDict
                        childDict["child" + str(i)] = questionDict
                        #print(childDict)
                        #print("previous question -> ", qText, "\n\n")
                    #print("previous question -> ", qText , "\n\n")
                    qText = next.text
                else:
                    qText += "\n" + next.text
            if next.name == 'ol':
                lis = next.findAll("li")
                for li in lis:
                    qText += "\n" + li.text
            if next.name == 'h2':
                if(qText != ""):
                    i +=1
                    questionDict = {}
                    qText = qText.replace(qText.split(" ")[0], "Q.")
                    questionDict["question"] = qText
                    tagsDict = [titleh2.text, year, "UPSC"]
                    questionDict["tags"] = tagsDict
                    childDict["child" + str(i)] = questionDict
                    #print("previous question -> ", qText, "\n\n")
                qText = ""
                year = next.text
        except AttributeError:
            if qText != "":
                i += 1
                questionDict = {}
                qText = qText.replace(qText.split(" ")[0], "Q.")
                questionDict["question"] = qText
                tagsDict = [titleh2.text, year, "UPSC"]
                questionDict["tags"] = tagsDict
                childDict["child" + str(i)] = questionDict
                #print("previous question -> ", qText, "\n\n")
            print("Attribute error", " no next child for current child")
            break
    parentDict["child"] = childDict
    #print(parentDict)
    filename = titleh2.text + ".json"
    with open("./outputJSON/"+filename, "w") as f:
        f.write(json.dumps(parentDict, indent=4))
        print("written to json in ", filename, "\ntotal questions = ", i, "\n\n")





def download(pageurl):
    questionsArr = []
    urlList = []
    if pageurl != "":
        print(pageurl)
        print("checking", pageurl)
        r = requests.get(pageurl)
        print("reading", pageurl, "...")
        soup = bs(r.content, "html.parser")
        print("collecting list of questions...")
        divP = soup.find("div", {"class":"list-category"})
        divC = divP.find_all("div", {"class":"content"})
        for div in divC:
            a = div.find("a")
            #print(a["href"])
            urlList.append(a["href"])
    print("url list collected.\n")
    i = 0
    for url in urlList:
        getQuestionsFromUrl(url)
        continue

def writeQuestionInFile(question):
    print("writing question in file")
    outputFile.write(str(question + " #UPSC") + "\n")

def writeQuestionsInFile(questionsArr, tags):
    for question in questionsArr:
        outputFile.write(str(question) + "\t")
        for tag in tags:
            outputFile.write(str("#" + tag))
        outputFile.write("\n")

urlFile = open("./pyq.txt", "r")
for line in urlFile.readlines():
    url = line.split("#")[0]
    tags = line.split("#")[1:]
    url = "https://www.drishtiias.com/mains/mains-previous-year-papers/subject-wise-papers"
    download(url)
    #writeQuestionsInFile(questionsArr, tags)
    break

urlFile.close()
outputFile.close()
