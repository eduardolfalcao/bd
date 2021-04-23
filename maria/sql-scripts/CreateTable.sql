CREATE DATABASE universidade;
USE universidade;

/* aqui criaremos as tabelas */
CREATE TABLE IF NOT EXISTS Funcionario(
	cpf INT PRIMARY KEY,
	p_nome VARCHAR(100) NOT NULL,
	m_inicial CHAR,
	u_nome VARCHAR(100) NOT NULL,
	dt_nasc DATE NOT NULL,
	endereco VARCHAR(200),
	sexo CHAR NOT NULL,
	salario FLOAT,
	cpf_sup INT, 
	FOREIGN KEY (cpf_sup) REFERENCES Funcionario(cpf) 
);


