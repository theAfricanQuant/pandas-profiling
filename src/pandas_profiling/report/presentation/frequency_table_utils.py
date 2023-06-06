def freq_table(freqtable, n: int, max_number_to_print: int) -> list:
    """Render the rows for a frequency table (value, count).

    Args:
      freqtable: The frequency table.
      n: The total number of values.
      max_number_to_print: The maximum number of observations to print.

    Returns:
        The rows of the frequency table.
    """
    rows = []

    # TODO: replace '' by '(Empty)' ?

    max_number_to_print = min(max_number_to_print, n)
    if max_number_to_print < len(freqtable):
        freq_other = sum(freqtable.iloc[max_number_to_print:])
        min_freq = freqtable.values[max_number_to_print]
    else:
        freq_other = 0
        min_freq = 0

    freq_missing = n - sum(freqtable)
    # No values
    if len(freqtable) == 0:
        return rows

    max_freq = max(freqtable.values[0], freq_other, freq_missing)

    # TODO: Correctly sort missing and other
    # No values
    if max_freq == 0:
        return rows

    rows.extend(
        {
            "label": label,
            "width": freq / max_freq,
            "count": freq,
            "percentage": float(freq) / n,
            "n": n,
            "extra_class": "",
        }
        for label, freq in freqtable.iloc[:max_number_to_print].items()
    )
    if freq_other > min_freq:
        rows.append(
            {
                "label": f"Other values ({str(freqtable.count() - max_number_to_print)})",
                "width": freq_other / max_freq,
                "count": freq_other,
                "percentage": min(float(freq_other) / n, 1.0),
                "n": n,
                "extra_class": "other",
            }
        )

    if freq_missing > min_freq:
        rows.append(
            {
                "label": "(Missing)",
                "width": freq_missing / max_freq,
                "count": freq_missing,
                "percentage": float(freq_missing) / n,
                "n": n,
                "extra_class": "missing",
            }
        )

    return rows


def extreme_obs_table(freqtable, number_to_print, n, ascending=True) -> list:
    """Similar to the frequency table, for extreme observations.

    Args:
      freqtable: The frequency table.
      number_to_print: The number of observations to print.
      n: The total number of observations.
      ascending: The ordering of the observations (Default value = True)

    Returns:
        The HTML rendering of the extreme observation table.
    """
    # If it's mixed between base types (str, int) convert to str. Pure "mixed" types are filtered during type
    # discovery
    # TODO: should be in cast?
    if "mixed" in freqtable.index.inferred_type:
        freqtable.index = freqtable.index.astype(str)

    sorted_freqtable = freqtable.sort_index(ascending=ascending)
    obs_to_print = sorted_freqtable.iloc[:number_to_print]
    max_freq = max(obs_to_print.values)

    return [
        {
            "label": label,
            "width": freq / max_freq if max_freq != 0 else 0,
            "count": freq,
            "percentage": float(freq) / n,
            "extra_class": "",
            "n": n,
        }
        for label, freq in obs_to_print.items()
    ]
