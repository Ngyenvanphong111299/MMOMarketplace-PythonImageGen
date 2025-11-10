#!/bin/bash
# Wrapper script cho Chromium với các flags cần thiết cho Docker
exec /usr/bin/chromium --no-sandbox --disable-dev-shm-usage --disable-gpu "$@"

