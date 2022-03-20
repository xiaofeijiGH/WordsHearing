import os
from pydub import AudioSegment
import time



class Assemble:
    def __init__(self,date=None):
        '''
        初始化函数，完成参数变量的初始化
        :return:
        '''
        self.music_path = '.\\Speech_US'

        self.music_name = []
        self.voidMusicTime = 3 * 1000  # 3秒
        self.voidMusic = 'voidMusic.mp3'

        # 先制造3秒的空白片段
        if not os.path.exists('void_3_seconds'):
            self.segment_three_seconds()
        # 考虑输入的单词本名存在以前的日期
        if date == None:
            self.date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        else:
            self.date = date
        self.joinMusic()
        self.store()

    def geturl(self):
        '''
        得到单词音频的路径，并返回
        :return:
        '''
        self.music_path = self.music_path + '\\' +self.date
        print("self.music_path is {}".format(self.music_path))

        if os.path.exists(self.music_path):
            self.music_name = os.listdir(self.music_path)
        else:
            raise Exception('The path doesn`t exist')

        self.music_name = [self.music_path+'\\'+i for i in self.music_name]

    def joinMusic(self):
        '''
        对单词音频进行拼接，每两个单词之间添加一个2秒的空白段void(2).mp3
        :return:
        '''
        # 避免程序运行时，毫无显示。每完成一个单词音频添加，打印出来完成程度
        current_nums = 0

        self.jointMusic = AudioSegment.from_mp3(self.voidMusic)
        void = AudioSegment.from_mp3(self.voidMusic)
        if self.music_name == []:
            self.geturl()

        total_nums = len(self.music_name)
        for path in self.music_name:
            word_music = AudioSegment.from_mp3(path)
            # 单词音频中，每个单词读三遍
            self.jointMusic = self.jointMusic + word_music + void + word_music + void + word_music + void
            current_nums += 1
            print('The current_num is {}, there are {} words to left.'.format(current_nums,total_nums-current_nums))

    def store(self):
        '''
        存储最终拼接好的单词音频，存储到hearing文件夹下
        :return:
        '''
        path = os.getcwd() + '\\hearing'
        if os.path.exists(path):
            self.jointMusic.export(path+'\\'+self.date + '.mp3' ,format='mp3')
        else:
            os.mkdir(path)
            self.jointMusic.export(path+'\\'+self.date + '.mp3',format='mp3')
        print('Succeed to store!')

    def convert_mp3_to_wav(self):
        '''
        由于我的pydub库中AudioSegment.from_mp3()方法出了问题，并且这应该是内部库文件的接口问题。但导入wav格式文件没问题
        所以首先利用ffmpeg批量转换下载下来的音频文件格式，再进行拼接。

        后续：莫名其妙可以成功导入mp3文件了
        :return:
        '''
        pass

    def segment_three_seconds(self):
        '''
        我这里下载的是一个3分多的空白音频文件，但我只需要3秒，所以切割一部分出来
        :return:
        '''
        voidMusic = AudioSegment.from_mp3('void.mp3')[:self.voidMusicTime]
        voidMusic.export(self.voidMusic,format='mp3')

if __name__ =='__main__':

    assemble = Assemble()




