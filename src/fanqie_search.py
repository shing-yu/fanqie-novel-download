# 导入必要的模块
import requests

# 定义搜索番茄小说的函数
def fanqie_s(key):
    response=requests.get(f'https://fanqienovel.com/api/author/search/search_book/v1?filter=127,127,127,127&page_count=10&page_index=0&query_type=0&query_word={key}').json()
    book_list=response['data']['search_book_data_list']
    for i,j in zip(book_list,range(len(book_list))):
        print('\n'+str(j+1)+'.'+i['book_name']+'\n'+i['author']+'\n'+i['category'])
    num=input('序号：')
    return book_list[int(num)-1]['book_id']