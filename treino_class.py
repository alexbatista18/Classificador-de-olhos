import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


arquivo = "open and close"
dados = pd.read_csv(arquivo)
fz = 512
tempo = dados['Time:512Hz']
channels = dados.iloc[:,2:18]
nomes = channels.columns.tolist()
df = pd.DataFrame(channels)

#aplicando filtro passa-banda de ordem 2 de 7 a 45 hz em todos os canais.
b1, a1 = signal.butter(2, [7, 45], btype='bandpass', fs=fz)
df_filt = df.apply(lambda col: signal.filtfilt(b1, a1, col))
df_filt.columns = nomes

#aplicando filtro CAR
meanss = df_filt.mean(1)
all_car = []
for col in df.columns:
  all_car.append(df_filt[col] - meanss)
all_car = pd.DataFrame(all_car).T
all_car.columns = nomes

#função para somar os valores das amplitudes das frequencias de interesse
def som_win(data):
  faixa = []
  faixa_x = []
  n = 0
  f, p = signal.welch(data, fz,  nperseg=fz*0.4, noverlap=fz/30)
  for j in f:
    if 6.0 <= j <= 16.0:
      faixa.append(n)
      faixa_x.append(j)
    n = n + 1
  soma_welch = []
  f, p = signal.welch(data, fz,  nperseg=fz*0.4, noverlap=fz/30)
  faixa_p = []
  for n in faixa:
    faixa_p.append(p[n])
  return(np.sum(faixa_p))
#separando os tempos de olhos abertos e olhos fechados
open_eyes = all_car.iloc[:, 0:int(fz*60/2)]
close_eyes = all_car.T.iloc[:, int(fz*60/2):int(fz*60)].T

#fazendo a média do sinal dos canais O1 e O2
carr = (all_car['O1']+all_car['O2'])/2

#separando 30 janelas de olhos abertos e olhos fechados
win_open = []
for i in range(30):
  valor_i = i*512
  valor_f = valor_i + fz*1
  win = []
  for j in carr[valor_i:valor_i + fz*1]:
    win.append(j)
  win_open.append(win)
win_close = []
for i in range(30):
  valor_i = (i+30)*512
  valor_f = valor_i + fz*1
  win = []
  for j in carr[valor_i:valor_i + fz*1]:
    win.append(j)
  win_close.append(win)

janelas_open = []
for win in win_open:
  janelas_open.append(som_win(win))
janelas_close = []
for win in win_close:
  janelas_close.append(som_win(win))

#rotulando as classes
y_olhos_abertos = np.zeros(len(janelas_open))  # rótulo 0 para olhos abertos
y_olhos_fechados = np.ones(len(janelas_close))  # rótulo 1 para olhos fechados

#juntando os dados e rótulos
X = janelas_open + janelas_close
y = np.concatenate((y_olhos_abertos, y_olhos_fechados))

#dividindo os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier()

#treinando o classificador e prevendo os valores
clf.fit(np.array(X_train).reshape(-1, 1), y_train)
y_pred = clf.predict(np.array(X_test).reshape(-1, 1))

#calculando a acurácia
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do classificador: {accuracy}")

joblib.dump(clf, 'modelo_treinado.pkl')