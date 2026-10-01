from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db

from app.schemas.qr_code import (
    QRCodeResponse,
)

from app.services.qr_code_service import (
    create_qr_code,
    get_qr_code,
    update_qr_code,
    delete_qr_code,
    qr_to_response,
)

from app.services.wedding_service import (
    get_wedding_by_id,
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/qr",
    tags=["QR Code"],
)


# =====================================================
# VERIFY WEDDING ACCESS
# =====================================================

def verify_wedding_access(
    wedding_id: int,
    db: Session,
    current_user: dict,
):
    firebase_uid = (
        current_user.get("uid")
    )

    wedding = get_wedding_by_id(
        db,
        wedding_id,
        firebase_uid,
    )

    if wedding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wedding not found",
        )

    return wedding


# =====================================================
# GET QR
# =====================================================

@router.get(
    "",
    response_model=QRCodeResponse,
)
def get_qr_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        get_current_user
    ),
):

    wedding = verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    qr = get_qr_code(
        db,
        wedding_id,
    )

    if qr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code not found",
        )

    return qr_to_response(
        qr,
        wedding,
    )


# =====================================================
# CREATE QR
# =====================================================

@router.post(
    "",
    response_model=QRCodeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_qr_api(
    wedding_id: int,

    qr_image: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        get_current_user
    ),
):

    wedding = verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    try:

        qr = await create_qr_code(
            db=db,
            wedding=wedding,
            qr_image=qr_image,
        )

        return qr_to_response(
            qr,
            wedding,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# =====================================================
# UPDATE QR
# =====================================================

@router.patch(
    "",
    response_model=QRCodeResponse,
)
async def update_qr_api(
    wedding_id: int,

    qr_image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        get_current_user
    ),
):

    wedding = verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    try:

        qr = await update_qr_code(
            db=db,
            wedding=wedding,
            qr_image=qr_image,
        )

        if qr is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR Code not found",
            )

        return qr_to_response(
            qr,
            wedding,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# =====================================================
# DELETE QR
# =====================================================

@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_qr_api(
    wedding_id: int,

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        get_current_user
    ),
):

    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    deleted = delete_qr_code(
        db,
        wedding_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR Code not found",
        )

    return None