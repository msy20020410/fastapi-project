"""索引权重接口。"""
from fastapi import APIRouter

router = APIRouter(prefix="/index-weights", tags=["Index Weights"])


@router.post("/")
async def create_index_weights(weights: dict[int, float]):
    return weights
