import time
from src import printcolors as pc

class Command:
    def __init__(self, osintgram):
        self.osintgram = osintgram
        self.commands = {
            "help": self.help,
            "info": self.osintgram.get_info,
            "followers": self.osintgram.get_followers,
            "following": self.osintgram.get_followings,
            "hashtags": self.osintgram.get_hashtags,
            "posts": self.osintgram.get_posts,
            "posts_analysis": self.osintgram.get_posts_analysis,
            "profile_summary": self.osintgram.get_profile_summary,
            "sentiment": self.osintgram.get_sentiment_analysis,
            "hashtag_categories": self.osintgram.get_hashtag_categories,
            "timeline": self.osintgram.get_timeline_correlation,
            "ai_report": self.osintgram.get_ai_report,
            "target_priority": self.osintgram.get_target_prioritization,
            "target_report": self.osintgram.get_target_report,
            "target_relationships": self.osintgram.get_target_relationships,
            "addrs": self.osintgram.get_addrs,
            "cache": self.osintgram.clear_cache,
            "captions": self.osintgram.get_captions,
            "commentdata": self.osintgram.get_comment_data,
            "comments": self.osintgram.get_total_comments,
            "fwersemail": self.osintgram.get_fwersemail,
            "fwingsemail": self.osintgram.get_fwingsemail,
            "fwersnumber": self.osintgram.get_fwersnumber,
            "fwingsnumber": self.osintgram.get_fwingsnumber,
            "mediatype": self.osintgram.get_media_type,
            "photodes": self.osintgram.get_photo_description,
            "photos": self.osintgram.get_user_photo,
            "propic": self.osintgram.get_user_propic,
            "stories": self.osintgram.get_user_stories,
            "tagged": self.osintgram.get_people_tagged_by_user,
            "target": self.osintgram.change_target,
            "wcommented": self.osintgram.get_people_who_commented,
            "wtagged": self.osintgram.get_people_who_tagged,
            "ip_status": self._show_ip_status,
            "rotate_ip": self._rotate_ip_manual
        }

    def help(self):
        """Show help message"""
        pc.printout("\nAvailable commands:\n", pc.CYAN)
        pc.printout("help - Show this help message\n", pc.WHITE)
        pc.printout("\nBasic Commands:\n", pc.YELLOW)
        pc.printout("info - Get target info\n", pc.WHITE)
        pc.printout("followers - Get target followers\n", pc.WHITE)
        pc.printout("following - Get users followed by target\n", pc.WHITE)
        pc.printout("hashtags - Get hashtags used by target\n", pc.WHITE)
        pc.printout("photos - Download target's photos\n", pc.WHITE)
        pc.printout("stories - Download target's stories\n", pc.WHITE)
        pc.printout("target - Set new target\n", pc.WHITE)
        
        pc.printout("\nAI-Powered Analysis:\n", pc.YELLOW)
        pc.printout("posts_analysis - Get AI analysis of posts\n", pc.WHITE)
        pc.printout("profile_summary - Get AI-powered profile summary\n", pc.WHITE)
        pc.printout("sentiment - Get sentiment analysis (caption/comment)\n", pc.WHITE)
        pc.printout("hashtag_categories - Get AI-powered hashtag categorization\n", pc.WHITE)
        pc.printout("timeline - Get AI-powered timeline correlation\n", pc.WHITE)
        pc.printout("ai_report - Generate comprehensive AI report\n", pc.WHITE)
        pc.printout("target_priority - Get AI-powered target prioritization\n", pc.WHITE)
        pc.printout("target_report - Generate comprehensive target report\n", pc.WHITE)
        pc.printout("target_relationships - Analyze relationships between targets\n", pc.WHITE)
        
        pc.printout("\nAdvanced Commands:\n", pc.YELLOW)
        pc.printout("addrs - Get all registered addresses\n", pc.WHITE)
        pc.printout("captions - Get target's photos captions\n", pc.WHITE)
        pc.printout("commentdata - Get comments on target's posts\n", pc.WHITE)
        pc.printout("fwersemail - Get email of target followers\n", pc.WHITE)
        pc.printout("fwingsemail - Get email of users followed by target\n", pc.WHITE)
        pc.printout("fwersnumber - Get phone number of target followers\n", pc.WHITE)
        pc.printout("fwingsnumber - Get phone number of users followed by target\n", pc.WHITE)
        pc.printout("mediatype - Get target's posts type\n", pc.WHITE)
        pc.printout("photodes - Get description of target's photos\n", pc.WHITE)
        pc.printout("propic - Download target's profile picture\n", pc.WHITE)
        pc.printout("tagged - Get list of users tagged by target\n", pc.WHITE)
        pc.printout("wcommented - Get users who commented\n", pc.WHITE)
        pc.printout("wtagged - Get users who tagged target\n", pc.WHITE)
        
        pc.printout("\nOutput Options:\n", pc.YELLOW)
        pc.printout("FILE=y/n - Enable/disable .txt output\n", pc.WHITE)
        pc.printout("JSON=y/n - Enable/disable .json output\n", pc.WHITE)
        pc.printout("cache - Clear cache of the tool\n", pc.WHITE)
        pc.printout("\nIP Rotation Commands:\n", pc.YELLOW)
        pc.printout("ip_status - Show current IP rotation status\n", pc.WHITE)
        pc.printout("rotate_ip - Manually rotate IP address\n", pc.WHITE)

    def execute(self, command):
        """Execute command"""
        if command in self.commands:
            if command == "sentiment":
                data_type = input("Enter data type (caption/comment): ").lower()
                if data_type not in ["caption", "comment"]:
                    pc.printout("Invalid data type. Use 'caption' or 'comment'.\n", pc.RED)
                    return
                self.commands[command](data_type)
            else:
                self.commands[command]()
        else:
            pc.printout("Command not found. Type 'help' to see available commands.\n", pc.RED)

    def _show_ip_status(self):
        """Show IP rotation status"""
        if self.osintgram.ip_rotator.enabled:
            pc.printout("\nIP Rotation Status:\n", pc.CYAN)
            pc.printout(f"Enabled: Yes\n", pc.WHITE)
            pc.printout(f"Rotation Interval: {self.osintgram.ip_rotator.rotation_interval} seconds\n", pc.WHITE)
            pc.printout(f"Last Rotation: {time.ctime(self.osintgram.ip_rotator.last_rotation)}\n", pc.WHITE)
        else:
            pc.printout("\nIP Rotation is currently disabled\n", pc.RED)
            pc.printout("Enable it in config/ip_config.ini\n", pc.YELLOW)

    def _rotate_ip_manual(self):
        """Manually rotate IP address"""
        if self.osintgram.ip_rotator.rotate_ip():
            pc.printout("IP address successfully rotated\n", pc.GREEN)
        else:
            pc.printout("Failed to rotate IP address\n", pc.RED) 