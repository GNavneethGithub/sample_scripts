from pprint import pprint
from tabulate import tabulate

def format_number(num):
    """
    Format a number to compact notation with 2 decimal places.
    Examples: 1234567890 -> 1.23B, 456789 -> 456.79K
    
    Args:
        num: Integer or float to format
    
    Returns:
        Tuple of (formatted_string, suffix, original_magnitude)
        Examples: ("1.23B", "B", 1_000_000_000), ("45.67K", "K", 1_000)
    """
    
    suffixes = [
        (1_000_000_000, 'B'),      # Billion
        (1_000_000, 'M'),          # Million
        (1_000, 'K'),              # Thousand
    ]
    
    is_negative = num < 0
    num_abs = abs(num)
    
    # Find the appropriate suffix for this number
    chosen_suffix = None
    chosen_magnitude = 1
    
    if num_abs >= 1_000:
        for threshold, suffix in suffixes:
            if num_abs >= threshold:
                chosen_suffix = suffix
                chosen_magnitude = threshold
                break
    
    # Format the number
    if chosen_suffix:
        scaled = num / chosen_magnitude
        result = f"{scaled:.2f}{chosen_suffix}"
    else:
        result = f"{num:.2f}"
    
    # Add negative sign if needed
    if is_negative and num_abs >= 1_000:
        result = '-' + result
    elif is_negative:
        result = '-' + result
    
    return result, chosen_suffix, chosen_magnitude


def format_difference(x1, x2):
    """
    Calculate difference between x1 and x2, and format using the same suffix as the larger number.
    
    Args:
        x1: First number
        x2: Second number
    
    Returns:
        Formatted difference string in the same scale as the largest number
        Examples: "1.23B", "0.00M", "45.67K"
    """
    
    # Get formatted versions to determine the suffix of the largest number
    formatted_x1, suffix_x1, mag_x1 = format_number(x1)
    formatted_x2, suffix_x2, mag_x2 = format_number(x2)
    
    # Determine which number is larger and use its suffix/magnitude
    largest_num = max(abs(x1), abs(x2))
    
    # Get the magnitude of the largest number
    if largest_num < 1_000:
        magnitude_to_use = 1
        suffix_to_use = None
    elif largest_num >= 1_000_000_000:
        magnitude_to_use = 1_000_000_000
        suffix_to_use = 'B'
    elif largest_num >= 1_000_000:
        magnitude_to_use = 1_000_000
        suffix_to_use = 'M'
    elif largest_num >= 1_000:
        magnitude_to_use = 1_000
        suffix_to_use = 'K'
    
    # Calculate the difference
    difference = x1 - x2
    
    # Scale the difference to match the largest number's magnitude
    if suffix_to_use:
        scaled_diff = difference / magnitude_to_use
        result = f"{scaled_diff:.2f}{suffix_to_use}"
    else:
        result = f"{difference:.2f}"
    
    return result


# Test cases
if __name__ == "__main__":
    test_cases = [
        # (x1, x2, description)
        (123654789963, 123654789000, "Both in Billions - small difference"),
        (5000000000, 4500000000, "Both Billions - 500M difference"),
        (1500000000, 1400000000, "Both Billions - 100M difference"),
        (100000000, 50000000, "Both Millions - 50M difference"),
        (100000, 50000, "Both Thousands - 50K difference"),
        (1234567890, 1234000000, "1.23B and 1.23B - shows 567K in B scale"),
        (999999999, 888888888, "Nearly 1B - shows difference in B scale"),
        (50000, 30000, "Thousands - 20K difference"),
        (500, 100, "Small numbers - below 1K"),
        (123654789963, 100, "Billion and hundereds"),
    ]
    
    # Prepare data for tabulate
    table_data = []
    for x1, x2, desc in test_cases:
        formatted_x1, _, _ = format_number(x1)
        formatted_x2, _, _ = format_number(x2)
        diff = format_difference(x1, x2)
        
        table_data.append({
            "X1": f"{x1:,}",
            "X2": f"{x2:,}",
            "X1 Formatted": formatted_x1,
            "X2 Formatted": formatted_x2,
            "Difference": diff,
            "Description": desc
        })
    
    # Print using tabulate
    print("\n")
    print(tabulate(table_data, headers="keys", tablefmt="grid", showindex=False))
    print("\n")