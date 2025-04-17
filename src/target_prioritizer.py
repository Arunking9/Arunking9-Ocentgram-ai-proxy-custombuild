import configparser
import os
import openai
from src import printcolors as pc
from datetime import datetime
import json

class TargetPrioritizer:
    def __init__(self):
        self.enabled = False
        self.client = None
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 1000
        self._load_config()
    
    def _load_config(self):
        """Load AI configuration from file"""
        config_path = os.path.join("config", "ai_config.ini")
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)
            self.enabled = config.getboolean("AI", "enabled", fallback=False)
            if self.enabled:
                api_key = config.get("AI", "api_key", fallback="")
                if api_key:
                    self.client = openai.OpenAI(api_key=api_key)
                    self.model = config.get("AI", "model", fallback="gpt-3.5-turbo")
                    self.max_tokens = config.getint("AI", "max_tokens", fallback=1000)
    
    def analyze_targets(self, targets_data):
        """Analyze multiple targets and provide prioritization recommendations"""
        if not self.enabled or not self.client:
            return None
        
        prompt = f"""Analyze these Instagram targets and provide prioritization recommendations:
        {json.dumps(targets_data, indent=2)}
        
        Please provide:
        1. Target prioritization based on:
           - Engagement metrics
           - Content quality
           - Activity level
           - Follower growth
           - Post frequency
        2. Risk assessment for each target
        3. Recommended investigation order
        4. Key insights and patterns
        5. Potential investigation strategies
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in target prioritization: {str(e)}")
            return None
    
    def generate_target_report(self, targets_data):
        """Generate a comprehensive report for multiple targets"""
        if not self.enabled or not self.client:
            return None
        
        prompt = f"""Generate a comprehensive report for these Instagram targets:
        {json.dumps(targets_data, indent=2)}
        
        Please provide:
        1. Executive summary
        2. Target comparison matrix
        3. Risk assessment
        4. Investigation priorities
        5. Recommended actions
        6. Timeline suggestions
        7. Resource allocation recommendations
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating target report: {str(e)}")
            return None
    
    def analyze_target_relationships(self, targets_data):
        """Analyze relationships and connections between multiple targets"""
        if not self.enabled or not self.client:
            return None
        
        prompt = f"""Analyze relationships and connections between these Instagram targets:
        {json.dumps(targets_data, indent=2)}
        
        Please provide:
        1. Network analysis
        2. Common connections
        3. Interaction patterns
        4. Group dynamics
        5. Communication patterns
        6. Relationship strength indicators
        7. Potential collaboration evidence
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing target relationships: {str(e)}")
            return None 