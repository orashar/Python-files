import json

def read_csv(title, file):
    parentDict = {}
    childDict = {}
    parentDict["title"] = title

    lines = []
    with open(file, "r") as f:
        lines = f.readlines()

    i = 0
    for line in lines:
        i += 1
        arr = line.split(",")

        questionDict = {}
        qText = arr[0]
        questionDict["question"] = qText
        tagsDict = arr[1:]
        tagsDict.append("UPSC")
        questionDict["tags"] = tagsDict
        childDict["child" + str(i)] = questionDict
        parentDict["child"] = childDict

    filename = file.replace(".csv", ".json")
    writeInJson(parentDict, filename)

def writeInJson(dictionary, filename):
    with open("./outputJSON/" + filename, "w") as f:
        f.write(json.dumps(dictionary, indent=4))

file = "test.csv"
read_csv("pdf_questions", file)