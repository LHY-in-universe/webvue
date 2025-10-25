#!/usr/bin/env python3
"""
Comprehensive API test cases for projects.py endpoints
Tests all endpoints and identifies issues
Updated with proper authentication flow
"""

import requests
import json
import time
from typing import Dict, Any, List
import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from test_auth_helper import TestAuthHelper

# Base URL for the API
BASE_URL = "http://localhost:8000"
PROJECTS_BASE = f"{BASE_URL}/api/edgeai/projects"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.created_project_id = None
        self.auth_helper = TestAuthHelper()
    
    def get_headers(self):
        """获取带认证的请求头"""
        return self.auth_helper.get_headers()
        
    def log_test(self, test_name: str, success: bool, message: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "response_data": response_data,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
    
    def test_get_projects(self):
        """Test GET /edgeai/projects/ - Get all projects"""
        try:
            response = self.session.get(f"{PROJECTS_BASE}/", headers=self.get_headers())
            success = response.status_code == 200
            self.log_test(
                "GET /projects/", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("GET /projects/", False, f"Exception: {str(e)}")
            return False
    
    def test_get_projects_with_filters(self):
        """Test GET /edgeai/projects/ with query parameters"""
        try:
            # Test with status filter
            response = self.session.get(f"{PROJECTS_BASE}/?status=created", headers=self.get_headers())
            success = response.status_code == 200
            self.log_test(
                "GET /projects/ with status filter", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            
            # Test with search parameter
            response = self.session.get(f"{PROJECTS_BASE}/?search=test", headers=self.get_headers())
            success = response.status_code == 200
            self.log_test(
                "GET /projects/ with search filter", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            
            return success
        except Exception as e:
            self.log_test("GET /projects/ with filters", False, f"Exception: {str(e)}")
            return False
    
    def test_create_project(self):
        """Test POST /edgeai/projects/ - Create new project"""
        try:
            project_data = {
                "name": "Test Project API",
                "description": "Test project created by API test",
                "model": "test-model",
                "nodes": [
                    {"ip": "192.168.1.100", "name": "Test Node 1"},
                    {"ip": "192.168.1.101", "name": "Test Node 2"}
                ],
                "training_alg": "sft",
                "fed_alg": "fedavg",
                "secure_aggregation": "shamir_threshold",
                "total_epochs": 50,
                "num_rounds": 5,
                "batch_size": 16,
                "lr": "1e-3",
                "num_computers": 2,
                "threshold": 2,
                "num_clients": 2,
                "sample_clients": 2,
                "max_steps": 50,
                "model_name_or_path": "test-model",
                "dataset_name": "test-dataset",
                "dataset_sample": 100
            }
            
            response = self.session.post(f"{PROJECTS_BASE}/", json=project_data, headers=self.get_headers())
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                self.created_project_id = response_data.get("id")
                self.log_test(
                    "POST /projects/", 
                    success, 
                    f"Status: {response.status_code}, Created ID: {self.created_project_id}",
                    response_data
                )
            else:
                self.log_test(
                    "POST /projects/", 
                    success, 
                    f"Status: {response.status_code}",
                    response.text
                )
            
            return success
        except Exception as e:
            self.log_test("POST /projects/", False, f"Exception: {str(e)}")
            return False
    
    def test_get_project_by_id(self):
        """Test GET /edgeai/projects/{project_id}/ - Get specific project"""
        if not self.created_project_id:
            self.log_test("GET /projects/{id}/", False, "No project ID available")
            return False
            
        try:
            response = self.session.get(f"{PROJECTS_BASE}/{self.created_project_id}/")
            success = response.status_code == 200
            self.log_test(
                "GET /projects/{id}/", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("GET /projects/{id}/", False, f"Exception: {str(e)}")
            return False
    
    def test_update_project(self):
        """Test PUT /edgeai/projects/{project_id} - Update project"""
        if not self.created_project_id:
            self.log_test("PUT /projects/{id}", False, "No project ID available")
            return False
            
        try:
            update_data = {
                "name": "Updated Test Project",
                "description": "Updated test project description",
                "model": "updated-model",
                "nodes": [
                    {"ip": "192.168.1.200", "name": "Updated Node 1"}
                ],
                "training_alg": "dpo",
                "fed_alg": "fedygi",
                "secure_aggregation": "shamir_threshold",
                "total_epochs": 100,
                "num_rounds": 10,
                "batch_size": 32,
                "lr": "1e-4",
                "num_computers": 3,
                "threshold": 2,
                "num_clients": 3,
                "sample_clients": 2,
                "max_steps": 100,
                "model_name_or_path": "updated-model",
                "dataset_name": "updated-dataset",
                "dataset_sample": 200
            }
            
            response = self.session.put(f"{PROJECTS_BASE}/{self.created_project_id}", json=update_data)
            success = response.status_code == 200
            self.log_test(
                "PUT /projects/{id}", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("PUT /projects/{id}", False, f"Exception: {str(e)}")
            return False
    
    def test_project_operations(self):
        """Test project control operations (start, pause, stop)"""
        if not self.created_project_id:
            self.log_test("Project operations", False, "No project ID available")
            return False
            
        operations = [
            ("start", "POST /projects/{id}/start"),
            ("pause", "POST /projects/{id}/pause"),
            ("stop", "POST /projects/{id}/stop")
        ]
        
        for operation, test_name in operations:
            try:
                response = self.session.post(f"{PROJECTS_BASE}/{self.created_project_id}/{operation}")
                success = response.status_code == 200
                self.log_test(
                    test_name, 
                    success, 
                    f"Status: {response.status_code}",
                    response.json() if success else response.text
                )
            except Exception as e:
                self.log_test(test_name, False, f"Exception: {str(e)}")
    
    def test_duplicate_project(self):
        """Test POST /edgeai/projects/{project_id}/duplicate - Duplicate project"""
        if not self.created_project_id:
            self.log_test("POST /projects/{id}/duplicate", False, "No project ID available")
            return False
            
        try:
            response = self.session.post(f"{PROJECTS_BASE}/{self.created_project_id}/duplicate")
            success = response.status_code == 200
            self.log_test(
                "POST /projects/{id}/duplicate", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("POST /projects/{id}/duplicate", False, f"Exception: {str(e)}")
            return False
    
    def test_project_visualization(self):
        """Test GET /edgeai/projects/{project_id}/visualization - Get project visualization"""
        if not self.created_project_id:
            self.log_test("GET /projects/{id}/visualization", False, "No project ID available")
            return False
            
        try:
            response = self.session.get(f"{PROJECTS_BASE}/{self.created_project_id}/visualization")
            success = response.status_code == 200
            self.log_test(
                "GET /projects/{id}/visualization", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("GET /projects/{id}/visualization", False, f"Exception: {str(e)}")
            return False
    
    def test_import_project(self):
        """Test POST /edgeai/projects/import - Import project"""
        try:
            import_data = {
                "project_data": {
                    "name": "Imported Test Project",
                    "description": "Imported from test",
                    "type": "Computer Vision"
                },
                "overwrite": False
            }
            
            response = self.session.post(f"{PROJECTS_BASE}/import", json=import_data, headers=self.get_headers())
            success = response.status_code == 200
            self.log_test(
                "POST /projects/import", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("POST /projects/import", False, f"Exception: {str(e)}")
            return False
    
    def test_export_project(self):
        """Test POST /edgeai/projects/{project_id}/export - Export project"""
        if not self.created_project_id:
            self.log_test("POST /projects/{id}/export", False, "No project ID available")
            return False
            
        try:
            export_data = {
                "include_models": True,
                "include_data": False,
                "format": "json"
            }
            
            response = self.session.post(f"{PROJECTS_BASE}/{self.created_project_id}/export", json=export_data)
            success = response.status_code == 200
            self.log_test(
                "POST /projects/{id}/export", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("POST /projects/{id}/export", False, f"Exception: {str(e)}")
            return False
    
    def test_system_stats(self):
        """Test GET /edgeai/projects/stats/overview - Get system stats"""
        try:
            response = self.session.get(f"{PROJECTS_BASE}/stats/overview")
            success = response.status_code == 200
            self.log_test(
                "GET /projects/stats/overview", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("GET /projects/stats/overview", False, f"Exception: {str(e)}")
            return False
    
    def test_project_templates(self):
        """Test GET /edgeai/projects/templates - Get project templates"""
        try:
            response = self.session.get(f"{PROJECTS_BASE}/templates")
            success = response.status_code == 200
            self.log_test(
                "GET /projects/templates", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("GET /projects/templates", False, f"Exception: {str(e)}")
            return False
    
    def test_import_history(self):
        """Test GET /edgeai/projects/import-history - Get import history"""
        try:
            response = self.session.get(f"{PROJECTS_BASE}/import-history")
            success = response.status_code == 200
            self.log_test(
                "GET /projects/import-history", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("GET /projects/import-history", False, f"Exception: {str(e)}")
            return False
    
    def test_load_from_url(self):
        """Test POST /edgeai/projects/load-from-url - Load project from URL"""
        try:
            url_data = {
                "url": "https://example.com/project-config.json"
            }
            
            response = self.session.post(f"{PROJECTS_BASE}/load-from-url", json=url_data)
            success = response.status_code == 200
            self.log_test(
                "POST /projects/load-from-url", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("POST /projects/load-from-url", False, f"Exception: {str(e)}")
            return False
    
    def test_delete_project(self):
        """Test DELETE /edgeai/projects/{project_id} - Delete project"""
        if not self.created_project_id:
            self.log_test("DELETE /projects/{id}", False, "No project ID available")
            return False
            
        try:
            response = self.session.delete(f"{PROJECTS_BASE}/{self.created_project_id}")
            success = response.status_code == 200
            self.log_test(
                "DELETE /projects/{id}", 
                success, 
                f"Status: {response.status_code}",
                response.json() if success else response.text
            )
            return success
        except Exception as e:
            self.log_test("DELETE /projects/{id}", False, f"Exception: {str(e)}")
            return False
    
    def test_error_cases(self):
        """Test error cases"""
        # Test invalid project ID
        try:
            response = self.session.get(f"{PROJECTS_BASE}/invalid_id/")
            success = response.status_code == 400
            self.log_test(
                "GET /projects/invalid_id/ (error case)", 
                success, 
                f"Status: {response.status_code}",
                response.text
            )
        except Exception as e:
            self.log_test("GET /projects/invalid_id/ (error case)", False, f"Exception: {str(e)}")
        
        # Test non-existent project ID
        try:
            response = self.session.get(f"{PROJECTS_BASE}/99999/")
            success = response.status_code == 404
            self.log_test(
                "GET /projects/99999/ (not found)", 
                success, 
                f"Status: {response.status_code}",
                response.text
            )
        except Exception as e:
            self.log_test("GET /projects/99999/ (not found)", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all test cases with authentication"""
        print("🚀 Starting comprehensive API tests for projects.py endpoints...")
        print("=" * 80)
        
        # 设置认证
        print("🔐 Setting up authentication...")
        if not self.auth_helper.setup_auth():
            print("❌ Failed to setup authentication. Cannot run tests.")
            return
        
        try:
            # Test basic endpoints first
            self.test_get_projects()
            self.test_get_projects_with_filters()
            self.test_system_stats()
            self.test_project_templates()
            self.test_import_history()
            
            # Test project creation and management
            self.test_create_project()
            if self.created_project_id:
                self.test_get_project_by_id()
                self.test_update_project()
                self.test_project_operations()
                self.test_duplicate_project()
                self.test_project_visualization()
                self.test_export_project()
            
            # Test import functionality
            self.test_import_project()
            self.test_load_from_url()
            
            # Test error cases
            self.test_error_cases()
            
            # Clean up - delete created project
            if self.created_project_id:
                self.test_delete_project()
            
            # Print summary
            self.print_summary()
            
        finally:
            # 清理认证
            print("\n🔐 Cleaning up authentication...")
            self.auth_helper.cleanup_auth()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        print("\n" + "=" * 80)

def main():
    """Main function"""
    tester = APITester()
    tester.run_all_tests()
    
    # Exit with error code if any tests failed
    failed_tests = sum(1 for result in tester.test_results if not result["success"])
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()
