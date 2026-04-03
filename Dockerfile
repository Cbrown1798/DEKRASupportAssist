(
echo FROM python:3.11-slim
echo.
echo WORKDIR /app
echo.
echo COPY requirements.txt .
echo RUN pip install --no-cache-dir -r requirements.txt
echo.
echo COPY . .
echo.
echo EXPOSE 8080
echo.
echo CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
) > Dockerfile