import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.score = None
        self.dreamT = []
        self.graph = None
        self.idMap = {}


    def get_years(self):
        return DAO.get_years()

    def buildGraph(self, anno):
        self.graph = nx.DiGraph()

        allNodes = DAO.getAllNodes(anno)
        self.graph.add_nodes_from(allNodes)
        for n in allNodes:
            self.idMap[n.driverId] = n

        self.getArchi1(anno)

    def getArchi1(self, anno):
        listaRis = DAO.getArchi1(anno)
        for r1 in listaRis:
            for r2 in listaRis:
                if r1[1] == r2[1] and r1[2] < r2[2]:
                    if self.graph.has_edge(self.idMap[r1[0]], self.idMap[r2[0]]):
                        self.graph[self.idMap[r1[0]]][self.idMap[r2[0]]]['weight'] = self.graph[self.idMap[r1[0]]][self.idMap[r2[0]]]['weight'] + 1
                    else:
                        self.graph.add_edge(self.idMap[r1[0]], self.idMap[r2[0]], weight=1)

    def getArchi2(self, anno):
        listaArchi = DAO.getArchi2(anno)
        for a in listaArchi:
            self.graph.add_edge(self.idMap[a[0]], self.idMap[a[1]], weight=a[2])

    def getMigliore(self):
        result = []
        for nodo1 in self.idMap.values():
            tot = 0
            for nodo2 in self.idMap.values():
                if self.graph.has_edge(nodo1, nodo2):
                    tot += self.graph[nodo1][nodo2]['weight']
                if self.graph.has_edge(nodo2, nodo1):
                    tot -= self.graph[nodo2][nodo1]['weight']
            result.append((nodo1, tot))
        result.sort(key = lambda x:x[1], reverse = True)
        return result[0]

    def graphExists(self):
        if self.graph is None:
            return False
        return True

    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getDreamT(self, k):
        # mi da la soluzione ottima
        self.ricorsione([], k)
        return self.dreamT, self.score

    def ricorsione(self, parziale, k):
        # calcola la soluzione ottima
        if len(parziale) == k:
            if self.score is None or self.getScore(parziale) < self.score:
                self.dreamT = copy.deepcopy(parziale)
                self.score = self.getScore(parziale)

        else:
            for nodo in self.idMap.values():
                if self.condizione(nodo, parziale):
                    parziale.append(nodo)
                    self.ricorsione(parziale, k)
                    parziale.pop()

    def condizione(self, nodo, parziale):
        if len(parziale) == 0 :
            return True
        if nodo in parziale:
            return False
        return True

    def getScore(self, parziale):
        result = 0
        for nodo1 in self.idMap.values():
            for nodo2 in self.idMap.values():
                if nodo1 in parziale and nodo2 not in parziale:
                    if self.graph.has_edge(nodo2, nodo1): # arco entrante
                        result += self.graph[nodo2][nodo1]['weight']
        return result
