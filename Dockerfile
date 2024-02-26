# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./noteapp/requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Change the working directory to /code/noteapp
WORKDIR /code/noteapp

# Expose port 8000 to the outside world
EXPOSE 8000

# Specify the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
