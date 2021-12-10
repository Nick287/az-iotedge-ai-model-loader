from msrest.authentication import ApiKeyCredentials
import requests
import time
import sys
from time import sleep
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult
from azure.iot.hub.protocol.operations.devices_operations import DevicesOperations

iothub_connection_str = ""
device_id = ""
module_id = ""

# RegistryManager
iothub_registry_manager = IoTHubRegistryManager.from_connection_string(iothub_connection_str)
module_twin = iothub_registry_manager.get_module_twin(device_id,module_id)

# if module_twin.properties.reported["LatestAIModelName"] is not None:
#     print(module_twin.properties.reported["LatestAIModelName"])

module_twin.properties.desired["FileName"] = "tensorflow001.zip"
module_twin.properties.desired["DownloadUrl"] = "https://avasample76havxesh5rb6.blob.core.windows.net/testaidownload/tensorflow001.zip?sp=r&st=2021-11-25T14:32:49Z&se=2022-09-28T22:32:49Z&sv=2020-08-04&sr=b&sig=INTK5SNsvKU%%3D"
module_twin.properties.desired["ContentMD5"] = "wPJ4M5M4BVAkuk6fdJYODg=="

iothub_registry_manager.update_module_twin(device_id,module_id,module_twin,module_twin.etag)

time.sleep(2)
module_twin = iothub_registry_manager.get_module_twin(device_id,module_id)
reportedTwins = module_twin.properties.reported
if "LatestAIModelNam1e" in reportedTwins:
    print(reportedTwins["LatestAIModelName"])