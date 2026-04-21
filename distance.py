import numpy as np
import pyvrp, pyvrp.stop, pyvrp.plotting
from pyvrp.plotting import plot_solution
import matplotlib.pyplot as plt

class Distance:
    def __init__(self, G, pos, factory_nodes, wholesale_nodes, mode):
        self.G = G
        self.pos = pos
        self.factory_nodes = list(factory_nodes)
        self.wholesale_nodes = list(wholesale_nodes)
        self.mode = mode

    def solve(self):
        m = pyvrp.Model()
        depots = []

        for i, f in enumerate(self.factory_nodes):
            x, y = self.pos[f]
            depot = m.add_depot(location=m.add_location(x, y), name=f"Depot {i+1}")
            depots.append(depot)

        #skapar grossister med varierande behov
        for i, w in enumerate(self.wholesale_nodes):
            x, y = self.pos[w]
            demand = self.G.nodes[w]['demand']
            max_cap = max(self.G.nodes[f]['demand'] for f in self.factory_nodes)

            #om en grossist har ett stort behov kan dess behov delas i två då PyVRP inte stödjer flera
            #lastbilar till samma grossist 
            if demand >= np.ceil(10+np.sqrt(10)):
                m.add_client(location=m.add_location(x, y), 
                     delivery=demand // 2, name=f"Client {i+1}a")
                m.add_client(location=m.add_location(x, y), 
                     delivery=demand - demand // 2, name=f"Client {i+1}b")
            else:
                m.add_client(location=m.add_location(x, y), 
                     delivery=demand, name=f"Client {i+1}")

        #skapar lastbilar för varje fabrik där lastbilarnas last varierar baserat på fabrikernas produktion
        for i, (depot, f) in enumerate(zip(depots, self.factory_nodes)): 
            prod_cap = self.G.nodes[f]['demand']
            m.add_vehicle_type(
                num_available=1,
                capacity=prod_cap,
                start_depot=depot,
                end_depot=depot,
                )

        #skapar euklidiska avstånd mellan alla noder
        for frm in m.locations:
            for to in m.locations:
                dist = int(np.sqrt((frm.x - to.x)**2 + (frm.y - to.y)**2))
                m.add_edge(frm, to, distance=dist)

        res = m.solve(stop=pyvrp.stop.MaxRuntime(10)) #Anger hur länge varje kompilering körs

        #print statements för att kunna följa rutterna. Kommentera bort vid simulering. 
        '''for idx, route in enumerate(res.best.routes()):
            print(f"Route #{idx} [duration = {route.duration()}]:")

            for activity in route:
                if activity.is_depot():
                    where = m.depots[activity.idx]
                else:
                    where = m.clients[activity.idx]
                print(f" - [t = {activity.start_time:>03}] At {where}.")
        '''
        if self.mode == 0: #Enkel kompilering
            pyvrp.plotting.plot_solution(res.best, m.data(), plot_clients = False)
            plt.show()
        return res


