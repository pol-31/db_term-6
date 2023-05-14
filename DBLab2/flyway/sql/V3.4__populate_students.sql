
INSERT INTO tbl_zno_student (id, birth, sex, status, class_profile, class_lang, fk_student_reg, fk_eo)
SELECT tbl_zno_results.OUTID, tbl_zno_results.Birth, tbl_zno_results.SEXTYPENAME,
    tbl_zno_results.REGTYPENAME, tbl_zno_results.ClassProfileNAME,
    tbl_zno_results.ClassLangName, tbl_zno_reg_region.id, tbl_zno_eo.id
FROM tbl_zno_results
LEFT OUTER JOIN tbl_zno_region ON (tbl_zno_region.ter = tbl_zno_results.TERNAME OR tbl_zno_region.ter = tbl_zno_results.EOTerName)
LEFT OUTER JOIN tbl_zno_reg_region ON tbl_zno_region.id = tbl_zno_reg_region.fk_region 
LEFT OUTER JOIN tbl_zno_eo ON tbl_zno_region.id = tbl_zno_eo.fk_region
ON CONFLICT DO NOTHING;

