FROM python:latest

COPY . .

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

CMD pytest /tests