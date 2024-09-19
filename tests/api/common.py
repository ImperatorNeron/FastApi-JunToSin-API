from factory.alchemy import SQLAlchemyModelFactory
from httpx import AsyncClient


async def post_items(
    async_client: AsyncClient,
    prefix: str,
    factory: SQLAlchemyModelFactory,
    expected_count: int,
):
    items = factory.build_batch(size=expected_count)
    items_data = [item.to_read_model().model_dump(mode="json") for item in items]
    for json_item in items_data:
        await async_client.post(prefix, json=json_item)
    return items_data
