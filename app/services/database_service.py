
from app.database.models.operation import Operation

class DatabaseService:
    _operations: dict[Operation] = {}
    _fake_db_id = 1

    async def save_operation(self, name, priority, restrictions):
        self._operations[name] = Operation(name, priority, restrictions)
        return self._fake_db_id

    async def get_operation(self, name):
        return self._operations[name]