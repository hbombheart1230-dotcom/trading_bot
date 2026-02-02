from typing import TypedDict, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    ticker: str
    market_data: Dict[str, Any]
    decision: str
    reason: str
    logs: Annotated[List[str], operator.add]
    messages: Annotated[List[Any], operator.add]
