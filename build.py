import tarfile
import shutil
import os
import subprocess
import getpass
from pathlib import Path

current_user = getpass.getuser()
actual_conf_location = f"/home/{current_user}/servers/servers.conf"

# this will be used as nginx configuration
NGINX_CONF = f"""
user {current_user}; # even if nginx is run as root, created files are still writable for the current user.

events {{
    worker_connections 1024;
}}

http {{
    include mime.types;
    default_type application/octet-stream;
    
    include {actual_conf_location} ;
}}
"""

# do cleanup
for p in [ "nginx", "nginx-root", "src" ]:
    path = Path(p)
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

for d in [ "nginx-root", "src" ]:
    Path(d).mkdir()

# untar sources
for archive_path in Path("archives").glob("*.tar.gz"):
    archive = tarfile.open(archive_path, "r") # read mode
    archive.extractall("src") # creates the directory "src/mylib-1.2.3"
    archive.close()
    dir_path = "src/" + archive_path.name.removesuffix(".tar.gz") # where the archive was extracted
    dir_dst = dir_path.split("-")[0] # removing "-1.2.3"
    Path(dir_path).rename(dir_dst)
# at the end, we have extracted archives/*-1.2.3.tar.gz to src/*

def absolute_path(path_str):
    return str(Path(path_str).resolve())

os.chdir("src/nginx")

# configuring nginx, cf. http://nginx.org/en/docs/configure.html
subprocess.run(["sh", "./configure",
    "--prefix=" + absolute_path("../../nginx-root"),
    "--sbin-path=" + absolute_path("../../nginx"),
    "--with-pcre=" + absolute_path("../pcre"),
    "--with-zlib=" + absolute_path("../zlib"),
    "--with-http_ssl_module",
    "--with-http_addition_module",
])

# building nginx
subprocess.run(["make", "install"])

os.chdir("../..")

# overwrite configuration (optional step)
with open("nginx-root/conf/nginx.conf", "w") as conf_file:
    conf_file.write(NGINX_CONF)
    

