import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys 

class Graph: 
    #Anger koordinater för Sverige
    LAT_MIN, LAT_MAX = 55.3, 69.1   
    LON_MIN, LON_MAX = 10.9, 24.2  

    #Grossisternas städer och dess koordinater
    CITIES = {
            "Stockholm":   (59.33, 18.07),
            "Gothenburg":  (57.71, 11.97),
            "Malmö":       (55.60, 13.00),
            "Uppsala":     (59.86, 17.64),
            "Västerås":    (59.61, 16.54),
            "Örebro":      (59.27, 15.21),
            "Linköping":   (58.41, 15.62),
            "Helsingborg": (56.05, 12.69)
            }
    city_pos = list(CITIES.values())
    centroid_x = np.mean([x for x, y in city_pos])
    centroid_y = np.mean([y for x, y in city_pos])
    #Fabrikernas städer och koordinater
    FACTORIES = {
            "Landskrona":  (55.87, 12.83), 
            "Jönköping":   (57.78, 14.16),
            "Norrköping":   (58.59, 16.19),
            #"Mellanlager" : (59.61, 16.54) #Ändra var du vill placera mellanlagret här. 
            #Kommentera bort om inget mellanlager
            }

    def __init__(self, factories, wholesalers):
        self.factories = factories
        self.wholesalers = wholesalers
        #a, b är parametrar till ellipsformen som Sverige antas ha 
        self.a = 3
        self.b = 10
        self.city_pos = {
            city: self.latlon_to_ellipse(lat, lon)
            for city, (lat, lon) in self.CITIES.items()
        }
        self.factory_pos = {
            factory : self.latlon_to_ellipse(lat, lon)
            for factory, (lat, lon) in self.FACTORIES.items()
        }
    
    #normerad konvertering av koordinater i latitud och longitud till kartesiska på [-1, 1]
    def latlon_to_ellipse(self, lat, lon):
        u = (lon - self.LON_MIN) / (self.LON_MAX - self.LON_MIN) * 2 - 1  
        v = (lat - self.LAT_MIN) / (self.LAT_MAX - self.LAT_MIN) * 2 - 1  
        x = self.a * u
        y = self.b * v
        return x, y

    def createGraph(self): 
        #välj vilka noder som är fabriker eller grossister 
        factory_index_nodes = list(range(1, self.factories + 1))
        wholesale_index_nodes = list(range(self.factories + 1, self.factories + self.wholesalers + 1))

        G = nx.Graph()

        #skapar vägar mellan alla grossister
        for i in wholesale_index_nodes:
            for j in wholesale_index_nodes:
                if (i != j):
                    G.add_edge(i, j)

        #skapar vägar mellan alla fabriker och grossister 
        for i in factory_index_nodes:
            for j in wholesale_index_nodes:
                G.add_edge(i, j)

        city_names = list(self.CITIES.keys())
        city_pos_list = list(self.city_pos.values()) 
        factory_names = list(self.FACTORIES.keys())
        factory_pos_list = list(self.factory_pos.values()) 

        #Skapar en lista av positioner för att kunna bilda ett euklidkskt avstånd mellan alla noder
        pos = {}
        for i, f in enumerate(factory_index_nodes):
            pos[f] = factory_pos_list[i]
        for i, w in enumerate(wholesale_index_nodes):
            pos[w] = city_pos_list[i]  

        for u, v in G.edges():
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            G[u][v]['weight'] = round(distance)
        
        self.initialize_flow(G, wholesale_index_nodes, factory_index_nodes)

        return G, pos, factory_index_nodes, wholesale_index_nodes

    #Definerar grossisternas behov och fabrikernas produktion (flöde) som varierar 
    #Krav att totala produktion > totala behov
    def initialize_flow(self, G, wholesale_index_nodes, factory_index_nodes):
        w_total = 0
        for w in wholesale_index_nodes:
            G.nodes[w]['demand'] = np.random.poisson(10)
            w_total += G.nodes[w]['demand']

        #Alla fabriker utom mellanlagret får produktion
        for f in factory_index_nodes: #Obs ta bort [:-1] om inget mellanlager
            G.nodes[f]['demand'] = np.random.poisson(27)

        #Hitta fabriken med högst produktion
        #max_factory = max(factory_index_nodes[:-1], key=lambda f: G.nodes[f]['demand'])
        #max_demand = G.nodes[max_factory]['demand']

        #Mellanlager får hälften av max fabrikens produktion
        #mellanlager = factory_index_nodes[-1]
        #G.nodes[mellanlager]['demand'] = int(max_demand * 0.7)
        #G.nodes[max_factory]['demand'] = int(max_demand *0.3)

        f_total = sum(G.nodes[f]['demand'] for f in factory_index_nodes)

        if f_total < w_total:
            self.initialize_flow(G, wholesale_index_nodes, factory_index_nodes)
    
    #Ritar grafen med noder och vägar
    @staticmethod
    def drawGraph(G, pos, factory_index_nodes, wholesale_index_nodes): 
        nx.draw_networkx_nodes(G, pos, nodelist=factory_index_nodes, node_shape='s', node_color='blue')
        nx.draw_networkx_nodes(G, pos, nodelist=wholesale_index_nodes, node_shape='o', node_color='red')
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos)

        plt.gca().set_aspect('equal') 
        plt.savefig("graph.png")
        plt.show()