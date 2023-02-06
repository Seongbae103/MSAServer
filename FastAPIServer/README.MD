pip install fastapi 'uvicorn[standard]'
pip install uvicorn
python -m uvicorn main:app --reload
또는 uvicorn main:app --reload

docker rm -f $(docker ps -aq)
docker rmi $(docker images -q)

# 목록
## app
## services
#### chatbot
#### translator
