# Search Engine Project - Future Improvements Checklist

> Professional Review by 10+ Years Experience Engineer
> Last Updated: April 23, 2026

---

## 🔴 PHASE 1: CRITICAL FIXES (Week 1 - Do This First)

### Code Quality & Bugs
- [ ] Remove duplicate CORS import in `main.py` (line 6)
  - Currently importing CORSMiddleware twice
  - Keep only one import statement
  
- [ ] Remove hardcoded credentials from `db.py`
  - Verify `.env` file contains all DB configs:
    - [ ] DB_HOST
    - [ ] DB_USER
    - [ ] DB_PASSWORD
    - [ ] DB_NAME
  
- [ ] Add input validation using Pydantic models
  - [ ] Create `schemas.py` file with Pydantic models
  - [ ] Create `SearchQuery` model for `/search` endpoint
  - [ ] Validate query length (min 1 char, max 500 chars)
  - [ ] Validate maxPrice (min 0, max 1,000,000)
  - [ ] Validate minRating (0-5 range)
  - [ ] Validate sort options (price_asc, price_desc, rating_desc)

### Security & Configuration
- [ ] Restrict CORS origins (NOT wildcard "*")
  - [ ] Change from: `allow_origins=["*"]`
  - [ ] Change to: `allow_origins=["https://your-frontend-domain.com", "http://localhost:3000"]`
  - [ ] Update when deploying to production

- [ ] Add error handling to all endpoints
  - [ ] Wrap search logic in try-except blocks
  - [ ] Return proper HTTP status codes (400, 404, 500)
  - [ ] Return meaningful error messages to frontend

- [ ] Create `.env` file template
  - [ ] Create `.env.example` for developers
  - [ ] Document all required environment variables

### Architecture: Switch to Database-First Approach
- [ ] Remove CSV-based search completely
  - [ ] Delete `df = pd.read_csv(csv_path)` from `search.py`
  - [ ] Delete `vectorizer = TfidfVectorizer()` initialization
  - [ ] Delete `tfidf_matrix = vectorizer.fit_transform()` calculation
  - [ ] Delete `tokenized_corpus` initialization
  - [ ] Delete global BM25 model initialization

- [ ] Refactor filter extraction (Use URL Parameters Instead of Regex)
  - [ ] Replace `extract_price()` function usage with URL param `maxPrice`
  - [ ] Replace `extract_rating()` function usage with URL param `minRating`
  - [ ] Replace `extract_sort()` function usage with URL param `sort`
  - [ ] Update endpoint signature: `/search?q=query&maxPrice=2000&minRating=4&sort=price_asc`
  - [ ] Delete these helper functions after migration:
    - [ ] `extract_price()`
    - [ ] `extract_rating()`
    - [ ] `extract_sort()`

- [ ] Modify `search_products()` function
  - [ ] Accept separate parameters: `query`, `max_price`, `min_rating`, `sort`
  - [ ] Query MySQL directly instead of filtering dataframe
  - [ ] Use `get_products_by_ids()` properly or refactor to direct search
  - [ ] Return results directly from database

- [ ] Update main.py endpoint
  - [ ] Change `/search` endpoint to accept URL parameters
  - [ ] Old: `def search(q: str)` with parsing
  - [ ] New: `def search(q: str, maxPrice: int = None, minRating: float = None, sort: str = None)`

---

## 🟡 PHASE 2: PERFORMANCE OPTIMIZATION (Week 2-3)

### Caching Layer (Redis)
- [ ] Install Redis
  - [ ] `pip install redis`
  - [ ] Add to `requirements.txt`

- [ ] Set up Redis connection
  - [ ] Create `cache.py` file with Redis client initialization
  - [ ] Add Redis config to `.env`:
    - [ ] REDIS_HOST (default: localhost)
    - [ ] REDIS_PORT (default: 6379)
    - [ ] REDIS_DB (default: 0)

