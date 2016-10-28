import sys
import getopt
import time
import json
import requests

def get_data(api_key, lat, lon):
    query_url = "https://api.darksky.net/forecast/"
    url = query_url + api_key + "/"
    url = url + lat + "," + lon

    req = requests.get(url.encode("utf-8"))
    try:
        req.raise_for_status()
    except HTTPError as e:
        print e
        print("ERR: %s (%f,%f)" % (url, lat, lon))
        sys.exit(1)

    req_json = req.json()
    req.close()

    return req_json

def process_data(req_json):
    hourly = req_json["hourly"]

    now = time.time(); # Time in seconds since epoch
    now_idx = 0
    print("now: %f" % (now))
    for d in hourly["data"]:
        print("\t%d" % (d["time"]))
        if d["time"] < now:
            now_idx = now_idx + 1

    print("We are now in time block %d" % (now_idx))


def usage(name):
    print("python %s -x lat -y lon -k api_key" % (name))
    print("python %s -f sample_data" % (name))

def load_data(filename):
    f = open(filename, 'r')
    data = json.loads(f.read())
    f.close()

    return data

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hx:y:f:k:')
    except getopt.GetoptError as e:
        print(str(e))
        usage(sys.argv[0])
        sys.exit(-1)

    api_key = None;
    lat = None
    lon = None
    json_data = None
    for o, a in opts:
        if o == "-h":
            usage()
            sys.exit()
        elif o == "-x":
            lat = a
        elif o == "-y":
            lon = a
        elif o == "-f":
            json_data = load_data(a)
        elif o == "-k":
            api_key = a;

    if json_data is None:
        if lat is None or lon is None or api_key is None:
            usage(sys.argv[0])
            sys.exit(-1)
        json_data = get_data(api_key, lat, lon);

        with open('/tmp/weather_data.json', 'w') as outfile:
            json.dump(json_data, outfile);
            outfile.close()

    process_data(json_data);
