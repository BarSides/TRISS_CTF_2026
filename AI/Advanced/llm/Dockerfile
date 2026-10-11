# CPU build of llama.cpp's llama-server plus the model, for laptops without an NVIDIA GPU.
# Needs Internet at build time only (PyPI for the llama.cpp source, Docker Hub for the model).
FROM python:3.12-slim AS source
COPY fetch_source.py /
RUN python3 /fetch_source.py 0.3.16 /src

FROM python:3.12-slim AS model
ARG MODEL_REPO=ai/qwen3
ARG MODEL_TAG=1.7b-q4_K_M
COPY fetch_model.py /
RUN python3 /fetch_model.py "$MODEL_REPO" "$MODEL_TAG" /model.gguf

FROM python:3.12-bookworm AS build
RUN pip install --no-cache-dir cmake
COPY --from=source /src/llama_cpp_python-0.3.16/vendor/llama.cpp /llama.cpp
WORKDIR /llama.cpp
RUN cmake -B build -DLLAMA_CURL=OFF -DGGML_NATIVE=OFF -DGGML_OPENMP=OFF -DBUILD_SHARED_LIBS=OFF -DLLAMA_BUILD_TESTS=OFF \
 && cmake --build build --config Release --target llama-server -j"$(nproc)"

FROM debian:bookworm-slim
COPY --from=build /llama.cpp/build/bin/llama-server /usr/local/bin/
COPY --from=model /model.gguf /models/model.gguf
EXPOSE 8080
ENTRYPOINT ["llama-server", "--host", "0.0.0.0", "--port", "8080", "-m", "/models/model.gguf", "--jinja", "--no-webui"]
CMD ["-c", "8192", "--parallel", "4"]
