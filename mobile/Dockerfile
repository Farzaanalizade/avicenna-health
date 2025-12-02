FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    unzip \
    openjdk-11-jdk \
    android-sdk \
    && rm -rf /var/lib/apt/lists/*

# Download Flutter SDK
RUN git clone https://github.com/flutter/flutter.git -b stable /opt/flutter

# Add Flutter to PATH
ENV PATH="/opt/flutter/bin:/opt/flutter/bin/cache/dart-sdk/bin:$PATH"

# Run flutter doctor
RUN flutter doctor

# Accept Android licenses
RUN yes | flutter doctor --android-licenses

# Set working directory
WORKDIR /app

# Copy project
COPY . /app

# Build APK
RUN flutter clean && \
    flutter pub get && \
    flutter build apk --release

# Expose APK
CMD ["sh", "-c", "cp build/app/outputs/flutter-apk/app-release.apk /output/avicenna-health.apk && echo 'APK ready at /output/avicenna-health.apk'"]
