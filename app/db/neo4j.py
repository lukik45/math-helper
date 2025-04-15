from neo4j import GraphDatabase
from loguru import logger

from app.core.config import settings


class Neo4jDatabase:
    """Connection manager for Neo4j database"""
    
    def __init__(self):
        self._driver = None

    def get_driver(self):
        """Get or create Neo4j driver"""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                # Verify the connection
                with self._driver.session() as session:
                    result = session.run("RETURN 1 AS n")
                    record = result.single()
                    if record is None or record["n"] != 1:
                        raise Exception("Neo4j connection test failed")
                logger.info("Neo4j connection established")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {str(e)}")
                raise
        return self._driver
    
    def close(self):
        """Close the Neo4j driver"""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")
    
    def session(self):
        """Get a Neo4j session"""
        return self.get_driver().session()
    
    def run_query(self, query, parameters=None):
        """Run a query and return all results"""
        with self.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]
    
    def run_query_single(self, query, parameters=None):
        """Run a query and return a single result"""
        with self.session() as session:
            result = session.run(query, parameters or {})
            return result.single()


# Create a Neo4j database instance
neo4j_db = Neo4jDatabase()