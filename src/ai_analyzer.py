import os
import configparser
from openai import OpenAI
from src import printcolors as pc
from .print_color import print_color

class AIAnalyzer:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join('config', 'ai_config.ini')
        self.client = None
        self.enabled = False
        self.model = None
        self.max_tokens = None
        
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
            self.enabled = self.config.getboolean('AI', 'enabled', fallback=False)
            if self.enabled:
                api_key = self.config.get('AI', 'api_key', fallback='')
                self.model = self.config.get('AI', 'model', fallback='gpt-3.5-turbo')
                self.max_tokens = self.config.getint('AI', 'max_tokens', fallback=500)
                if api_key:
                    self.client = OpenAI(api_key=api_key)
    
    def _get_analysis(self, prompt, data):
        """Get AI analysis for given prompt and data"""
        if not self.enabled or not self.client:
            return None
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Instagram analyst."},
                    {"role": "user", "content": f"{prompt}\n\nData:\n{data}"}
                ],
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print_color(f"Error getting AI analysis: {str(e)}", "red")
            return None
    
    def analyze_followers(self, followers):
        """Analyze followers data"""
        if not followers:
            return None
        prompt = "Analyze these Instagram followers and provide insights about their demographics, engagement patterns, and potential fake accounts."
        return self._get_analysis(prompt, str(followers))
    
    def analyze_posts(self, posts):
        """Analyze posts data"""
        if not posts:
            return None
        prompt = "Analyze these Instagram posts and provide insights about content strategy, engagement patterns, and post timing."
        return self._get_analysis(prompt, str(posts))
    
    def analyze_hashtags(self, hashtags):
        """Analyze hashtags data"""
        if not hashtags:
            return None
        prompt = "Analyze these Instagram hashtags and provide insights about their relevance, popularity, and potential reach."
        return self._get_analysis(prompt, str(hashtags))
    
    def get_profile_summary(self, profile_data):
        """Generate profile summary"""
        if not profile_data:
            return None
        prompt = "Generate a comprehensive summary of this Instagram profile, including key metrics, content themes, and growth patterns."
        return self._get_analysis(prompt, str(profile_data))
    
    def analyze_sentiment(self, text_data, data_type="captions"):
        """Analyze sentiment of text data"""
        if not text_data:
            return None
        prompt = f"Analyze the sentiment of these Instagram {data_type} and provide insights about emotional tone and engagement patterns."
        return self._get_analysis(prompt, str(text_data))
    
    def categorize_hashtags(self, hashtags):
        """Categorize hashtags"""
        if not hashtags:
            return None
        prompt = "Categorize these Instagram hashtags into relevant groups and explain their strategic value."
        return self._get_analysis(prompt, str(hashtags))
    
    def correlate_timeline(self, timeline_data):
        """Correlate timeline events"""
        if not timeline_data:
            return None
        prompt = "Analyze this Instagram timeline data and identify patterns, correlations, and significant events."
        return self._get_analysis(prompt, str(timeline_data))
    
    def generate_report(self, all_data):
        """Generate comprehensive report"""
        if not all_data:
            return None
        prompt = "Generate a comprehensive Instagram analysis report covering profile performance, content strategy, audience insights, and growth recommendations."
        return self._get_analysis(prompt, str(all_data)) 