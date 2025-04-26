from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jDB:
    def __init__(self):
        self.driver = None
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD

    def connect(self):
        """Connect to Neo4j database"""
        if not self.driver:
            self.driver = GraphDatabase.driver(
                self.uri, auth=(self.user, self.password)
            )
        return self.driver

    def close(self):
        """Close the Neo4j connection"""
        if self.driver:
            self.driver.close()
    
    def get_driver(self):
        """Get the Neo4j driver"""
        if not self.driver:
            self.connect()
        return self.driver

# Create global instance
neo4j_db = Neo4jDB()

def get_neo4j():
    """Dependency to get Neo4j driver"""
    driver = neo4j_db.get_driver()
    return driver