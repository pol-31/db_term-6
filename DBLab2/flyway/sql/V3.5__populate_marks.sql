
INSERT INTO tbl_zno_subject (name)
VALUES  ('ukr'),
        ('hist'),
        ('math'),
        ('phys'),
        ('chem'),
        ('bio'),
        ('geo'),
        ('eng'),
        ('fra'),
        ('deu'),
        ('spa')
ON CONFLICT (name) DO NOTHING;


INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, adapt_scale, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.UkrTest, tbl_zno_results.UkrTestStatus, CAST(REPLACE(tbl_zno_results.UkrBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.UkrBall12 as int2), cast(tbl_zno_results.UkrBall as int2), cast(tbl_zno_results.UkrAdaptScale as int2),
    tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.UkrPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'ukr'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, lang, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.histTest, tbl_zno_results.histTestStatus, CAST(REPLACE(tbl_zno_results.histBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.histBall12 as int2), cast(tbl_zno_results.histBall as int2),
    tbl_zno_results.HistLang, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.histPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'hist'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, lang, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.mathTest, tbl_zno_results.mathTestStatus, CAST(REPLACE(tbl_zno_results.mathBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.mathBall12 as int2), cast(tbl_zno_results.mathBall as int2),
    tbl_zno_results.mathLang, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.mathPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'math'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, lang, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.physTest, tbl_zno_results.physTestStatus, CAST(REPLACE(tbl_zno_results.physBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.physBall12 as int2), cast(tbl_zno_results.physBall as int2),
    tbl_zno_results.physLang, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.physPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'phys'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, lang, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.chemTest, tbl_zno_results.chemTestStatus, CAST(REPLACE(tbl_zno_results.chemBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.chemBall12 as int2), cast(tbl_zno_results.chemBall as int2),
    tbl_zno_results.chemLang, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.chemPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'chem'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, lang, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.bioTest, tbl_zno_results.bioTestStatus, CAST(REPLACE(tbl_zno_results.bioBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.bioBall12 as int2), cast(tbl_zno_results.bioBall as int2),
    tbl_zno_results.bioLang, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.bioPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'bio'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, lang, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.geoTest, tbl_zno_results.geoTestStatus, CAST(REPLACE(tbl_zno_results.geoBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.geoBall12 as int2), cast(tbl_zno_results.geoBall as int2),
    tbl_zno_results.geoLang, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.geoPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'geo'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, dpa, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.engTest, tbl_zno_results.engTestStatus,  CAST(REPLACE(tbl_zno_results.engBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.engBall12 as int2), cast(tbl_zno_results.engBall as int2),
    tbl_zno_results.engDPALevel, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.engPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'eng'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, dpa, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.fraTest, tbl_zno_results.fraTestStatus,  CAST(REPLACE(tbl_zno_results.fraBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.fraBall12 as int2), cast(tbl_zno_results.fraBall as int2),
    tbl_zno_results.fraDPALevel, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.fraPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'fra'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, dpa, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.deuTest, tbl_zno_results.deuTestStatus,  CAST(REPLACE(tbl_zno_results.deuBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.deuBall12 as int2), cast(tbl_zno_results.deuBall as int2),
    tbl_zno_results.deuDPALevel, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.deuPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'deu'
ON CONFLICT DO NOTHING;

INSERT INTO tbl_zno_marks (test, test_status, ball100, ball12,
                ball, dpa, fk_student_id, fk_subject, fk_pt)
SELECT tbl_zno_results.fraTest, tbl_zno_results.fraTestStatus,  CAST(REPLACE(tbl_zno_results.fraBall100, ',', '.') AS decimal),
    cast(tbl_zno_results.fraBall12 as int2), cast(tbl_zno_results.fraBall as int2),
    tbl_zno_results.fraDPALevel, tbl_zno_results.outid, tbl_zno_subject.id, tbl_zno_pt.id
FROM tbl_zno_results
JOIN tbl_zno_region ON tbl_zno_region.ter = tbl_zno_results.fraPTTerName
JOIN tbl_zno_pt ON tbl_zno_region.id = tbl_zno_pt.fk_region 
JOIN tbl_zno_subject ON tbl_zno_subject.name = 'fra'
ON CONFLICT DO NOTHING;


