import csv
import re
import pdb
import requests
from bs4 import BeautifulSoup

from config import *


def getGiteeData(pkg, pUrl):
    # todo: show specific branch status not only newest commit
    # get git source data, copied from src-oe-verinfo
    print(pUrl)
    service_url = pUrl.replace("project/monitor", "source").rpartition("?")[2] + '/{}/_service'.format(pkg)
    service_resp = requests.get(service_url)
    # service_resp = requests.get(service_url, auth=HTTPBasicAuth(account['user'], account['password']))
    service_data = service_resp.text
    # print ('service_data', service_data)
    git_pattern = 'com:.*git'
    revision_pattern = '[0-9a-f]{40}'
    try:
        gitinfo = re.search(git_pattern, service_data).group()
        revision = re.search(revision_pattern, service_data).group()
        # print (gitinfo)
        # print (revision)
        gitinfo = re.search('>.*<', gitinfo).group()[1:-1]
        revision = re.search('>.*<', revision).group()[1:-1]
        if len(revision) == 0:
            revision = 'None'
        # print ('revision', revision)
    except:
        gitinfo = 'None'
        revision = 'None'
        print('failed to get url and revision')
    # process gitinfo
    gitinfo = gitinfo[14:-4]
    print('git', gitinfo)


def getGiteeStat():
    # todo: get gitee pkg lists
    # query pkg which do not have yaml
    # get upstream pkg commit, compare
    # get fork pkg list
    
def getProjStat():
    # todo: auto get branched packages status
    noYamlList = []
    repoList = []  # csv header
    pkgRepoDict = {}  # pkg: repo: status
    for repo in projRepoUrl:  # project is the set of pkgs, repos is set of systems
        proj = projRepoUrl[repo][projRepoUrl[repo].rfind("/")+1:]
        print(projRepoUrl[repo])
        html = requests.get(projRepoUrl[repo]).text
        b = BeautifulSoup(html, "html.parser").table.tbody
        _arch = dict(eval(b["data-tableinfo"]))[repo]  # b.attrs["data-tableinfo"]
        repoList.append(repo)
        pkgStats = eval(b["data-statushash"])[repo][_arch]
        for pkg in pkgStats:
            print(pkg)
            # getGiteeData(j, projRepoUrl[i])
            if pkg not in pkgRepoDict:
                pkgRepoDict[pkg] = {proj + repo: pkgStats[pkg]["code"]}  # {pkgName: buildStat}
            else:
                pkgRepoDict[pkg].update({proj + repo: pkgStats[pkg]["code"]})
            # query package project have .yaml file
            # if projRepoUrl[repo].find
            url = projRepoUrl[repo].replace("project", "package").replace("monitor", "show") + f"/{pkg}"
            e = None
            try:
                b = BeautifulSoup(requests.get(url).text, "html.parser").table.tbody
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
    return pkgRepoDict, repoList


def main():
    pkg, repoList = getProjStat()
    with open(csvName, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([""] + repoList)
        for pname in pkg:
            l = [pname]
            for repo in repoList:
                if repo not in pkg[pname]:
                    l += [""]
                else:
                    l += [pkg[pname][repo]]
            writer.writerow(l)


if __name__ == '__main__':
    main()
