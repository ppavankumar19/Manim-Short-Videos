import json, sys, urllib.parse, urllib.request, pathlib
UA = {"User-Agent": "Mozilla/5.0 (manim-edu-resource-fetch)"}
def api(q):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))
def info(title):
    d = api({"action":"query","titles":title,"prop":"imageinfo","iiprop":"url|size|extmetadata|mime","format":"json"})
    p = next(iter(d["query"]["pages"].values()))
    ii = p.get("imageinfo", [{}])[0]
    m = ii.get("extmetadata", {})
    return ii.get("url"), ii.get("mime"), ii.get("size"), m.get("LicenseShortName",{}).get("value"), m.get("Artist",{}).get("value","")[:80]
for t in sys.argv[1:]:
    try:
        print(t, "|", info(t))
    except Exception as e:
        print(t, "ERR", e)
