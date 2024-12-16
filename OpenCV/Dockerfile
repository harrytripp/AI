# Use Python 3.13.1 as the base image
FROM python:3.13.1-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for OpenCV and video device support
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-opencv \
        ffmpeg \
        libsm6 \
        libxext6 \
        libgl1-mesa-glx \
        libglib2.0-0 \
        v4l-utils \
        libgtk2.0-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install OpenCV using the headless version
RUN pip install opencv-contrib-python

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose video devices as a volume
VOLUME ["/dev/video0"]

# Set environment variables for video device and display
ENV DISPLAY=:0
# ENV OPENCV_IO_MAX_IMAGE_PIXELS=2**64

# Entrypoint script to handle device permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Create directories for input and output images
RUN mkdir -p /app/images /app/imageOutput

# Copy images into the container: copies the 'images' directory and its contents
COPY scripts/images/ /app/images

# Default command to run your application
CMD ["python", "scripts/readWrite.py"]
