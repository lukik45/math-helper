# Models representing Neo4j curriculum nodes
from typing import List, Dict, Any, Optional


class Chapter:
    """
    Chapter node in Neo4j
    
    Represents a chapter in the Polish math curriculum.
    """
    id: str
    name: str
    grade_level: int
    
    def __init__(self, id: str, name: str, grade_level: int):
        self.id = id
        self.name = name
        self.grade_level = grade_level
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Chapter":
        """Create a Chapter instance from a dictionary"""
        return Chapter(
            id=data.get("id"),
            name=data.get("name"),
            grade_level=data.get("grade_level")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Chapter to a dictionary for Neo4j"""
        return {
            "id": self.id,
            "name": self.name,
            "grade_level": self.grade_level
        }


class Requirement:
    """
    Requirement node in Neo4j
    
    Represents a specific requirement from the Polish math curriculum.
    """
    id: str
    description: str
    
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Requirement":
        """Create a Requirement instance from a dictionary"""
        return Requirement(
            id=data.get("id"),
            description=data.get("description")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Requirement to a dictionary for Neo4j"""
        return {
            "id": self.id,
            "description": self.description
        }


class Goal:
    """
    Goal node in Neo4j
    
    Represents an educational goal associated with requirements.
    """
    id: str
    description: str
    
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Goal":
        """Create a Goal instance from a dictionary"""
        return Goal(
            id=data.get("id"),
            description=data.get("description")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Goal to a dictionary for Neo4j"""
        return {
            "id": self.id,
            "description": self.description
        }


class CurriculumService:
    """
    Service class for interacting with curriculum data in Neo4j
    """
    def __init__(self, neo4j_db):
        self.neo4j_db = neo4j_db
    
    def get_all_chapters(self) -> List[Chapter]:
        """Get all chapters from the curriculum"""
        records = self.neo4j_db.run_query(
            "MATCH (c:Chapter) RETURN c.id as id, c.name as name, c.grade_level as grade_level"
        )
        return [Chapter.from_dict(record) for record in records]
    
    def get_requirements_by_chapter(self, chapter_id: str) -> List[Requirement]:
        """Get all requirements for a specific chapter"""
        records = self.neo4j_db.run_query(
            """
            MATCH (c:Chapter {id: $chapter_id})-[:HAS_REQUIREMENT]->(r:Requirement)
            RETURN r.id as id, r.description as description
            """,
            {"chapter_id": chapter_id}
        )
        return [Requirement.from_dict(record) for record in records]
    
    def get_goals_by_requirement(self, requirement_id: str) -> List[Goal]:
        """Get all goals for a specific requirement"""
        records = self.neo4j_db.run_query(
            """
            MATCH (r:Requirement {id: $requirement_id})-[:HAS_GOAL]->(g:Goal)
            RETURN g.id as id, g.description as description
            """,
            {"requirement_id": requirement_id}
        )
        return [Goal.from_dict(record) for record in records]
    
    def get_all_goals(self) -> List[Goal]:
        """Get all goals from the curriculum"""
        records = self.neo4j_db.run_query(
            "MATCH (g:Goal) RETURN g.id as id, g.description as description"
        )
        return [Goal.from_dict(record) for record in records]