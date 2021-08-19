# -*- coding: UTF-8 -*-
import json

import chardet
import pypinyin as pypinyin

sensitiveFile='sensitive_words.json'

class book():
    _NORMAL=0
    _SECTIONEND=1
    _BOOKEND=2


    # 初始化函数，调用getbook获取book内容
    def __init__(self, path):
        self.bookjson = self.getbook(path)
        self.sectionIndex = 0
        self.paragraphIndex = 0
        self.sectionNum=len(self.bookjson['section_list'])
        self.paragraphNum=len(self.bookjson['section_list'][self.sectionIndex]['paragraph_list'])
        with open(sensitiveFile, 'rb') as f:
            strF = f.read()
            codetype = chardet.detect(strF)['encoding']
            self.sensitive_words = set(json.loads(strF.decode(codetype))['sensitive_words'])
        self.title=self.bookjson['title']
        for word in self.sensitive_words:
            self.title = self.title.replace(word, pypinyin.lazy_pinyin(word[0])[0] + word[1:])



    # 获取book内容
    def getbook(self, path):
        with open(path, 'rb') as f:
            strF = f.read()
            codetype = chardet.detect(strF)['encoding']
            book = json.loads(strF.decode(codetype))
        return book


    def getsection(self):
        section=self.bookjson['section_list'][self.sectionIndex]
        self.section=section
        return section

    def nextsection(self):
        self.sectionIndex+=1
        isEnd=False
        if self.sectionIndex>=self.sectionNum:
            self.sectionIndex=0
            isEnd=True
        return isEnd

    def getparagraph(self):
        self.getsection()
        paragraph=self.section['paragraph_list'][self.paragraphIndex]
        self.paragraph=paragraph
        return paragraph

    def nextparagraph(self):
        self.paragraphIndex+=1
        status=self._NORMAL
        if self.paragraphIndex>=self.paragraphNum:  # 小节已经读完
            if self.nextsection():  # 一本book已经读完
                status=self._BOOKEND
            else:  # 小节读完，且不是book的最后一个小节
                status=self._SECTIONEND
            self.getsection()
            self.paragraphNum=len(self.section['paragraph_list'])
            self.sectionIndex=0

        return status

    def getinputlist(self):
        self.getparagraph()
        inputlist=[]
        last_index=0
        paragraph_str=self.paragraph['context']
        for word in self.sensitive_words:
            paragraph_str = paragraph_str.replace(word, pypinyin.lazy_pinyin(word[0])[0] + word[1:])
        while len(paragraph_str)!=0:
            index=paragraph_str.find('。')
            if index==-1:
                index=len(paragraph_str)-1
            if index+last_index<60:
                try:
                    inputlist[-1]+=paragraph_str[:index+1]
                    print(inputlist)
                except:
                    inputlist.append(paragraph_str[:index + 1])
                last_index+=index+1
            else:
                last_index=index+1
                inputlist.append(paragraph_str[:index + 1])
            paragraph_str=paragraph_str[index+1:]
            if len(paragraph_str)==0:
                break
        return inputlist


if __name__ == '__main__':
    oneBook=book('./bookpool/book1.json')
    print(oneBook.bookjson)
    print(oneBook.sectionIndex)
    oneBook.getinputlist()
