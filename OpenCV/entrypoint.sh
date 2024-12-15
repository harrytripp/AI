#!/bin/bash

# Check and set video device permissions
if [ -e /dev/video0 ]; then
    # Attempt to set correct permissions for the video device
    chmod 666 /dev/video0 || true
fi

# Execute the CMD from the Dockerfile
exec "$@"
