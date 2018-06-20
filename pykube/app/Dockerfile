FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY service.yaml ./
COPY statefulset.yaml ./
COPY kubecalls.py ./
CMD [ "python", "./kubecalls.py" ]
