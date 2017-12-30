import sys
from dokuwiki import DokuWiki, DokuWikiError
import getopt

def main(argv):
    pname = ''
    domain = ''
    helptext='crwiki.py -p <page> -d <domain:>'
    try:
        opts, args = getopt.getopt(argv, "hp:d:", [])
    except getopt.GetoptError:
        print(helptext)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helptext)
            sys.exit()
        elif opt in ("-p"):
            pname = arg
        elif opt in ("-d"):
            domain = arg
    if pname =='' or domain =='':
            print(helptext)
    else:
        wikiappend(pname, domain,'')

def crwiki():
    try:
        wiki = DokuWiki( "http://10.148.38.142/wiki/lib/exe/xmlrpc.php", "rpcxml", "lmxcpr")
    except DokuWikiError as err:
        print(err)
        sys.exit(1)
    #print(wiki.version)
    return wiki

def pagedetect(pagename,domain):
    '''return true if page presents in wiki (also checks for  upper or lower case)'''
    wiki=crwiki()
    syslist = []
    pagenames = [pagename.upper(),pagename.lower()]
    pagelist = (wiki.pages.list(domain))  # list all pages in the given namespace
    for page in pagelist:
        sysn = page.get('id')
        sysn = sysn.replace(domain, "")
        syslist.append(sysn)
    return bool(set(pagenames).intersection(syslist))

def wikiappend(pname,domain,content):
    wiki = crwiki()
    if pagedetect(pname,domain)== False:
        pname=":{}:{}".format(domain,pname)
        wiki.pages.append(pname,content)
        print('Page created successfully')
    else:
        print('Page already created, please check')


if __name__ == "__main__":
    main(sys.argv[1:])