nitro-cli terminate-enclave --all

rm enclave.eif 

docker build --network=host -t enclave-test -f Dockerfile.enclave.ubuntu .

nitro-cli build-enclave --docker-uri enclave-test:latest --output-file enclave.eif

nitro-cli run-enclave --eif-path enclave.eif --cpu-count 2 --memory 3000 --enclave-cid 24 --debug-mode

