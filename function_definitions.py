def seconds_to_hms(seconds):
    """
    Convert seconds to hours, minutes, and seconds.
    
    Args:
        seconds (int): Number of seconds.
        
    Returns:
        tuple: A tuple containing the number of hours, minutes, and remaining seconds.
    """
    
    # Calculate hours, minutes, and remaining seconds
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return hours, minutes, seconds
