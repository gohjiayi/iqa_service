cd /
export PYTHONPATH=$PYTHONPATH:$PWD
export PORT=8000
echo TRYING TO RUN ON $PORT
uvicorn app.main:app --host 0.0.0.0 --port $PORT
# 8000 

# Without Docker,
# uvicorn app.main:app --host 127.0.0.1 --port 8000 
# ^default host and port https://www.uvicorn.org/#command-line-options
# A socket is identified using the IP address of the network node, and the port number within the network node.
# We nust bind (assign) a socket to a host and port, in order for that socket to accept connections. 
# For the uvicorn server socket, 
# --host is the ip address of the node in the network (i.e. the uvicorn server in our localhost) 
# that clients can connect to to access the the uvicorn server - i.e. the server socket is bound to that host ip
# --port is the port number of that^ socket that clients can connect to
# In this case we can use our browser to go to 127.0.0.1:8000 (i.e. localhost:8000).

# But now, with Docker, 
# 127.0.0.1 almost always means “this container” that runs the server, not “this machine”, e.g. If you make
# an outbound connection to 127.0.0.1 from a container, it will return to the same container.
# The default allowed host for uvicorn (and other servers like gunicorn, live-server, etc) is 127.0.0.1 which means 
# it can only be accessed from the docker container itself. 
# But when we change it to 0.0.0.0, it means everyone can access it. 
# from https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/44
# You must set a container’s main process to bind to the special 0.0.0.0 “all interfaces” address, or 
# it will be unreachable from outside the container.
# from https://stackoverflow.com/questions/59179831/docker-app-server-ip-address-127-0-0-1-difference-of-0-0-0-0-ip