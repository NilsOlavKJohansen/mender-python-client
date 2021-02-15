# Copyright 2021 Northern.tech AS
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import logging
from mender.log.log import DeploymentLogHandler

log = logging.getLogger(__name__)


# Only used for testing, when mender.py has not been run.
class SetUpLogForTesting:
    log_file = False
    log_level = "debug"
    no_syslog = False


def setup_logger(args=SetUpLogForTesting()):
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(name)s %(asctime)s %(levelname)-8s %(message)s",
    )
    root_logger = logging.getLogger("mender")
    level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }.get(args.log_level, logging.INFO)
    log.critical(level)
    handlers = []
    syslogger = (
        logging.NullHandler() if args.no_syslog else logging.handlers.SysLogHandler()
    )
    handlers.append(syslogger)
    if args.log_file:
        handlers.append(logging.FileHandler(args.log_file))
    deployment_log_handler = DeploymentLogHandler()
    handlers.append(deployment_log_handler)
    root_logger.deployment_log_handler = deployment_log_handler
    root_logger.setLevel(level)
    root_logger.handlers = handlers
    log.info(f"Log level set to {logging.getLevelName(level)}")
