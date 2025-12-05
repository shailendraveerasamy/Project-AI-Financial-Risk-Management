# this is stable version ideal for official python image
FROM python:3.10-slim

# it will set work directory
WORKDIR /app

# easily copy requirements first (better caching)
COPY requirements.txt .

# it will install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# it will copy your project files
COPY . .

# that will expose port (FastAPI default with uvicorn)
EXPOSE 8000

# this command will run FastAPI with uvicorn
CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8000"]
