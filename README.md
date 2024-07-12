# oauth_demo_app
Demo app to experience OAuth2.0

## Demo Flow
1. ただ、ユーザー情報を取得する API の作成
2. API を Entra ID に登録し、アクセス トークンによって保護する (JWT の署名検証なし)
3. FrontEnd を追加し、 Entra ID の認証を行い、ユーザー情報の一覧を取得する

## Demo Flow 1
### 初期設定
1. git clone https://github.com/iamkdada/oauth_demo_app.git -b 0.0.1
2. cd backend
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirement.txt


### 動作確認
1. API 起動
   - uvicorn src.main:app --reload
2.  ブラウザアクセス
    - http://127.0.0.1:8000/users/
    - http://127.0.0.1:8000/users/1/

## Demo Flow 2

### 初期設定
1. ソースコード切り替え
   - git checkout -b 0.0.2
2. API の登録
   1. [アプリの登録] から API を登録する
   2. API の公開にて、 User.Read を追加する
   3. テナント ID、アプリケーション ID URI をクライアント ID を控えておく
3. クライアント アプリの登録
   1. [アプリの登録] からリダイレクト URL に https://jwt.ms としたクライアント アプリを登録する
   2. テナント ID、アプリケーション ID URI をクライアント ID を控えておく
   3. implicit flow を許可する

4. ソースコードの編集
   1. main.py の "application ID URI" に 1.3 のアプリケーション ID URI を入れる

### 動作確認
1. API 起動
   - uvicorn src.main:app --reload
2. ブラウザからアクセスし、エラーになることを確認
    - http://127.0.0.1:8000/users/
    - http://127.0.0.1:8000/users/1
3. 以下 URL にアクセスし、アクセス トークンを取得
    ```
    https://login.microsoftonline.com/<tenant_id>/oauth2/v2.0/authorize?
    client_id=<client_app_id>
    &response_type=token
    &redirect_uri=https://jwt.ms
    &scope=<api application id uri>/User.Read
    &response_mode=fragment
    &state=12345
    &nonce=678910
    ```
4. 以下コマンドを実施し、ユーザー情報を取得できることを確認
   - curl http://127.0.0.1:8000/users/ -H "Authorization: Bearer your_token"
   
        ```
        PowerShell

        $token = "your_access_token"
        $url = "http://127.0.0.1:8000/users/"
        $headers = @{
            "Authorization" = "Bearer $token"
        }
        ```

## Demo Flow 3
### 初期設定
1. ソースコード切り替え
   - git checkout -b 0.0.3
   - backend/src/main.py の "application ID URI" に 1.3 のアプリケーション ID URI を入れる
   - frontend/src の authConfig.js, UserTable.js を API やアプリの設定値を変更する
   - cd frontend
   - npm install

2. クライアント アプリの変更
   1. アプリの登録から、 SPA のリダイレクト URL を登録する http://localhost:3000

### 動作確認
1. アプリを起動
   - npm start
   - uvicorn src.main:app --reload
2. アプリにアクセス