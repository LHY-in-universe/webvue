#!/usr/bin/env python3
"""
Test script for the Cluster API endpoints
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/edgeai/clusters"

def test_cluster_api():
    """Test the cluster API endpoints"""
    
    print("Testing Cluster API...")
    
    # Test data
    test_cluster = {
        "name": "Test Cluster",
        "project_id": 1
    }
    
    # Test 1: Create a cluster
    print("\n1. Testing cluster creation...")
    try:
        response = requests.post(f"{BASE_URL}/", json=test_cluster)
        if response.status_code == 200:
            cluster_data = response.json()
            cluster_id = cluster_data["id"]
            print(f"✅ Cluster created successfully with ID: {cluster_id}")
        else:
            print(f"❌ Failed to create cluster: {response.status_code} - {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure the server is running on localhost:8000")
        return
    
    # Test 2: Get all clusters
    print("\n2. Testing get all clusters...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            clusters = response.json()
            print(f"✅ Retrieved {len(clusters)} clusters")
        else:
            print(f"❌ Failed to get clusters: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error getting clusters: {e}")
    
    # Test 3: Get specific cluster
    print(f"\n3. Testing get specific cluster (ID: {cluster_id})...")
    try:
        response = requests.get(f"{BASE_URL}/{cluster_id}/")
        if response.status_code == 200:
            cluster = response.json()
            print(f"✅ Retrieved cluster: {cluster['name']}")
        else:
            print(f"❌ Failed to get cluster: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error getting cluster: {e}")
    
    # Test 4: Update cluster
    print(f"\n4. Testing update cluster (ID: {cluster_id})...")
    update_data = {
        "name": "Updated Test Cluster",
        "project_id": 2
    }
    try:
        response = requests.put(f"{BASE_URL}/{cluster_id}", json=update_data)
        if response.status_code == 200:
            updated_cluster = response.json()
            print(f"✅ Cluster updated successfully: {updated_cluster['name']}")
        else:
            print(f"❌ Failed to update cluster: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error updating cluster: {e}")
    
    # Test 5: Get user clusters
    print("\n5. Testing get user clusters...")
    try:
        response = requests.get(f"{BASE_URL}/user/1/clusters")
        if response.status_code == 200:
            user_clusters = response.json()
            print(f"✅ Retrieved {len(user_clusters)} clusters for user 1")
        else:
            print(f"❌ Failed to get user clusters: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error getting user clusters: {e}")
    
    # Test 6: Get project clusters
    print("\n6. Testing get project clusters...")
    try:
        response = requests.get(f"{BASE_URL}/project/1/clusters")
        if response.status_code == 200:
            project_clusters = response.json()
            print(f"✅ Retrieved {len(project_clusters)} clusters for project 1")
        else:
            print(f"❌ Failed to get project clusters: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error getting project clusters: {e}")
    
    # Test 7: Delete cluster
    print(f"\n7. Testing delete cluster (ID: {cluster_id})...")
    try:
        response = requests.delete(f"{BASE_URL}/{cluster_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Cluster deleted successfully: {result['message']}")
        else:
            print(f"❌ Failed to delete cluster: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error deleting cluster: {e}")
    
    print("\n🎉 Cluster API testing completed!")

if __name__ == "__main__":
    test_cluster_api()
