#Raphaella Brandão Jacques, Rafael Torres Nantes

# Bibliotecas necessárias
LIBS = socket threading json logging sys random time

# Comandos para executar os programas
RUN_CLIENT = python src/cliente.py
RUN_SAI = python src/sai.py

all: cliente servidor

cliente: src/cliente.py
	@echo "Compilando o cliente..."
	python src/cliente.py

servidor: src/sai.py
	@echo "Compilando o sai..."
	python src/sai.py

run: cliente servidor
	@echo "Executando o cliente..."
	$(RUN_CLIENT)
	@echo "Executando o servidor..."
	$(RUN_SAI)

clean:
	@echo "Limpando os arquivos compilados..."
	rm -f src/cliente.pyc src/sai.pyc

.PHONY: all cliente servidor run clean