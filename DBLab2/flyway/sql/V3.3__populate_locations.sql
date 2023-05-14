
INSERT INTO tbl_zno_reg_region (ter_type, fk_region)
SELECT 
    tbl_zno_results.TerTypeName,
    tbl_zno_region.id
FROM 
    tbl_zno_results
    LEFT OUTER JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.TERNAME
ON CONFLICT (fk_region) DO NOTHING;


INSERT INTO tbl_zno_eo (name, type, parent, fk_region)
SELECT tbl_zno_results.EONAME, tbl_zno_results.EOTYPENAME,
       tbl_zno_results.EOParent, tbl_zno_region.id
FROM tbl_zno_results
INNER JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.EOTerName
ON CONFLICT (fk_region) DO NOTHING;


INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.UkrPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.UkrPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.histPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.histPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.mathPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.mathPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.physPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.physPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.chemPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.chemPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.bioPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.bioPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.geoPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.geoPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.engPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.engPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.fraPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.fraPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.deuPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.deuPTTerName
ON CONFLICT (fk_region) DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.spaPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.spaPTTerName
ON CONFLICT (fk_region) DO NOTHING;


