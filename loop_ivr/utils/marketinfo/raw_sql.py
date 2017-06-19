last_three_trans = ''''SELECT 
    final.crop, final.mandi, final.datee, final.minp, final.maxp
FROM
    (SELECT 
        add_row_no.crop,
            add_row_no.mandi,
            add_row_no.datee,
            add_row_no.minp,
            add_row_no.maxp,
            (@num:=IF(@crop = add_row_no.crop
                AND @mandi = add_row_no.mandi, @num + 1, IF(@crop:=add_row_no.crop
                AND @mandi:=add_row_no.mandi, 1, 1))) 'row_number'
    FROM
        (SELECT 
        lc.crop_id 'crop',
            lc.mandi_id 'mandi',
            lc.date 'datee',
            MIN(lc.price) 'minp',
            MAX(lc.price) 'maxp'
    FROM
        loop_combinedtransaction lc
    where lc.crop_id in [%s] AND lc.mandi_id in [%s]
    GROUP BY lc.date , lc.crop_id , lc.mandi_id
    ORDER BY lc.crop_id , lc.mandi_id , lc.date DESC) add_row_no
    CROSS JOIN (SELECT @num:=0, @crop:=NULL, @mandi:=NULL) c) final
WHERE
    final.row_number <= 3
'''