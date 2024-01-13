# Olá, bem vindo ao Classificador de olhos abertos e fechados
Este código visa o Treinamento do Classificador para Detecção de Olhos Abertos ou Fechados com Base em Sinais Cerebrais, antes de ir para o código segue o raciicínio logo abaixo.

Objetivo: Desenvolver um classificador capaz de diferenciar entre momentos em que a pessoa está com os olhos abertos ou fechados, utilizando sinais cerebrais obtidos por meio de eletroencefalograma (EEG).

Coleta de Dados: Os dados dispostos em '[open and close](https://github.com/alexbatista18/Classificador-de-olhos/blob/main/open%20and%20close)' são de autoria própria e foram coletados ao total 1 minuto de gravação. Os primeiros 30 segundos correspondem ao voluntário com os olhos abertos, enquanto os últimos 30 segundos representam a condição de olhos fechados.

Região de Interesse e Canais: A atividade ocular ocorre na região occipital. Foi dada maior importância aos canais O1 e O2, localizados nessa região.

Processamento do Sinal: O sinal EEG foi processado para destacar a atividade nos canais O1 e O2. A análise focou em uma faixa específica, a banda alfa (8-13 Hz), considerando sua relevância para a detecção de olhos fechados.

Segmentação do Sinal e Extração de Características: Cada categoria foi segmentada em 30 janelas, para cada janela, foi calculada a transformada de Welch, técnica para estimar a densidade espectral de potência. As bandas de interesse, relacionadas à banda alfa, foram identificadas e somadas para cada janela.

## Treinamento
O arquivo '[treino_class.py](https://github.com/alexbatista18/Classificador-de-olhos/blob/main/treino_class.py)' contém o código desenvolvido para o treinamento do classificador utilizandos os dados dispostos.

## Aplicação do Classificador
O classificador foi aplicado em um sofwater chamado [OpenVibe](http://openvibe.inria.fr/) próprio para aquisição de sinais cerebrais em tempo real. Como podem ver na iamgem abaixo, a box chamada 'Python 3 scripting' é utilizada para acessar o script '[aply_class.py](https://github.com/alexbatista18/Classificador-de-olhos/blob/main/aply_class.py)'.

![classificador](https://github.com/alexbatista18/Classificador-de-olhos/assets/129801029/b7d3ef1f-af85-4d23-88f3-989768425f4a)

Foram utilizados os mesmo dados de treino apenas para verificar a integridade do código.
