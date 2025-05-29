# 构建 enclave 镜像
docker build -t enclave-test -f Dockerfile.enclave .

# 创建 eif 文件
nitro-cli build-enclave --docker-uri enclave-test:latest --output-file enclave.eif

# 运行 enclave
nitro-cli run-enclave --eif-path enclave.eif --cpu-count 2 --memory 512 --debug-mode

# 获取 enclave CID
nitro-cli describe-enclaves

# 在父实例运行测试代码
python3 parent.py

