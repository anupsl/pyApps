import thriftpy
from src.Constant.constant import constant


path = constant.rootPath + '/src/thriftFiles/'


nsadmin = thriftpy.load(path+"nsadmin.thrift", module_name="nsadmin_thrift")
darknight = thriftpy.load(path+"dark-knight.thrift", module_name="darknight_thrift")

luci = thriftpy.load(path+"luci.thrift", module_name="luci_thrift")
dracarys = thriftpy.load(path+"dracarys.thrift", module_name="dracarys_thrift")
pointsEngineRules = thriftpy.load(path+"pointsengine_rules.thrift", module_name="pointsengine_rules_thrift")
pointsEngine = thriftpy.load(path+"points_engine.thrift", module_name="points_engine_thrift")
nrules = thriftpy.load(path+"nrules.thrift", module_name="nrules_thrift")
emf = thriftpy.load(path+"emf.thrift", module_name="emf_thrift")
datamanager = thriftpy.load(path+"datamanager.thrift", module_name="datamanager_thrift")
peb = thriftpy.load(path+"peb.thrift", module_name="peb_thrift")

timeline = thriftpy.load(path+"temporal_engine.thrift", module_name="temporal_engine_thrift")
veneno = thriftpy.load(path+"veneno.thrift", module_name="veneno_thrift")
campaignShard = thriftpy.load(path+"campaign_shard.thrift", module_name="campaignShard_thrift")
facebook = thriftpy.load(path+"facebook.thrift", module_name="facebook_thrift")
reonDimension = thriftpy.load(path+"dimension.thrift", module_name="dimension_thrift")


