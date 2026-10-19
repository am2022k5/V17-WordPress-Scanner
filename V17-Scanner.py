#!/usr/bin/env python3
# V17.0 PACKAGED - FINAL FINAL
import requests, re, argparse, os, datetime
requests.packages.urllib3.disable_warnings()

BANNER = """
\033[92m
██╗   ██╗ ██╗ ███████╗    ██████╗  █████╗  ██████╗██╗  ██╗ █████╗  ██████╗ ███████╗██████╗ 
██║   ██║███║╚════██║   ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝██╔══██╗
██║   ██║╚██║  ███╔═╝    ██████╔╝███████║██║     █████╔╝ ███████║██║  ███╗█████╗  ██║  ██║
╚██╗ ██╔╝ ██║██╔══╝      ██╔═══╝ ██╔══██║██║     ██╔═██╗ ██╔══██║██║   ██║██╔══╝  ██║  ██║
 ╚████╔╝  ██║███████╗    ██║     ██║  ██║╚██████╗██║  ██╗██║  ██║╚██████╔╝███████╗██████╔╝
  ╚═══╝   ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═════╝ 
\033[0m\033[93m                      V17.0 FINAL LEGEND - Built in Al Kut, Iraq\033[0m
"""

def scan(url):
    clean=url.strip().replace("https://","").replace("http://","").split("/")[0]
    d={"site":clean,"wp":False,"ver":"?","theme":"?","plugins":[],"users":[],"h":0}
    try:
        r=requests.get(f"https://{clean}",timeout=10,verify=False)
        txt=r.text
        d["wp"]=True if "wp-content" in txt.lower() else False
        m=re.search(r'WordPress ([\d.]+)',txt,re.I)
        if m: d["ver"]=m.group(1)
        m=re.search(r'/themes/([^/\'"\s]+)',txt,re.I)
        if m: d["theme"]=m.group(1)
        pls=re.findall(r'/plugins/([a-z0-9-_]+)',txt,re.I)
        d["plugins"]=list(set([p for p in pls if len(p)>2]))[:8]
        for h in ["X-Frame-Options","X-Content-Type-Options","Strict-Transport-Security","Content-Security-Policy"]:
            if h in r.headers: d["h"]+=1
        if d["wp"]:
            try:
                ru=requests.get(f"https://{clean}/wp-json/wp/v2/users",timeout=6,verify=False)
                if ru.status_code==200:
                    for u in ru.json()[:5]:
                        d["users"].append(u.get('slug'))
            except: pass
    except: pass
    return d

def main():
    print(BANNER)
    parser=argparse.ArgumentParser(description="V17 WordPress Legend Scanner")
    parser.add_argument("-t","--target", help="Single target")
    parser.add_argument("-l","--list", help="File with targets")
    parser.add_argument("-o","--output", help="Output html", default=None)
    args=parser.parse_args()
    
    targets=[]
    if args.target: targets=[args.target]
    elif args.list:
        with open(args.list) as f: targets=f.read().splitlines()
    else:
        targets=["wordpress.org","yoast.com","github.com"]
    
    results=[]
    for t in targets:
        print(f"\033[92m[SCANNING]\033[0m {t}")
        d=scan(t)
        print(f"  -> WP:{d['wp']} Ver:{d['ver']} Theme:{d['theme']} Users:{d['users']} Headers:{d['h']}/4")
        results.append(d)
    
    fname=args.output or f"V17_FINAL_{datetime.datetime.now().strftime('%H%M')}.html"
    html="<html><head><meta charset='utf-8'><title>V17</title><style>body{background:#000;color:#0f0;font-family:monospace;padding:20px}table{width:100%;border-collapse:collapse}th,td{border:1px solid #0f0;padding:8px}th{background:#111}</style></head><body><h1>V17.0 FINAL LEGEND - Al Kut</h1><table><tr><th>Site</th><th>WP</th><th>Ver</th><th>Users</th><th>Plugins</th><th>H</th></tr>"
    for r in results:
        html+=f"<tr><td>{r['site']}</td><td>{r['wp']}</td><td>{r['ver']}</td><td>{','.join(r['users'])}</td><td>{','.join(r['plugins'][:3])}</td><td>{r['h']}/4</td></tr>"
    html+="</table></body></html>"
    open(fname,'w',encoding='utf-8').write(html)
    os.system(f"cp {fname} /sdcard/Download/ 2>/dev/null")
    print(f"\n\033[92m✅ SAVED: {fname} -> /sdcard/Download/\033[0m")
    print("\033[93m🏁 Usage: python v17.py -t wordpress.org\033[0m")
    print("\033[93m🏁 Usage: python v17.py -l targets.txt -o myreport.html\033[0m")

if __name__=="__main__":
    main()
