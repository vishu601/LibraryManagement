# 1. Base Python image use karenge
FROM python:3.12-slim

# 2. Server ke andar ka working directory set karo
WORKDIR /app

# 3. Python files ko buffering se rokne ke liye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Sirf Django install karne ke liye commands run karenge
RUN pip install --no-cache-dir django==6.0.7

# 5. Apne local pc ka saara code container ke andar copy karo
COPY . /app/

# 6. Django server ko background me chalane ke liye port expose karo
EXPOSE 8000

# 7. Server start karne ka command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
