from abc import ABC, abstractmethod
from sqlalchemy import func

from model_sqlalchemy import *
from model_mongodb import *

class Zno(ABC):
    pass
    
#reaquired tables for database
class ZnoRegion(ABC):
    pass
class ZnoRegRegion(ABC):
    pass 
class ZnoEO(ABC):
    pass
class ZnoPT(ABC):
    pass
class ZnoStudent(ABC):
    pass
class ZnoSubject(ABC):
    pass
class ZnoMarks(ABC):
    pass

class Database(ABC):
    # __init__ requires: db, name
    #fltr = {filter_name:value, ...}
    #form: wtform 

    @abstractmethod
    def get(self, tbl, num):
        pass
    
    @abstractmethod
    def add(self, tbl, form_):
        pass
      
    @abstractmethod  
    def update(self, tbl, fltr, form_):
        pass
       
    @abstractmethod 
    def delete(self, tbl, fltr):
        pass
        
    @abstractmethod
    def get_by_id(self, tbl, fltr):
        pass
        
    @abstractmethod
    def make_query(self, regionValue, subjectValue, yearValue):
        pass


class DatabaseMongo(Database):
    def __init__(self, db_):
        self.db = db_
        self.name = "mongo"
        self.db_prefix = "coll"

    def get(self, coll, num):
        coll = globals()[self.db_prefix + coll.__name__]
        result = coll.collection.find().limit(num)
        return list(result)
        
    def add(self, coll, form_):
        coll = globals()[self.db_prefix + coll.__name__]
        document = {}
    
        for attr in coll.document:
            document[attr] = getattr(form_, attr).data
    
        try:
            coll.collection.insert_one(document)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            
    def update(self, coll, fltr, form_):
        coll = globals()[self.db_prefix + coll.__name__]
        filter_query = {}
    
        for attr in fltr:
            filter_query[attr] = fltr[attr]
    
        try:
            update_query = {'$set': {}}
            for attr in coll.document:
                update_query['$set'][attr] = getattr(form_, attr).data
            
            coll.collection.update_one(filter_query, update_query)
            
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def delete(self, coll, fltr):
        coll = globals()[self.db_prefix + coll.__name__]
        filter_query = {}
    
    
        # delete __marks__ (composite key)
        for attr in fltr:
            filter_query[attr] = fltr[attr]
    
        try:
            coll.collection.delete_one(filter_query)
        
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def get_by_id(self, coll, fltr):
        coll = globals()[self.db_prefix + coll.__name__]
        filter_query = {}
    
        for attr in fltr:
            filter_query[attr] = fltr[attr]
        
        result = coll.collection.find_one(filter_query)
        return result
        
    def make_query(self, regionValue, subjectValue, yearValue):
        pipeline = []

        if regionValue == '0':
            pipeline = [
                {'$match': {'test_status': 'Зараховано'}},
                {
                    '$lookup': {
                        'from': 'coll_zno_student',
                        'localField': 'fk_student_id',
                        'foreignField': 'id',
                        'as': 'student'
                    }
                },
                {
                    '$lookup': {
                        'from': 'coll_zno_reg_region',
                        'localField': 'student.fk_student_reg',
                        'foreignField': 'id',
                        'as': 'reg_region'
                    }
                },
                {
                    '$lookup': {
                        'from': 'coll_zno_region',
                        'localField': 'reg_region.fk_region',
                        'foreignField': 'id',
                        'as': 'region'
                    }
                },
                {
                    '$group': {
                        '_id': '$region.reg',
                        'avg_ball': {'$avg': '$ball100'},
                        'min_region': {'$min': '$region.reg'}
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'avg_ball': 1,
                        'min_region': 1
                    }
                }
            ]
        else:
            pipeline = [
                {'$match': {'test_status': 'Зараховано', 'region.reg': regionValue}},
                {
                    '$lookup': {
                        'from': 'coll_zno_student',
                        'localField': 'fk_student_id',
                        'foreignField': 'id',
                        'as': 'student'
                    }
                },
                {
                    '$lookup': {
                        'from': 'coll_zno_reg_region',
                        'localField': 'student.fk_student_reg',
                        'foreignField': 'id',
                        'as': 'reg_region'
                    }
                },
                {
                    '$lookup': {
                        'from': 'coll_zno_region',
                        'localField': 'reg_region.fk_region',
                        'foreignField': 'id',
                        'as': 'region'
                    }
                },
                {
                    '$group': {
                        '_id': '$region.area',
                        'avg_ball': {'$avg': '$ball100'},
                        'min_area': {'$min': '$region.area'}
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'avg_ball': 1,
                        'min_area': 1
                    }
                }
            ]
    
        if subjectValue != 0:
            pipeline.insert(1, {'$match': {'fk_subject': subjectValue}})
    
        if yearValue == 1:
            pipeline.insert(1, {'$match': {'student.birth': {'$gte': 2002}}})
        elif yearValue == 2:
            pipeline.insert(1, {'$match': {'student.birth': {'$lte': 2002}}})
    
        if regionValue == '0':
            pipeline.append({'$sort': {'avg_ball': 1}})
            pipeline.append({'$group': {'_id': '$min_region', 'avg_ball': {'$first': '$avg_ball'}}})
        else:
            pipeline.append({'$sort': {'avg_ball': 1}})
            pipeline.append({'$group': {'_id': '$min_area', 'avg_ball': {'$first': '$avg_ball'}}})
    
        result = self.db['ormTblZnoMarks'].aggregate(pipeline)
        return list(result)


