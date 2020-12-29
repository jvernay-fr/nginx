# nginx compilation script

The nginx configuration expects that all the `server { ... }` are inside an external configuration file.
By default, it is `/home/<current_user>/servers/servers.conf`.
You can modify the `actual_conf_location` variable inside `build.py` to modify the location.
(or directly in `/nginx-root/conf/nginx.conf` after compilation)

Then, to compile nginx, execute `python3 build.py` from this directory.
Then, execute `./nginx` to start nginx server.

The directory structure is the following (after `build.py` is executed):
```
- build.py      # script file to configure and compile nginx
- nginx         # nginx executable
- archives/     # contains archives of the sources of nginx and its dependencies
- src/          # source files and compilation result
- nginx-root/   # where nginx is installed after compilation
```
