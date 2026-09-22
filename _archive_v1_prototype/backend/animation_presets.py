"""
Feature 4: Animation Presets
Pre-configured animation sequences for common animations
"""


class AnimationPresets:
    """Pre-configured animation sequences"""
    
    @staticmethod
    def get_greeting_animation():
        """Happy greeting sequence"""
        return [
            ('neutral', 'X', 1),
            ('happy', 'A', 1),
            ('happy', 'E', 1),
            ('happy', 'O', 1),
            ('neutral', 'X', 1)
        ]
    
    @staticmethod
    def get_questioning_animation():
        """Confused/questioning sequence"""
        return [
            ('neutral', 'X', 2),
            ('sad', 'I', 2),
            ('sad', 'X', 2),
        ]
    
    @staticmethod
    def get_laughing_animation():
        """Laughing sequence"""
        return [
            ('happy', 'A', 1),
            ('happy', 'E', 1),
            ('happy', 'A', 1),
            ('happy', 'E', 1),
            ('happy', 'A', 1),
            ('neutral', 'X', 2)
        ]
    
    @staticmethod
    def get_angry_animation():
        """Angry sequence"""
        return [
            ('angry', 'X', 2),
            ('angry', 'MBP', 1),
            ('angry', 'X', 1),
            ('angry', 'MBP', 1),
            ('angry', 'X', 2)
        ]
    
    @staticmethod
    def get_surprise_animation():
        """Surprised sequence"""
        return [
            ('neutral', 'X', 1),
            ('happy', 'O', 2),
            ('happy', 'X', 1),
            ('neutral', 'X', 1)
        ]
    
    @staticmethod
    def get_sad_animation():
        """Sad sequence"""
        return [
            ('sad', 'X', 2),
            ('sad', 'E', 1),
            ('sad', 'X', 2)
        ]
    
    @staticmethod
    def list_presets():
        """List all available presets"""
        return [
            'greeting',
            'questioning',
            'laughing',
            'angry',
            'surprise',
            'sad'
        ]
