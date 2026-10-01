import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.qr_code import QRCode


UPLOAD_DIR = Path("uploads/qr_codes")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALLOWED_CONTENT_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
}


MAX_FILE_SIZE = 5 * 1024 * 1024


# =====================================================
# IMAGE VALIDATION
# =====================================================

def validate_image(file: UploadFile):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            "Only PNG, JPG, and WEBP images are allowed."
        )


# =====================================================
# SAVE IMAGE
# =====================================================

async def save_qr_image(
    file: UploadFile,
) -> str:

    validate_image(file)

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError(
            "QR image size must be less than 5MB."
        )

    extension = ALLOWED_CONTENT_TYPES[
        file.content_type
    ]

    filename = (
        f"{uuid4().hex}{extension}"
    )

    file_path = (
        UPLOAD_DIR / filename
    )

    file_path.write_bytes(
        file_content
    )

    return (
        f"/uploads/qr_codes/{filename}"
    )


# =====================================================
# DELETE IMAGE
# =====================================================

def delete_qr_image(
    image_url: str | None,
):
    if not image_url:
        return

    filename = Path(
        image_url
    ).name

    file_path = (
        UPLOAD_DIR / filename
    )

    if file_path.exists():
        file_path.unlink()


# =====================================================
# GENERATE REGISTRY SLUG
# =====================================================

def create_registry_slug(
    first_partner: str,
    second_partner: str,
) -> str:

    couple_name = (
        f"{first_partner}-{second_partner}"
    )

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        couple_name.lower(),
    ).strip("-")

    return slug


# =====================================================
# GENERATE REGISTRY URL
# =====================================================

def get_registry_link(wedding):
    slug = create_registry_slug(
        wedding.first_partner,
        wedding.second_partner,
    )

    return (
        f"http://localhost:3000/r/{slug}"
    )


# =====================================================
# GET QR
# =====================================================

def get_qr_code(
    db: Session,
    wedding_id: int,
):
    return (
        db.query(QRCode)
        .filter(
            QRCode.wedding_id == wedding_id
        )
        .first()
    )


# =====================================================
# BUILD RESPONSE
# =====================================================

def qr_to_response(
    qr: QRCode,
    wedding,
):

    couple_name = (
        f"{wedding.first_partner} "
        f"& "
        f"{wedding.second_partner}"
    )

    return {
        "id": qr.id,
        "wedding_id": qr.wedding_id,

        "couple_name": couple_name,

        "wedding_date": (
            wedding.wedding_date
        ),

        "wedding_venue": (
            wedding.wedding_venue
        ),

        "registry_link": get_registry_link(
            wedding
        ),

        "qr_image_url": qr.qr_image_url,

        "created_at": qr.created_at,
        "updated_at": qr.updated_at,
    }


# =====================================================
# CREATE QR
# =====================================================

async def create_qr_code(
    db: Session,
    wedding,
    qr_image: UploadFile,
):

    existing_qr = get_qr_code(
        db,
        wedding.id,
    )

    if existing_qr is not None:
        raise ValueError(
            "A QR Code already exists for this wedding."
        )

    image_url = await save_qr_image(
        qr_image
    )

    try:
        qr = QRCode(
            wedding_id=wedding.id,
            qr_image_url=image_url,
        )

        db.add(qr)

        db.commit()

        db.refresh(qr)

        return qr

    except Exception:
        db.rollback()

        delete_qr_image(
            image_url
        )

        raise


# =====================================================
# UPDATE QR
# =====================================================

async def update_qr_code(
    db: Session,
    wedding,
    qr_image: UploadFile | None = None,
):

    qr = get_qr_code(
        db,
        wedding.id,
    )

    if qr is None:
        return None

    old_image_url = (
        qr.qr_image_url
    )

    new_image_url = None

    if qr_image is not None:
        new_image_url = (
            await save_qr_image(
                qr_image
            )
        )

        qr.qr_image_url = (
            new_image_url
        )

    try:
        db.commit()

        db.refresh(qr)

        if new_image_url:
            delete_qr_image(
                old_image_url
            )

        return qr

    except Exception:
        db.rollback()

        if new_image_url:
            delete_qr_image(
                new_image_url
            )

        raise


# =====================================================
# DELETE QR
# =====================================================

def delete_qr_code(
    db: Session,
    wedding_id: int,
):

    qr = get_qr_code(
        db,
        wedding_id,
    )

    if qr is None:
        return False

    image_url = (
        qr.qr_image_url
    )

    db.delete(qr)

    db.commit()

    delete_qr_image(
        image_url
    )

    return True