class DatabasePostgre(Database):
    def __init__(self, db_):
        self.db = db_
        self.name = "postgre"
        self.db_prefix = "ormTbl"

    def get(self, tbl, num):
        tbl = globals()[self.db_prefix + tbl.__name__]
        return self.db.session.query(tbl).limit(num).all()

    def add(self, tbl, form_):
        tbl = globals()[self.db_prefix + tbl.__name__]
        obj = tbl()
            
        for attr in tbl.__table__.columns:
            setattr(obj, attr.name, getattr(form_, attr.name).data)
    
        try:
            self.db.session.add(obj)
            self.db.session.commit()
                
        except Exception as e:
            self.db.session.rollback()
            print(f"ERROR: {str(e)}")

    # fltr = dictionary {attr_name; value}
    def update(self, tbl, fltr, form_):
        obj = self.get_by_id(tbl, fltr)
        tbl = globals()[self.db_prefix + tbl.__name__]
        
        try:
            for attr in tbl.__table__.columns:
                setattr(obj, attr.name, getattr(form_, attr.name).data)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            print(f"ERROR: {str(e)}")
            
    def delete(self, tbl, fltr): 
        obj = self.get_by_id(tbl, fltr)
        tbl = globals()[self.db_prefix + tbl.__name__]   
            
        try:
            self.db.session.delete(obj)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            print(f"ERROR: {str(e)}")
        
    def get_by_id(self, tbl, fltr):
        tbl = globals()[self.db_prefix + tbl.__name__]
        obj = self.db.session.query(tbl)
        for f in fltr:
            obj = obj.filter(
                getattr(tbl, f) == fltr.get(f)
            )
                
        return obj.one()
            
    def make_query(self, regionValue, subjectValue, yearValue):
        if regionValue == '0':
            query = (
                self.db.session.query(
                    func.avg(ormTblZnoMarks.ball100).label('avg_ball'),
                    func.min(ormTblZnoRegion.reg)
                ).join(
                ormTblZnoStudent,
                ormTblZnoStudent.id == ormTblZnoMarks.fk_student_id
                ).join(
                    ormTblZnoRegRegion,
                    ormTblZnoRegRegion.id == ormTblZnoStudent.fk_student_reg
                ).join(
                    ormTblZnoRegion,
                    ormTblZnoRegRegion.fk_region == ormTblZnoRegion.id
                ).filter(
                    ormTblZnoMarks.test_status == 'Зараховано'
                )
            )
        else:
            query = (
                self.db.session.query(
                    func.avg(ormTblZnoMarks.ball100).label('avg_ball'),
                    func.min(ormTblZnoRegion.area)
                ).join(
                    ormTblZnoStudent,
                    ormTblZnoStudent.id == ormTblZnoMarks.fk_student_id
                ).join(
                    ormTblZnoRegRegion,
                    ormTblZnoRegRegion.id == ormTblZnoStudent.fk_student_reg
                ).join(
                    ormTblZnoRegion,
                    ormTblZnoRegRegion.fk_region == ormTblZnoRegion.id
                ).filter(
                    ormTblZnoMarks.test_status == 'Зараховано'
                ).filter(
                    ormTblZnoRegion.reg == regionValue
                )
            )

        if subjectValue != 0:
            query = query.filter(
                ormTblZnoMarks.fk_subject == subjectValue
            )

        if yearValue == 1:
            query = query.filter(
                ormTblZnoStudent.birth >= 2002
            )
        elif yearValue == 2:
            query = query.filter(
                ormTblZnoStudent.birth <= 2002
            )

        if regionValue == 0:
            query = query.group_by(
                ormTblZnoRegion.reg
            ).order_by(
                'avg_ball'
            )
        else:
            query = query.group_by(
                ormTblZnoRegion.area
            ).order_by(
                'avg_ball'
            )
        
        return query.all()
        
        
