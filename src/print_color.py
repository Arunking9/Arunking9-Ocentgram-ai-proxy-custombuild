def print_color(text, color, end='\n'):
    """Print colored text to console"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    if color in colors:
        print(f"{colors[color]}{text}{colors['reset']}", end=end)
    else:
        print(text, end=end) 