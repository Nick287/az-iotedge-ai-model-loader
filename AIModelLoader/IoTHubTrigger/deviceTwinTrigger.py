from msrest.authentication import ApiKeyCredentials
import requests
import time
import sys
from time import sleep
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult
from azure.iot.hub.protocol.operations.devices_operations import DevicesOperations

# bo AVA
# iothub_connection_str = "HostName=avasample76havxesh5rb6.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=q/8JCYncr2r1JS3CQCJVat5FpLl/2zA3SIoWZ6XShT0="
# device_id = "avasample-iot-edge-device"
# module_id = "APIModel"


iothub_connection_str = "HostName=avasample76havxesh5rb6.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=q/8JCYncr2r1JS3CQCJVat5FpLl/2zA3SIoWZ6XShT0="
device_id = "EdgeVM001"
module_id = "TensorFlowLoader"

# RegistryManager
iothub_registry_manager = IoTHubRegistryManager.from_connection_string(iothub_connection_str)
module_twin = iothub_registry_manager.get_module_twin(device_id,module_id)


module_twin.properties.desired["FileName"] = "tensorflow001.zip"
module_twin.properties.desired["DownloadUrl"] = "https://avasample76havxesh5rb6.blob.core.windows.net/testaidownload/tensorflow001.zip?sp=r&st=2021-11-25T14:32:49Z&se=2022-09-28T22:32:49Z&sv=2020-08-04&sr=b&sig=INTK5SNsvKU%2FYTlYkg7l11pTGjRFWvWk2T1MPbKS0QQ%3D"
module_twin.properties.desired["ContentMD5"] = "wPJ4M5M4BVAkuk6fdJYODg=="

iothub_registry_manager.update_module_twin(device_id,module_id,module_twin,module_twin.etag)

time.sleep(2)
module_twin = iothub_registry_manager.get_module_twin(device_id,module_id)
reportedTwins = module_twin.properties.reported

# if module_twin.properties.reported["LatestAIModelName"] is not None:
#     print(module_twin.properties.reported["LatestAIModelName"])

if "LatestAIModelName" in reportedTwins:
    print(reportedTwins["LatestAIModelName"])