# COMP445_A3
*UDP-ifying httpc and httpfs library*

## Setting Up
**Router Terminal:**
1. Go to your OS relevant router folder `cd /path/to/router/[mac|linux]/router`
2. Run `./router_x64 --port=3000 --drop-rate=0 --max-delay=10ms --seed=1`

**Server Terminal:**
1. `cd /path/to/COMP445_A3/src/`
2. Run `python httpfs.py -v --port 8000`

**Client Terminal:**
1. `cd /path/to/COMP445_A3/src/`
2. Run `python httpc.py -v -h "Accept: */*" http://localhost:8000`

## Test the Basic Functionality
### GET / : 
- All files `httpc get -v -h "Accept: */*" http://localhost:8000/`
- Specific files: `httpc get -v -h "Accept: json" http://localhost:8000/`
  
### GET /foo:
- `httpc get -v http://localhost:8000/sample_json.json`

### POST /bar:
- 201 - New File: `httpc post -v -d "A brand new file" http://localhost:8000/brandnewfile.txt`
- 200 - Write to file: `httpc post -v -d "Updating the brand new file" http://localhost:8000/brandnewfile.txt"`
- 409 - Overwrite is set to false: `httpc post -v -d "Trying to modify the brand new file without overwrite permission" -h "Overwrite: False" 
http://localhost:8000/brandnewfile.txt`
