#!/usr/bin/env python3
"""
Script to test database connections and verify setup.
Run this script after setting up your environment variables to test connectivity.
"""

import os
import sys
import time
from pathlib import Path

# Add parent directory to path to import app modules
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

# Configure environment variables
from dotenv import load_dotenv
load_dotenv()

import logging
from loguru import logger
from sqlalchemy import text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger.info("Testing database connections...")

try:
    # Import database modules
    from app.db.sqlite import init_sqlite_db, SessionLocal
    from app.db.neo4j import neo4j_db, init_neo4j_db
    
    # Test SQLite connection
    logger.info("Testing SQLite connection...")
    init_sqlite_db()
    db = SessionLocal()
    result = db.execute(text("SELECT 1")).fetchone()
    assert result[0] == 1, "SQLite test query failed"
    db.close()
    logger.info("✅ SQLite connection successful!")
    
    # Test Neo4j connection
    logger.info("Testing Neo4j connection...")
    init_neo4j_db()
    result = neo4j_db.run_query_single("RETURN 1 as test")
    assert result and result["test"] == 1, "Neo4j test query failed"
    logger.info("✅ Neo4j connection successful!")
    
    # Verify curriculum structure
    logger.info("Verifying Neo4j curriculum structure...")
    structure_valid = neo4j_db.verify_curriculum_structure()
    if structure_valid:
        logger.info("✅ Neo4j curriculum structure is valid")
    else:
        logger.warning("⚠️ Neo4j curriculum structure is incomplete or invalid")
        
        # Prompt to create structure
        if input("Do you want to create sample curriculum structure? (y/n): ").lower() == 'y':
            neo4j_db.create_curriculum_structure()
            logger.info("Created sample curriculum structure")
    
    # Test completed
    logger.info("All database tests completed successfully!")
    
except Exception as e:
    logger.error(f"Database connection test failed: {str(e)}")
    sys.exit(1)