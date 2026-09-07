"""Hero 相关的 API 端点。"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app.core.database import SessionDep
from app.schemas.hero import Hero, HeroPublic, HeroCreate

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/{hero_id}", response_model=Hero)
def update_hero(
        hero_id: int,
        hero_data: Hero,
        session: SessionDep
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
def delete_hero(hero_id: int, session: SessionDep):
    """删除 Hero。"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"ok": True}
