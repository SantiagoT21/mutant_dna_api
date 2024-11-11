# mutant_dna_api
A repository to save info about mutant_dna_api

Importante: tener Python3 Instalado
python -m venv venv
windows: .\venv\Scripts\activate
pip install -r requirements.txt  (pip freeze > requirements1.txt)
uvicorn app.main:app --reload

Docker:
docker build -t mutant-analyzer-api .
docker run -it -v mutant-analyzer-api-code:/var/app -p 3002:8000 mutant-analyzer-api