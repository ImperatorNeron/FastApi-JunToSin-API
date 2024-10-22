from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.utils.unitofwork import (
    IUnitOfWork,
    UnitOfWork,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
