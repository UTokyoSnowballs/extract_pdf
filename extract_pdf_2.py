import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import glob
import sys

searchword = re.compile(r"プレスリリース")

def pdfsearch(path):
    rsrcmgr = PDFResourceManager()
    outfp = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    fp = open(path, 'rb') #open a pdf file
    # PDFPageInterpreterオブジェクトを作成．PDFDocumentから任意のページのオブジェクトPagePDF を投げると，page contentが処理される
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagecount = 0
    pagelist = []
    matchtime = 0
    for page in PDFPage.get_pages(fp, maxpages=0):
        interpreter.process_page(page)
        # この時点で outfpにページのデータが追加される
        text = re.sub(r"\s+","", outfp.getvalue())
        if matchtime < len(searchword.findall(text)):
            pagelist.append(pagecount)
        matchtime = len(searchword.findall(text))
        print(str(pagecount+1), end=" ")
        sys.stdout.flush()
        pagecount = pagecount + 1
    fp.close()
    device.close()
    outfp.close()
    print(pagelist)
    return pagelist


def makepdf(filename, output):
    print("searching "+filename)
    pagelist = pdfsearch(filename)
    input = PdfFileReader(filename, "r")
    print("extracting", end=" ")
    sys.stdout.flush()
    for i in pagelist:
        print(i,end=" ")
        sys.stdout.flush()
        page = input.getPage(i)
        output.addPage(page)
    print("done")

output = PdfFileWriter()
filelist = glob.glob("./**/**.pdf")
filelist.sort()
for file in filelist:
    makepdf(file, output)


with open("プレスリリース.pdf", "wb") as out_f:
    output.write(out_f)