- [ ] Implement cache for search results
  - [ ] Cache key format: `search:{query}:{maxPrice}:{minRating}:{sort}`
  - [ ] TTL: 5 minutes (300 seconds)
  - [ ] Check cache before querying database
  - [ ] Update cache after database query
  - [ ] Return cached results if available

- [ ] Implement cache invalidation
  - [ ] Clear cache when data is updated
  - [ ] Clear cache when new products are added
  - [ ] Add cache statistics endpoint for monitoring

### Database Optimization
- [ ] Create MySQL Indexes
  - [ ] `CREATE INDEX idx_name ON products(name);`
  - [ ] `CREATE INDEX idx_brand ON products(brand);`
  - [ ] `CREATE INDEX idx_price ON products(price);`
  - [ ] `CREATE INDEX idx_rating ON products(rating);`
  - [ ] `CREATE INDEX idx_category ON products(category);`
  - [ ] `CREATE FULLTEXT INDEX idx_fulltext ON products(name, description, brand);`

- [ ] Update search query to use FULLTEXT search
  - [ ] Replace BM25 scoring with MySQL FULLTEXT search
  - [ ] Query pattern: `MATCH(name, description, brand) AGAINST(? IN BOOLEAN MODE)`
  - [ ] This is much faster than in-memory BM25

- [ ] Test query performance
  - [ ] Run `EXPLAIN` on all search queries
  - [ ] Verify indexes are being used
  - [ ] Benchmark query times before/after

- [ ] Optimize filtering queries
  - [ ] Use indexed columns for WHERE clauses
  - [ ] Test with large datasets (100k+ products)

### Connection Management
- [ ] Install SQLAlchemy
  - [ ] `pip install sqlalchemy pymysql`
  - [ ] Add to `requirements.txt`

- [ ] Refactor `db.py` to use connection pooling
  - [ ] Replace raw `mysql.connector` with SQLAlchemy
  - [ ] Create engine with `QueuePool`
  - [ ] Pool size: 20 connections
  - [ ] Max overflow: 10
  - [ ] Pool recycle: 3600 seconds
  - [ ] Connection timeout: 30 seconds

- [ ] Replace all database calls
  - [ ] Update `get_products_by_ids()` to use SQLAlchemy session
  - [ ] Update `search_products()` to use connection pool
  - [ ] Test connections are reused (not creating new ones)

- [ ] Test pool under load
  - [ ] Verify connections are being recycled
  - [ ] Monitor connection count stays stable

---

## 🟠 PHASE 3: SCALABILITY & RELIABILITY (Week 4-5)

### Rate Limiting
- [ ] Install slowapi
  - [ ] `pip install slowapi`
  - [ ] Add to `requirements.txt`

- [ ] Configure rate limiter
  - [ ] Limit: 100 requests per minute per IP
  - [ ] Apply to `/search` endpoint
  - [ ] Add `@limiter.limit()` decorator

- [ ] Handle rate limit violations
  - [ ] Return HTTP 429 (Too Many Requests)
  - [ ] Include `Retry-After` header
  - [ ] Return clear error message

### Logging & Monitoring
- [ ] Set up structured logging (JSON format)
  - [ ] Create `logger.py` file
  - [ ] Configure JSON logging
  - [ ] Add Python logging configuration

- [ ] Log all search operations
  - [ ] Query text
  - [ ] Filter parameters (maxPrice, minRating, sort)
  - [ ] Response time (ms)
  - [ ] Number of results returned
  - [ ] User IP address

- [ ] Log all errors
  - [ ] Error type
  - [ ] Error message
  - [ ] Stack trace
  - [ ] Timestamp

- [ ] Monitor database connection pool
  - [ ] Log pool size
  - [ ] Log active connections
  - [ ] Log connection timeouts
  - [ ] Alert if pool is exhausted

- [ ] Create `/metrics` endpoint
  - [ ] Average response time (ms)
  - [ ] Total request count
  - [ ] Error rate (%)
  - [ ] Cache hit rate (%)
  - [ ] Database query time (ms)

