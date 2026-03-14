# Source - https://stackoverflow.com/a
# Posted by hughdbrown, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-24, License - CC BY-SA 3.0

from itertools import permutations

def unique_perms(series):
    return {"".join(p) for p in permutations(series)}

print(sorted(unique_perms('11110000')))
