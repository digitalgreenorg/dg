last_three_trans = '''SELECT
    lc.crop_id AS 'crop',
    lc.mandi_id AS 'mandi',
    lc.date AS 'date',
    MIN(lc.price) AS 'minp',
    MAX(lc.price) AS 'maxp',
    SUM(lc.price * lc.quantity) / SUM(lc.quantity) AS 'mean'
FROM
    loop_combinedtransaction lc
WHERE
    lc.crop_id in {} AND lc.mandi_id in {} and date in {}
GROUP BY lc.date , lc.crop_id , lc.mandi_id
ORDER BY lc.crop_id , lc.mandi_id , lc.date DESC
'''

query_for_transactions = '''SELECT
    lc.date AS 'Date',
    lc.user_created_id AS 'Aggregator',
    lc.mandi_id AS 'Market_Real',
    lc.crop_id AS 'Crop',
    lc.quantity AS 'Quantity_Real',
    lc.price AS 'Price',
    lc.amount AS 'Amount'
FROM
    loop_combinedtransaction lc
WHERE
    lc.crop_id in {} AND lc.mandi_id in {} and date in {}
'''
