
INSERT INTO tbl_zno_reg_region (ter_type, fk_region)
SELECT tbl_zno_results.TerTypeName, tbl_zno_region.id
FROM tbl_zno_results
JOIN tbl_zno_region ON (tbl_zno_region.ter = tbl_zno_results.TERNAME AND
						tbl_zno_region.area = tbl_zno_results.AREANAME AND
						tbl_zno_region.reg = tbl_zno_results.REGNAME )
ON CONFLICT DO NOTHING;


INSERT INTO tbl_zno_eo (name, type, parent, fk_region)
SELECT tbl_zno_results.EONAME, tbl_zno_results.EOTYPENAME, tbl_zno_results.EOParent, tbl_zno_region.id
FROM tbl_zno_results
JOIN tbl_zno_region ON (tbl_zno_region.ter = tbl_zno_results.EOTerName AND
						tbl_zno_region.area = tbl_zno_results.EOAreaName AND
						tbl_zno_region.reg = tbl_zno_results.EORegName )
ON CONFLICT DO NOTHING;


INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.UkrPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.UkrPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.UkrPTRegName AND
    tbl_zno_region.area = tbl_zno_results.UkrPTAreaName
ON CONFLICT DO NOTHING;


INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.histPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.histPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.histPTRegName AND
    tbl_zno_region.area = tbl_zno_results.histPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.mathPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.mathPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.mathPTRegName AND
    tbl_zno_region.area = tbl_zno_results.mathPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.physPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.physPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.physPTRegName AND
    tbl_zno_region.area = tbl_zno_results.physPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.chemPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.chemPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.chemPTRegName AND
    tbl_zno_region.area = tbl_zno_results.chemPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.bioPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.bioPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.bioPTRegName AND
    tbl_zno_region.area = tbl_zno_results.bioPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.geoPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.geoPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.geoPTRegName AND
    tbl_zno_region.area = tbl_zno_results.geoPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.engPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.engPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.engPTRegName AND
    tbl_zno_region.area = tbl_zno_results.engPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.fraPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.fraPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.fraPTRegName AND
    tbl_zno_region.area = tbl_zno_results.fraPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.deuPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.deuPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.deuPTRegName AND
    tbl_zno_region.area = tbl_zno_results.deuPTAreaName
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_pt (name, fk_region)
SELECT tbl_zno_results.spaPTName, tbl_zno_region.id
FROM tbl_zno_results, tbl_zno_region 
WHERE tbl_zno_region.ter = tbl_zno_results.spaPTTerName AND
    tbl_zno_region.reg = tbl_zno_results.spaPTRegName AND
    tbl_zno_region.area = tbl_zno_results.spaPTAreaName
ON CONFLICT DO NOTHING;



