## Inledning
Vehicle Routing Problem är ett välkänt problem som många företag kämpar med. I detta projekt löses ett sådant problem utifrån ett statistiskt förhållningssätt, där det antas existera ett godtyckligt antal producenter och konsumenter med en varierande produktion och konsumtion som antas vara stokastiska poissonfördelade variabler. Konsumenterna och producenter antas existera i Sverige och kan väljas godtyckligt.

## Kod
I koden är antalet producenter (fabriker) och konsumenter (grossister) förinställt till 3 respektive 8, men kan väljas godtyckligt i `main.py` genom att ändra parametrarna till `Graph(x, y)`. Deras produktion respektive konsumtion antas vara poissonfördelade med väntevärde 27 respektive 10 men 
kan väljas något godtyckligt i `graph.py` så länge den totala produktionen är minst lika stor som den totala konsumtionen. 

Om en önskar att få en optimerad lösning utifrån PyVRP väljs `mode = 0` i `main.py`. Om `n` simuleringar av mode = 0 önskas väljs `mode = 1` där `n` väljs godtyckligt. Observera att en stor simulering kan ta några minuter. Därför har `ProcessPoolExecutor` används för att utnyttja fler processorkärnor.

Var producenter och konsumenter placeras väljs i `graph.py` där `CITIES` respektive `FACTORIES` anger latitudinella respektive longitudinella koordinater för konsumenter respektive producenter. Om en funderar på att bygga ett mellanlager som ej antas ha en egen produktion kan det väljas i `FACTORIES` som ett extra element.

## Installation
Observera att PyVRP 0.14.0 eller senare behövs. Följande kommando installerar PyVRP direkt från GitHub:
```bash
pip install 'pyvrp @ git+https://github.com/PyVRP/PyVRP'
```

