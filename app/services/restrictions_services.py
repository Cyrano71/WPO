from enum import Enum
from app.services.check_services import CheckService

class OPERATORS(Enum):
    AND = 0
    OR = 1

class RestrictionsService:
    def __init__(self, check_service: CheckService) -> None:
        self._check_service = check_service

    async def run(self, items, arguments, operator: OPERATORS = OPERATORS.AND):
        result = True if operator == OPERATORS.AND else False
        operators = None
        if operator == OPERATORS.AND:
            operators = lambda a,b : a & b
        else:
            operators = lambda a,b : a | b

        for item in items:
            if "@or" in item:
                result = operators(result, await self.run(item["@or"], arguments, OPERATORS.OR))
            elif "@and" in item:
                result = operators(result, await self.run(item["@and"], arguments, OPERATORS.AND))
            else:
                result = operators(result, await self._check_service.run(item, arguments))
          
        return result