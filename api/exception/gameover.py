class GameOver(Exception):
    """
    Custom exception raised when the game ends.

    This exception is used to signal that the game has reached a termination 
    condition, such as the snake colliding with an obstacle or itself.
    """
    pass
