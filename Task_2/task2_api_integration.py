"""
TASK 2: API Integration & JSON Handling

"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

# ============================================================================
# SECTION 1: BASIC API REQUESTS
# ============================================================================

def fetch_json_data(url: str, params: Optional[Dict] = None) -> Optional[Dict]:
    """
    Fetches JSON data from an API endpoint.
    
    Args:
        url: API endpoint URL
        params: Optional query parameters as dictionary
    
    Returns:
        Parsed JSON data or None if error occurs
    
    Error Handling:
    - ConnectionError: Network/connection issues
    - Timeout: Request takes too long
    - HTTPError: Bad HTTP status codes (4xx, 5xx)
    - JSONDecodeError: Invalid JSON response
    """
    try:
        # Set timeout to avoid hanging requests (default 5 seconds)
        response = requests.get(url, params=params, timeout=5)
        
        # Raise exception for bad status codes (4xx, 5xx)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        print(f"✓ Successfully fetched data from: {url}")
        return data
    
    except requests.exceptions.ConnectionError:
        # Network connection error (no internet, DNS failure, etc.)
        print(f"✗ Connection Error: Cannot reach {url}")
        print("  Check your internet connection and URL validity")
        return None
    
    except requests.exceptions.Timeout:
        # Request timed out
        print(f"✗ Timeout Error: Request took too long for {url}")
        return None
    
    except requests.exceptions.HTTPError as e:
        # HTTP error (404 Not Found, 500 Server Error, etc.)
        print(f"✗ HTTP Error: {e.response.status_code} - {e.response.reason}")
        return None
    
    except json.JSONDecodeError:
        # Response is not valid JSON
        print(f"✗ JSON Decode Error: Response is not valid JSON")
        return None
    
    except Exception as e:
        # Catch any other unexpected errors
        print(f"✗ Unexpected error: {e}")
        return None


# ============================================================================
# SECTION 2: API DATA EXTRACTION & FORMATTING
# ============================================================================

def extract_user_info(users_data: List[Dict]) -> List[Dict]:
    """
    Extracts relevant user information from API response.
    Demonstrates JSON navigation and data extraction.
    
    Args:
        users_data: List of user dictionaries from API
    
    Returns:
        List of simplified user records with selected fields
    """
    try:
        simplified_users = []
        
        for user in users_data:
            # Extract and restructure data
            simplified_user = {
                'id': user.get('id'),                    # Safe access with .get()
                'name': user.get('name', 'Unknown'),     # Default value if missing
                'username': user.get('username'),
                'email': user.get('email'),
                'city': user.get('address', {}).get('city'),  # Nested dictionary access
                'company': user.get('company', {}).get('name')
            }
            simplified_users.append(simplified_user)
        
        return simplified_users
    
    except Exception as e:
        print(f"✗ Error extracting user info: {e}")
        return []


# ============================================================================
# SECTION 3: DATA FILTERING & SEARCH
# ============================================================================

def filter_by_email_domain(users: List[Dict], domain: str) -> List[Dict]:
    """
    Filters users by email domain.
    
    Args:
        users: List of user dictionaries
        domain: Email domain to filter by (e.g., "example.com")
    
    Returns:
        List of users with matching email domain
    """
    try:
        filtered = [
            user for user in users 
            if user.get('email', '').endswith(f'@{domain}')
        ]
        print(f"✓ Found {len(filtered)} users with @{domain} email")
        return filtered
    
    except Exception as e:
        print(f"✗ Error filtering by domain: {e}")
        return []


def search_by_username(users: List[Dict], search_term: str) -> List[Dict]:
    """
    Searches users by username (case-insensitive partial match).
    
    Args:
        users: List of user dictionaries
        search_term: Search term to match
    
    Returns:
        List of matching users
    """
    try:
        search_term_lower = search_term.lower()
        results = [
            user for user in users
            if search_term_lower in user.get('username', '').lower()
        ]
        print(f"✓ Search for '{search_term}' found {len(results)} users")
        return results
    
    except Exception as e:
        print(f"✗ Error searching users: {e}")
        return []


def filter_by_location(users: List[Dict], city: str) -> List[Dict]:
    """
    Filters users by city location.
    
    Args:
        users: List of user dictionaries
        city: City name to filter by
    
    Returns:
        List of users in specified city
    """
    try:
        filtered = [
            user for user in users
            if user.get('city', '').lower() == city.lower()
        ]
        print(f"✓ Found {len(filtered)} users in {city}")
        return filtered
    
    except Exception as e:
        print(f"✗ Error filtering by location: {e}")
        return []


# ============================================================================
# SECTION 4: ADVANCED JSON OPERATIONS
# ============================================================================

def analyze_data_structure(data: Dict) -> None:
    """
    Analyzes and displays the structure of JSON data.
    Useful for understanding API responses.
    
    Args:
        data: Dictionary to analyze
    """
    try:
        def print_structure(obj, indent=0):
            """Recursive function to print nested structure"""
            prefix = "  " * indent
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        print(f"{prefix}• {key}: {type(value).__name__}")
                        print_structure(value, indent + 1)
                    else:
                        value_type = type(value).__name__
                        print(f"{prefix}• {key}: {value_type}")
            
            elif isinstance(obj, list):
                if obj and isinstance(obj[0], (dict, list)):
                    print(f"{prefix}[List with {len(obj)} items]")
                    print_structure(obj[0], indent + 1)
                else:
                    print(f"{prefix}[List with {len(obj)} items]")
        
        print("\nJSON Structure:")
        print("=" * 50)
        print_structure(data)
        print("=" * 50)
    
    except Exception as e:
        print(f"✗ Error analyzing structure: {e}")


def save_to_json_file(data: Dict, filename: str) -> bool:
    """
    Saves data to a JSON file with pretty printing.
    
    Args:
        data: Data to save
        filename: Output filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Use indent for readable formatting
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Data saved to: {filename}")
        return True
    
    except IOError as e:
        print(f"✗ Error saving file: {e}")
        return False


