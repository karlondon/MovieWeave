"""CartoonCharacter - Load and render cartoon character sprites"""
from PIL import Image
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class CartoonCharacter:
    """Loads and renders cartoon character sprites"""
    
    def __init__(self, name: str, base_path: Path):
        """Initialize cartoon character
        
        Args:
            name: Character name (e.g., 'hero_001')
            base_path: Path to character directory
        """
        self.name = name
        self.base_path = Path(base_path)
        self.expressions = {}
        self.mouth_shapes = {}
        self._load_assets()
    
    def _load_assets(self):
        """Load all expressions and mouth shapes"""
        # Load expressions
        for expr in ['neutral', 'happy', 'sad', 'angry']:
            expr_path = self.base_path / f"{self.name}_{expr}.png"
            if expr_path.exists():
                self.expressions[expr] = Image.open(expr_path)
                logger.debug(f"Loaded expression: {expr}")
        
        # Load mouth shapes
        mouths_dir = self.base_path / "mouths"
        if mouths_dir.exists():
            for mouth_file in mouths_dir.glob("*.png"):
                mouth_name = mouth_file.stem
                self.mouth_shapes[mouth_name] = Image.open(mouth_file)
                logger.debug(f"Loaded mouth shape: {mouth_name}")
    
    def get_available_expressions(self) -> List[str]:
        """Get list of available expressions"""
        return list(self.expressions.keys())
    
    def get_available_mouths(self) -> List[str]:
        """Get list of available mouth shapes"""
        return list(self.mouth_shapes.keys())
    
    def get_expression_frame(self, expression: str) -> Optional[Image.Image]:
        """Get expression frame
        
        Args:
            expression: Expression name (neutral, happy, sad, angry)
            
        Returns:
            PIL Image or None if not found
        """
        if expression in self.expressions:
            return self.expressions[expression].copy()
        logger.warning(f"Expression '{expression}' not found for {self.name}")
        return None
    
    def get_mouth_shape(self, mouth_shape: str) -> Optional[Image.Image]:
        """Get mouth shape
        
        Args:
            mouth_shape: Mouth shape (A, E, I, O, U, MBP, X)
            
        Returns:
            PIL Image or None if not found
        """
        if mouth_shape in self.mouth_shapes:
            return self.mouth_shapes[mouth_shape].copy()
        logger.warning(f"Mouth shape '{mouth_shape}' not found")
        return None
    
    def render_frame(self, expression: str = 'neutral', mouth_shape: str = 'X') -> Optional[Image.Image]:
        """Render character frame with expression and mouth
        
        Args:
            expression: Expression (neutral, happy, sad, angry)
            mouth_shape: Mouth shape (A, E, I, O, U, MBP, X)
            
        Returns:
            PIL Image with character and mouth overlay
        """
        expr_frame = self.get_expression_frame(expression)
        if not expr_frame:
            return None
        
        # For now, just return the expression frame
        # In a full implementation, you would overlay the mouth shape
        return expr_frame
    
    def __repr__(self) -> str:
        return f"CartoonCharacter(name='{self.name}', expressions={len(self.expressions)}, mouths={len(self.mouth_shapes)})"
