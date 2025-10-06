FROM registry.scontain.com/sconecuratedimages/experimental/minio:master-alpine3.21-5.9.0-831-g2f59cb75a AS base

COPY ./files/minio_server.sh /minio_server.sh
COPY ./files/make_binary-fs.demo.sh /make_binary-fs.demo.sh
COPY ./files/make_fspf.demo.sh /make_fspf.demo.sh

RUN set -eux; \
    chmod +x /minio_server.sh /make_binary-fs.demo.sh /make_fspf.demo.sh


###
# embedded binary-fs preparation
RUN set -eux; \
    /make_binary-fs.demo.sh; \
    /make_fspf.demo.sh
#
###


###
# compile binary-fs for later use with SCONE_EXTENSIONS_PATH if necessary
FROM registry.scontain.com/scone.cloud/crosscompilers:5.9.0-rc.7 AS crosscompiler

COPY --from=base /binary_fs_blob.s /.
COPY --from=base /binary_fs.blob /.
COPY --from=base /libbinary_fs_template.a /.

RUN set -eux; \
    scone gcc ./binary_fs_blob.s ./libbinary_fs_template.a -shared -o /libbinary-fs.so && \
    ls -l /libbinary-fs.so
#
###


###
# final stage
FROM base AS base2

COPY --from=crosscompiler /libbinary-fs.so /lib/libbinary-fs.so
ENV _SCONE_EXTENSIONS_PATH=/lib/libbinary-fs.so

RUN set -eux; \
    ls -l /lib/libbinary-fs.so; \
    rm -v /binary_fs_blob.s \
          /binary_fs.blob \
          /libbinary_fs_template.a \
          /files.txt \
          files.txt.formatted \
          make_binary-fs.demo.sh \
          make_fspf.demo.sh \
          script; \
    rm -rf /opt/scone/bin
