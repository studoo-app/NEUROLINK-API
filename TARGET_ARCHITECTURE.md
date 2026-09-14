# Architecture cible

Ce document décrit l'arborescence cible du projet et, pour chaque fichier, la provenance attendue depuis le code actuel.

## Arborescence cible

```text
NEUROLINK-API/
├─ app/
│  ├─ main.py
│  │  └─ Contient le bootstrap FastAPI :
│  │     - création de `app = FastAPI(...)`
│  │     - `Base.metadata.create_all(bind=engine)`
│  │     - inclusion des routers
│  │     Source actuelle : `main.py`
│  │     Remarque : aujourd'hui `main.py` pointe encore vers `routers.*`, pas vers `features/*`.
│  │
│  ├─ startup.py
│  │  └─ Contiendra les hooks de démarrage :
│  │     - initialisation DB
│  │     - seed au démarrage si conservé
│  │     Source actuelle : logique partiellement dans `main.py`
│  │     et potentiellement `seed.py`
│  │
│  └─ config.py
│     └─ Contiendra la configuration applicative :
│        - DATABASE_URL
│        - variables d'environnement
│        - paramètres de sécurité
│        Source actuelle : `database.py` pour `DATABASE_URL`
│        Aucun vrai fichier dédié aujourd'hui.
│
├─ core/
│  ├─ __init__.py
│  │  └─ Package marker
│  │
│  ├─ database.py
│  │  └─ Contient :
│  │     - `engine`
│  │     - `Base`
│  │     - `SessionLocal`
│  │     - `get_db()`
│  │     - `get_session()`
│  │     Source actuelle : `database.py`
│  │
│  ├─ enums.py
│  │  └─ Contiendra les enums métier partagés :
│  │     - `Tier`
│  │     - `Category`
│  │     - `Severity`
│  │     - `ApiKeyRole`
│  │     Source actuelle : `schemas/enums.py`
│  │     Remarque : `core/enums.py` n'existe pas dans le repo actuel.
│  │
│  ├─ security.py
│  │  └─ Contiendra uniquement les helpers de sécurité techniques :
│  │     - `API_KEY_PREFIX`
│  │     - `generate_api_key()`
│  │     - `hash_api_key()`
│  │     - `extract_key_id()`
│  │     Source actuelle : `security/hashing.py`
│  │     Remarque : la logique de dépendance FastAPI de `security/api_key.py`
│  │     ne doit pas aller ici, mais dans `features/auth/dependencies.py`.
│  │
│  └─ base.py
│     └─ Optionnel.
│        Si créé, il contiendra éventuellement `Base` ou des utilitaires ORM communs.
│        Source actuelle : aujourd'hui `Base` est dans `database.py`.
│
├─ features/
│  ├─ auth/
│  │  ├─ __init__.py
│  │  │  └─ Exports éventuels du module auth
│  │  │
│  │  ├─ models.py
│  │  │  └─ Contiendra `ApiKeyModel`
│  │  │     Source actuelle : `models/models.py`
│  │  │     Correspondance exacte :
│  │  │     - classe `ApiKeyModel`
│  │  │
│  │  ├─ schemas.py
│  │  │  └─ Contiendra :
│  │  │     - `ApiKeyCreate`
│  │  │     - `ApiKeyResponse`
│  │  │     - `ApiKeyCreatedResponse`
│  │  │     Source actuelle : `schemas/ApiKey.py`
│  │  │
│  │  ├─ service.py
│  │  │  └─ Contiendra la logique métier auth :
│  │  │     - `create_api_key(...)`
│  │  │     - plus tard révocation / listing / rotation si besoin
│  │  │     Source actuelle : `services/api_key.py`
│  │  │
│  │  ├─ dependencies.py
│  │  │  └─ Contiendra les dépendances FastAPI :
│  │  │     - `get_current_api_key(...)`
│  │  │     - `require_admin(...)`
│  │  │     Source actuelle : `security/api_key.py`
│  │  │     Remarque : ce fichier est bien de la feature auth,
│  │  │     pas du core security.
│  │  │
│  │  ├─ router.py
│  │  │  └─ Contiendra les endpoints :
│  │  │     - `POST /authentification/generate-key`
│  │  │     - `GET /authentification/list-keys`
│  │  │     - `DELETE /authentification/revoke/{key_id}`
│  │  │     Source actuelle : `routers/api_keys.py`
│  │  │
│  │  └─ seed.py
│  │     └─ Optionnel.
│  │        Contiendra un seed auth si tu veux créer une clé admin par défaut
│  │        ou préparer des données de dev.
│  │        Source actuelle : pas de vrai seed auth dédié.
│  │        `create_admin_keys.py` est un script manuel, pas un seed runtime.
│  │
│  ├─ implants/
│  │  ├─ __init__.py
│  │  │  └─ Exports éventuels du module implants
│  │  │
│  │  ├─ models.py
│  │  │  └─ Contiendra :
│  │  │     - `implant_incompatibilities`
│  │  │     - `ImplantModel`
│  │  │     - `SideEffectModel`
│  │  │     Source actuelle : `models/models.py`
│  │  │     Correspondances exactes :
│  │  │     - table `implant_incompatibilities`
│  │  │     - classe `ImplantModel`
│  │  │     - classe `SideEffectModel`
│  │  │
│  │  ├─ schemas.py
│  │  │  └─ Contiendra :
│  │  │     - `Implant`
│  │  │     - `Prerequisites`
│  │  │     - `SideEffect`
│  │  │     Source actuelle :
│  │  │     - `schemas/Implant.py`
│  │  │     - `schemas/Prerequisites.py`
│  │  │     - `schemas/SideEffect.py`
│  │  │
│  │  ├─ service.py
│  │  │  └─ Contiendra la logique métier implants :
│  │  │     - construction / transformation des implants
│  │  │     - sérialisation éventuelle
│  │  │     - seed des implants si tu gardes ce choix ici
│  │  │     Source actuelle :
│  │  │     - `seed.py` pour les données et seed
│  │  │     - une partie du mapping est actuellement dans `routers/implants.py`
│  │  │
│  │  ├─ router.py
│  │  │  └─ Contiendra les endpoints implants :
│  │  │     - `GET /implants/`
│  │  │     - plus tard `GET /implants/{reference}`
│  │  │     Source actuelle : `routers/implants.py`
│  │  │
│  │  ├─ seed.py
│  │  │  └─ Optionnel si tu veux séparer clairement seed et service.
│  │  │     Source actuelle : `seed.py`
│  │  │     Remarque : aujourd'hui le seed est top-level, pas dans la feature.
│  │  │
│  │  └─ repository.py
│  │     └─ Optionnel.
│  │        Requêtes SQLAlchemy dédiées si la feature grossit.
│  │        Pas de source dédiée aujourd'hui.
│  │
│  └─ hello/
│     ├─ __init__.py
│     │  └─ Package marker
│     │
│     └─ router.py
│        └─ Contiendra :
│           - `GET /hello/`
│           - `GET /hello/health`
│           Source actuelle : `routers/hello.py`
│
├─ scripts/
│  ├─ create_admin_keys.py
│  │  └─ Script manuel de création d'une clé admin
│  │     Source actuelle : `create_admin_keys.py`
│  │     Remarque : à corriger ensuite car il importe encore
│  │     `schemas.enums` et `services.api_key`.
│  │
│  └─ seed_dev_data.py
│     └─ Optionnel.
│        Pour lancer les seeds hors runtime applicatif.
│        Source actuelle potentielle : `seed.py`
│
├─ tests/
│  ├─ test_auth.py
│  │  └─ À créer : tests des clés API et permissions
│  ├─ test_implants.py
│  │  └─ À créer : tests listing implants / détail / auth
│  └─ test_health.py
│     └─ À créer : tests hello / health
│
├─ .env
│  └─ À créer si tu externalises config et secrets
│
├─ .env.example
│  └─ À créer comme modèle de config
│
├─ Dockerfile
│  └─ Source actuelle : `Dockerfile`
│
├─ docker-compose.yml
│  └─ Source actuelle : `docker-compose.yml`
│
├─ pyproject.toml
│  └─ Source actuelle : `pyproject.toml`
│
├─ README.md
│  └─ Source actuelle : `README.md`
│
└─ database.db
   └─ Base SQLite actuelle
```

## Correspondances importantes vérifiées

| Cible | Source actuelle vérifiée |
|---|---|
| `core/database.py` | `database.py` |
| `core/enums.py` | `schemas/enums.py` |
| `core/security.py` | `security/hashing.py` |
| `features/auth/models.py` | `models/models.py` (`ApiKeyModel`) |
| `features/auth/schemas.py` | `schemas/ApiKey.py` |
| `features/auth/service.py` | `services/api_key.py` |
| `features/auth/dependencies.py` | `security/api_key.py` |
| `features/auth/router.py` | `routers/api_keys.py` |
| `features/implants/models.py` | `models/models.py` (`ImplantModel`, `SideEffectModel`, `implant_incompatibilities`) |
| `features/implants/schemas.py` | `schemas/Implant.py`, `schemas/Prerequisites.py`, `schemas/SideEffect.py` |
| `features/implants/router.py` | `routers/implants.py` |
| `features/implants/seed.py` | `seed.py` |
| `features/hello/router.py` | `routers/hello.py` |

## Point de vigilance

Le repo actuel est encore dans l'ancienne architecture :

- pas de dossier `core/`
- pas de dossier `features/`
- `main.py` importe encore `routers.*`
- les enums sont encore dans `schemas/enums.py`

Ce document décrit donc bien la cible, avec les correspondances réelles vérifiées depuis le code présent.

## Contenu cible de chaque fichier

Cette section décrit le contenu attendu de chaque fichier cible, en repartant du code actuel et de la structure souhaitée.

### `app/main.py`

Doit contenir le point d'entrée FastAPI :

- création de l'application
- import des routers depuis `features/*`
- initialisation du schéma SQLAlchemy
- appel du startup/seed si retenu

Provenance actuelle :

- `main.py`

Contenu attendu :

```python
from fastapi import FastAPI

from app.startup import run_startup
from core.database import Base, engine
from features.auth.router import router as auth_router
from features.hello.router import router as hello_router
from features.implants.router import router as implants_router

app = FastAPI(
    title="NeuroLink API",
    description="API for managing implants and related data",
    version="1.0.0",
)

api_route_prefix = "/api/v1"

Base.metadata.create_all(bind=engine)
run_startup()

app.include_router(hello_router, prefix=api_route_prefix)
app.include_router(auth_router, prefix=api_route_prefix)
app.include_router(implants_router, prefix=api_route_prefix)
```

### `app/startup.py`

Doit isoler ce qui est aujourd'hui fait implicitement au démarrage.

Provenance actuelle :

- `main.py`
- `seed.py`

Contenu attendu :

```python
from features.implants.seed import seed_database


def run_startup() -> None:
    seed_database()
```

### `app/config.py`

Doit centraliser les variables de configuration.

Provenance actuelle :

- `database.py` pour `DATABASE_URL`

Contenu attendu :

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
```

### `core/database.py`

Doit reprendre le contenu de l'actuel `database.py`.

Provenance actuelle :

- `database.py`

Contenu attendu :

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    return SessionLocal()
```

### `core/enums.py`

Doit reprendre les enums actuellement placés dans `schemas/enums.py`.

Provenance actuelle :

- `schemas/enums.py`

Contenu attendu :

```python
from enum import Enum


class Tier(str, Enum):
    SALVAGE = "Salvage"
    STANDARD = "Standard"
    CLINICAL = "Clinical"
    PRIME = "Prime"
    MILSPEC = "MilSpec"
    PROTOTYPE = "Prototype"


class Category(str, Enum):
    NEURAL = "Neural"
    SENSORY = "Sensory"
    MOTOR = "Motor"
    METABOLIC = "Metabolic"
    CARDIOVASCULAR = "Cardiovascular"
    DERMAL = "Dermal"


class Severity(str, Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"


class ApiKeyRole(str, Enum):
    USER = "User"
    ADMIN = "Admin"
    SUPERADMIN = "SuperAdmin"
```

### `core/security.py`

Doit reprendre les helpers techniques de `security/hashing.py`.

Provenance actuelle :

- `security/hashing.py`

Contenu attendu :

```python
import hashlib
import secrets

API_KEY_PREFIX = "sk"


def generate_api_key() -> tuple[str, str]:
    key_id = secrets.token_hex(4)
    secret = secrets.token_urlsafe(32)
    api_key = f"{API_KEY_PREFIX}_{key_id}_{secret}"
    return api_key, key_id


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def extract_key_id(api_key: str) -> str | None:
    parts = api_key.split("_", maxsplit=2)
    if len(parts) != 3:
        return None

    prefix, key_id, _ = parts
    if prefix != API_KEY_PREFIX:
        return None

    return key_id
```

### `features/auth/models.py`

Doit contenir uniquement le modèle SQLAlchemy des clés API.

Provenance actuelle :

- `models/models.py`

Contenu attendu :

```python
from sqlalchemy import Boolean, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from core.enums import ApiKeyRole


class ApiKeyModel(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )
    key_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[ApiKeyRole] = mapped_column(Enum(ApiKeyRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
```

### `features/auth/schemas.py`

Doit reprendre `schemas/ApiKey.py`.

Provenance actuelle :

- `schemas/ApiKey.py`

Contenu attendu :

```python
from pydantic import BaseModel, ConfigDict

from core.enums import ApiKeyRole


class ApiKeyCreate(BaseModel):
    name: str
    role: ApiKeyRole


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    key_id: str
    role: ApiKeyRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreatedResponse(ApiKeyResponse):
    api_key: str
```

### `features/auth/service.py`

Doit reprendre la logique métier de `services/api_key.py`.

Provenance actuelle :

- `services/api_key.py`

Contenu attendu :

```python
from sqlalchemy.orm import Session

from core.enums import ApiKeyRole
from core.security import generate_api_key, hash_api_key
from features.auth.models import ApiKeyModel


def create_api_key(
    db: Session,
    name: str,
    role: ApiKeyRole,
) -> tuple[ApiKeyModel, str]:
    api_key, key_id = generate_api_key()

    db_api_key = ApiKeyModel(
        name=name,
        key_id=key_id,
        key_hash=hash_api_key(api_key),
        role=role,
        is_active=True,
    )

    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    return db_api_key, api_key
```

### `features/auth/dependencies.py`

Doit reprendre `security/api_key.py`, car c'est la logique d'utilisation de l'auth dans FastAPI.

Provenance actuelle :

- `security/api_key.py`

Contenu attendu :

```python
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from core.enums import ApiKeyRole
from core.security import extract_key_id, hash_api_key
from features.auth.models import ApiKeyModel

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_api_key(
    api_key: Annotated[str | None, Depends(api_key_header)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiKeyModel:
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    key_id = extract_key_id(api_key)
    if key_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    statement = select(ApiKeyModel).where(ApiKeyModel.key_id == key_id)
    db_api_key = db.scalar(statement)

    if db_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    if not db_api_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key disabled",
        )

    if not secrets.compare_digest(hash_api_key(api_key), db_api_key.key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return db_api_key


def require_admin(
    api_key: Annotated[ApiKeyModel, Depends(get_current_api_key)],
) -> ApiKeyModel:
    if api_key.role != ApiKeyRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin API key required",
        )

    return api_key
```

### `features/auth/router.py`

Doit reprendre `routers/api_keys.py`.

Provenance actuelle :

- `routers/api_keys.py`

Contenu attendu :

```python
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from features.auth.dependencies import require_admin
from features.auth.models import ApiKeyModel
from features.auth.schemas import ApiKeyCreate, ApiKeyCreatedResponse, ApiKeyResponse
from features.auth.service import create_api_key

router = APIRouter(
    prefix="/authentification",
    tags=["Authentification"],
    dependencies=[Depends(require_admin)],
)


@router.post(
    "/generate-key",
    response_model=ApiKeyCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_key(
    payload: ApiKeyCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_key, api_key = create_api_key(
        db=db,
        name=payload.name,
        role=payload.role,
    )

    return ApiKeyCreatedResponse(
        id=db_key.id,
        name=db_key.name,
        key_id=db_key.key_id,
        role=db_key.role,
        is_active=db_key.is_active,
        api_key=api_key,
    )


@router.get("/list-keys", response_model=list[ApiKeyResponse])
def list_api_keys(db: Annotated[Session, Depends(get_db)]):
    statement = select(ApiKeyModel)
    return db.scalars(statement).all()


@router.delete("/revoke/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    statement = select(ApiKeyModel).where(ApiKeyModel.key_id == key_id)
    api_key = db.scalar(statement)

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    api_key.is_active = False
    db.commit()
```

### `features/implants/models.py`

Doit extraire du fichier actuel `models/models.py` uniquement les modèles implants.

Provenance actuelle :

- `models/models.py`

Contenu attendu :

```python
from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.enums import Category, Severity, Tier

implant_incompatibilities = Table(
    "implant_incompatibilities",
    Base.metadata,
    Column("implant_reference", ForeignKey("implants.reference"), primary_key=True),
    Column(
        "incompatible_implant_reference",
        ForeignKey("implants.reference"),
        primary_key=True,
    ),
)


class ImplantModel(Base):
    __tablename__ = "implants"

    reference: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    category: Mapped[Category] = mapped_column(Enum(Category), nullable=False)
    tier: Mapped[Tier] = mapped_column(Enum(Tier), nullable=False)
    prerequisites: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    side_effects: Mapped[list[SideEffectModel]] = relationship(
        back_populates="implant",
        cascade="all, delete-orphan",
    )
    incompatible_implants: Mapped[list[ImplantModel]] = relationship(
        "ImplantModel",
        secondary=implant_incompatibilities,
        primaryjoin=reference == implant_incompatibilities.c.implant_reference,
        secondaryjoin=reference == implant_incompatibilities.c.incompatible_implant_reference,
    )


class SideEffectModel(Base):
    __tablename__ = "side_effects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    implant_reference: Mapped[str] = mapped_column(
        ForeignKey("implants.reference"),
        nullable=False,
        index=True,
    )
    reference: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    implant: Mapped[ImplantModel] = relationship(back_populates="side_effects")
```

### `features/implants/schemas.py`

Doit fusionner les fichiers `schemas/Implant.py`, `schemas/Prerequisites.py` et `schemas/SideEffect.py`.

Provenance actuelle :

- `schemas/Implant.py`
- `schemas/Prerequisites.py`
- `schemas/SideEffect.py`

Contenu attendu :

```python
from pydantic import BaseModel, ConfigDict, Field

from core.enums import Category, Tier


class Prerequisites(BaseModel):
    minAge: int | None = None
    maxAge: int | None = None
    minSize: int | None = None
    maxSize: int | None = None
    minWeight: int | None = None
    maxWeight: int | None = None
    incompatibleImplants: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SideEffect(BaseModel):
    reference: str
    name: str
    severity: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class Implant(BaseModel):
    reference: str
    name: str
    description: str
    category: Category
    tier: Tier
    prerequisites: Prerequisites | None = Prerequisites()
    sideseffects: list[SideEffect] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
```

### `features/implants/service.py`

Doit contenir :

- la génération des implants de seed
- la génération des side effects
- la description
- le seed principal
- idéalement la sérialisation depuis SQLAlchemy vers Pydantic

Provenance actuelle :

- `seed.py`
- une partie du mapping de `routers/implants.py`

Contenu attendu :

```python
from __future__ import annotations

from core.database import SessionLocal
from core.enums import Category, Severity, Tier
from features.implants.models import ImplantModel, SideEffectModel
from features.implants.schemas import Implant, Prerequisites

IMPLANT_COUNT = 50

SIDE_EFFECT_TEMPLATES = (
    {
        "reference": "SE-HEADACHE",
        "name": "Headache",
        "severity": Severity.MILD,
        "description": "Transient discomfort during neural calibration.",
    },
    {
        "reference": "SE-NAUSEA",
        "name": "Nausea",
        "severity": Severity.MODERATE,
        "description": "Vestibular disturbance after synchronization.",
    },
    {
        "reference": "SE-INFLAMMATION",
        "name": "Inflammation",
        "severity": Severity.SEVERE,
        "description": "Localized tissue reaction requiring follow-up.",
    },
)

IMPLANT_NAMES = {
    Category.NEURAL: [
        "CortexLink",
        "Synapse Relay",
        "Myelin Mesh",
        "NeuroFuse",
        "Cranial Array",
        "Signal Lattice",
        "Axon Gate",
        "Cerebral Node",
        "Pulse Thread",
        "Thought Bridge",
    ],
    Category.SENSORY: [
        "Optic Bloom",
        "Auditory Lattice",
        "Tactile Veil",
        "Spectral Lens",
        "Sensory Mesh",
        "Retina Thread",
        "Vibrance Array",
        "Echo Crown",
        "Signal Bloom",
        "Perception Grid",
    ],
    Category.MOTOR: [
        "Torque Anchor",
        "Kinetic Spine",
        "Flexion Core",
        "Motion Tether",
        "Stride Relay",
        "Servo Thread",
        "Joint Matrix",
        "Power Lattice",
        "Muscle Sync",
        "Limb Mesh",
    ],
    Category.METABOLIC: [
        "Nutrient Gate",
        "Cellular Regulator",
        "Flux Array",
        "Metabolic Core",
        "Balance Mesh",
        "Biofilter Node",
        "Vital Lattice",
        "Assimilation Drive",
        "Homeostasis Thread",
        "Metabolic Crown",
    ],
    Category.CARDIOVASCULAR: [
        "Heartline Coil",
        "Pulse Beacon",
        "Vascular Mesh",
        "Flow Anchor",
        "Circulation Core",
        "Hemodynamic Thread",
        "Aortic Relay",
        "Cardio Lattice",
        "Pulse Matrix",
        "Valve Sync",
    ],
    Category.DERMAL: [
        "Skin Shield",
        "Thermal Veil",
        "Barrier Mesh",
        "Dermal Weave",
        "Shield Lattice",
        "Protective Thread",
        "Cell Guard",
        "Barrier Core",
        "Skin Relay",
        "Thermal Anchor",
    ],
}


def build_prerequisites(index: int) -> dict[str, int | None]:
    return {
        "minAge": 18 + (index % 5),
        "maxAge": 55 + (index % 15),
        "minSize": 145 + (index % 10),
        "maxSize": 190 + (index % 12),
        "minWeight": 45 + (index % 8),
        "maxWeight": 95 + (index % 10),
    }


def build_description(category: Category, tier: Tier, name: str) -> str:
    benefit_map = {
        Category.NEURAL: "restores cortical signal fidelity and cuts synaptic delay during high-load neural tasks.",
        Category.SENSORY: "sharpens sensory input, stabilizes perception, and improves contextual awareness in noisy environments.",
        Category.MOTOR: "increases biomechanical control, smooths movement, and reduces fatigue under sustained exertion.",
        Category.METABOLIC: "regulates nutrient transfer and keeps homeostatic rhythms stable during stress or recovery.",
        Category.CARDIOVASCULAR: "supports circulatory efficiency and maintains reliable flow under prolonged physical demand.",
        Category.DERMAL: "improves barrier resilience and thermal control while reducing irritation and tissue stress.",
    }
    tier_map = {
        Tier.SALVAGE: "a reclaimed device intended for emergency fallback and short-term stabilization",
        Tier.STANDARD: "a dependable field model built for everyday performance",
        Tier.CLINICAL: "a clinically validated implant engineered for precision and long-term safety",
        Tier.PRIME: "a premium implant designed for exceptional endurance and adaptive control",
        Tier.MILSPEC: "a hardened implant optimized for harsh operating environments and physical stress",
        Tier.PROTOTYPE: "an experimental platform designed for controlled testing and iterative refinement",
    }
    return (
        f"{name} is {tier_map[tier]} for users who need consistent performance in demanding conditions. "
        f"It {benefit_map[category]}"
    )


def build_implant(index: int) -> ImplantModel:
    categories = list(Category)
    tiers = list(Tier)
    category = categories[index % len(categories)]
    tier = tiers[index % len(tiers)]
    name = IMPLANT_NAMES[category][index % len(IMPLANT_NAMES[category])]

    implant = ImplantModel(
        reference=f"REF{index + 1:03d}",
        name=name,
        description=build_description(category, tier, name),
        category=category,
        tier=tier,
        prerequisites=build_prerequisites(index),
    )

    implant.side_effects = [
        SideEffectModel(
            reference=f"{template['reference']}-{index + 1:03d}",
            name=template["name"],
            severity=template["severity"],
            description=template["description"],
        )
        for template in SIDE_EFFECT_TEMPLATES[: 2 + (index % 2)]
    ]

    return implant


def serialize_implant(implant: ImplantModel) -> Implant:
    prerequisites_data = dict(implant.prerequisites or {})
    prerequisites_data["incompatibleImplants"] = [
        incompatible.reference for incompatible in implant.incompatible_implants
    ]

    return Implant(
        reference=implant.reference,
        name=implant.name,
        description=implant.description,
        category=implant.category,
        tier=implant.tier,
        prerequisites=Prerequisites(**prerequisites_data),
        sideseffects=[
            {
                "reference": side_effect.reference,
                "name": side_effect.name,
                "severity": side_effect.severity.value,
                "description": side_effect.description,
            }
            for side_effect in implant.side_effects
        ],
    )


def seed_implants() -> None:
    with SessionLocal() as db:
        if db.query(ImplantModel).count() >= IMPLANT_COUNT:
            return

        implants = [build_implant(index) for index in range(IMPLANT_COUNT)]
        implants_by_reference = {implant.reference: implant for implant in implants}
        seen_pairs: set[tuple[str, str]] = set()

        for index, implant in enumerate(implants):
            candidates: list[ImplantModel] = []
            for offset in (1, 7, 13, 19, 25):
                candidate_index = (index + offset) % IMPLANT_COUNT
                candidate_ref = f"REF{candidate_index + 1:03d}"
                if candidate_ref == implant.reference:
                    continue
                pair = (implant.reference, candidate_ref)
                reverse = (candidate_ref, implant.reference)
                if pair in seen_pairs or reverse in seen_pairs:
                    continue
                seen_pairs.add(pair)
                candidates.append(implants_by_reference[candidate_ref])
                if len(candidates) >= 2:
                    break
            implant.incompatible_implants = candidates

        db.add_all(implants)
        db.commit()
```

### `features/implants/router.py`

Doit reprendre `routers/implants.py`, mais sans la logique métier inline.

Provenance actuelle :

- `routers/implants.py`

Contenu attendu :

```python
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from features.auth.dependencies import get_current_api_key
from features.implants.models import ImplantModel
from features.implants.schemas import Implant
from features.implants.service import serialize_implant

router = APIRouter(
    prefix="/implants",
    tags=["Implant"],
    dependencies=[Depends(get_current_api_key)],
)


@router.get("/", response_model=list[Implant])
async def list_implants(db: Annotated[Session, Depends(get_db)]):
    implants = db.scalars(select(ImplantModel).order_by(ImplantModel.reference)).all()
    return [serialize_implant(implant) for implant in implants]


@router.get("/{reference}", response_model=Implant)
async def get_implant(
    reference: str,
    db: Annotated[Session, Depends(get_db)],
):
    implant = db.scalar(
        select(ImplantModel).where(ImplantModel.reference == reference)
    )
    if implant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Implant '{reference}' not found",
        )
    return serialize_implant(implant)
```

### `features/implants/seed.py`

Doit être un wrapper fin vers le service de seed.

Provenance actuelle :

- `seed.py`

Contenu attendu :

```python
from features.implants.service import seed_implants


def seed_database() -> None:
    seed_implants()
```

### `features/hello/router.py`

Doit reprendre `routers/hello.py`.

Provenance actuelle :

- `routers/hello.py`

Contenu attendu :

```python
from fastapi import APIRouter

router = APIRouter(prefix="/hello")


@router.get("/")
async def root():
    return {"message": "Welcome to NeuroLink Corp Components API!"}


@router.get("/health")
async def health():
    return {"message": "API is running smoothly!"}
```

### `scripts/create_admin_keys.py`

Doit garder le rôle de script manuel, mais avec les nouveaux imports.

Provenance actuelle :

- `create_admin_keys.py`

Contenu attendu :

```python
from core.database import get_session
from core.enums import ApiKeyRole
from features.auth.service import create_api_key


def main() -> None:
    db = get_session()

    try:
        db_key, api_key = create_api_key(
            db=db,
            name="Initial admin",
            role=ApiKeyRole.ADMIN,
        )

        print()
        print("Admin API key created")
        print()
        print(f"Key ID : {db_key.key_id}")
        print(f"API Key: {api_key}")
        print()
        print("Save this key now. It will not be displayed again.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
```
