FROM postgres
ENV POSTGRES_PASSWORD=de_test
RUN mkdir /app
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]