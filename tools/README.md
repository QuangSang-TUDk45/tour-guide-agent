# Tools Documentation

This folder contains professional-grade tools for the Tour Guide Agent system. All tools are designed with advanced filtering, error handling, and consistent APIs.

## Available Tools

### 1. Destination Search (`get_destination.py`)
Search for tourist destinations with flexible filtering.

```python
from tools.get_destination import get_destination

# Search by location
results = get_destination(location="Quy Nhơn")

# Search by category
results = get_destination(category="biển")  # beach destinations

# Combined search
results = get_destination(location="Phú Yên", category="núi", limit=5)
```

**Parameters:**
- `location`: Location filter (city, province)
- `category`: Category filter (biển/beach, núi/mountain, etc.)
- `name`: Specific destination name
- `limit`: Max results (default: 10)

### 2. Hotel Search (`get_hotel.py`)
Advanced hotel search with price filtering and ratings.

```python
from tools.get_hotel import get_hotel

# Search hotels by location and price
results = get_hotel(location="Quy Nhơn", price_condition="dưới 1 triệu")

# Search by rating
results = get_hotel(location="Nha Trang", min_rating=4.0)

# Combined filters
results = get_hotel(
    location="Đà Nẵng",
    price_condition="từ 500k đến 2 triệu",
    min_rating=3.5,
    limit=5
)
```

**Parameters:**
- `location`: Location filter
- `price_condition`: Price filters ("dưới 1 triệu", "trên 500k", "từ 1-2 triệu")
- `name`: Hotel name filter
- `limit`: Max results (default: 10)

*Note: Rating filtering not available (no rating data in database)*

### 3. Restaurant Search (`get_restaurant.py`)
Find restaurants with cuisine and location filtering.

```python
from tools.get_restaurant import get_restaurant

# Search by cuisine
results = get_restaurant(category="hải sản")  # seafood restaurants

# Search by location
results = get_restaurant(location="Quy Nhơn")

# Combined search
results = get_restaurant(location="Đà Nẵng", category="Việt Nam")
```

**Parameters:**
- `location`: Location filter
- `category`: Cuisine type (hải sản/seafood, Việt Nam/Vietnamese, etc.)
- `name`: Restaurant name filter
- `limit`: Max results (default: 10)

### 4. Food Search (`get_food.py`)
Discover local foods and specialties.

```python
from tools.get_food import get_food

# Search by category
results = get_food(category="món chính")  # main dishes

# Search by tags
results = get_food(tags="hải sản")  # seafood dishes

# Combined search
results = get_food(category="đồ tráng miệng", name="chè")
```

**Parameters:**
- `category`: Food category (món chính, đồ uống, etc.)
- `tags`: Tag-based search
- `name`: Specific food name
- `limit`: Max results (default: 10)

### 5. Service Search (`get_service.py`)
Find tourism services and activities.

```python
from tools.get_service import get_service

# Search services by location
results = get_service(location="Eo Gió")

# Search by category
results = get_service(category="tour")

# Combined with price filter
results = get_service(
    location="Quy Nhơn",
    category="activity",
    price_condition="dưới 500k"
)
```

**Parameters:**
- `location`: Location/destination filter
- `category`: Service type (tour, activity, ticket)
- `name`: Service name filter
- `price_condition`: Price filters
- `limit`: Max results (default: 10)

### 6. Weather Tool (`weather_tool.py`)
Get current weather information for any location.

```python
from tools.weather_tool import get_weather

# Get weather by coordinates
weather = get_weather(lat=13.7825, lon=109.2196)  # Quy Nhơn

# Result includes:
# - temperature (°C)
# - windspeed (km/h)
# - weather description
# - coordinates
```

**Features:**
- GPS coordinate validation
- 30-minute caching
- Comprehensive weather descriptions
- Error handling

## Utility Functions (`utils.py`)

Common utilities used across all tools:

- **Price parsing**: Handle Vietnamese price formats
- **Location search**: Flexible address matching
- **Category mapping**: Vietnamese to English translations
- **Database safety**: Error-handled queries

## Key Improvements

### 1. **Smart Filtering**
- Vietnamese language support
- Flexible keyword matching
- Category translations (biển → beach, núi → mountain)

### 2. **Advanced Price Handling**
- Parse complex price ranges ("500k-2tr", "dưới 1 triệu")
- Support multiple currencies and formats
- Intelligent filtering ("hơn 1 triệu" vs "dưới 500k")

### 3. **Location Intelligence**
- Multi-keyword location search
- Address and name matching
- Geographic coordinate support

### 4. **Error Resilience**
- Graceful database error handling
- Empty result management
- Input validation

### 5. **Performance**
- Efficient database queries
- Result caching (weather)
- Optimized sorting and limiting

## Usage Examples

### Complex Hotel Search
```python
# Find budget hotels in Quy Nhơn
hotels = get_hotel(
    location="Quy Nhơn",
    price_condition="dưới 800k",
    limit=3
)
```

### Restaurant Discovery
```python
# Find seafood restaurants in coastal areas
restaurants = get_restaurant(
    category="hải sản",
    location="biển"
)
```

### Activity Planning
```python
# Find affordable activities in Phú Yên
services = get_service(
    location="Phú Yên",
    category="activity",
    price_condition="dưới 1 triệu"
)
```

## Backward Compatibility

All tools maintain backward compatibility with existing function signatures where possible. Legacy functions are preserved with `_legacy` suffix.

## Error Handling

All tools return appropriate error messages and empty DataFrames when no results are found, ensuring robust operation in the agent system.

## Current Status ✅

**All tools are fully functional and tested:**

- ✅ **Database Schema**: Fixed column name mismatches (price_mean vs price)
- ✅ **Import Paths**: Corrected module imports for all tools
- ✅ **Dependencies**: Resolved NumPy compatibility issues
- ✅ **Price Filtering**: Working with Vietnamese price conditions ("dưới 1 triệu", "trên 500k")
- ✅ **Location Search**: Multi-keyword matching for Vietnamese place names
- ✅ **Category Mapping**: Vietnamese to English translations working
- ✅ **Weather Tool**: GPS-based weather with caching operational
- ✅ **Error Handling**: Graceful failure and empty result management

**Database Tables Confirmed:**
- `hotel`: name, address, description, price_mean (text), gps_lat, gps_lon
- `service`: id, destination_id, name, description, price (bigint), type
- `restaurant`: name, address, category, description
- `destination`: name, category, address, description
- `food`: name, category, tags, description

**Tested Queries:**
- Hotel search with price filtering: ✅ Working
- Location-based searches: ✅ Working
- Category filtering: ✅ Working
- Weather API: ✅ Working