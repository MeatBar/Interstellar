import json
import os
import re
import time
from os.path import join
from pathlib import Path
from typing import List, Tuple, Optional

import dash
import plotly.graph_objects as go
from cryptography.fernet import Fernet as F
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_extensions.enrich import MultiplexerTransform, TriggerTransform, DashProxy


app = DashProxy(__name__, transforms=[TriggerTransform(), MultiplexerTransform()],
                external_stylesheets=[r'./assets/bWLwgP.css'])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
