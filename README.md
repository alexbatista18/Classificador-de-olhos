# Olá, bem-vindo ao Classificador de Olhos Abertos e Fechados

## Raciocínio

### Objetivo
Desenvolver um classificador capaz de diferenciar estados de olhos abertos e fechados utilizando sinais cerebrais.

### Coleta de Dados
Os dados, disponíveis em '[open and close](https://github.com/alexbatista18/Classificador-de-olhos/blob/main/open%20and%20close)', são autênticos e representam 1 minuto de gravação. Os primeiros 30 segundos correspondem a olhos abertos, seguidos por 30 segundos de olhos fechados.

### Região de Interesse e Canais
A atividade ocular foi focada na região occipital, priorizando os canais O1 e O2.

### Processamento do Sinal
O sinal EEG foi processado, destacando a atividade nos canais O1 e O2. A análise concentrou-se na banda alfa (8-13 Hz), crucial para a detecção de olhos fechados.

### Segmentação do Sinal e Extração de Características
Cada categoria foi dividida em 30 janelas. Para cada janela, a transformada de Welch foi calculada para estimar a densidade espectral de potência. As bandas alfa foram identificadas e somadas para cada janela.

## Treinamento

O treinamento do classificador está implementado no arquivo '[treino_class.py](https://github.com/alexbatista18/Classificador-de-olhos/blob/main/treino_class.py)'. Este script utiliza os dados disponíveis para treinar o modelo.

## Aplicação do Classificador

O classificador foi integrado ao software [OpenVibe](http://openvibe.inria.fr/) para a aquisição de sinais cerebrais em tempo real. O script '[aply_class.py](https://github.com/alexbatista18/Classificador-de-olhos/blob/main/aply_class.py)' é acessado através da box 'Python 3 scripting'.

![classificador](https://github.com/alexbatista18/Classificador-de-olhos/assets/129801029/b7d3ef1f-af85-4d23-88f3-989768425f4a)

Explore o código, experimente o treinamento do classificador e sua aplicação em tempo real com o OpenVibe! Se tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato.
