from neo4j import GraphDatabase
from loguru import logger

# Import settings from config
from app.core.config import settings


class Neo4jDatabase:
    """Connection manager for Neo4j database"""
    
    def __init__(self):
        self._driver = None
        # Log the connection details for debugging
        logger.info(f"Neo4j will connect to: {settings.NEO4J_URI} with user '{settings.NEO4J_USER}'")

    def get_driver(self):
        """Get or create Neo4j driver"""
        if self._driver is None:
            try:
                logger.info(f"Connecting to Neo4j at {settings.NEO4J_URI}...")
                self._driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                # Verify the connection
                with self._driver.session() as session:
                    logger.info("Testing Neo4j connection...")
                    result = session.run("RETURN 1 AS n")
                    record = result.single()
                    if record is None or record["n"] != 1:
                        raise Exception("Neo4j connection test failed")
                logger.info("Neo4j connection established successfully")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {str(e)}")
                # Try to provide more context about the error
                if "Cannot resolve address" in str(e):
                    logger.error(f"Cannot resolve Neo4j host. Make sure the server is running and accessible at {settings.NEO4J_URI}")
                elif "authentication failure" in str(e).lower():
                    logger.error(f"Neo4j authentication failed. Check your username and password.")
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
    
    def verify_curriculum_structure(self):
        """Verify that the Neo4j database has the expected curriculum structure"""
        try:
            # Check that Chapter nodes exist
            chapter_count = self.run_query_single(
                "MATCH (c:Chapter) RETURN count(c) as count"
            )
            if not chapter_count or chapter_count["count"] == 0:
                logger.warning("No Chapter nodes found in Neo4j database")
                return False
            
            # Check that Requirement nodes exist
            req_count = self.run_query_single(
                "MATCH (r:Requirement) RETURN count(r) as count"
            )
            if not req_count or req_count["count"] == 0:
                logger.warning("No Requirement nodes found in Neo4j database")
                return False
            
            # Check that Goal nodes exist
            goal_count = self.run_query_single(
                "MATCH (g:Goal) RETURN count(g) as count"
            )
            if not goal_count or goal_count["count"] == 0:
                logger.warning("No Goal nodes found in Neo4j database")
                return False
            
            # Check relationships
            rel_check = self.run_query_single(
                """
                MATCH (:Chapter)-[r1:HAS_REQUIREMENT]->(:Requirement)-[r2:HAS_GOAL]->(:Goal)
                RETURN count(r1) > 0 as has_requirements, count(r2) > 0 as has_goals
                """
            )
            if not rel_check or not rel_check["has_requirements"] or not rel_check["has_goals"]:
                logger.warning("Missing required relationships in curriculum structure")
                return False
            
            logger.info("Neo4j curriculum structure verified successfully")
            return True
        except Exception as e:
            logger.error(f"Error verifying Neo4j curriculum structure: {str(e)}")
            return False
    
    def create_curriculum_structure(self):
        """Create basic curriculum structure if it doesn't exist"""
        try:
            # Check if structure already exists
            if self.verify_curriculum_structure():
                logger.info("Curriculum structure already exists")
                return
            
            # Create constraints for unique IDs
            self.run_query("CREATE CONSTRAINT chapter_id IF NOT EXISTS FOR (c:Chapter) REQUIRE c.id IS UNIQUE")
            self.run_query("CREATE CONSTRAINT requirement_id IF NOT EXISTS FOR (r:Requirement) REQUIRE r.id IS UNIQUE")
            self.run_query("CREATE CONSTRAINT goal_id IF NOT EXISTS FOR (g:Goal) REQUIRE g.id IS UNIQUE")
            
            # Create sample curriculum structure
            self.run_query(
                """
                // Create Chapters
                CREATE (c1:Chapter {id: 'C1', name: 'Numbers and Arithmetic', grade_level: 8})
                CREATE (c2:Chapter {id: 'C2', name: 'Algebra and Equations', grade_level: 8})
                CREATE (c3:Chapter {id: 'C3', name: 'Geometry', grade_level: 8})
                
                // Create Requirements for each Chapter
                CREATE (r1:Requirement {id: 'R1', description: 'Understanding real numbers and their properties'})
                CREATE (r2:Requirement {id: 'R2', description: 'Performing arithmetic operations'})
                CREATE (r3:Requirement {id: 'R3', description: 'Solving linear equations'})
                CREATE (r4:Requirement {id: 'R4', description: 'Understanding algebraic expressions'})
                CREATE (r5:Requirement {id: 'R5', description: 'Calculating geometric measurements'})
                CREATE (r6:Requirement {id: 'R6', description: 'Understanding geometric transformations'})
                
                // Create Goals for each Requirement
                CREATE (g1:Goal {id: 'G1', description: 'Classify and compare real numbers'})
                CREATE (g2:Goal {id: 'G2', description: 'Represent numbers on the number line'})
                CREATE (g3:Goal {id: 'G3', description: 'Add and subtract integers'})
                CREATE (g4:Goal {id: 'G4', description: 'Multiply and divide rational numbers'})
                CREATE (g5:Goal {id: 'G5', description: 'Solve linear equations with one variable'})
                CREATE (g6:Goal {id: 'G6', description: 'Solve linear equations with variables on both sides'})
                CREATE (g7:Goal {id: 'G7', description: 'Simplify algebraic expressions'})
                CREATE (g8:Goal {id: 'G8', description: 'Factor quadratic expressions'})
                CREATE (g9:Goal {id: 'G9', description: 'Calculate area and perimeter of polygons'})
                CREATE (g10:Goal {id: 'G10', description: 'Calculate volume and surface area of solids'})
                CREATE (g11:Goal {id: 'G11', description: 'Apply translations, rotations, and reflections'})
                CREATE (g12:Goal {id: 'G12', description: 'Identify congruent and similar shapes'})
                
                // Connect Chapters to Requirements
                CREATE (c1)-[:HAS_REQUIREMENT]->(r1)
                CREATE (c1)-[:HAS_REQUIREMENT]->(r2)
                CREATE (c2)-[:HAS_REQUIREMENT]->(r3)
                CREATE (c2)-[:HAS_REQUIREMENT]->(r4)
                CREATE (c3)-[:HAS_REQUIREMENT]->(r5)
                CREATE (c3)-[:HAS_REQUIREMENT]->(r6)
                
                // Connect Requirements to Goals
                CREATE (r1)-[:HAS_GOAL]->(g1)
                CREATE (r1)-[:HAS_GOAL]->(g2)
                CREATE (r2)-[:HAS_GOAL]->(g3)
                CREATE (r2)-[:HAS_GOAL]->(g4)
                CREATE (r3)-[:HAS_GOAL]->(g5)
                CREATE (r3)-[:HAS_GOAL]->(g6)
                CREATE (r4)-[:HAS_GOAL]->(g7)
                CREATE (r4)-[:HAS_GOAL]->(g8)
                CREATE (r5)-[:HAS_GOAL]->(g9)
                CREATE (r5)-[:HAS_GOAL]->(g10)
                CREATE (r6)-[:HAS_GOAL]->(g11)
                CREATE (r6)-[:HAS_GOAL]->(g12)
                """
            )
            
            logger.info("Created sample curriculum structure in Neo4j")
            
        except Exception as e:
            logger.error(f"Error creating curriculum structure: {str(e)}")
            raise


# Create a Neo4j database instance
neo4j_db = Neo4jDatabase()

def init_neo4j_db():
    """Initialize Neo4j database and verify/create curriculum structure"""
    try:
        # Test connection
        neo4j_db.get_driver()
        
        # Verify/create curriculum structure
        if not neo4j_db.verify_curriculum_structure():
            neo4j_db.create_curriculum_structure()
        
        logger.info("Neo4j database initialized successfully")
    except Exception as e:
        logger.error(f"Neo4j initialization failed: {str(e)}")
        raise