class EarthLensError(Exception):
    """Base exception for EarthLens."""
    pass

class DatasetNotFoundError(EarthLensError):
    """Raised when a dataset is not found in the registry."""
    pass

class InsufficientDataError(EarthLensError):
    """Raised when there is not enough data to perform an analysis."""
    pass

class InvalidRegionError(EarthLensError):
    """Raised when an invalid region is specified."""
    pass

class AnalysisError(EarthLensError):
    """Raised when statistical analysis fails."""
    pass
