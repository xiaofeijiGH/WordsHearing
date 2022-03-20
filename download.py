'''
程序思想：
有两个本地语音库，美音库Speech_US，英音库Speech_US
调用有道api，获取语音MP3，存入对应的语音库中
'''
 
import os
import urllib.request
import requests
import numpy as np
import time

class youdao():
    def __init__(self, type=0, word='hello',date=None):
        '''
        调用youdao API
        type = 0：美音
        type = 1：英音
        判断当前目录下是否存在两个语音库的目录
        如果不存在，创建
        '''
        word = word.lower()  # 小写
        self._type = type  # 发音方式
        self._word = word  # 单词
        if date == None:
            self.date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        else:
            self.date = date

        # 文件根目录
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        if 0 == self._type:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US\\'+self.date)  # 美音库

        else:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN\\'+self.date)  # 英音库
 
        # 判断是否存在美音库
        if not os.path.exists('Speech_US'):
            # 不存在，就创建
            os.makedirs('Speech_US')
        # 判断是否存在英音库
        if not os.path.exists('Speech_EN'):
            # 不存在，就创建
            os.makedirs('Speech_EN')

        if not os.path.exists('Speech_US'+'\\'+self.date):
            os.mkdir('Speech_US'+'\\'+self.date)
 
    def setAccent(self, type=0):
        '''
        type = 0：美音
        type = 1：英音
        '''
        self._type = type  # 发音方式
 
        if 0 == self._type:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_US')  # 美音库
        else:
            self._dirSpeech = os.path.join(self._dirRoot, 'Speech_EN')  # 英音库
 
    def getAccent(self):
        '''
        type = 0：美音
        type = 1：英音
        '''
        return self._type
 
    def down(self, word):
        '''
        下载单词的MP3
        判断语音库中是否有对应的MP3
        如果没有就下载
        '''
        word = word.lower()  # 小写
        tmp = self._getWordMp3FilePath(word)
        if tmp is None:
            self._getURL()  # 组合URL
            print(self._filePath)
            # 调用下载程序，下载到目标文件夹
            # print('不存在 %s.mp3 文件\n将URL:\n' % word, self._url, '\n下载到:\n', self._filePath)
            # 下载到目标地址
            urllib.request.urlretrieve(self._url, filename=self._filePath)
            print('%s.mp3 下载完成' % self._word)
        else:
            print('已经存在 %s.mp3, 不需要下载' % self._word)
 
        # 返回声音文件路径
        return self._filePath
 
    def _getURL(self):
        '''
        私有函数，生成发音的目标URL
        http://dict.youdao.com/dictvoice?type=0&audio=
        '''
        self._url = r'http://dict.youdao.com/dictvoice?type=' + str(
            self._type) + r'&audio=' + self._word.replace(" ", "%20")
 
    def _getWordMp3FilePath(self, word):
        '''
        获取单词的MP3本地文件路径
        如果有MP3文件，返回路径(绝对路径)
        如果没有，返回None
        '''
        word = word.lower()  # 小写
        self._word = word
        self._fileName = self._word + '.mp3'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # 判断是否存在这个MP3文件
        if os.path.exists(self._filePath):
            # 存在这个mp3
            return self._filePath
        else:
            # 不存在这个MP3，返回none
            return None

    def crawl(self,word):
        '''
        This module  crawls the Chinese translation of English words.
        Return: result
        '''
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        data = {'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false'}
        r = requests.post(url,data)
        answer = r.json()
        print(answer)
        result = answer['translateResult'][0][0]['tgt']
        return result

    def store(self,word,result):
        '''
        This module saves the Chinese translation of the word.
        :param result: the translation
        :return: nothing
        '''
        # 没有文件，创建文件先
        if not os.path.exists(self.date+'.npy'):
            np.save(self.date + '.npy',{})

        dictionary = np.load(self.date+'.npy',allow_pickle=True).item()
        if word not in dictionary:
            dic = {word:result}
            dictionary.update(dic)

        filename  = self.date + '.npy'
        np.save(filename,dictionary)
        print(dictionary)


if __name__ == "__main__":
    path = 'C:\\Users\\xiaofeiji\\Desktop\\Words'
    # files = os.listdir(path)
    files = ["2022-3-8.txt"]
    words = []
    for file in files:
        position = path + '\\' +file
        with open(position,encoding='utf-8') as f:
            for line in f:
                data = line.strip()
                # 若是空数据，跳过这次循环
                if data == '':
                    continue
                words.append(data.rstrip())
    print(words)
    sp = youdao()
    for word in words:
        sp.down(word)
        result = sp.crawl(word)
        time.sleep(2)
        sp.store(word,result)

