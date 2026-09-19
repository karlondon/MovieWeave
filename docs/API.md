# MovieWeave API Documentation

## Base URL
```
https://movieweave.myblognow.uk
http://34.204.47.202:8000 (for local testing)
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "aws_ok": true
}
```

### 2. Check Free Tier Status
**GET** `/api/free-tier`

Check how many free conversions are remaining today.

**Response:**
```json
{
  "is_free_tier": true,
  "used": 2,
  "remaining": 1,
  "limit": 3
}
```

### 3. Upload Document
**POST** `/upload`

Upload a PDF, DOCX, or TXT file to convert to video.

**Parameters:**
- `file` (multipart/form-data): The document file

**cURL Example:**
```bash
curl -X POST "http://34.204.47.202:8000/upload" \
  -F "file=@your_document.pdf"
```

**Response:**
```json
{
  "job_id": "job_abc123def456",
  "status": "pending",
  "message": "Document uploaded. Processing started."
}
```

### 4. Get Job Status
**GET** `/jobs/{job_id}`

Check the processing status of a conversion job.

**cURL Example:**
```bash
curl "http://34.204.47.202:8000/jobs/job_abc123def456"
```

**Response:**
```json
{
  "job_id": "job_abc123def456",
  "status": "processing",
  "progress": 45,
  "created_at": "2026-09-19T10:30:00",
  "updated_at": "2026-09-19T10:32:15"
}
```

**Status Values:**
- `pending` - Waiting to process
- `processing` - Currently generating video
- `completed` - Video ready for download
- `failed` - Processing encountered an error

### 5. Download Video
**GET** `/jobs/{job_id}/download`

Download the completed video file.

**cURL Example:**
```bash
curl "http://34.204.47.202:8000/jobs/job_abc123def456/download" \
  -o output.mp4
```

**Response:** MP4 video file (binary)

## Error Responses

### 404 - Not Found
```json
{"detail": "Job not found"}
```

### 400 - Bad Request
```json
{"detail": "Video not ready"}
```

### 500 - Server Error
```json
{"detail": "Error message describing the issue"}
```

## Workflow Example

1. **Upload Document**
   ```bash
   curl -X POST "http://34.204.47.202:8000/upload" \
     -F "file=@story.pdf"
   ```
   Response: `{"job_id": "job_xyz789", "status": "pending"}`

2. **Poll Status** (every 5 seconds)
   ```bash
   curl "http://34.204.47.202:8000/jobs/job_xyz789"
   ```

3. **Download When Ready**
   ```bash
   # When status = "completed"
   curl "http://34.204.47.202:8000/jobs/job_xyz789/download" \
     -o my_video.mp4
   ```

## Rate Limits

**Free Tier:** 3 conversions per day per user (based on IP + User Agent)

**Paid Tier:** Unlimited (coming soon)

## Response Times

- Small document (< 5 pages): 2-5 minutes
- Medium document (5-20 pages): 5-15 minutes
- Large document (> 20 pages): 15-30 minutes

## Supported File Formats

- PDF (.pdf)
- Word Documents (.docx)
- Text Files (.txt)

Maximum file size: 500MB

## Rate Limiting

All requests are rate-limited to prevent abuse:
- Per IP: 60 requests per minute
- Per job ID: 10 status checks per minute

## CORS

CORS is enabled for all origins. Include:
```
Access-Control-Allow-Origin: *
```

## Authentication

Currently no authentication required (MVP phase).
Production will use API keys.

## WebSocket (Coming Soon)

Real-time job status updates via WebSocket:
```
wss://movieweave.myblognow.uk/ws/jobs/{job_id}
```
