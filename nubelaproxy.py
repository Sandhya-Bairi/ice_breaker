import requests

api_key = "YOUR_API_KEY"
headers = {"Authorization": "Bearer " + api_key}
api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
params = {
    "twitter_profile_url": "https://twitter.com/johnrmarty/",
    "facebook_profile_url": "https://facebook.com/johnrmarty/",
    "linkedin_profile_url": "https://linkedin.com/in/johnrmarty/",
    "extra": "include",
    "github_profile_id": "include",
    "facebook_profile_id": "include",
    "twitter_profile_id": "include",
    "personal_contact_number": "include",
    "personal_email": "include",
    "inferred_salary": "include",
    "skills": "include",
    "use_cache": "if-present",
    "fallback_to_cache": "on-error",
}
response = requests.get(api_endpoint, params=params, headers=headers)
