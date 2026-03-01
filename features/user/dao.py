"""Data Access Object (DAO) module for the user feature."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.security.encryption import encrypt_data
from common.security.hash import get_password_hash
from features.user.models import User
from features.user.schemas import UserCreate, UserUpdate
from sqlalchemy.orm import selectinload


class UserDAO:
    """Handles direct database access for the User entity."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the UserDAO with a database session.

        Args:
            session (AsyncSession): The asynchronous database session.
        """
        self.session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Fetch a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            Optional[User]: The user instance if found, otherwise None.
        """
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Fetch a user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            Optional[User]: The user instance if found, otherwise None.
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, user_in: UserCreate) -> User:
        """
        Create a new user record with protected data.

        Args:
            user_in (UserCreate): The user data transfer object.

        Returns:
            User: The newly created database user instance.
        """
        hashed_pwd = get_password_hash(user_in.password)

        # Encryption of PII (Personally Identifiable Information)
        enc_phone = None
        if user_in.phone_number:
            enc_phone = encrypt_data(user_in.phone_number)

        enc_addr = None
        if user_in.address:
            enc_addr = encrypt_data(user_in.address)

        new_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            second_last_name=user_in.second_last_name,
            username=user_in.username,
            password=hashed_pwd,
            address=enc_addr,
            phone_number=enc_phone,
            email=user_in.email,
            role_id=user_in.role_id,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get_by_id(self, user_id: int) -> Optional[User]:
            """Busca un usuario por ID cargando su rol para validaciones de seguridad."""
            query = select(User).options(selectinload(User.role), selectinload(User.vehicles)).where(User.id == user_id)
            result = await self.session.execute(query)
            return result.scalars().first()

    async def get_all(self) -> list[User]:
        """Obtiene todos los usuarios cargando sus roles."""
        query = select(User).filter(User.is_active == True).options(selectinload(User.role))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, db_user: User) -> None:
        """update  a user's is_active status to False."""
        db_user.is_active = False
        if db_user.vehicles:
            for vehicle in db_user.vehicles:
                vehicle.is_active = False
        await self.session.commit()

    async def update(self, db_user: User, user_in: UserUpdate) -> User:
        """
        Updates an existing user's attributes.
        Handles re-hashing of passwords and re-encryption of sensitive data.
        """
        update_data = user_in.model_dump(exclude_unset=True)

        # If the user wants to update their password, hash it before saving
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])

        # If the user wants to update phone or address, encrypt them
        if "phone_number" in update_data:
            update_data["phone_number"] = encrypt_data(update_data["phone_number"])

        if "address" in update_data:
            update_data["address"] = encrypt_data(update_data["address"])

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user