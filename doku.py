import sys
import os
from dokuwiki import DokuWiki, DokuWikiError

try:
    wiki = DokuWiki( "http://10.148.38.142/wiki/lib/exe/xmlrpc.php", "rpcxml", "lmxcpr")
except DokuWikiError as err:
    print(err)
    sys.exit(1)

print(wiki.version)
domain='infinidat:'
outpdir='C:/wiki/'

def pagedetect(pagename):
    '''return true if page presents in wiki (also checks for  upper or lower case)'''
    syslist = []
    pagenames = []
    pagenames.append(pagename.upper())
    pagenames.append(pagename.lower())
    pagelist = (wiki.pages.list(domain))  # list all pages in the given namespace

    for page in pagelist:
        sysn = page.get('id')
        sysn = sysn.replace(domain, "")
        syslist.append(sysn)

    return bool(set(pagenames).intersection(syslist))



def wikiappend(pname, content):
    if pagedetect(pname)== False:
        pname="{}:{}".format(domain,pname)
        wiki.pages.append(pname,content)
        print('Page created successfully')
    else:
        print('Page already created, please check')

wikiappend("iboxtst","test")




def savepage(pagename):
        if pagedetect(pagename):
            cont=wiki.pages.html("{}:{}".format(domain,pagename))
            print('Contents of ', pagename)
            #print(wiki.pages.get("{}:{}".format(domain,req))) # print the content of the page
            print(cont)
            outp= open((os.path.join(outpdir,pagename+'.html')), 'w')
            outp.write(cont)
            outp.close()
        else:
            print("Page {} not found".format(pagename))

#savepage("ibox1903")

def wikisearch(cond):
    condlist=[]
    result = []
    condlist.append(cond.upper())
    condlist.append(cond.lower())

    for c in condlist:
        r=wiki.pages.search(c)
        if len(r):
            result.append(r)

    return result

#print(wikisearch('j11dlt4'))

