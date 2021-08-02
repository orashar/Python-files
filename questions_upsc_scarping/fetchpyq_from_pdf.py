from PyPDF2 import PdfFileReader
import re

r = PdfFileReader(open("./1.pdf", "rb"))
questionContent = ""
for i in range(3):
    questionContent += r.getPage(i).extractText()
questionContent = questionContent.split("ANSWER SHEET")[0].split("Answer all the following questions. Contents of the answer are more important than its length.")[-1]
print(questionContent)
print("now reges content")
ress = re.findall("\AQ*", questionContent)
print(ress)"""

#questionContent = r["content"].split("ANSWER SHEET")[0].split("Answer all the following questions. Contents of the answer are more important than its length.")[-1]
#print(questionContent)

