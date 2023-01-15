# Use an official PyTorch runtime as a parent image
FROM registry.baidubce.com/paddlepaddle/paddle:2.4.1

# Set the working directory
WORKDIR /docker_detection

# Copy the current directory contents into the container
COPY . /docker_detection

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run when the container launches
CMD ["python", "ppyoloe_models.py"]
