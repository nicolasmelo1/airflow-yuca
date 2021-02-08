SELECT
  SUM(price)/COUNT(*) AS avarage_price_in_sao_paulo,
FROM
   `properati-data-public.properties_br.properties_rent_{}`
WHERE
state_name = 'São Paulo'
AND property_type = 'apartment'
AND place_name = 'São Paulo'