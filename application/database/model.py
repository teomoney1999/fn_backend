import uuid
from sqlalchemy.dialects.postgresql import UUID

#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, String, Integer, BigInteger,
    DateTime, Date, Boolean,
    event, func
)

from application.database import db
from application.common.helpers import now_timestamp

def default_uuid():
    return str(uuid.uuid4())

def model_oncreate_listener(mapper, connection, instance):
    instance.created_at = now_timestamp()
    instance.updated_at = now_timestamp()
    instance.revision = str(now_timestamp())
    
def model_onupdate_listener(mapper, connection, instance):
    instance.created_at = instance.created_at
    instance.updated_at = instance.updated_at
    instance.revision = str(now_timestamp())
    if instance.deleted is True:
        instance.deleted_at = now_timestamp()
        
def adjacency_model_oncreate_listener(mapper, connection, instance):
    #print "adjacency_model_oncreate_listener"
    
    pass
    
def adjacency_model_onupdate_listener(mapper, connection, instance):
    #print "adjacency_model_onupdate_listener"
    #phai biet cap tren cua model la gi?
    children = instance.children_ids()
    if( instance.parent_id in children):
        pass
        #raise ProcessingException(description=u'Parent node is not correct',code=401)


def adjacency_model_ondelete_listener(mapper, connection, instance):
    #print "adjacency_model_onupdate_listener"
    children = instance.children_ids()
    if len(children) > 1:
        pass
        #raise ProcessingException(description=u'Can not delete non empty adjacency model',code=401)

class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(String(255), index=True, primary_key=True, default=default_uuid)
    created_at = db.Column(BigInteger, index=True, default=now_timestamp)
    created_by = db.Column(String, index=True, nullable=True)
    # created_by_name = db.Column(String)
    updated_at = db.Column(BigInteger, index=True, default=now_timestamp)
    updated_by = db.Column(String, index=True, nullable=True)
    # updated_by_name = db.Column(String)
    deleted = db.Column(Boolean, default=False)
    deleted_by = db.Column(String, index=True, nullable=True)
    deleted_at = db.Column(BigInteger, index=True, default=now_timestamp)
    # deleted_by_name = db.Column(String)
    # revision = db.Column(String(255))
    

event.listen(CommonModel, 'before_insert', model_oncreate_listener, propagate=True)
event.listen(CommonModel, 'before_update', model_onupdate_listener, propagate=True)


class CommonAdjacencyModel(CommonModel):
    __abstract__ = True
    def __todict__(self):
        return {"id":self.id}
    
    def dump(self, _indent=0):
        obj = self.__todict__()
        obj["children"] = [c.dump() for c in self.children.values()]
        return obj
    
    def _children_ids(self, data):
        if type(data) is list:
            data.append(self.id)
            for r in self.children.values():
                r._children_ids(data)
    
    def children_ids(self):
        data = []
        self._children_ids(data)
        return data
    
    #validate break chain insert,delete,update
    
event.listen(CommonAdjacencyModel, 'before_insert', adjacency_model_oncreate_listener, propagate=True)
event.listen(CommonAdjacencyModel, 'before_update', adjacency_model_onupdate_listener, propagate=True)
event.listen(CommonAdjacencyModel, 'before_delete', adjacency_model_ondelete_listener, propagate=True)