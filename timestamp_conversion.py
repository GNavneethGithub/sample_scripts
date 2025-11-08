from datetime import datetime, timezone

def _convert_readable_to_strftime(readable_format: str) -> str:
    """
    Convert human-readable format to strftime format.
    
    Examples:
        "YYYY-MM-DDTHH:MI:SSoffset" -> "%Y-%m-%dT%H:%M:%S%z"
        "YYYY-MM-DD" -> "%Y-%m-%d"
        "HH:MI:SS" -> "%H:%M:%S"
    
    Note: Use "offset" without hyphen (it already includes + or -)
    """
    # Important: replace in specific order to avoid conflicts
    result = readable_format
    result = result.replace("YYYY", "%Y")
    result = result.replace("MM", "%m")   # Month (uppercase MM)
    result = result.replace("DD", "%d")
    result = result.replace("HH", "%H")
    result = result.replace("MI", "%M")   # Minute (use MI instead of mm)
    result = result.replace("SS", "%S")
    result = result.replace("offset", "%z")
    result = result.replace("TZ", "%Z")
    
    return result


def convert_timestamp_format(ts: str, target_format: str) -> str:
    """
    Convert timestamp to target format using human-readable format templates.
    
    Args:
        ts (str): Input timestamp string
                 Example: "2025-11-01T00:00:00-08:00"
        target_format (str): Target format template or custom format name
                            
    Supported human-readable format templates:
        "YYYY-MM-DDTHH:MI:SSoffset"        -> 2025-11-01T00:00:00-0800
        "YYYY-MM-DDTHH:MI:SS.nnnnnnnnnZ"   -> 2025-11-07T21:09:16.015204763Z
        "YYYY-MM-DD"                        -> 2025-11-01
        "HH:MI:SS"                          -> 00:00:00
        "YYYY-MM-DDTHH:MI:SS"               -> 2025-11-01T00:00:00
    
    Supported custom formats:
        "epoch_ms"    -> Milliseconds since epoch
        "epoch_sec"   -> Seconds since epoch
    
    Format codes:
        YYYY       - 4-digit year
        MM         - 2-digit month
        DD         - 2-digit day
        HH         - 2-digit hour
        MI         - 2-digit minute
        SS         - 2-digit second
        nnnnnnnnn  - nanoseconds (9 digits)
        offset     - timezone offset (-0800 or +0530 format)
        Z          - literal Z (UTC indicator)
        TZ         - timezone abbreviation
    
    Returns:
        str: Converted timestamp
    """
    
    try:
        # Parse the input timestamp (handle both with and without colon in timezone)
        dt = None
        
        # Try parsing with colon in timezone
        try:
            dt = datetime.fromisoformat(ts)
        except:
            # Try parsing without colon in timezone
            if len(ts) >= 5 and ts[-5] in ["+", "-"] and ts[-3] != ":":
                # Add colon for parsing: "2025-11-01T00:00:00-0800" -> "2025-11-01T00:00:00-08:00"
                ts_with_colon = ts[:-2] + ":" + ts[-2:]
                dt = datetime.fromisoformat(ts_with_colon)
        
        if dt is None:
            raise ValueError(f"Could not parse timestamp: {ts}")
        
        # Handle custom format names with special logic
        if target_format == "epoch_ms":
            # Milliseconds since epoch
            return str(int(dt.timestamp() * 1000))
        
        elif target_format == "epoch_sec":
            # Seconds since epoch
            return str(int(dt.timestamp()))
        
        # ADD MORE CUSTOM FORMATS HERE USING elif
        # elif target_format == "your_custom_format":
        #     return your_custom_logic(dt)
        
        else:
            # Check if format contains nanoseconds placeholder
            if "nnnnnnnnn" in target_format:
                # Extract nanoseconds from microseconds
                # datetime only has microseconds, so pad with zeros to make 9 digits
                microseconds = dt.microsecond
                nanoseconds = microseconds * 1000  # Convert microseconds to nanoseconds
                nanos_str = str(nanoseconds).zfill(9)  # Pad with zeros to 9 digits
                
                # Check if format contains Z (UTC indicator)
                if "Z" in target_format:
                    # Convert to UTC before formatting
                    dt_utc = dt.astimezone(timezone.utc).replace(tzinfo=None)
                    strftime_format = target_format.replace("nnnnnnnnn", "{NANOS}").replace("Z", "")
                    strftime_format = _convert_readable_to_strftime(strftime_format)
                    result = dt_utc.strftime(strftime_format) + "Z"
                else:
                    # Remove 'nnnnnnnnn' and add formatted nanoseconds
                    strftime_format = target_format.replace("nnnnnnnnn", "{NANOS}")
                    
                    # Convert human-readable format to strftime format
                    strftime_format = _convert_readable_to_strftime(strftime_format)
                    
                    # Format the timestamp
                    result = dt.strftime(strftime_format)
                
                # Replace {NANOS} placeholder with actual nanoseconds
                result = result.replace("{NANOS}", nanos_str)
                return result
            else:
                # Check if format contains Z (UTC indicator)
                if "Z" in target_format:
                    # Convert to UTC before formatting
                    dt_utc = dt.astimezone(timezone.utc).replace(tzinfo=None)
                    strftime_format = target_format.replace("Z", "")
                    strftime_format = _convert_readable_to_strftime(strftime_format)
                    result = dt_utc.strftime(strftime_format) + "Z"
                else:
                    # Convert human-readable format to strftime format
                    strftime_format = _convert_readable_to_strftime(target_format)
                    result = dt.strftime(strftime_format)
                
                return result
    
    except Exception as e:
        raise Exception(f"Error converting timestamp: {str(e)}")


# Example usage
if __name__ == "__main__":
    test_cases = [
        "2025-11-01T00:00:00-08:00",
        "2025-11-07T10:49:44-08:00",
    ]
    
    print("Timestamp Format Conversion - Human-Readable Formats")
    print("=" * 70)
    
    # Format 1: Full ISO with timezone offset
    print("\n--- Format: YYYY-MM-DDTHH:MI:SSoffset ---")
    print("Expected Output: 2025-11-01T00:00:00-0800\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "YYYY-MM-DDTHH:MI:SSoffset")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")
    
    # Format 2: Date only
    print("\n--- Format: YYYY-MM-DD ---")
    print("Expected Output: 2025-11-01\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "YYYY-MM-DD")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")
    
    # Format 3: Time only
    print("\n--- Format: HH:MI:SS ---")
    print("Expected Output: 00:00:00\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "HH:MI:SS")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")
    
    # Format 4: ISO without timezone
    print("\n--- Format: YYYY-MM-DDTHH:MI:SS ---")
    print("Expected Output: 2025-11-01T00:00:00\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "YYYY-MM-DDTHH:MI:SS")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")
    
    # Custom Format: epoch_ms
    print("\n--- Custom Format: epoch_ms ---")
    print("Expected Output: 1761984000000\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "epoch_ms")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")
    
    # Custom Format: epoch_sec
    print("\n--- Custom Format: epoch_sec ---")
    print("Expected Output: 1761984000\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "epoch_sec")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")
    
    # Format 5: With nanoseconds and Z (UTC indicator)
    print("\n--- Format: YYYY-MM-DDTHH:MI:SS.nnnnnnnnnZ ---")
    print("Expected Output: 2025-11-01T00:00:00.000000000Z\n")
    for ts in test_cases:
        result = convert_timestamp_format(ts, "YYYY-MM-DDTHH:MI:SS.nnnnnnnnnZ")
        print(f"Input:  {ts}")
        print(f"Output: {result}\n")