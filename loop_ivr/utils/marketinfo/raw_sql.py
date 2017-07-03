last_three_trans = '''SELECT 
    lc.crop_id 'crop',
    lc.mandi_id 'mandi',
    lc.date,
    MIN(lc.price) 'minp',
    MAX(lc.price) 'maxp',
    SUM(lc.price * lc.quantity) / SUM(lc.quantity) AS 'mean'
FROM
    loop_combinedtransaction lc
WHERE
    lc.crop_id in {} AND lc.mandi_id in {} and date in {}
GROUP BY lc.date , lc.crop_id , lc.mandi_id
ORDER BY lc.crop_id , lc.mandi_id , lc.date DESC
'''