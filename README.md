# Text analysis tool

# 依赖包

```cmd
pip install jieba, requests, zhconv
```



## 1. textcleanser

用于文本分析初步处理中所需要的：将list of text转化为list of word list (***str2wordlist***)

- 文本初步清理
  - 去除非中文非英文: ***keep_cn_en_num***
  - 去掉没有中文的文本: ***del_no_chinese***
  - 全角半角: ***strQ2B***
  - 繁简转化: ***f2j***
- jieba分词: ***jieba_wordcut***