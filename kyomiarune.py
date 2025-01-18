# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# 作ったものの微妙だった機能 ↓

# def kyomiarunelist ():
#     # 認証ヘッダーとリクエストのパラメーター
#     headersValue = {"Authorization": os.getenv('API_KEY')}
#     paramsValue = {
#     'per_page': 50,
#     'fields': 'title,media,status.kind'
#     }

#     url = "https://api.annict.com/v1/me/works"
#     allData = []  # データをリセット
#     resultList = []  # 結果のリセット
#     page = 1  # ページ数の初期化

#     while True:
#         paramsValue['page'] = page  # ページ数のセット
#         result = requests.get(url, headers=headersValue, params=paramsValue)
        
#         if result.status_code == 200:
#             data = result.json()
#             if 'works' not in data or not data['works']:  # 空のデータの処理
#                 break
#             allData.extend(data['works'])
            
#             # 次のページがない場合終了
#             if len(data['works']) < paramsValue['per_page']:
#                 break
            
#             page += 1  # 次のページに進む
            
#         else:
#             print(f"エラー: {result.status_code}")
#             print(result.json())
#             break

#     for work in allData:
#         if work.get('media') == 'tv' and work.get('status', {}).get('kind') == 'wanna_watch':  # TV番組のみフィルタ
#             resultList.append(work.get('title'))
        
#     return resultList

# def kyomiaruneId(name):
#      # 認証ヘッダーとリクエストのパラメーター
#     headersValue = {"Authorization": os.getenv('API_KEY')}
#     paramsValue = {
#     'fields': 'id'
#     }

#     url = f"https://api.annict.com/v1/works?filter_title={name}"
    
#     result = requests.get(url, headers=headersValue, params=paramsValue)
        
#     if result.status_code == 200:
#         data = result.json()
#         print(data["works"][0]["id"])
#     else:
#         print(f"IDのエラー: {result.status_code}")
#         print(result.json())
                    
#     return data["works"][0]["id"]
    
# def kyomiaruneadd (work_id):
#     # 認証ヘッダーとリクエストのパラメーター
#     headersValue = {"Authorization": os.getenv('API_KEY')}
#     paramsValue = {
#     'work_id': f'{work_id}',
#     'kind': 'wanna_watch'
#     }
#     url = "https://api.annict.com/v1/me/statuses"
    
#     result = requests.post(url, headers=headersValue, params=paramsValue)
#     print(result)
    
#     if result.status_code == 204:
#         print("登録成功")
#         return True
#     else:
#         print(f"登録のエラー: {result.status_code}")
#         print(result.json())  
#         return False
    
# def kyomiarunedelete (work_id):
#     # 認証ヘッダーとリクエストのパラメーター
#     headersValue = {"Authorization": os.getenv('API_KEY')}
#     paramsValue = {
#     'work_id': f'{work_id}',
#     'kind': 'no_select'
#     }
#     url = "https://api.annict.com/v1/me/statuses"
    
#     result = requests.post(url, headers=headersValue, params=paramsValue)
#     print(result)
    
#     if result.status_code == 204:
#         print("削除成功")
#         return True
#     else:
#         print(f"削除のエラー: {result.status_code}")
#         print(result.json())  
#         return False
