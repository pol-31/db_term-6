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
    def get_attrs(self, tbl):
        pass
        
    @abstractmethod
    def get_value(self, obj, attr):
        pass
        
    @abstractmethod
    def get_new_id(self, tbl):
        pass
        
    @abstractmethod
    def make_query(self, regionValue, subjectValue, yearValue):
        pass


class DatabaseMongo(Database):
    def __init__(self, db_):
        self.db = db_
        self.name = "mongo"
        self.db_prefix = "coll"
        self.bg_color = "orange"

    def get(self, coll, num):
        coll = globals()[self.db_prefix + coll.__name__]
        result = coll.collection.find().limit(num)
        return list(result)
        
    def add(self, coll, form_):
        coll = globals()[self.db_prefix + coll.__name__]
        document = {}
    
        for attr in coll.document:
            try:
                document[attr] = int(getattr(form_, attr).data)
            except:
                document[attr] = getattr(form_, attr).data.rstrip()
    
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
                try:
                    update_query['$set'][attr] = int(getattr(form_, attr).data)
                except:
                    update_query['$set'][attr] = getattr(form_, attr).data.rstrip()
            
            coll.collection.update_one(filter_query, update_query)
            
        except Exception as e:
            print(f"ERROR: {str(e)}")

    def delete(self, coll, fltr):
        coll = globals()[self.db_prefix + coll.__name__]
        filter_query = {}
    
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
            print("attr ", attr)
            print("value ", fltr[attr])
            filter_query[attr] = fltr[attr]
        
        print("filter: ", filter_query)
        result = coll.collection.find_one(filter_query)
        return result
        
    def get_attrs(self, coll):
        coll = globals()[self.db_prefix + coll.__name__]
        return list(coll.document)
        
    def get_value(self, obj, attr):
        return obj[attr]
        
    def get_new_id(self, coll):
        coll = globals()[self.db_prefix + coll.__name__]
        return int(coll.collection.find_one({}, sort=[("id", -1)])["id"]) + 1
        
    def make_query(self, regionValue, subjectValue, yearValue):
        pipeline = []

        if regionValue == '0':
            pipeline = [
                {'$match': {'test_status': 'Зараховано'}},
                {
                    '$lookup': {
                        'from': collZnoStudent.collection.name,
                        'localField': 'fk_student_id',
                        'foreignField': 'id',
                        'as': 'student'
                    }
                },
                {
                    '$lookup': {
                        'from': collZnoRegRegion.collection.name,
                        'localField': 'student.fk_student_reg',
                        'foreignField': 'id',
                        'as': 'reg_region'
                    }
                },
                {
                    '$lookup': {
                        'from': collZnoRegion.collection.name,
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
                }
            ]
        else:
            pipeline = [
                {'$match': {'test_status': 'Зараховано'}},
                {
                    '$lookup': {
                        'from': collZnoStudent.collection.name,
                        'localField': 'fk_student_id',
                        'foreignField': 'id',
                        'as': 'student'
                    }
                },
                {
                    '$lookup': {
                        'from': collZnoRegRegion.collection.name,
                        'localField': 'student.fk_student_reg',
                        'foreignField': 'id',
                        'as': 'reg_region'
                    }
                },
                {
                    '$lookup': {
                        'from': collZnoRegion.collection.name,
                        'localField': 'reg_region.fk_region',
                        'foreignField': 'id',
                        'as': 'region'
                    }
                },
                {'$match': {'region.reg': regionValue}},
                {
                    '$group': {
                        '_id': '$region.area',
                        'avg_ball': {'$avg': '$ball100'},
                        'min_area': {'$min': '$region.area'}
                    }
                }
            ]
    
        if yearValue == 1:
            pipeline.insert(2, {'$match': {'student.birth': {'$gte': 2002}}})
        elif yearValue == 2:
            pipeline.insert(2, {'$match': {'student.birth': {'$lte': 2002}}})
    
        if subjectValue != 0:
            pipeline.insert(1, {'$match': {'fk_subject': subjectValue}})
    
        result = collZnoMarks.collection.aggregate(pipeline)
        
        avg_ball = []
        reg = []
        for i in result:
            reg = reg + i['_id']
            avg_ball.append(i['avg_ball'])
        return tuple(avg_ball), tuple(reg)


class DatabasePostgre(Database):
    def __init__(self, db_):
        self.db = db_
        self.name = "postgre"
        self.db_prefix = "ormTbl"
        self.bg_color = "green"

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
        
    def get_attrs(self, tbl):
        tbl = globals()[self.db_prefix + tbl.__name__]
        attrs = []
        for i in tbl.__table__.columns:
            attrs.append(i.name)
        return attrs
        
    def get_value(self, obj, attr):
        return getattr(obj, attr)
        
    def get_new_id(self, tbl):
        tbl = globals()[self.db_prefix + tbl.__name__]
        return self.db.session.query(func.max(tbl.id)).scalar() + 1
            
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
        result = query.all()
        return zip(*result)
        
        
