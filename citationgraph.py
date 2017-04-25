"""
Module for creating a Citation Graph from PubMed database
"""
import requests
from re import sub
from graphviz import Digraph

"""
class Article:
    def __init__(self, PMID):
        self.PMID = PMID
        self.isExploredCitedBy = False
        self.citedBy = set()
    def exploreCitedBy(self):
        #Use APIs to collect articles
        #Let's say we got a list of PMIDs
        pass

class Graph:
    def __init__(self):
        self.articles = dict()

    #this should contain as a parameter the PMID of the cited (or citing?) article
    def addArticleCiting(self, PMID):
        if PMID in self.articles:
            pass #or eventually update that article
        else:
            self.articles[PMID] = Article(PMID)
            #Eventually add infos about this article
            # eg: if this PMID was found while looking for citing article, 
"""

"""
terms = "traumatic brain injury AND (complement OR c3 OR cd55 OR mac OR c5b-9) AND (human OR mouse OR rat) AND (brain OR spinal cord)"
url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
payload = {'db': 'pubmed', 'term': terms}
payload['retmode'] = 'json'
payload['retmax'] = 1000
r = requests.get(url, params=payload)
print('URL:\t'+r.url)
r = r.json()
print('count:\t' + r['esearchresult']['count'])
print('retmax:\t' + r['esearchresult']['retmax'])
print('retstart:\t' + r['esearchresult']['retstart'])
PMIDs = set(r['esearchresult']['idlist'])
"""
PMIDs = {'26538301', '26998601'}
print(PMIDs)

dot = Digraph(comment='Citation Graph', engine='neato')
url = 'https://www.ncbi.nlm.nih.gov/pubmed'
payload = {'linkname': 'pubmed_pubmed_citedin', 'report': 'uilist'}
payload['dispmax'] = 200
payload['format'] = 'text'
counter = 0
for ID in PMIDs:
    dot.attr('node', style='filled')
    dot.node(str(ID), _attributes={'style':'filled'})
    # Eventually add label
    payload['from_uid'] = ID
    r = requests.get(url, params=payload)
    #print(r.url)
    r = r.text
    r = sub(r'<.*>\n?', '', r)
    IDsCitating = r.splitlines()
    #print("l'articolo " + ID + " ha " + str(len(IDsCitating)) + " citazioni")
    #print(IDsCitating)
    dot.attr('node', style='')
    for citer in IDsCitating:
        if citer in PMIDs:
            dot.edge(citer, ID)
            # print("Un citatore è già presente! " + citer + " -> " + ID)
        """
        else:
            dot.node(citer, _attributes={'style':''})
            dot.edge(citer, ID)
        """    
        
    counter+=1
    print("Checked {0}/{1} articles. {2}% done.".format(counter, len(PMIDs), round(counter/len(PMIDs)*100, 1)))
        
    
# print(dot.source)
dot.render('test-output/citation-graph.gv', view=True)