# ============================================================================
# SECTION 5: BATCH OPERATIONS & AGGREGATION
# ============================================================================

def get_stats_by_city(users: List[Dict]) -> Dict[str, int]:
    """
    Creates a summary of users per city.
    Demonstrates data aggregation.
    
    Args:
        users: List of user dictionaries
    
    Returns:
        Dictionary with city names as keys and user counts as values
    """
    try:
        stats = {}
        
        for user in users:
            city = user.get('city', 'Unknown')
            # Count users in each city
            stats[city] = stats.get(city, 0) + 1
        
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
    
    except Exception as e:
        print(f"✗ Error calculating statistics: {e}")
        return {}


def create_user_directory(users: List[Dict]) -> Dict[int, Dict]:
    """
    Creates an indexed directory of users by ID.
    Useful for quick lookups.
    
    Args:
        users: List of user dictionaries
    
    Returns:
        Dictionary with user IDs as keys
    """
    try:
        directory = {user.get('id'): user for user in users}
        return directory
    
    except Exception as e:
        print(f"✗ Error creating directory: {e}")
        return {}


# ============================================================================
# SECTION 6: MAIN DEMONSTRATION
# ============================================================================

def main():
    """
    Main function demonstrating API integration and JSON handling.
    Uses JSONPlaceholder - a free fake REST API for testing.
    """
    print("=" * 80)
    print("TASK 2: API INTEGRATION & JSON HANDLING")
    print("=" * 80)
    
    # Step 1: Create sample data (simulating API response)
    print("\n[STEP 1] Loading sample API response data...")
    print("-" * 80)
    print("(Simulating API data structure from REST endpoint)")
    
    # Sample user data simulating a real API response
    users_data = [
        {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {"city": "Gwenborough"},
            "company": {"name": "Romaguera-Crona"}
        },
        {
            "id": 2,
            "name": "Erwin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv",
            "address": {"city": "Amesbury"},
            "company": {"name": "Deckow-Crist"}
        },
        {
            "id": 3,
            "name": "Clementine Bauch",
            "username": "Samantha",
            "email": "Nathan@yesenia.net",
            "address": {"city": "McKenziehaven"},
            "company": {"name": "Romaguera-Jacobson"}
        },
        {
            "id": 4,
            "name": "Patricia Lebsack",
            "username": "Karianne",
            "email": "Julianne.OConner@kory.com",
            "address": {"city": "South Elvis"},
            "company": {"name": "Robel-Corkery"}
        },
        {
            "id": 5,
            "name": "Chelsey Dietrich",
            "username": "Kamren",
            "email": "Lucio_Hettinger@annie.ca",
            "address": {"city": "Roscoeview"},
            "company": {"name": "Keebler LLC"}
        }
    ]
    
    print(f"✓ Loaded {len(users_data)} user records (simulated API response)")
    
    # Step 2: Display API response structure
    print("\n[STEP 2] Analyzing JSON response structure...")
    print("-" * 80)
    analyze_data_structure(users_data[0])  # Show structure of first user
    
    # Step 3: Extract and simplify data
    print("\n[STEP 3] Extracting relevant user information...")
    print("-" * 80)
    simplified_users = extract_user_info(users_data)
    
    print("\nSample extracted user data:")
    print(json.dumps(simplified_users[0:2], indent=2))
    
    # Step 4: Demonstrate filtering operations
    print("\n[STEP 4] Filtering data by various criteria...")
    print("-" * 80)
    
    # Filter by email domain
    gmail_users = filter_by_email_domain(simplified_users, "example.com")
    if gmail_users:
        print("\nFirst Gmail user:")
        print(json.dumps(gmail_users[0], indent=2))
    
    # Search functionality
    search_results = search_by_username(simplified_users, "bret")
    if search_results:
        print("\nSearch results for 'bret':")
        print(json.dumps(search_results, indent=2))
    
    # Filter by city
    city_results = filter_by_location(simplified_users, "Amesbury")
    if city_results:
        print("\nUsers in Amesbury:")
        print(json.dumps(city_results, indent=2))
    
    # Step 5: Data aggregation and statistics
    print("\n[STEP 5] Generating statistics...")
    print("-" * 80)
    
    city_stats = get_stats_by_city(simplified_users)
    print("\nUsers per city (top 5):")
    for city, count in list(city_stats.items())[:5]:
        print(f"  • {city}: {count} user(s)")
    
    # Step 6: Save processed data
    print("\n[STEP 6] Saving processed data to JSON files...")
    print("-" * 80)
    
    # Save simplified user list
    save_to_json_file(simplified_users, "users_simplified.json")
    
    # Save statistics
    stats_data = {
        'total_users': len(simplified_users),
        'total_cities': len(city_stats),
        'users_by_city': city_stats,
        'generated_at': datetime.now().isoformat()
    }
    save_to_json_file(stats_data, "users_stats.json")
    
    # Save search results
    save_to_json_file({
        'search_term': 'bret',
        'results': search_results,
        'count': len(search_results)
    }, "search_results.json")
    
    # Step 7: Create indexed directory
    print("\n[STEP 7] Creating indexed user directory...")
    print("-" * 80)
    user_directory = create_user_directory(simplified_users)
    print(f"✓ Created directory with {len(user_directory)} indexed users")
    print("  Quick lookup example - User ID 1:")
    print(json.dumps(user_directory[1], indent=2))
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    print("  • users_simplified.json - Cleaned and simplified user data")
    print("  • users_stats.json - Statistics and aggregation results")
    print("  • search_results.json - API search results")


if __name__ == "__main__":
    main()