from graph import Graph
from distance import Distance
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import contextlib, os, sys

class Main:
    @staticmethod
    def simulation(_):
        g = Graph(3, 8) #Anger antalet fabriker respektive grossister
        G, pos, factory_nodes, wholesale_nodes = g.createGraph()
        d = Distance(G, pos, factory_nodes, wholesale_nodes, 1)

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                res = d.solve()

        if not res.best.is_feasible():
            return None
        return res.best.distance_cost()

    @staticmethod
    def mainSimulation():
        n = 1000 #Anger antalet kompileringar 
        with ProcessPoolExecutor() as executor:
            res = list(executor.map(Main.simulation, range(n)))
        valid = [r for r in res if r is not None]
        infeasible = [r for r in res if r is None]

        print(f"Valid runs: {len(valid)}/{n}")
        print(f"Infeasible runs: {len(infeasible)}/{n}")
        print(f"Mean cost: {np.mean(valid)}")
        print(f"Min cost: {np.min(valid)}")
        print(f"Max cost: {np.max(valid)}")
        print(f"Std deviation: {np.std(valid)}")

    @staticmethod
    def main():
        mode = 0 #1 = simulering, 0 = enkel kompilering

        if mode == 0:
            g = Graph(3, 8)
            G, pos, factory_nodes, wholesale_nodes = g.createGraph()
            Graph.drawGraph(G, pos, factory_nodes, wholesale_nodes)
            d = Distance(G, pos, factory_nodes, wholesale_nodes, mode)
            d.solve()

        else: 
            Main.mainSimulation()

if __name__ == '__main__':
    Main.main()
