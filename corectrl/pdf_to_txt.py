"""

    此文件提供一个函数pdf2txt，即将pdf文件转为字符串，由方法返回值传出

"""
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
from PyPDF2 import PdfFileReader
import re

def pdf2txt(url):
    """ 将pdf文件转为txt文件，返回一个字符串"""
    try:
        # 打开一个pdf文件
        fp = open(url, 'rb')
        # 创建一个PDF文档解析器对象
        parser = PDFParser(fp)
        # 创建一个PDF文档对象存储文档结构
        # 提供密码初始化，没有就不用传该参数
        # document = PDFDocument(parser, password)
        document = PDFDocument(parser)
        # 检查文件是否允许文本提取
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # 创建一个PDF资源管理器对象来存储共享资源
        # caching = False不缓存
        rsrcmgr = PDFResourceManager(caching=False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 创建一个PDF页面聚合对象
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解析器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理文档当中的每个页面

        # doc.get_pages() 获取page列表
        # for i, page in enumerate(document.get_pages()):
        # PDFPage.create_pages(document) 获取page列表的另一种方式
        replace = re.compile(r'\s+')
        # 循环遍历列表，每次处理一个page的内容
        texts = ''
        pages = PDFPage.create_pages(document)
        reader = PdfFileReader(url)
        yeshu = reader.getNumPages()
        print(yeshu)
        for i, page in zip(range(0, yeshu), pages):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            for x in layout:
                # 如果x是水平文本对象的话
                if (isinstance(x, LTTextBoxHorizontal)):
                    text = re.sub(replace, '', x.get_text())
                    if len(text) != 0:
                        texts = texts + text
            print("{:.2f}".format((float)((i + 1) / yeshu) * 100), "%")
        return texts

    except:
        print("邮件发送失败\n")

if __name__ == "__main__":
    t = pdf2txt("F:/pythonprojects/data/sh_mid/600028_2019_n.pdf")
    print(t)