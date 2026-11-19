import nbformat, asyncio, sys
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) if sys.platform=='win32' else None
nb = nbformat.read(r'C:/Users/marci/Downloads/CMTC.ipynb', as_version=4)
c = nb.cells
c[4].source = ("# Conectar com o Google Drive\n"
 "# Execução local (fora do Colab): o drive.mount foi substituído por uma pasta local\n"
 "# from google.colab import drive\n# drive.mount('/content/gdrive')")
c[6].source = ("# Path para pasta de DADOS (local)\n"
 "caminho_dados = './'\n\n# Path para pasta de PDF\ncaminho_pdf = './'\n\n# Nome do notebook\nnome = 'CMTC'")
c[10].source = r'''def cmtcP(Q):
    [r,c] = Q.shape
    # A matriz que deve duas minensões iguais
    # A soma das linhas deve ser igual a 0
    # Na construção da matriz podem ser gerados valores cuja soma é muito próxima de zero
    # Testar se o valor da soma é muito próximo de zero
    if ((r != c) | (not np.all(np.isclose(np.sum(Q, 1),0)))):
        raise Exception('Matriz Q invalida!')

    # Coloque seu código aqui
    # A = Transposta(Q) concatenada com uma linha de 1s (condição de normalização)
    A = np.vstack((Q.T, np.ones(r)))
    # B = vetor de zeros de tamanho n concatenado com [1]
    B = np.concatenate((np.zeros(r), [1]))
    # PI = pseudo-inversa(A) . B  (solução de PI.Q = 0 com soma(PI) = 1)
    A_pinv = np.linalg.pinv(A)
    PI = np.dot(A_pinv, B)

    return PI'''
c[14].source = '''# Vetor de taxas de permanência
Mu = np.array([1/40, 1/20, 1/60, 1/10, 1/30])
print(Mu)'''
c[16].source = '''# Criar e imprimir a matriz P
P = np.array([[0,    1,    0,    0,    0   ],
              [0,    0,    0.92, 0,    0.08],
              [0,    0,    0,    0.88, 0.12],
              [0.96, 0,    0,    0,    0.04],
              [1,    0,    0,    0,    0   ]])
print(P)'''
c[19].source = '''# Calcular a matriz Q
Q = cmtcPtoQ(P, Mu)
np.set_printoptions(precision=4, suppress=True)
print(Q)'''
c[21].source = '''# Calcular o vetor PI
# Se o seu código estiver correto a respota deve ser [0.30799585 0.15399792 0.4241859  0.06235533 0.05146501]
np.set_printoptions(precision=8, suppress=True)
PI = cmtcP(Q)
print(PI)
print('Soma de PI =', PI.sum())
print('Verificação PI.Q = 0:', np.allclose(PI @ Q, 0))'''
c.append(nbformat.v4.new_markdown_cell(r'''### Resposta
O dispositivo permanece **em operação (estado 2) cerca de 42,5 % do tempo** ($\pi_2 = 0{,}4247$ com as taxas exatas).'''))
c.append(nbformat.v4.new_code_cell(r'''estados = ['desligado', 'aquecimento', 'operação', 'esfriamento', 'manutenção']
for e, p in zip(estados, PI):
    print(f'{e:12s}: {p:.4f}  ({p*100:.2f} % do tempo)')
print(f'\nProporção do tempo em operação = {PI[2]:.4f} ({PI[2]*100:.2f} %)')'''))
c.append(nbformat.v4.new_markdown_cell(r"""### Observação sobre a resposta esperada
A resposta indicada no enunciado ([0.30799585 0.15399792 0.4241859 0.06235533 0.05146501]) usa as taxas **arredondadas** da tabela de taxas de transição
($\mu_{23}=0{,}0147$ e $\mu_{24}=0{,}0020$, ou seja $\mu_2 \approx 0{,}0167$ em vez de $1/60 = 0{,}016667$).
Com as taxas exatas o resultado é $\pi_2 = 0{,}4247$; com $\mu_2 = 0{,}0167$ o resultado coincide com o esperado até a 4ª casa decimal ($\pi_2 \approx 0{,}4242$).
Nos dois casos, o dispositivo fica **cerca de 42 % do tempo em operação**."""))
c.append(nbformat.v4.new_code_cell("""# Mesmo cálculo com a taxa de permanência do estado 2 arredondada (0,0147 + 0,0020 = 0,0167)
Mu_arred = np.array([1/40, 1/20, 0.0167, 1/10, 1/30])
PI_arred = cmtcP(cmtcPtoQ(P, Mu_arred))
print(PI_arred)
print(f'Proporção do tempo em operação (taxas arredondadas) = {PI_arred[2]:.4f}')"""))
from nbclient import NotebookClient
NotebookClient(nb, timeout=120, kernel_name='python3', resources={'metadata': {'path': '.'}}).execute()
nbformat.write(nb, 'AD01_FORMATIVA19.ipynb')
for cell in nb.cells:
    if cell.cell_type == 'code':
        for o in cell.get('outputs', []):
            if 'text' in o: print(o['text'])
