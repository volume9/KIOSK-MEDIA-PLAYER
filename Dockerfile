FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy toàn bộ file code vào container
COPY . /app

# Cài đặt thư viện
RUN pip install --no-cache-dir flask werkzeug

# Cấp quyền thực thi cho file khởi động
RUN chmod a+x run.sh

# Chạy ứng dụng
CMD [ "/app/run.sh" ]