from fastapi import APIRouter, Request, HTTPException

from ..identity_node import IdentityNode
from ..models import DataBaseModel, CopyDataBaseModel, NicknameIdentityBaseModel


router = APIRouter(prefix="/info", tags=["info"])


@router.post("/identity/{nickname}")
def nickname_identity_node(nickname: str, model: NicknameIdentityBaseModel, request: Request):
    node: IdentityNode = request.state.node

    identity = node.nickname_identity_node(nickname, model.search_id)
    if identity:
        return identity.serialize()

    raise HTTPException(
        status_code=500, detail="node search failed!")


@router.get("/search_entity/{nickname}")
def search_identity_node(nickname: str, request: Request):
    node: IdentityNode = request.state.node

    identity = node.search_identity_node(nickname)
    if identity:
        return identity.serialize()

    raise HTTPException(
        status_code=500, detail="node search failed!")


@router.put("/replicate")
def replicate(model: CopyDataBaseModel, request: Request):
    node: IdentityNode = request.state.node

    try:
        node.replicate(model.source, model.database_id)
        return node.serialize()
    except:
        raise HTTPException(
            status_code=500, detail="replicate database failed!")


@router.get("/replication_data")
def get_replication_data(request: Request):
    node: IdentityNode = request.state.node

    try:
        result = node.get_replication_data()
        return result.serialize()
    except:
        raise HTTPException(
            status_code=500, detail="replicate database failed!")


@router.post("/users")
def get_users(model: DataBaseModel, request: Request):
    node: IdentityNode = request.state.node

    try:
        users = node.get_users(model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="get users failed!"
        )
    else:
        return [{"nickname": nickname, "password": password, "ip": ip, "port": port} for (nickname, password, ip, port) in users]


@router.get("/all/{search_id}")
def get_all_nodes(search_id: int, request: Request):
    node: IdentityNode = request.state.node

    nodes = node.all_nodes(search_id)
    return [node.serialize() for node in nodes]