### API Improvements
- [ ] Add `/health` endpoint
  - [ ] Check database connectivity
  - [ ] Check Redis connectivity
  - [ ] Return 200 if healthy, 503 if not
  - [ ] Used by load balancers for health checks

- [ ] Implement pagination
  - [ ] Add `limit` parameter (default 10, max 100)
  - [ ] Add `offset` parameter (default 0)
  - [ ] Return `total_count` in response
  - [ ] Return `limit` and `offset` in response

- [ ] Add request timeout handling
  - [ ] Set database query timeout: 30 seconds
  - [ ] Set Redis timeout: 5 seconds
  - [ ] Return timeout errors gracefully

- [ ] Implement circuit breaker pattern
  - [ ] If database fails 5 times, stop trying
  - [ ] Try again after 60 seconds
  - [ ] Return error message to user

- [ ] Add response validation
  - [ ] Ensure all responses match expected schema
  - [ ] Return consistent response format

### Load Testing
- [ ] Install Locust
  - [ ] `pip install locust`
  - [ ] Add to `requirements.txt`

- [ ] Create load test script (`load_test.py`)
  - [ ] Simulate 100+ concurrent users
  - [ ] Run various search queries
  - [ ] Test with different filters
  - [ ] Measure response times
  - [ ] Track error rates

- [ ] Run load tests
  - [ ] Test with 100 concurrent users
  - [ ] Test with 500 concurrent users
  - [ ] Test with 1000 concurrent users
  - [ ] Identify bottlenecks

- [ ] Document baseline metrics
  - [ ] Average response time
  - [ ] P95 response time
  - [ ] P99 response time
  - [ ] Error rate
  - [ ] Throughput (requests/second)

---

## 🟢 PHASE 4: ASYNC & ADVANCED (Optional - For 10k+ Users)

- [ ] Switch to PostgreSQL (optional, for better async support)
  - [ ] Install `pip install asyncpg`
  - [ ] Migrate data from MySQL to PostgreSQL
  - [ ] Update connection strings

- [ ] Implement async database operations
  - [ ] Refactor all DB functions to `async def`
  - [ ] Use `await` for database calls
  - [ ] Implement async connection pooling

- [ ] Convert FastAPI endpoints to async
  - [ ] Change `def search()` to `async def search()`
  - [ ] Use `await` for all I/O operations
  - [ ] This allows handling many concurrent requests with few threads

- [ ] Set up message queue
  - [ ] Install Celery: `pip install celery`
  - [ ] Use Redis as broker
  - [ ] Move heavy computations to background tasks

- [ ] Implement background tasks
  - [ ] Pre-compute search result rankings
  - [ ] Update product statistics
  - [ ] Warm-up cache with popular searches

- [ ] Add search analytics
  - [ ] Track most searched queries
  - [ ] Track search patterns
  - [ ] Use data to optimize indexes and caching

---

## 📋 NEW FILES TO CREATE

- [ ] `config.py`
  - [ ] Centralized configuration management
  - [ ] Load from `.env` file
  - [ ] Define constants and settings

- [ ] `schemas.py`
  - [ ] Pydantic models for request validation
  - [ ] Pydantic models for response formatting
  - [ ] Models: SearchQuery, SearchResponse, ProductResult

- [ ] `cache.py`
  - [ ] Redis connection management
  - [ ] Cache helper functions
  - [ ] Cache key generation
  - [ ] Cache invalidation logic

- [ ] `logger.py`
  - [ ] Structured logging setup
  - [ ] JSON formatter configuration
  - [ ] Log level management

- [ ] `.env.example`
  - [ ] Template for `.env` file
  - [ ] Document all required variables
  - [ ] Provide example values

- [ ] `load_test.py`
  - [ ] Locust load test script
  - [ ] Simulate concurrent users
  - [ ] Test various search scenarios

- [ ] `test_search.py` (Update existing)
  - [ ] Unit tests for search function
  - [ ] Unit tests for filter validation
  - [ ] Integration tests

---

## 🧪 TESTING CHECKLIST

