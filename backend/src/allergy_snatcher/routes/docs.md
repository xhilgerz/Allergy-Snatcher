# Allergy Snatcher API Documentation

This document outlines the API endpoints for the Allergy Snatcher application, covering authentication, food data management, and administrative tasks.

- [Allergy Snatcher API Documentation](#allergy-snatcher-api-documentation)
  - [Authentication](#authentication)
- [Authentication Routes](#authentication-routes)
    - [`POST /auth/register`](#post-authregister)
    - [`POST /auth/login`](#post-authlogin)
    - [`POST /auth/refresh`](#post-authrefresh)
    - [`GET /auth/status`](#get-authstatus)
    - [`POST /auth/logout`](#post-authlogout)
- [API Routes](#api-routes)
  - [Food Endpoints](#food-endpoints)
    - [`GET /api/foods/<food_id>`](#get-apifoodsfood_id)
    - [`PATCH /api/foods/<food_id>`](#patch-apifoodsfood_id)
    - [`DELETE /api/foods/<food_id>`](#delete-apifoodsfood_id)
    - [`PUT /api/foods/`](#put-apifoods)
    - [`GET /api/foods/category/<category_id>/<limit>/<offset>/<showhidden>`](#get-apifoodscategorycategory_idlimitoffsetshowhidden)
    - [`GET /api/foods/cuisine/<cuisine_id>/<limit>/<offset>/<showhidden>`](#get-apifoodscuisinecuisine_idlimitoffsetshowhidden)
  - [Category \& Cuisine Endpoints](#category--cuisine-endpoints)
    - [`GET /api/categories/`](#get-apicategories)
    - [`POST /api/categories/`](#post-apicategories)
    - [`DELETE /api/categories/<category_id>`](#delete-apicategoriescategory_id)
    - [`GET /api/cuisines/`](#get-apicuisines)
    - [`POST /api/cuisines/`](#post-apicuisines)
    - [`DELETE /api/cuisines/<cuisine_id>`](#delete-apicuisinescuisine_id)


## Authentication

Authentication is handled via session tokens. A successful login provides a short-lived `session_token` (sent in the response body) and a long-lived `refresh_token` (sent as an `HttpOnly` cookie).

- **Session Token**: Sent as a Bearer token in the `Authorization` header for requests that require authentication.
  - `Authorization: Bearer <session_token>`
- **Refresh Token**: Sent as an `HttpOnly` cookie to the `/auth/refresh` endpoint to get a new session token.

---

# Authentication Routes

These routes handle user registration, login, logout, and session management.

### `POST /auth/register`

- **Method:** `POST`
- **Description:** Registers a new user.
- **Access:** Public
- **Authentication:** None
- **Body:** `{"username": "string", "email": "string", "password": "string"}`

### `POST /auth/login`

- **Method:** `POST`
- **Description:** Authenticates a user and returns a session token in the body and a refresh token as an `HttpOnly` cookie.
- **Access:** Public
- **Authentication:** None
- **Body:** `{"username": "string", "password": "string"}`

### `POST /auth/refresh`

- **Method:** `POST`
- **Description:** Renews an expired session token using a valid refresh token. Requires the `refresh_token` cookie obtained during login.
- **Access:** Public (requires cookie)
- **Authentication:** Via `refresh_token` cookie.

### `GET /auth/status`

- **Method:** `GET`
- **Description:** Checks if the current session token is valid and returns the user's information if logged in.
- **Access:** Public
- **Authentication:** Optional. Checks for `Authorization: Bearer <token>` header.

### `POST /auth/logout`

- **Method:** `POST`
- **Description:** Logs the user out by invalidating their current session. Deletes the `refresh_token` cookie.
- **Access:** Authenticated User
- **Authentication:** Session token required.

---

# API Routes

These routes handle the core application data, such as foods, categories, and cuisines.

## Food Endpoints

### `GET /api/foods/<food_id>`

- **Method:** `GET`
- **Description:** Retrieves a single food item.
- **Access:** Public for `public` items. Private items require the user to be the owner or an admin.
- **Authentication:** Optional. Required for viewing non-public food items.

### `PATCH /api/foods/<food_id>`

- **Method:** `PATCH`
- **Description:** Updates a food item. Behavior depends on user role and food status.
- **Access:** Authenticated User
- **Authentication:** Session token required.
- **Headers & Rules:**
    - **Contributor:** Can only update their own `private` or `unlisting` items.
    - **Admin:** Can update any item. If the item is `public` or belongs to another user, a confirmation header `confirmation: force` is required.

### `DELETE /api/foods/<food_id>`

- **Method:** `DELETE`
- **Description:** Deletes a food item.
- **Access:** Authenticated User
- **Authentication:** Session token required.
- **Headers & Rules:**
    - **Contributor:** Can only delete their own `private` or `unlisting` items. Requires `confirmation: force` header.
    - **Admin:** Can delete any item. Requires `confirmation: force` header.

### `PUT /api/foods/`

- **Method:** `PUT`
- **Description:** Creates a new food item. New items are always created with `private` status.
- **Access:** Authenticated User
- **Authentication:** Session token required.

### `GET /api/foods/category/<category_id>/<limit>/<offset>/<showhidden>`

- **Method:** `GET`
- **Description:** Retrieves a paginated list of foods by category.
- **Access:** Public (with limitations)
- **Authentication:** Optional. Unauthenticated users see only `public` foods. Authenticated users see `public` and their own foods. Admins can see all foods.
- **URL Parameters:**
    - `showhidden`: (boolean) If `true`, admins can view all private items, not just their own.

### `GET /api/foods/cuisine/<cuisine_id>/<limit>/<offset>/<showhidden>`

- **Method:** `GET`
- **Description:** Retrieves a paginated list of foods by cuisine.
- **Access:** Public (with limitations)
- **Authentication:** Optional. Same rules as getting food by category.
- **URL Parameters:**
    - `showhidden`: (boolean) If `true`, admins can view all private items, not just their own.

## Category & Cuisine Endpoints

### `GET /api/categories/`

- **Method:** `GET`
- **Description:** Retrieves a list of all food categories.
- **Access:** Public
- **Authentication:** None

### `POST /api/categories/`

- **Method:** `POST`
- **Description:** Creates a new food category.
- **Access:** Admin Only
- **Authentication:** Session token with `admin` role required.

### `DELETE /api/categories/<category_id>`

- **Method:** `DELETE`
- **Description:** Deletes a category. Fails if any food items still reference it.
- **Access:** Admin Only
- **Authentication:** Session token with `admin` role required.

### `GET /api/cuisines/`

- **Method:** `GET`
- **Description:** Retrieves a list of all food cuisines.
- **Access:** Public
- **Authentication:** None

### `POST /api/cuisines/`

- **Method:** `POST`
- **Description:** Creates a new food cuisine.
- **Access:** Admin Only
- **Authentication:** Session token with `admin` role required.

### `DELETE /api/cuisines/<cuisine_id>`

- **Method:** `DELETE`
- **Description:** Deletes a cuisine. Fails if any food items still reference it.
- **Access:** Admin Only
- **Authentication:** Session token with `admin` role required.
