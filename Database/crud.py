from sqlalchemy import select
from Database.connection import async_session
from Database.models import User,PlatformIdentity

async def get_or_create_users(
    platform: str,
    platform_user_id: str,
    display_name: str | None = None,
) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(PlatformIdentity).where(
                PlatformIdentity.platform == platform,
                PlatformIdentity.platform_user_id == platform_user_id,
            )
        )
        identity = result.scalar_one_or_none()

        if identity:
            result =  await session.execute(select(User).where(User.id == identity.user_id))
            return result.scalar_one()

        user = User(display_name=display_name)
        session.add(user)
        await session.flush()

        identity = PlatformIdentity(
            user_id = user.id,
            platform = platform,
            platform_user_id = platform_user_id,
        )
        session.add(identity)

        await session.commit()
        return user