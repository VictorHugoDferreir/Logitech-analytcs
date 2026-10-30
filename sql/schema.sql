DROP TABLE IF EXISTS controle_qualidade CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS transportadoras CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    estado VARCHAR(2) NOT NULL
);

CREATE TABLE transportadoras (
    transportadora_id SERIAL PRIMARY KEY,
    nome_transportadora VARCHAR(100) NOT NULL,
    sla_dias INT NOT NULL
);

CREATE TABLE pedidos (
    pedido_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    transportadora_id INT REFERENCES transportadoras(transportadora_id),
    data_pedido TIMESTAMP NOT NULL,
    data_envio TIMESTAMP,
    data_entrega_prometida TIMESTAMP,
    data_entrega_real TIMESTAMP,
    status_pedido VARCHAR(30) NOT NULL,
    valor_frete DECIMAL(10,2) NOT NULL,
    valor_pedido DECIMAL(10,2) NOT NULL
);

CREATE TABLE controle_qualidade (
    inspecao_id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(pedido_id) UNIQUE,
    motivo_devolucao VARCHAR(100) NOT NULL,
    custo_prejuizo DECIMAL(10,2) NOT NULL
);
