import logging as log
import time
import os
import tarfile
from io import BytesIO


def copy_to_container(src, dest, owner, group, container):

    def create_tar_stream(file_content, file_name):
        # metadata for internal file
        tarinfo = tarfile.TarInfo(name=file_name)
        tarinfo.size = len(file_content)
        tarinfo.mtime = time.time()

        tarstream = BytesIO()
        tar = tarfile.TarFile(fileobj=tarstream, mode='w')
        tar.addfile(tarinfo, BytesIO(file_content))
        tar.close()
        tarstream.seek(0)
        return tarstream

    log.info('copying to container: %s', locals())
    dest_file = os.path.basename(dest)
    dest_dir = os.path.dirname(dest)
    file_data = open(src).read().encode('utf-8')

    tar_stream = create_tar_stream(file_content=file_data, file_name=dest_file)
    container.put_archive(path=dest_dir, data=tar_stream)
    container.exec_run('chown {0}:{1} -R {2}'.format(owner, group, dest))
