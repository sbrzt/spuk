import os
import json
import hashlib
from datetime import datetime

class SimpleEntityCache:
    def __init__(self, cache_file=".build_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load()
        
    def _load(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"entities": {}, "templates": {}}
    
    def _save(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _entity_signature(self, entity_data):
        """Simple signature of entity data"""
        return f"{len(entity_data.properties)}:{len(entity_data.types)}"
    
    def _template_changed(self):
        """Check if any template has changed"""
        template_files = [
            "static/templates/entity.html",
            "static/templates/index.html"
        ]
        
        for template_file in template_files:
            if not os.path.exists(template_file):
                continue
                
            mtime = os.path.getmtime(template_file)
            cached_mtime = self.cache["templates"].get(template_file, 0)
            
            if mtime > cached_mtime:
                # Update all template times and return True
                for tf in template_files:
                    if os.path.exists(tf):
                        self.cache["templates"][tf] = os.path.getmtime(tf)
                self._save()
                return True
        return False
    
    def should_rebuild_entity(self, entity_data):
        """Check if entity should be rebuilt"""
        # If templates changed, rebuild all
        if self._template_changed():
            return True
            
        # Check if this specific entity changed
        current_sig = self._entity_signature(entity_data)
        cached_sig = self.cache["entities"].get(entity_data.uri)
        
        return current_sig != cached_sig
    
    def mark_entity_built(self, entity_data):
        """Mark entity as built"""
        self.cache["entities"][entity_data.uri] = self._entity_signature(entity_data)
        self._save()