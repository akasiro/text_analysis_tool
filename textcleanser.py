import jieba,requests,re, os, sqlite3, pickle
from zhconv import convert
from str_stopwords_raw import str_stopwords_raw

class textcleanser():
    '''
    用于文本分析清理数据
    Attributes:
        stopwords (list): 停用词列表
    '''
    def __init__(self, stopwords=None, add_words=None, stopword_output=None):
        '''
        Args:
            stopwords (str): 停用词文件路径，pkl格式, default None
            add_words (list): 补充的停用词， default None
            stopword_output (str): Default None, 保存停用词的路径,pkl格式
        '''
        self.stopwords = self.gen_stopword(stopwords,add_words,stopword_output)
        
    def gen_stopword(self,stopwords=None, add_words=None,output=None):
        '''
        读取停用词
        Args:
            stopwords (str): 停用词文件路径，pkl格式, default None
            add_words (list): 补充的停用词， default None
            output (str): Default None, 保存停用词的路径,pkl格式
        '''
#         path_stopwords_raw = os.path.join(PATH_TEXTCLEANSER,'str_stopwords_raw.txt')
        if stopwords is not None:
            with open(stopwords,'rb') as f:
                stopword_f = pickle.load(f)
        else:
#             with open(path_stopwords_raw, 'r') as f:
#                 stopword_f = f.read()
#                 stopword_f = stopword_f.split('\n')
            stopword_f = str_stopwords_raw.split('\n')
        if add_words is not None:
            stopword_f += add_words
        if output is not None:
            with open(output,'wb') as f:
                pickle.dump(stopword_f,f)
        return stopword_f
    
    def str2wordlist(self, value):
        '''
        对文本进行初步的处理，包括：
            1. 删除日文，将不包含中文的文本转化为np.nan
            2. 全角转半角
            3. 使用zhconv.convert将繁体转化为简体
            4. 分词去掉停用词
        Args:
            value (str): 语料
        Returns:
            (list): 词列表
        '''
        value = self.keep_cn_en_num(value)
        value = self.del_no_chinese(value)
        value = self.strQ2B(value)
        value = self.f2j(value)
        wl = self.jieba_wordcut(value)
        return wl
    def keep_cn_en_num(self,value):
        '''
        只保留英文中文和数字、
        Args:
            value (str)
        Returns:
            string
        '''
        value = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', value)
        return value
    def del_no_chinese(self,value):
        '''
        删除日文
        将不含有中文的文本转化为''
        Args:
            value (str)
        Returns:
            string
        '''
        re_words_cn = re.compile(r'[\u4e00-\u9fa5]+')
        re_words_jp=re.compile(r"[ぁ-ん]+|[ァ-ヴー]+")
        value = re.sub(re_words_jp, '', value)
        m = re.search(re_words_cn, value)
        if m == None:
            value = ''
        return value
    def strQ2B(self,ustring):
        '''
        全角转半角
        Args:
            ustring (str)
        Returns:
            string
        '''
        if ustring == '':
            return ustring
        ss = []
        for s in ustring:
            rstring = ""
            for uchar in s:
                inside_code = ord(uchar)
                if inside_code == 12288:  # 全角空格直接转换
                    inside_code = 32
                elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                    inside_code -= 65248
                rstring += chr(inside_code)
            ss.append(rstring)
            tmp = ''.join(ss)
        return tmp
    def f2j(self,value):
        '''
        繁体转简体
        '''
        if value == '':
            return value
        return convert(value, 'zh-cn')
    def jieba_wordcut(self,value):
        '''
        用jieba分词，去掉停用词
        Args:
            value (str):
        Returns:
            list
        '''
        if value == '':
            return []
        word_list = jieba.lcut(value)
        tmp = []
        for i in word_list:
            if i not in self.stopwords:
                tmp.append(i.lower())
        return tmp
if __name__ == "__main__":
    t = textcleanser()
    test_str = '基尼你奶较厚i符号i和覅就覅还放假放假就覅和覅hi放假后覅合计hi合计1jijijiihi334342341412312312432432jふぃあじfじゃい'
    print(t.str2wordlist(test_str))
