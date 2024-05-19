from supabase import create_client, Client
import pycryp,os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

username = "a"
current_user = "a"
password = "a"

current_level = supabase.table("progress").select("current_level").eq("username", username).execute()
current_level = current_level.data[0]["current_level"]
print(current_level)
supabase.table("progress").update({"current_level": current_level+1}).eq("username", current_user).execute()

print(supabase.table("progress").select("current_level").eq("username", username).execute().data[0]["current_level"])

# import json

# f = open("static/password.json", "r")
# data = json.load(f)

# print(data["1"])
