# Dolphin V3 Common Utilities

A reusable Django utility package designed to centralize common functionality
for Dolphin V3 modules, including:

- Bloodbank  
- DartaChalani  
- Housekeeping  
- Pharmacy  

This package allows you to avoid code duplication and ensures consistent behavior across projects.

---

## 🚀 Features

### Auth Utilities
- Password hashing and verification
- Token generation
- Custom permission utilities (`PermissionUtils`, `CustomPermissionClass`)

### Cache Utilities
- Redis-backed caching with `RedisClient`
- Utility function to generate Django `CACHES` config (`get_redis_cache_config`)

### Datetime Utilities
- Timezone-aware datetime conversion
- Date range generation
- First/last date of month
- String to date/time parsing

### Models & Mixins
- `BaseModel` for standardized table naming
- `BaseTimeStampModelMixin`, `BaseAuditModelMixin` for audit fields
- `SoftDeleteModelMixin` with `SoftDeleteManager` for soft-delete logic

### Pagination
- `CustomDefaultPagination` (PageNumberPagination)
- `CustomLimitOffsetPagination` (LimitOffsetPagination)

### Serializers
- `DynamicFieldsModelSerializer` for field-level control
- `BaseAuditSerializer` for automatic `created_by` / `updated_by`

### Responses
- `ResponseHandlerMixin` for standardized success, error, and exception responses
- Paginated response helper with user permissions

### Views
- `AbstractViewSet` combining `ResponseHandlerMixin` and `PermissionUtils`
- Built-in CRUD with standardized responses and soft-delete support

---

## 📦 Installation

### 1. Install from Github (HTTPS)

For public repo:

```bash
pip install git+https://gitea.mavorion.com/sdhimal/dolphin-v3-common-utils.git
```

For private repo:

```bash
pip install git+https://gitea.mavorion.com/sdhimal/dolphin-v3-common-utils.git
```
---

### 2. Add to `requirements.txt`

```txt
dolphin-v3-common-utils @ git+https://gitea.mavorion.com/sdhimal/dolphin-v3-common-utils.git

```

Install:

```bash
pip install -r requirements.txt
```

---

## 📣 Updating to Latest Version

Whenever you push updates to the common utils repository:

```bash
pip install --upgrade dolphin-v3-common-utils @ git+https://gitea.mavorion.com/sdhimal/dolphin-v3-common-utils.git
```

---

## 📝 Usage

### Auth Utilities

```python
from dolphin_v3.auth.utils import hash_password, verify_password, generate_token

hashed = hash_password("mypassword")
verify_password("mypassword", hashed)

token = generate_token()
```

### Redis Caching

```python
from dolphin_v3.cache.redis_cache import redis_client, get_redis_cache_config

CACHES = get_redis_cache_config(host="127.0.0.1", db=1)

redis_client.set("count", 5, ttl=60)
value = redis_client.get("count")
```

### Datetime Utilities

```python
from dolphin_v3.datetime.date_time import make_timezone_aware, timezone_conversion, get_date_range

dt_aware = make_timezone_aware(datetime.now(), "Asia/Kathmandu")
converted = timezone_conversion(dt_aware, "Asia/Kathmandu", "UTC")
dates = get_date_range(date(2025,12,1), date(2025,12,10))
```

### Models & Mixins

```python
from dolphin_v3.models.mixins import BaseTimeStampModelMixin, BaseAuditModelMixin, SoftDeleteModelMixin

class MyModel(SoftDeleteModelMixin, BaseTimeStampModelMixin, BaseAuditModelMixin):
    name = models.CharField(max_length=255)
```

### Pagination

```python
from dolphin_v3.pagination.default_pagination import CustomDefaultPagination

paginator = CustomDefaultPagination()
```

### Serializers

```python
from dolphin_v3.serializers.base_serializer import DynamicFieldsModelSerializer, BaseAuditSerializer
```

### Response Handling

```python
from dolphin_v3.response.mixins import ResponseHandlerMixin

class MyView(APIView, ResponseHandlerMixin):
    def get(self, request):
        data = {"msg": "Hello"}
        return self.success_response(data)
```

### Abstract ViewSet

```python
from dolphin_v3.views import AbstractViewSet

class MyModelViewSet(AbstractViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

### Permissions

```python
from dolphin_v3.users.permissions import PermissionUtils, CustomPermissionClass

permission_utils = PermissionUtils(user=request.user, model=MyModel)
has_perm = permission_utils.has_permission("view")
```

---

## 📚 Project Structure

```
dolphin_v3/
├── auth/
├── cache/
├── datetime/
├── models/
├── pagination/
├── response/
├── serializers/
├── users/
├── views/
├── apps.py
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a pull request

---

## 📄 License

Private and proprietary.  
All rights reserved © Shreeram Dhimal

---

## 📬 Support

Contact: Shree Dhimal  
Email: shreedhimal1@gmail.com