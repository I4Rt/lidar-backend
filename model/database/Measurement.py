from config import *
from model.database.BaseData import BaseData 
from tools.DBSessionMaker import *

class Measurement(BaseData):
    __tablename__ = 'Measurement'
    
    text = Column(Text, unique=False)
    
    h_1_1   = Column(Double, nullable=False)
    h_1_2   = Column(Double, nullable=False)
    h_1_3   = Column(Double, nullable=False)
    
    h_2_1   = Column(Double, nullable=False)
    h_2_2   = Column(Double, nullable=False)
    h_2_3   = Column(Double, nullable=False)
    
    l_1_1   = Column(Double, nullable=False)
    l_1_2   = Column(Double, nullable=False)
    l_1_3   = Column(Double, nullable=False)
    
    l_2_1   = Column(Double, nullable=False)
    l_2_2   = Column(Double, nullable=False)
    l_2_3   = Column(Double, nullable=False)
    
    w_1_1    = Column(Double, nullable=False)
    w_1_2    = Column(Double, nullable=False)
    w_1_3    = Column(Double, nullable=False)

    w_2_1    = Column(Double, nullable=False)
    w_2_2    = Column(Double, nullable=False)
    w_2_3    = Column(Double, nullable=False)
    
    is_sent = Column(Boolean, nullable=False, default=False)
    
    def __init__(self, h_1_1, h_1_2, h_1_3, 
                       h_2_1, h_2_2, h_2_3,
                       l_1_1, l_1_2, l_1_3, 
                       l_2_1, l_2_2, l_2_3,
                       w_1_1, w_1_2, w_1_3, 
                       w_2_1, w_2_2, w_2_3,
                       ):
        BaseData.__init__(self)
        
        self.h_1_1   = h_1_1
        self.h_1_2   = h_1_2
        self.h_1_3   = h_1_3
        
        self.h_2_1   = h_2_1
        self.h_2_2   = h_2_2
        self.h_2_3   = h_2_3
        
        self.l_1_1   = l_1_1
        self.l_1_2   = l_1_2
        self.l_1_3   = l_1_3
        
        self.l_2_1   = l_2_1
        self.l_2_2   = l_2_2
        self.l_2_3   = l_2_3
        
        self.w_1_1   = w_1_1
        self.w_1_2   = w_1_2
        self.w_1_3   = w_1_3
        
        self.w_2_1   = w_2_1
        self.w_2_2   = w_2_2
        self.w_2_3   = w_2_3
        
        self.is_sent = False

    @classmethod        
    def getLastNotSent(cls) -> "Measurement":
        with DBSessionMaker.getSession() as ses:
            return ses.query(cls).filter_by(is_sent=False).order_by(cls.id).first() 
        
    def setSent(self):
        with DBSessionMaker.getSession() as ses:
            print('set', self.id)
            self.is_sent = True
            ses.add(self)
            ses.commit()
            return True
        