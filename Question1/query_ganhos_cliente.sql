SELECT cliente_nome, CAST(SUM(lucro) - SUM(desconto_taxa) AS DECimal(10, 2)) as valor
FROM(
  SELECT
  	cli.nome AS cliente_nome,
    (transac.valor_total * (cont.percentual / 100)) AS lucro,
  	(transac.valor_total * (cont.percentual / 100)) * (transac.percentual_desconto /100) as desconto_taxa
  FROM cliente cli
  INNER JOIN contrato cont ON cont.cliente_id = cli.cliente_id
  INNER JOIN transacao transac ON transac.contrato_id = cont.contrato_id
  WHERE cont.ativo = 1
) AS calculo
group by cliente_nome;