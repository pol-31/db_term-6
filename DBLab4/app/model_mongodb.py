from db_config import mongo_db

class collZnoRegion:
    collection = mongo_db['coll_zno_region']
    document = {
        'id': 'null',
        'reg': 'null',
        'area': 'null',
        'ter': 'null'
    }

    @classmethod
    def create(cls, id, reg, area, ter):
        document = {
            'id': int(id),
            'reg': 0 if (reg is None) else reg.rstrip(),
            'area': 0 if (area is None) else area.rstrip(),
            'ter': 0 if (ter is None) else ter.rstrip()
        }
        return cls.collection.insert_one(document)

class collZnoRegRegion:
    collection = mongo_db.db['coll_zno_reg_region']
    document = {
        'id': 'null',
        'ter_type': 'null',
        'fk_region': 'null'
    }

    @classmethod
    def create(cls, id, ter_type, fk_region):
        document = {
            'id': int(id),
            'ter_type': 0 if (ter_type is None) else ter_type.rstrip(),
            'fk_region': int(fk_region)
        }
        return cls.collection.insert_one(document)

class collZnoEO:
    collection = mongo_db.db['coll_zno_eo']
    document = {
        'id': 'null',
        'name': 'null',
        'type': 'null',
        'parent': 'null',
        'fk_region': 'null'
    }

    @classmethod
    def create(cls, id, name, type, parent, fk_region):
        document = {
            'id': int(id),
            'name': 0 if (name is None) else name.rstrip(),
            'type': 0 if (type is None) else type.rstrip(),
            'parent': 0 if (parent is None) else parent.rstrip(),
            'fk_region': int(fk_region)
        }
        return cls.collection.insert_one(document)

class collZnoPT:
    collection = mongo_db.db['coll_zno_pt']
    document = {
        'id': 'null',
        'name': 'null',
        'fk_region': 'null'
    }

    @classmethod
    def create(cls, id, name, fk_region):
        document = {
            'id': int(id),
            'name': 0 if (name is None) else name.rstrip(),
            'fk_region': int(fk_region)
        }
        return cls.collection.insert_one(document)

class collZnoStudent:
    collection = mongo_db.db['coll_zno_student']
    document = {
        'id': 'null',
        'birth': 'null',
        'sex': 'null',
        'status': 'null',
        'class_profile': 'null',
        'class_lang': 'null',
        'fk_student_reg': 'null',
        'fk_eo': 'null'
    }

    @classmethod
    def create(cls, id, birth, sex, status, class_profile, class_lang, fk_student_reg, fk_eo):
        document = {
            'id': id.rstrip(),
            'birth': int(birth),
            'sex': 0 if (sex is None) else sex.rstrip(),
            'status': 0 if (status is None) else status.rstrip(),
            'class_profile': 0 if (class_profile is None) else class_profile.rstrip(),
            'class_lang': 0 if (class_lang is None) else class_lang.rstrip(),
            'fk_student_reg': 0 if (fk_student_reg is None) else int(fk_student_reg),
            'fk_eo': 0 if (fk_eo is None) else int(fk_eo)
        }
        return cls.collection.insert_one(document)

class collZnoSubject:
    collection = mongo_db.db['coll_zno_subject']
    document = {
        'id': 'null',
        'name': 'null'
    }

    @classmethod
    def create(cls, id, name):
        document = {
            'id': int(id),
            'name': name.rstrip()
        }
        return cls.collection.insert_one(document)

class collZnoMarks:
    collection = mongo_db.db['coll_zno_marks']
    document = {
        'fk_student_id': 'null',
        'fk_subject': 'null',
        'fk_pt': 'null',
        'test': 'null',
        'test_status': 'null',
        'ball100': 'null',
        'ball12': 'null',
        'ball': 'null',
        'adapt_scale': 'null',
        'lang': 'null',
        'dpa': 'null'
    }

    @classmethod
    def create(cls, fk_student_id, fk_subject, fk_pt, test, test_status, ball100, ball12, ball, adapt_scale, lang, dpa):
        document = {
            'fk_student_id': fk_student_id.rstrip(),
            'fk_subject': int(fk_subject),
            'fk_pt': 0 if (fk_pt is None) else int(fk_pt),
            'test': 0 if (test is None) else test.rstrip(),
            'test_status': test_status.rstrip(),
            'ball100': 0 if (ball100 is None) else float(ball100),
            'ball12': 0 if (ball12 is None) else int(ball12),
            'ball': 0 if (ball is None) else int(ball),
            'adapt_scale': 0 if (adapt_scale is None) else int(adapt_scale),
            'lang': 0 if (lang is None) else lang.rstrip(),
            'dpa': 0 if (dpa is None) else dpa.rstrip()
        }
        return cls.collection.insert_one(document)

