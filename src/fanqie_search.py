# 导入必要的模块
import requests

# 定义搜索番茄小说的函数
def fanqie_s(key):
    # 获取搜索结果列表
    response=requests.get(f'https://fanqienovel.com/api/author/search/search_book/v1?filter=127,127,127,127&page_count=10&page_index=0&query_type=0&query_word={key}').json()
    book_list=response['data']['search_book_data_list']

    # 打印搜索结果
    for i,j in zip(book_list,range(len(book_list))):
        print('\n'+str(j+1)+'.'+i['book_name']+'  '+i['author']+'\n'+i['category'])
    
    # 选择
    num = input('请输入选项：')
    print('\n')


    return book_list[int(num)-1]['book_id']