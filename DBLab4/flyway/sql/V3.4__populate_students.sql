INSERT INTO tbl_zno_student (id, birth, sex, status, class_profile, class_lang, fk_student_reg, fk_eo)
SELECT tbl_zno_results.OUTID, tbl_zno_results.Birth, tbl_zno_results.SEXTYPENAME,
    tbl_zno_results.REGTYPENAME, tbl_zno_results.ClassProfileNAME,
    tbl_zno_results.ClassLangName, tbl_zno_reg_region.id,
    (SELECT tbl_zno_eo.id
    FROM tbl_zno_eo
    WHERE tbl_zno_eo.name = tbl_zno_results.EONAME
        AND tbl_zno_eo.parent = tbl_zno_results.EOParent
        AND tbl_zno_eo.type = tbl_zno_results.EOTYPENAME
    LIMIT 1) AS fk_eo
FROM tbl_zno_results
JOIN tbl_zno_region ON (tbl_zno_region.ter = tbl_zno_results.TERNAME AND
                                   tbl_zno_region.area = tbl_zno_results.AREANAME AND
                                   tbl_zno_region.reg = tbl_zno_results.REGNAME )
JOIN tbl_zno_reg_region ON tbl_zno_region.id = tbl_zno_reg_region.fk_region
ON CONFLICT DO NOTHING;

