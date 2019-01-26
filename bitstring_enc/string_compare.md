# Encodig bitstrings as Quantum States
10010010 This is an example state.

It can be saved on 8 bits - then we can encode 2^8 = 256 different states.
The idea is know how many position we need to address and: log2(len(bs1)) = 3 and add one extra qubit for data.
To encode this bit string we need only 3+1 bits. The first 3 points the posiotion, the last one says if its 0 or 1.
```
|\phi> = sqrt(1/2^3)* (|000>|1> + |001>|0> + |010>|0> + |011>|1> + |100>|0>  + |101>|0>  + |110>|1>   + |110>|0>)

|\phi> = sqrt(1/2^3)* (|0001> + |0010> + |0100> + |0111> + |1000>  + |1010>  + |1101>   + |1100>)
```
So the first 3 qubits holds the information about position and the 4. about the value at this pos

$$ \alpha $$

sqrt(1/2^3) - to amplituda prawdopodieństwa obsadzenia stanu. Suma kwadratów tych amplitud musi dawać 1.

Look at https://arxiv.org/abs/quant-ph/0406176v5 Section 2. there it is explained how to make initliazation
We make desired vector:
## Przygotowanie wektora do zainicjalizowania qubitów

Kubit posida dwa stany bazowe: |0> = (0,1)T lub |1> = (1,0)T. Jego dowolny stan (superpozycja)
możemy zapisać jako $$ \phi> = \alpha_0|0> + \alpha_0|1> = (\alpha_0 \alpha_2)T $$
Obliczamy wartość amplitudy prawdopodobieństwa dla naszego wektora stanu $$ sqrt(1/2^3) = 0.353 $$
Zapisując każdy bit w jako kubit |0> = (0,1)T lub |1> = (1,0)T i uwzględniając obliczoną amplitudę,
możemy zapisać nasz wektor incjalizacyjny dla kubitów dla przyjętego przez nas stanu jako:
```
0.353 * [(0, 1),  (1 0), (1, 0.), (0, 1), (1, 0), (1, 0), (0, 1), (1, 0)]
[(0, 0.353),  (0.353 0), (0.353, 0.), (0, 0.353), (0.353, 0), (0.353, 0), (0, 0.353), (0.353, 0)]

```

Inicjalizacji kubitów dokunujemy poprzez utworzeniu przewodu kwantowego i użycia metody `initialize()`.
```
qc.initialize(desired_vector, [qr[i] for i in range(n)])
```

Tylko co  z tym zakodowanym stringiem bitowym teraz by zrobić?


Tak jak to teraz rozumię, to wprowadzenie tej skompresowanej notacji było trochę mylące.
Może to miało wytłumaczyć jak mniejsza ilość qubitów potarfi przechować taki stan.
Faktycznie mniejszą ilość qubitów incjalizujemy jednak porzez desired_vector, który
składa się takiej ilości par (0 1) lub (1 0) ile bitów występuje w stringu.
To funkcja incialzująca powoduje kompresję przy zapisie (?).
OK. To jak zwrotnie odczytać zakodowany bit?


## Inverse

qiskit._compositegate.CompositeGate#inverse

MUST READ: https://www.quantiki.org/wiki/basic-concepts-quantum-computation