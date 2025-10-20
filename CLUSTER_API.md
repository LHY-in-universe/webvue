# Cluster API Documentation

This document describes the Cluster API endpoints for managing clusters in the Edge AI system.

## Overview

The Cluster API provides endpoints for creating, reading, updating, and deleting clusters. Clusters are associated with users and can optionally be linked to projects.

## Database Schema

```sql
CREATE TABLE cluster (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    project_id INT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_project_id (project_id)
);
```

## API Endpoints

### Base URL
```
/api/edgeai/clusters
```

### 1. Create Cluster
**POST** `/api/edgeai/clusters/`

Creates a new cluster.

**Request Body:**
```json
{
    "name": "My Cluster",
    "project_id": 1  // Optional
}
```

**Response:**
```json
{
    "id": "1",
    "name": "My Cluster",
    "user_id": 1,
    "project_id": 1,
    "created_time": "2024-01-15T10:30:00Z",
    "last_updated_time": "2024-01-15T10:30:00Z"
}
```

### 2. Get All Clusters
**GET** `/api/edgeai/clusters/`

Retrieves all clusters with optional filtering.

**Query Parameters:**
- `user_id` (optional): Filter by user ID
- `project_id` (optional): Filter by project ID
- `search` (optional): Search by cluster name

**Response:**
```json
[
    {
        "id": "1",
        "name": "My Cluster",
        "user_id": 1,
        "project_id": 1,
        "created_time": "2024-01-15T10:30:00Z",
        "last_updated_time": "2024-01-15T10:30:00Z"
    }
]
```

### 3. Get Specific Cluster
**GET** `/api/edgeai/clusters/{cluster_id}/`

Retrieves a specific cluster by ID.

**Response:**
```json
{
    "id": "1",
    "name": "My Cluster",
    "user_id": 1,
    "project_id": 1,
    "created_time": "2024-01-15T10:30:00Z",
    "last_updated_time": "2024-01-15T10:30:00Z"
}
```

### 4. Update Cluster
**PUT** `/api/edgeai/clusters/{cluster_id}`

Updates an existing cluster.

**Request Body:**
```json
{
    "name": "Updated Cluster Name",  // Optional
    "project_id": 2  // Optional
}
```

**Response:**
```json
{
    "id": "1",
    "name": "Updated Cluster Name",
    "user_id": 1,
    "project_id": 2,
    "created_time": "2024-01-15T10:30:00Z",
    "last_updated_time": "2024-01-15T11:00:00Z"
}
```

### 5. Delete Cluster
**DELETE** `/api/edgeai/clusters/{cluster_id}`

Deletes a cluster.

**Response:**
```json
{
    "success": true,
    "message": "Cluster 'My Cluster' deleted successfully"
}
```

### 6. Get User Clusters
**GET** `/api/edgeai/clusters/user/{user_id}/clusters`

Retrieves all clusters for a specific user.

**Response:**
```json
[
    {
        "id": "1",
        "name": "My Cluster",
        "user_id": 1,
        "project_id": 1,
        "created_time": "2024-01-15T10:30:00Z",
        "last_updated_time": "2024-01-15T10:30:00Z"
    }
]
```

### 7. Get Project Clusters
**GET** `/api/edgeai/clusters/project/{project_id}/clusters`

Retrieves all clusters for a specific project.

**Response:**
```json
[
    {
        "id": "1",
        "name": "My Cluster",
        "user_id": 1,
        "project_id": 1,
        "created_time": "2024-01-15T10:30:00Z",
        "last_updated_time": "2024-01-15T10:30:00Z"
    }
]
```

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Example error response:
```json
{
    "detail": "Cluster not found"
}
```

## Testing

To test the Cluster API, you can use the provided test script:

```bash
python test_cluster_api.py
```

Make sure the API server is running on `http://localhost:8000` before running the test.

## Database Migration

To add the cluster table to your database, run the migration:

```bash
# Apply the cluster migration
sqlite3 database/edgeai/edgeai.db < database/migrations/003_cluster_migration.sql
```

## Integration

The Cluster API is automatically integrated into the main FastAPI application and will be available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

The cluster endpoints are grouped under the "Clusters" tag in the API documentation.
