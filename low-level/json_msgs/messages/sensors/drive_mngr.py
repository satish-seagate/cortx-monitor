# Copyright (c) 2001-2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

"""
 ****************************************************************************
  Description:       Defines the JSON message transmitted by the
                    DriveManagerMonitor. There may be a time when we need to
                    maintain state as far as messages being transmitted.  This
                    may involve aggregation of multiple messages before
                    transmissions or simply deferring an acknowledgment to
                    a later point in time.  For this reason, the JSON messages
                    are stored as objects which can be queued up, etc.
 ****************************************************************************
"""

import json

from cortx.sspl.json_msgs.messages.sensors.base_sensors_msg import BaseSensorMsg

class DriveMngrMsg(BaseSensorMsg):
    """The JSON message transmitted by the DriveManagerMonitor"""

    SENSOR_RESPONSE_TYPE = "disk_status_drivemanager"
    MESSAGE_VERSION      = "1.0.0"

    def __init__(self, enclosure,
                       drive_num,
                       status,
                       serial_num,
                       path_id,
                       username  = "SSPL-LL",
                       signature = "N/A",
                       time      = "N/A",
                       expires   = -1):
        super(DriveMngrMsg, self).__init__()

        # Split apart the drive status into status and reason values
        # Status is first word before the first '_'
        status, reason = str(status).split("_", 1)

        self._username       = username
        self._signature      = signature
        self._time           = time
        self._expires        = expires
        self._enclosure      = enclosure
        self._drive_num      = drive_num
        self._status         = status
        self._reason         = reason
        self._serial_num     = serial_num
        self._path_id        = path_id

        self._json = {"title" : self.TITLE,
                      "description" : self.DESCRIPTION,
                      "username" : self._username,
                      "signature" : self._signature,
                      "time" : self._time,
                      "expires" : self._expires,

                      "message" : {
                          "sspl_ll_msg_header": {
                                "schema_version" : self.SCHEMA_VERSION,
                                "sspl_version" : self.SSPL_VERSION,
                                "msg_version" : self.MESSAGE_VERSION
                                },
                          "sensor_response_type": {
                                self.SENSOR_RESPONSE_TYPE: {
                                    "enclosureSN" : self._enclosure,
                                    "diskNum" : int(self._drive_num),
                                    "diskStatus" : self._status,
                                    "diskReason" : self._reason,
                                    "serialNumber" : self._serial_num,
                                    "pathID" : self._path_id
                                    }
                                }
                          }
                      }

    def getJson(self):
        """Return a validated JSON object"""    
        # Validate the current message    
        self._json = self.validateMsg(self._json)       
        return json.dumps(self._json)

    def getEnclosure(self):
        return self._enclosure

    def getDriveNum(self):
        return self._drive_num

    def getStatus(self):
        return self._status

    def setStatus(self, _status):
        status, reason = _status.split("_", 1)
        self._json["message"]["sensor_response_type"][self.SENSOR_RESPONSE_TYPE]["diskStatus"] = status
        self._json["message"]["sensor_response_type"][self.SENSOR_RESPONSE_TYPE]["diskReason"] = reason

    def set_uuid(self, _uuid):
        self._json["message"]["sspl_ll_msg_header"]["uuid"] = _uuid
