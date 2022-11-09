import requests, csv

def main():    
    pkgs = []
    with open("noyaml.csv", "r", newline="") as f:
        for i in csv.reader(f):
            if i[1] != "":
                pkgs.append(i[0])
    for pkg in pkgs:
        u = f"https://gitee.com/openeuler-risc-v/{pkg}/blob/master/{pkg}.spec"
        u = requests.get(u).text
        p = u.find("github.com");  # len = 10
        src = u[p + 11 : u.find("&#x000A;", p + 1)]
        if len(src) > 45: print(src); break;
        u = f"https://gitee.com/openeuler-risc-v/{pkg}/new/master"
        data = form; data["file_name"] = pkg; data["file_path"] = pkg;
        data["commit_message_header"] = f"add {pkg}."; data["content"].replace("{}", pkg)
        print(pkg, src)
##        u = requests.post(u, headers=headers, data=data, cookies=cookies)
        print(u)
        
main()      
