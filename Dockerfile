FROM arm64v8/gcc:latest
RUN apt-get update && apt-get install -y \
    cmake \
    libgtest-dev \
    python3 \
    python3-pip \
    python3-venv \
    python3.11-dev \
    libc6-dev \
    libffi-dev
RUN cd /usr/src/gtest && cmake . && make && cp lib/*.a /usr/lib/
WORKDIR /app
COPY . .
# ?terge orice mediu virtual existent
RUN rm -rf /app/venv
RUN python3 -m venv /app/venv
RUN /app/venv/bin/python -m ensurepip --upgrade
RUN /app/venv/bin/python -m pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt
# Corecteaza shebang-ul pentru toate scripturile din venv/bin
RUN find /app/venv/bin -type f -exec sed -i 's|#!/.*python.*|#!/app/venv/bin/python|' {} \;
# Verifica shebang-ul pentru pytest
RUN head -n 1 /app/venv/bin/pytest
ENV PATH="/app/venv/bin:$PATH"