#!/usr/bin/env python3
"""
Script to test Neo4j connection using the simpler approach
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from loguru import logger

# Set up logging
logger.info("Testing Neo4j connection only...")

try:
    # Import Neo4j module
    from app.db.neo4j import neo4j_db
    
    # Test connection
    result = neo4j_db.run_query_single("RETURN 1 as test")
    
    if result and result["test"] == 1:
        logger.info("✅ Neo4j connection successful!")
    else:
        logger.error("Neo4j query returned unexpected result")
        
except Exception as e:
    logger.error(f"Neo4j connection failed: {str(e)}")
    
    # Provide helpful context
    logger.info("Make sure:")
    logger.info("1. Neo4j is running (check if you can access http://localhost:7474 in browser)")
    logger.info("2. Username and password in app/db/neo4j.py are correct")
    logger.info("3. The port 7687 is accessible")
    
    # Check if the database is actually running
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 7687))
    if result == 0:
        logger.info("Port 7687 is open - Neo4j is likely running but credentials may be wrong")
    else:
        logger.info("Port 7687 is not open - Neo4j may not be running")
    sock.close()