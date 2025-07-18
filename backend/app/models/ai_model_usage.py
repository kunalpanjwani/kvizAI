"""
AIModelUsage model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, UUIDType


class AIModelUsage(Base):
    """AIModelUsage model for tracking AI model performance"""
    
    __tablename__ = "ai_model_usage"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Model information
    model_name = Column(String(100), nullable=False)  # llama2, gemini, etc.
    model_version = Column(String(50), nullable=True)
    
    # Usage statistics
    request_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    
    # Performance metrics
    total_processing_time = Column(Integer, default=0)  # milliseconds
    average_processing_time = Column(Integer, default=0)  # milliseconds
    min_processing_time = Column(Integer, nullable=True)  # milliseconds
    max_processing_time = Column(Integer, nullable=True)  # milliseconds
    
    # Error tracking
    last_error = Column(Text, nullable=True)
    last_error_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Date tracking
    date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<AIModelUsage(id={self.id}, model_name='{self.model_name}', date={self.date})>"
    
    def record_request(self, processing_time: int = None, success: bool = True, error: str = None):
        """Record a new request"""
        self.request_count += 1
        
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
            self.last_error = error
            self.last_error_at = func.now()
        
        if processing_time:
            self.total_processing_time += processing_time
            self.average_processing_time = self.total_processing_time // self.request_count
            
            if self.min_processing_time is None or processing_time < self.min_processing_time:
                self.min_processing_time = processing_time
            
            if self.max_processing_time is None or processing_time > self.max_processing_time:
                self.max_processing_time = processing_time
        
        self.last_used_at = func.now()
    
    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        if self.request_count > 0:
            return int((self.success_count / self.request_count) * 100)
        return 0 