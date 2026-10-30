-- LOGITECH ANALYTICS - CONSULTAS ANALÍTICAS E INSIGHTS DE NEGÓCIO

-- 1. Análise de Cumprimento de SLA por Transportadora
-- Objetivo: Identificar quais transportadoras possuem a maior taxa de atraso em relação ao SLA.
SELECT 
    t.nome_transportadora,
    t.sla_dias AS sla_contratado_dias,
    COUNT(p.pedido_id) AS total_pedidos,
    SUM(CASE WHEN p.data_entrega_real > p.data_entrega_prometida THEN 1 ELSE 0 END) AS qtd_atrasos,
    ROUND(
        (SUM(CASE WHEN p.data_entrega_real > p.data_entrega_prometida THEN 1 ELSE 0 END)::DECIMAL / COUNT(p.pedido_id)) * 100, 2
    ) AS taxa_atraso_pct
FROM pedidos p
JOIN transportadoras t ON p.transportadora_id = t.transportadora_id
GROUP BY t.nome_transportadora, t.sla_dias
ORDER BY taxa_atraso_pct DESC;

-- 2. Impacto Financeiro de Gargalos Operacionais por Estado
-- Objetivo: Mensurar o valor total de pedidos afetados por devoluções ou atrasos em cada estado.
SELECT 
    c.estado,
    p.status_pedido,
    COUNT(p.pedido_id) AS volume_pedidos,
    SUM(p.valor_frete) AS custo_total_frete,
    SUM(p.valor_pedido) AS valor_total_afetado
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.cliente_id
WHERE p.status_pedido IN ('Atrasado', 'Devolvido')
GROUP BY c.estado, p.status_pedido
ORDER BY valor_total_afetado DESC;

-- 3. Análise de Motivos de Devolução no Controle de Qualidade
-- Objetivo: Quantificar o prejuízo financeiro causado por cada tipo de falha operacional.
SELECT 
    cq.motivo_devolucao,
    COUNT(cq.inspecao_id) AS total_ocorrencias,
    SUM(cq.custo_prejuizo) AS prejuizo_acumulado_reais,
    ROUND(AVG(cq.custo_prejuizo), 2) AS prejuizo_medio_por_item
FROM controle_qualidade cq
GROUP BY cq.motivo_devolucao
ORDER BY prejuizo_acumulado_reais DESC;


-- 4. Análise Cronológica com Função de Janela (Window Function)
-- Objetivo: Calcular a variação do prazo real de entrega acumulado por pedido por cliente.
SELECT 
    c.nome AS cliente,
    p.pedido_id,
    p.data_pedido,
    p.status_pedido,
    EXTRACT(DAY FROM (p.data_entrega_real - p.data_envio)) AS dias_para_entrega,
    ROUND(
        AVG(EXTRACT(DAY FROM (p.data_entrega_real - p.data_envio))) OVER (
            PARTITION BY c.cliente_id 
            ORDER BY p.data_pedido
        )::numeric, 2
    ) AS media_movel_dias_cliente
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.cliente_id
ORDER BY c.nome, p.data_pedido;