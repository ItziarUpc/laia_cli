from fastapi import APIRouter
from laiagenlib.Domain.LaiaBaseModel.ModelRepository import ModelRepository
from laiagenlib.Application.LaiaBaseModel import ReadLaiaBaseModel, CreateLaiaBaseModel, DeleteLaiaBaseModel, SearchLaiaBaseModel, UpdateLaiaBaseModel

def ExtraRoutes(repository: ModelRepository=None):
    router = APIRouter(tags=["Extra Routes"])

    return router
                    
""" 
**************************************************************************
Instructions to develop new routes
**************************************************************************

- Import models from the models file with: 
from .models import modelName1, modelName2

- To operate with the crud operations on the models here are examples of the usage:
await CreateLaiaBaseModel.create_laia_base_model(dict(element), modelName1, user_roles, repository)
await UpdateLaiaBaseModel.update_laia_base_model(element_id, values, modelName1, user_roles, repository)
await ReadLaiaBaseModel.read_laia_base_model(element_id, modelName1, user_roles, repository)
await DeleteLaiaBaseModel.delete_laia_base_model(element_id, modelName1, user_roles, repository)
await SearchLaiaBaseModel.search_laia_base_model(skip, limit, filters, orders, modelName1, user_roles, repository)
"""