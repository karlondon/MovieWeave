"""CharacterManager - Load and cache cartoon characters"""
from pathlib import Path
from typing import Dict, Optional
import logging
from backend.cartoon_character import CartoonCharacter

logger = logging.getLogger(__name__)

class CharacterManager:
    """Manages loading and caching of cartoon characters"""
    
    def __init__(self, assets_dir: Path):
        """Initialize character manager
        
        Args:
            assets_dir: Path to characters directory
        """
        self.assets_dir = Path(assets_dir)
        self.characters: Dict[str, CartoonCharacter] = {}
        logger.info(f"CharacterManager initialized with assets: {self.assets_dir}")
    
    def load_character(self, name: str) -> Optional[CartoonCharacter]:
        """Load a character (cached)
        
        Args:
            name: Character name
            
        Returns:
            CartoonCharacter instance or None if not found
        """
        # Return cached character if available
        if name in self.characters:
            logger.debug(f"Returning cached character: {name}")
            return self.characters[name]
        
        # Try to load from disk
        char_path = self.assets_dir / name
        if not char_path.exists():
            logger.warning(f"Character path not found: {char_path}")
            return None
        
        try:
            character = CartoonCharacter(name, char_path)
            self.characters[name] = character
            logger.info(f"Loaded character: {name}")
            return character
        except Exception as e:
            logger.error(f"Failed to load character {name}: {e}")
            return None
    
    def get_available_characters(self) -> list[str]:
        """Get list of available character names"""
        if not self.assets_dir.exists():
            return []
        
        characters = [d.name for d in self.assets_dir.iterdir() if d.is_dir()]
        return sorted(characters)
    
    def load_all_characters(self) -> Dict[str, CartoonCharacter]:
        """Load all available characters"""
        loaded = {}
        for char_name in self.get_available_characters():
            char = self.load_character(char_name)
            if char:
                loaded[char_name] = char
        
        logger.info(f"Loaded {len(loaded)} characters")
        return loaded
    
    def clear_cache(self):
        """Clear character cache"""
        self.characters.clear()
        logger.info("Character cache cleared")
    
    def __repr__(self) -> str:
        return f"CharacterManager(loaded={len(self.characters)}, available={len(self.get_available_characters())})"
