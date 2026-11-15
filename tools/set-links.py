"""set-links.py - fills the editable placeholders in README.md in one go.
Example:
  python3 tools/set-links.py --github your-username
Placeholder replaced:  YOUR_GITHUB_USERNAME  (used by the GitHub stats cards; Instagram and Twitch are already set)
"""
import argparse, os

ap = argparse.ArgumentParser()
ap.add_argument('--github', help='GitHub username, e.g. octocat')
a = ap.parse_args()
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'README.md')
s = open(p, encoding='utf-8').read()
if a.github:
    s = s.replace('YOUR_GITHUB_USERNAME', a.github)
open(p, 'w', encoding='utf-8').write(s)
print('README.md updated')
