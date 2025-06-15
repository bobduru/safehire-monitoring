FROM python:3.10

WORKDIR /src

# Clone the repository
RUN git clone https://github.com/bobduru/safehire-monitoring.git .


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 

CMD ["python", "api.py"]