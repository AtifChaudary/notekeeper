# Use the official Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the Django project code into the container
COPY . .

# Expose port 8000
EXPOSE 8000


# Run the Tests
CMD python manage.py test

# Run the Django development server
CMD python manage.py runserver 0.0.0.0:8000
