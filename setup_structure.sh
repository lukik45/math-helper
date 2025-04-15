#!/bin/bash

# Create base directories
mkdir -p ai-math-tutor/.github/workflows
mkdir -p ai-math-tutor/app/{api,core,db,models,schemas,services}
mkdir -p ai-math-tutor/frontend/{pages,components,utils}
mkdir -p ai-math-tutor/tests/{test_api,test_services}

# Create empty files
touch ai-math-tutor/.github/workflows/main.yml

touch ai-math-tutor/app/api/__init__.py
touch ai-math-tutor/app/api/auth.py
touch ai-math-tutor/app/api/curriculum.py
touch ai-math-tutor/app/api/problems.py
touch ai-math-tutor/app/api/progress.py

touch ai-math-tutor/app/core/__init__.py
touch ai-math-tutor/app/core/config.py
touch ai-math-tutor/app/core/security.py
touch ai-math-tutor/app/core/utils.py

touch ai-math-tutor/app/db/__init__.py
touch ai-math-tutor/app/db/base.py
touch ai-math-tutor/app/db/neo4j.py
touch ai-math-tutor/app/db/postgres.py

touch ai-math-tutor/app/models/__init__.py
touch ai-math-tutor/app/models/curriculum.py
touch ai-math-tutor/app/models/problems.py
touch ai-math-tutor/app/models/users.py

touch ai-math-tutor/app/schemas/__init__.py
touch ai-math-tutor/app/schemas/auth.py
touch ai-math-tutor/app/schemas/curriculum.py
touch ai-math-tutor/app/schemas/problems.py
touch ai-math-tutor/app/schemas/progress.py

touch ai-math-tutor/app/services/__init__.py
touch ai-math-tutor/app/services/curriculum_matching.py
touch ai-math-tutor/app/services/openai_integration.py
touch ai-math-tutor/app/services/progress_tracking.py

touch ai-math-tutor/app/__init__.py
touch ai-math-tutor/app/main.py

touch ai-math-tutor/frontend/pages/1_🏠_Home.py
touch ai-math-tutor/frontend/pages/2_🧮_Problem_Solver.py
touch ai-math-tutor/frontend/pages/3_📊_Progress.py
touch ai-math-tutor/frontend/pages/4_⚙️_Settings.py

touch ai-math-tutor/frontend/components/__init__.py
touch ai-math-tutor/frontend/components/authentication.py
touch ai-math-tutor/frontend/components/problem_input.py
touch ai-math-tutor/frontend/components/solution_display.py

touch ai-math-tutor/frontend/utils/__init__.py
touch ai-math-tutor/frontend/utils/api.py
touch ai-math-tutor/frontend/utils/session.py

touch ai-math-tutor/tests/__init__.py
touch ai-math-tutor/tests/conftest.py
touch ai-math-tutor/tests/test_api/__init__.py
touch ai-math-tutor/tests/test_api/test_auth.py
touch ai-math-tutor/tests/test_api/test_curriculum.py
touch ai-math-tutor/tests/test_api/test_problems.py

touch ai-math-tutor/tests/test_services/__init__.py
touch ai-math-tutor/tests/test_services/test_curriculum_matching.py
touch ai-math-tutor/tests/test_services/test_openai_integration.py

# Root-level files
touch ai-math-tutor/.gitignore
touch ai-math-tutor/Dockerfile
touch ai-math-tutor/docker-compose.yml
touch ai-math-tutor/requirements.txt
touch ai-math-tutor/requirements-dev.txt
touch ai-math-tutor/README.md

echo "✅ Project structure for ai-math-tutor created!"
