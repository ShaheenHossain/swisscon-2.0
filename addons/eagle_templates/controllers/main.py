# -*- coding: utf-8 -*-

import json
import logging
import pprint

import requests
import werkzeug
from werkzeug import urls

from swiss import http
from swiss.addons.payment.models.payment_acquirer import ValidationError
from swiss.http import request

_logger = logging.getLogger(__name__)


