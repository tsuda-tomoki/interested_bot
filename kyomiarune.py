import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 認証ヘッダーとリクエストのパラメーター
headersValue = {"Authorization": os.getenv('API_KEY')}
paramsValue = {
    'per_page': 50,
    'fields': 'title,media'
}

def kyomiarunelist ():
    url = f"https://api.annict.com/v1/me/works"
    allData = []  # データをリセット
    resultList = []  # 結果のリセット
    page = 1  # ページ数の初期化

    while True:
        paramsValue['page'] = page  # ページ数のセット
        result = requests.get(url, headers=headersValue, params=paramsValue)
        
        if result.status_code == 200:
            data = result.json()
            if 'works' not in data or not data['works']:  # 空のデータの処理
                break
            allData.extend(data['works'])
            
            # 次のページがない場合終了
            if len(data['works']) < paramsValue['per_page']:
                break
            
            page += 1  # 次のページに進む
            
        else:
            print(f"エラー: {result.status_code}")
            break

    for work in allData:
        if work.get('media') == 'tv':  # TV番組のみフィルタ
            resultList.append(work.get('title'))
        
    return resultList
    
def kyomiaruneadd ():
    print("test")

