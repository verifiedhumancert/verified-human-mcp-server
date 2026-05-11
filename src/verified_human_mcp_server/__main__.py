"""Allow running as: python -m verified_human_mcp_server"""

import logging
import os
import sys

from .server import mcp

logging.basicConfig(
    stream=sys.stderr,
    level=os.environ.get("VHC_LOG_LEVEL", "WARNING").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

mcp.run()
