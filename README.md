# FastAPI Project

基于 FastAPI 的示例项目，接口已按企业级结构模块化拆分。

## 目录结构

```
fastapi-project/
├── main.py                  # 项目入口（兼容 fastapi dev / uvicorn main:app）
├── pyproject.toml
└── app/
    ├── main.py              # FastAPI 应用：创建 app、挂载路由、健康检查
    ├── core/
    │   └── config.py        # 应用配置（应用名、版本、API 前缀）
    ├── schemas/             # Pydantic 数据模型
    │   ├── item.py          # Item / Item2 / Item3 / Item4 / FilterParams
    │   ├── user.py          # User
    │   └── image.py         # Image
    └── api/
        └── v1/
            ├── router.py    # v1 路由汇总（统一前缀 /api/v1）
            ├── items.py     # /api/v1/items（含编号示例路由 02~12）
            ├── users.py     # /api/v1/users/{user_id}/items/{item_id}
            ├── images.py    # /api/v1/images
            ├── files.py     # /api/v1/files/{file_path:path}
            ├── ml_models.py # /api/v1/models/{model_name}
            └── weights.py   # /api/v1/index-weights
```

## 运行

```bash
uv run fastapi dev
```

交互式文档：<http://127.0.0.1:8000/docs>

## 约定

- 所有业务接口统一挂在 `/api/v1` 前缀下（见 `app/core/config.py`），根路径 `/` 为健康检查。
- 每个路由模块在 `APIRouter` 上声明自己的 `prefix` 与 `tags`，`app/api/v1/router.py` 只负责汇总。
- `items.py` 中的编号示例路由（`/items/03`、`/items/06`、`/items/12` 等）与通配路由
  `/items/{item_id}` 形状相同，FastAPI 按注册顺序取第一个匹配，因此固定路径全部注册在通配路径之前，调整顺序时需注意。
