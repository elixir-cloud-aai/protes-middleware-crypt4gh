# Dockerfile for athitheyag/c4gh:1.0
FROM lvarin/crypt4gh:1.6

WORKDIR /home
COPY crypt4gh_middleware/decrypt.py /home/decrypt.py