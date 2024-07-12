# oauth_demo_app
Demo app to experience OAuth2.0

git clone https://github.com/iamkdada/oauth_demo_app.git
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt

uvicorn src.main:app --reload

http://127.0.0.1:8000/users/
http://127.0.0.1:8000/users/1