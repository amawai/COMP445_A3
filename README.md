# COMP445_A3
*UDP-ifying httpc and httpfs library*

### Testing the Client
**Router Terminal:**
1. Go to your OS relevant router folder `cd /path/to/router/[mac|linux]/router`
2. Run `./router_x64 --port=3000 --drop-rate=0 --max-delay=10ms --seed=1`

**Server Terminal:**
1. `cd /path/to/COMP445_A3/provided_python/`
2. Run `python udp_server.py --port 8007`

**Client Terminal:**
1. `cd /path/to/COMP445_A3/src/`
2. Run `python httpc.py get http://httpbin.org/status/418`
3. Check out the terminal for packets that have been sent
