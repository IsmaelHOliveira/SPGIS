# Pacote de Códigos e Benchmarks — TP1 (APA)

Este diretório contém a implementação dos algoritmos de ordenação clássicos, o algoritmo autoral de referência (**DPES - Dual-Pivot Extremes Sieve Sort**), a suíte de testes de validação obrigatória e o framework de medição de desempenho e gráficos em **Python 3** e **C++17**.

---

## 📂 Estrutura de Arquivos

```text
codigo/
├── Makefile                          # Automação de compilação, testes e benchmarks
├── README.md                         # Este guia de execução e desenvolvimento
│
├── python/                           # Implementação em Python 3
│   ├── classical.py                  # Algoritmos clássicos (Bubble, Selection, Insertion, Merge, Quick)
│   ├── authorial.py                  # Algoritmo autoral de referência (DPES)
│   ├── metrics.py                    # Instrumentação (contagem de comparações, trocas e tempos)
│   ├── test_suite.py                 # Suíte com todos os cenários de teste obrigatórios (unittest)
│   ├── benchmark.py                  # Framework de benchmark com geração de gráficos matplotlib
│   └── student_template.py           # Template inicial para o aluno desenvolver seu algoritmo
│
└── cpp/                              # Implementação em C++17 (Alta Performance)
    ├── classical.hpp / .cpp          # Algoritmos clássicos instrumentados
    ├── authorial.hpp / .cpp          # Algoritmo autoral DPES em C++
    ├── test_runner.cpp               # Testes unitários com asserções em C++
    └── benchmark.cpp                 # Benchmark estatístico de alta resolução em C++
```

---

## 🚀 Como Executar

### 1. Suíte de Testes Obrigatória

* **Executar testes em Python:**
  ```bash
  make test_python
  # ou: python3 python/test_suite.py
  ```

* **Compilar e executar testes em C++:**
  ```bash
  make test_cpp
  ```

---

### 2. Benchmarks e Comparação de Desempenho

* **Executar benchmarks em Python (Gera tabelas Markdown e o gráfico `benchmark_results.png`):**
  ```bash
  make benchmark_python
  # ou: python3 python/benchmark.py --trials 3 --plot benchmark_results.png
  ```

* **Executar benchmarks em C++:**
  ```bash
  make run_benchmark_cpp
  ```

---

## 🧑‍💻 Guia para o Aluno (Como usar o template)

1. Abra o arquivo [`python/student_template.py`](file:///home/diogo/447658-ANALISE-E-PROJETOS-DE-ALGORITMOS/02-Semana-2-%2803-09-04-09%29/codigo/python/student_template.py).
2. Escreva a lógica do seu algoritmo na função `my_authorial_sort(arr)`.
3. Certifique-se de incrementar os contadores de comparações (`comps`) e movimentações (`moves`).
4. Execute o arquivo diretamente para validar seu algoritmo contra a suíte de testes:
   ```bash
   python3 python/student_template.py
   ```
5. Para comparar seu algoritmo diretamente contra a literatura no benchmark gráfico:
   * Importe seu método no `python/benchmark.py` e adicione ao dicionário `algorithms`.
   * Execute `python3 python/benchmark.py` para gerar as curvas de tempo e comparações para o seu relatório ou apresentação!
