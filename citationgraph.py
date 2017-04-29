"""Module for creating a Citation Graph from PubMed database"""
import requests
from re import sub
from graphviz import Digraph

"""
# This (incomplete) code is an implementation of the graph.
# If we just need to compile the graph, without exploring it,
# this implementation is not necessary.

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

def search(terms):
    """Function for retrieving a set of PMIDs (articles) from PubMed database, matching a search.
    terms: a string containing the expression to match"""
    url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    payload = {'db': 'pubmed', 'term': terms}
    payload['retmode'] = 'json'
    # If the search matches more than 1000 articles, we have a problem.
    payload['retmax'] = 1000
    r = requests.get(url, params=payload)
    # print('URL:\t'+r.url)
    r = r.json()
    # print('count:\t' + r['esearchresult']['count'])
    # print('retmax:\t' + r['esearchresult']['retmax'])
    # print('retstart:\t' + r['esearchresult']['retstart'])
    PMIDs = set(r['esearchresult']['idlist'])
    return PMIDs


def buildCitationGraph(PMIDs, expand=False):
    # TODO eventually check if PMIDs is iterable
    dot = Digraph(comment='Citation Graph', engine='dot')
    url = 'https://www.ncbi.nlm.nih.gov/pubmed'
    payload = {'linkname': 'pubmed_pubmed_citedin', 'report': 'uilist'}
    payload['dispmax'] = 200
    payload['format'] = 'text'
    counter = 0
    for ID in PMIDs:
        # TODO Eventually find metadata and add label
        # ...
        dot.node(str(ID), _attributes={'style': 'filled'})
        # For every article, let's find articles citing it
        payload['from_uid'] = ID
        r = requests.get(url, params=payload)
        # TODO try other formats, in order to remove headers
        r = r.text
        # Removing headers, quick & dirty
        r = sub(r'<.*>\n?', '', r)  # Remove headers tag
        IDsCitating = r.splitlines()
        # print(ID + " is cited " + str(len(IDsCitating)) + " times")
        for citer in IDsCitating:
            if citer in PMIDs:
                dot.edge(citer, ID)
                # print("Un citatore è già presente! " + citer + " -> " + ID)
            elif(expand):
                dot.node(citer, _attributes={'style': ''})
                dot.edge(citer, ID)
        counter += 1
        print("\rChecked {0}/{1} articles. {2}% done.".format(counter, len(PMIDs), round(counter/len(PMIDs)*100)), end='')
    print()
    return dot


if __name__ == '__main__':
    terms = "traumatic brain injury AND (complement OR c3 OR cd55 OR mac OR c5b-9) AND (human OR mouse OR rat) AND (brain OR spinal cord)"
    terms = "traumatic brain injury AND c5b-9"
    PMIDs = search(terms)
    # Test data
    # PMIDs = {'26538301', '26998601'}
    dot = buildCitationGraph(PMIDs)
    # print(dot.source)
    dot.render('output/citation-graph.gv', view=True)