- [ ] Unit Tests
  - [ ] Test `search_products()` with various queries
  - [ ] Test `search_products()` with filters (maxPrice, minRating)
  - [ ] Test `search_products()` with sorting
  - [ ] Test input validation (empty query, invalid filters)
  - [ ] Test edge cases (no results, single result)

- [ ] Database Tests
  - [ ] Test connection pooling
  - [ ] Test connection timeout handling
  - [ ] Test database failure recovery

- [ ] Cache Tests
  - [ ] Test cache hits
  - [ ] Test cache misses
  - [ ] Test cache invalidation
  - [ ] Test cache expiration

- [ ] Integration Tests
  - [ ] Full search flow with filters
  - [ ] Rate limiting triggers
  - [ ] Error handling (DB down, Redis down)
  - [ ] Pagination

- [ ] Load Tests
  - [ ] 100 concurrent users
  - [ ] 500 concurrent users
  - [ ] 1000 concurrent users
  - [ ] Sustained load for 10 minutes

- [ ] Performance Tests
  - [ ] Response time benchmarks
  - [ ] Database query performance
  - [ ] Cache effectiveness
  - [ ] Connection pool usage

---

## 📊 UPDATED requirements.txt

```
# Core Framework
fastapi==0.104.1
uvicorn==0.24.0

# Data Processing (reduce usage)
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
rank-bm25==0.2.1

# Database
mysql-connector-python==8.2.0
sqlalchemy==2.0.0
pymysql==1.1.0

# Caching
redis==5.0.0

# Configuration & Validation
python-dotenv==1.0.0
pydantic==2.4.0

# Rate Limiting
slowapi==0.1.9

# Monitoring & Testing
locust==2.17.0

# Optional (Phase 4)
# asyncpg==0.28.0
# celery==5.3.0
```

---

## ⏱️ ESTIMATED TIME & PRIORITY

| Phase | Duration | Priority | Impact |
|-------|----------|----------|--------|
| Phase 1 | 2-3 days | 🔴 CRITICAL | 5-10x performance |
| Phase 2 | 3-4 days | 🟡 HIGH | Additional 5x performance |
| Phase 3 | 4-5 days | 🟠 MEDIUM | Reliability & monitoring |
| Phase 4 | 5-7 days | 🟢 OPTIONAL | For 10k+ users |

---

## 🎯 COMPLETION MILESTONES

### Milestone 1: Database Migration (Day 1-3)
- [x] Complete Phase 1 checklist
- [x] Switch to database-first search
- [x] Remove CSV-based operations
- [x] Deploy and test

**Expected Improvement**: 5-10x faster responses

### Milestone 2: Caching & Connection Pooling (Day 4-7)
- [x] Complete Phase 2 checklist
- [x] Add Redis caching
- [x] Implement connection pooling
- [x] Create database indexes
- [x] Load test with 500 concurrent users

**Expected Improvement**: Additional 5x speedup + 10k concurrent users support

### Milestone 3: Monitoring & Reliability (Day 8-12)
- [x] Complete Phase 3 checklist
- [x] Add rate limiting
- [x] Implement structured logging
- [x] Add health checks
- [x] Load test with 1000 concurrent users

**Expected Result**: Production-ready system

### Milestone 4: Advanced Scaling (Optional - Day 13+)
- [ ] Complete Phase 4 checklist (if needed)
- [ ] Async operations
- [ ] Message queues
- [ ] Pre-computation

**Expected Result**: Support 10k+ concurrent users

---

## 📝 NOTES

- Start with Phase 1 immediately - it's critical
- Test thoroughly after each phase
- Monitor performance metrics continuously
- Document all changes in git commits
- Keep database backups before major changes
- Plan downtime for database migrations if needed

---

## 🔗 RELATED DOCUMENTATION

- Backend files: `backend/main.py`, `backend/search.py`, `backend/db.py`
- Frontend files: `frontend/src/App.js`
- Requirements: `requirements.txt`
- Environment: `.env` (create from `.env.example`)

---

**Last Updated**: April 23, 2026
**Status**: In Progress
**Next Review**: After completing Phase 1
