# Domain Reseller API Setup

## ConnectReseller API Integration

### 1. API Configuration

To use the domain availability check feature, you need to configure your ConnectReseller API key:

1. Open `hosting/settings.py`
2. Replace `'your-api-key-here'` with your actual ConnectReseller API key:

```python
# ConnectReseller API Settings
CONNECTRESELLER_API_KEY = 'YOUR_ACTUAL_API_KEY_HERE'  # Replace with your actual API key
CONNECTRESELLER_BASE_URL = 'https://api.connectreseller.com/ConnectReseller/ESHOP'
```

### 2. Features Implemented

#### Domain Availability Check
- **Endpoint**: `/api/check-domain/`
- **Method**: GET
- **Parameter**: `domain` (the domain name to check)
- **Features**:
  - Real-time domain availability checking
  - Pricing information (registration, renewal, transfer)
  - Clean domain name processing (removes protocols, www, etc.)
  - Error handling for API failures
  - Loading states and user feedback

#### Frontend Integration
- **Page**: `/register-domain/`
- **Features**:
  - AJAX-powered domain search
  - Real-time results display
  - Pricing information display
  - Available/unavailable status indicators
  - Error handling and user feedback
  - Loading spinners
  - Smooth scroll to results

### 3. Testing the Implementation

1. Start the Django server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to: `http://localhost:8000/register-domain/`

3. Enter a domain name in the search box and click "Search Domain"

4. The system will:
   - Make an API call to ConnectReseller
   - Display availability status
   - Show pricing information if available
   - Handle errors gracefully

### 4. API Response Format

The ConnectReseller API returns data in this format:

```json
{
  "statusCode": 200,
  "message": "Domain availability checked",
  "responseData": {
    "domainType": "com",
    "available": true,
    "registration fees": 8500,
    "renewalfees": 9200,
    "transferFees": 8500
  }
}
```

Our implementation transforms this into a cleaner format for the frontend:

```json
{
  "success": true,
  "available": true,
  "domain": "example.com",
  "domain_type": "com",
  "pricing": {
    "registration": 8500,
    "renewal": 9200,
    "transfer": 8500
  },
  "message": "Domain availability checked"
}
```

### 5. Next Steps

Once you have your API key configured, you can:

1. Test domain searches on the register domain page
2. Implement additional domain features like:
   - Domain suggestions
   - Bulk domain checking
   - Domain registration
   - Domain transfers

### 6. Error Handling

The implementation includes comprehensive error handling for:
- Network failures
- Invalid API responses
- Empty domain names
- API authentication errors
- Unexpected server errors

All errors are displayed to the user in a friendly format.