FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements from admin_dashboard
COPY admin_dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Change to admin_dashboard directory
WORKDIR /app/admin_dashboard

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]