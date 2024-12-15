# Use Python 3.13.1 as the base image
FROM python:3.13.1-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for OpenCV and video device support
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenCV
RUN pip install opencv-python

# Expose video devices as a volume
VOLUME ["/dev/video0"]

# Set environment variables for video device and display
ENV DISPLAY=:0
ENV OPENCV_IO_MAX_IMAGE_PIXELS=2**64

# Entrypoint script to handle device permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run your application
CMD ["python", "your_script.py"]
