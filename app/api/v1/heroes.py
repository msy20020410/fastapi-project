"""Hero 相关的 API 端点。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.schemas.hero import Hero

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.post("", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    """创建新的 Hero。"""
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("", response_model=list[Hero])
def read_heroes(
        offset: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    """获取 Hero 列表。"""
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    """根据 ID 获取 Hero。"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/{hero_id}", response_model=Hero)
def update_hero(
        hero_id: int,
        hero_data: Hero,
        session: Session = Depends(get_session)
):
    """更新 Hero 信息。"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_dict = hero_data.model_dump(exclude_unset=True)
    for key, value in hero_dict.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    """删除 Hero。"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"ok": True}
