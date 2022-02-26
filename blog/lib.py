import requests
import MeCab
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

# def get_text_from_url(url):
#     req  = requests.get(url)
#     con = req.content
#     soup = BeautifulSoup(con, 'html.parser')
#     p_all = soup.find_all('p')
#     tmp = []
#     for p in p_all:
#         tmp.append(p.text)
#     t = ''.join(tmp)
#     return t

def get_nouns_from_text(text):
    m = MeCab.Tagger().parse(text)
    nouns = ''
    for n in m.split('\n'):
        t = n.split('\t')
        for u in t:
            if '名詞' in u:
                nouns = nouns + ' ' + t[0]
    return nouns

# def get_nouns_from_url(url):
#     text = get_text_from_url(url)
#     nouns = get_nouns_from_text(text)
#     return nouns

# def  get_nouns_list_from_urls(urls):
#     nouns_list = []
#     for url in urls:
#         nouns = get_nouns_from_url(url)
#         nouns_list.append(nouns)
#     return np.array(nouns_list)

def get_nouns_list_from_posts(posts):
    nouns_list = []
    for post in posts:
        nouns = get_nouns_from_text(post.text)
        nouns_list.append(nouns)
    return np.array(nouns_list)

def calc_tfidf(docs):
    vectorizer = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
    X = vectorizer.fit_transform(docs)
    tfid_vecs = X.toarray()
    return  tfid_vecs

def calc_cosine_similarity(vecs):
    length = len(vecs) 
    cosine_similarity_matrix = np.zeros((length, length))
    for i in range(length - 1):
        for j in range(i + 1, length):
            cosine_similarity = np.dot(vecs[i], vecs[j]) / (np.linalg.norm(vecs[i]) * np.linalg.norm(vecs[j])) 
            cosine_similarity_matrix[i][j] = cosine_similarity
            cosine_similarity_matrix[j][i] = cosine_similarity
    return cosine_similarity_matrix

def calc_cosine_similarity_from_tfidf(docs):
    tfidf_vecs = calc_tfidf(docs)
    cosine_similarity_matrix = calc_cosine_similarity(tfidf_vecs)
    return cosine_similarity_matrix

# def get_cosine_similarity_from_urls(urls):
#     nouns_list = get_nouns_list_from_urls(urls)
#     cosine_similarity_matrix = calc_cosine_similarity_from_tfidf(nouns_list)
#     return cosine_similarity_matrix

def get_cosine_similarity_from_posts(posts):    
    nouns_list = get_nouns_list_from_posts(posts)
    cosine_similarity_matrix = calc_cosine_similarity_from_tfidf(nouns_list)
    return cosine_similarity_matrix

# def get_title_list_from_urls(urls):
#     title_list = []
#     for url in urls:
#         req  = requests.get(url)
#         con = req.content
#         soup = BeautifulSoup(con, 'html.parser')
#         title = soup.find('a', {'class': 'article-title'})
#         title_list.append(title.text)
#     return title_list

def get_pk_list_from_posts(posts):
    pk_list = []
    for post in posts:
        pk = post.pk
        pk_list.append(pk)
    return pk_list

def get_cosine_similarity_with_pk(cosine_similarity_matrix, pk_list):
    dic= {}
    idx = len(pk_list)
    for i in range(idx):
        dic[pk_list[i]] = {}
        for j in range(idx):
            if pk_list[i] == pk_list[j]:
                pass
            else:
                dic[pk_list[i]][pk_list[j]] = cosine_similarity_matrix[i][j]
        dic[pk_list[i]] = sorted(dic[pk_list[i]].items(), key=lambda x:x[1], reverse=True)
    return dic

# def get_cosine_similarity_with_title_from_urls(urls):
#     title_list = get_title_list_from_urls(urls)
#     cosine_similarity_matrix = get_cosine_similarity_from_urls(urls)
#     cosine_similarity_with_title = get_cosine_similarity_with_title(cosine_similarity_matrix, title_list)
#     return cosine_similarity_with_title

def get_cosine_similarity_with_pk_from_posts(posts):
    pk_list = get_pk_list_from_posts(posts)
    cosine_similarity_matrix = get_cosine_similarity_from_posts(posts)
    cosine_similarity_with_pk = get_cosine_similarity_with_pk(cosine_similarity_matrix, pk_list)
    return cosine_similarity_with_pk
    