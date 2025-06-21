"""
MetaNode dApp Templates
=====================
Template files for dApp integration with blockchain properties
"""

import os
import yaml
import json
from typing import Dict, Any, Optional

# Directory with template files
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_template(template_name: str) -> Dict[str, Any]:
    """
    Get template file contents
    
    Args:
        template_name: Name of template to get
        
    Returns:
        Template contents as dict
    """
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    
    if not os.path.exists(template_path):
        raise ValueError(f"Template does not exist: {template_name}")
    
    # Load YAML or JSON based on extension
    if template_name.endswith(('.yaml', '.yml')):
        with open(template_path, 'r') as f:
            return yaml.safe_load(f)
    elif template_name.endswith('.json'):
        with open(template_path, 'r') as f:
            return json.load(f)
    else:
        with open(template_path, 'r') as f:
            return f.read()
