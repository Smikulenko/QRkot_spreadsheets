from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.core.constant import (AMOUNT, ACTIVE,
                               INVESTMENT,
                               PROJECT_EXISTS,
                               CHECK_NAME)
from app.models import CharityProject


async def check_name(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_id_by_name(project_name, session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CHECK_NAME
        )


async def check_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_project_by_id(
        charity_project_id,
        session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_EXISTS
        )
    return charity_project


async def project_active(
    charity_project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ACTIVE
        )
    return charity_project


async def project_investment(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTMENT
        )


async def updated_amount(
    obj_in_full_amount: int,
    charity_project_inv_amount: int,
    session: AsyncSession
) -> None:
    if obj_in_full_amount < charity_project_inv_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=AMOUNT
        )
