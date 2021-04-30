import docx
import PyPDF2
import tkinter
from tkinter import filedialog as fd
import os
from google_trans_new import google_translator
from rake_nltk import Rake   # Rapid Automatic Keyword Extraction algorithm

#choice 1: pdf/all
def get_pdf_text(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    ptext = pageObj.extractText()
    return ptext

 #choice 2: doc/docx
def get_doc_text(filename):
    doc = docx.Document(filename)
    ftext = []
    for para in doc.paragraphs:
        ftext.append(para.text)
    return '\n'.join(ftext)

def detect_and_translate(text):
    translator = google_translator()
    r = Rake()
    original_lang = translator.detect(text)
    print("\nSource Language was : ",original_lang[1])
    if(original_lang[0]!='en'):
        print(text)
    translate_text = translator.translate(text,lang_tgt='en') 
    print("\nEnglish Translation \n")
    r.extract_keywords_from_sentences(translate_text.split('\n'))
    print(translate_text)
    ranked = r.get_ranked_phrases_with_scores()
    print("\nPhrases with Scores")
    print(ranked)

#Module to browse for files(pdf/doc/docx/all)
root = tkinter.Tk()
root.withdraw()
def menu():
    print("\n")
    print("Menu Driven Program for Language Detection and Translation ")
    print("**********************************************************")
    print("1.PDF")
    print("2.Docx")
    print("3.Quit")
    print("**********************************************************")
    while True:
        try:
            choice = int(input("Enter Choice: "))
            if choice == 1:
                tempdir=fd.askopenfilename(parent=root,
                           initialdir = "/",
                           title = "Select file",
                           filetypes = (("pdf","*.pdf"),("all files","*.*")))
                if len(tempdir) > 0:
                    print ("You choose %s" % tempdir)
                else:
                    print("Nothing is selected!")
                text = get_pdf_text(tempdir)
                detect_and_translate(text)
                menu()
                break
            elif choice == 2:
                tempdir=fd.askopenfilename(parent=root,
                           initialdir = "/",
                           title = "Select file",
                           filetypes = (("docx","*.docx"),("doc","*.doc")))
                if len(tempdir) > 0:
                    print ("You choose %s" % tempdir)
                else:
                    print("Nothing is selected!")
                text = get_doc_text(tempdir)
                detect_and_translate(text)
                menu()
                break
            elif choice == 3:
                break
            else:
                print("Enter digits between 1-3 only")
                menu()
        except ValueError:
            print("Invalid Input!Try Again ")
    exit

menu()