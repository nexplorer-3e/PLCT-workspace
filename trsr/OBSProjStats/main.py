from config import *

import csv, re, requests
import lxml, cchardet  # speed up bs4
from bs4 import BeautifulSoup, SoupStrainer

def getGiteeStat():
    # todo: show specific branch status not only newest commit
    # get upstream pkg commit log, compare
    # get fork pkg list
    pkgList = {}
    url = "https://gitee.com/organizations/openeuler-risc-v/projects?page="
    pg = 1
    while True:
        b = BeautifulSoup(requests.get(url+str(pg)).text, "lxml").find_all("a", "repository")
        if len(b) == 0:
            break
        pkgList.update({x["title"]:x["href"] for x in b})
        pg += 1
    url = "https://gitee.com"
    noYamlList = []
    commitList = []
    for pkg in pkgList:
        u = url + pkgList[pkg].replace("src-openeuler", "openeuler-RISC-V")
        # query if pkg have yaml
        if NoYaml != "":
            b = BeautifulSoup(requests.get(u).text, "lxml")
            l = [pkg]
            commit = b.find("a", "repo-index-commit-msg")["href"].rpartition("/")[-1]
            if pkg+".yaml" not in b.text:
                print(f"riscv {pkg} do not have yaml file")
                l.append("no yaml")
            else: l.append("")
            noYamlList.append(l.append(u))
        # compare commit
        if CommitCsv != "":
            b = BeautifulSoup(requests.get(url+pkgList[pkg]).text, "lxml")
            commitOrig = b.find("a", "repo-index-commit-msg")["href"].rpartition("/")[-1]
            if commitOrig != commit:
                print(f"pkg {pkg} differ from upstream")
            commitList.append([pkg, commit, commitOrig])
    if NoYaml != "":
        with open(NoYaml, "w", newline="") as f:
            csv.writer(f).writerows(noYamlList)
    if CommitCsv != "":
        with open(CommitCsv, "w", newline="") as f:
            csv.writer(f).writerows(commitList)
        
        
def getProjStat():
    # todo: auto get branched packages status
    noYamlList = []
    repoList = []  # csv header
    pkgRepoDict = {}  # pkg: repo: status
    for repo in projRepoUrl:  # project is the set of pkgs, repos is set of systems
        proj = projRepoUrl[repo][projRepoUrl[repo].rfind("/")+1:]
        html = requests.get(projRepoUrl[repo]).text
        b = BeautifulSoup(html, "lxml").table.tbody
        _arch = dict(eval(b["data-tableinfo"]))[repo]  # b.attrs["data-tableinfo"]
        repoList.append(repo)
        pkgStats = eval(b["data-statushash"])[repo][_arch]
        for pkg in pkgStats:
            # getGiteeData(j, projRepoUrl[i])
            if pkg not in pkgRepoDict:
                pkgRepoDict[pkg] = {proj + repo: pkgStats[pkg]["code"]}  # {pkgName: buildStat}
            else:
                pkgRepoDict[pkg].update({proj + repo: pkgStats[pkg]["code"]})
##    return pkgRepoDict, repoList
    with open(csvName, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([""] + repoList)
        for pkg in pkgRepoDict:
            l = [pkg]
            for repo in repoList:
                if repo not in pkgRepoDict[pkg]: l.append("")
                else: l.append(pkgRepoDict[pkg][repo])
            writer.writerow(l)
"""
            # query OBS package project have .yaml file, deprecated
            url = projRepoUrl[repo].replace("project", "package").replace("monitor", "show") + f"/{pkg}"
            e = None
            try:
                b = BeautifulSoup(requests.get(url).text, "lxml").table.tbody
                if b.text.find(pkg + ".yaml") == -1:
                    print("project {} package {} does not have yaml file".format(proj, pkg))
                    noYamlList.append((proj, pkg, url))
                if b.text.find("samba") != -1:
                    with open("debug.log", "w", newline="") as f:
                        f.write(str(b.findAll("tr")))
            except Exception as e:
                print(url); print(b); print(e) 
            # pdb.break_here()
    with open("noyaml.csv", "a+", newline="") as csvf:
        csv.writer(csvf).writerow(noYamlList)
"""



def main():
    getProjStat()
    getGiteeStat()

if __name__ == '__main__':
    main()
