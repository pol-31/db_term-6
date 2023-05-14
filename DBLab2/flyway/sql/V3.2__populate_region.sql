
INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT REGNAME, AREANAME, TERNAME
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT EORegName, EOAreaName, EOTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT UkrPTRegName, UkrPTAreaName, UkrPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT histPTRegName, histPTAreaName, histPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT mathPTRegName, mathPTAreaName, mathPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT physPTRegName, physPTAreaName, physPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT chemPTRegName, chemPTAreaName, chemPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT bioPTRegName, bioPTAreaName, bioPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT geoPTRegName, geoPTAreaName, geoPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT engPTRegName, engPTAreaName, engPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT fraPTRegName, fraPTAreaName, fraPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT deuPTRegName, deuPTAreaName, deuPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;

INSERT INTO tbl_zno_region (reg, area, ter)
SELECT DISTINCT spaPTRegName, spaPTAreaName, spaPTTerName
FROM tbl_zno_results
ON CONFLICT (reg) DO NOTHING;


