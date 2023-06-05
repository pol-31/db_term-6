from db_config import mongo_db

class collZnoRegion:
    collection = mongo_db['coll_zno_region']

    @classmethod
    def create(cls, reg, area, ter):
        document = {
            'reg': reg,
            'area': area,
            'ter': ter
        }
        return cls.collection.insert_one(document)

class collZnoRegRegion:
    collection = mongo_db.db['coll_zno_reg_region']

    @classmethod
    def create(cls, ter_type, fk_region):
        document = {
            'ter_type': ter_type,
            'fk_region': fk_region
        }
        return cls.collection.insert_one(document)

class collZnoEO:
    collection = mongo_db.db['coll_zno_eo']

    @classmethod
    def create(cls, name, type, parent, fk_region):
        document = {
            'name': name,
            'type': type,
            'parent': parent,
            'fk_region': fk_region
        }
        return cls.collection.insert_one(document)

class collZnoPT:
    collection = mongo_db.db['coll_zno_pt']

    @classmethod
    def create(cls, name, fk_region):
        document = {
            'name': name,
            'fk_region': fk_region
        }
        return cls.collection.insert_one(document)

class collZnoStudent:
    collection = mongo_db.db['coll_zno_student']

    @classmethod
    def create(cls, id, birth, sex, status, class_profile, class_lang, fk_student_reg, fk_eo):
        document = {
            'id': id,
            'birth': birth,
            'sex': sex,
            'status': status,
            'class_profile': class_profile,
            'class_lang': class_lang,
            'fk_student_reg': fk_student_reg,
            'fk_eo': fk_eo
        }
        return cls.collection.insert_one(document)

class collZnoSubject:
    collection = mongo_db.db['coll_zno_subject']

    @classmethod
    def create(cls, name):
        document = {
            'name': name
        }
        return cls.collection.insert_one(document)

class collZnoMarks:
    collection = mongo_db.db['coll_zno_marks']

    @classmethod
    def create(cls, fk_student_id, fk_subject, fk_pt, test, test_status, ball100, ball12, ball, adapt_scale, lang, dpa):
        document = {
            'fk_student_id': fk_student_id,
            'fk_subject': fk_subject,
            'fk_pt': fk_pt,
            'test': test,
            'test_status': test_status,
            'ball100': float(ball100),
            'ball12': ball12,
            'ball': ball,
            'adapt_scale': adapt_scale,
            'lang': lang,
            'dpa': dpa
        }
        return cls.collection.insert_one(document)

