


import yaml
from yaml import Loader 
	
from pydantic  import BaseModel
from typing import Optional
 
    
class Model(BaseModel):
	external_url: Optional[str] = 'http://localhost'
	listen: Optional[str] = '0.0.0.0'
	port: Optional[int] = '3050'
	version: Optional[str] = '1.0'
	worker: Optional[int] = 4
	loglevel: Optional[str] = 'info'
	cache: Optional[bool] = 'off'
	cache_srv: Optional[str] = 'redis'
	cache_port: Optional[int] = 6379
	debug: Optional[bool] = 'off'
	hunter: Optional[bool] = 'off'

class Settings:
	
	model:Model = None
    
	def __init__(self):
		with open("config.yaml", "r") as f:
			config = yaml.load(f,Loader=Loader)
			self.model = Model(**config)
   
   
Settings = Settings().model
 