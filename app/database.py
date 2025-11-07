from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    """데이터베이스 연결을 관리하는 클래스"""
    client: AsyncIOMotorClient = None
    
    async def connect_db(self):
        """MongoDB에 연결하는 메서드"""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        
    async def close_db(self):
        """MongoDB 연결을 닫는 메서드"""
        if self.client:
            self.client.close()
            
    def get_db(self):
        """데이터베이스 객체를 반환하는 메서드"""
        return self.client[settings.DATABASE_NAME]

# 전역 데이터베이스 인스턴스
db = Database() 