import re

def remove_emojis_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match emojis
    # We remove characters outside the basic multilingual plane or specific emoji ranges
    emoji_pattern = re.compile(r"[\U00010000-\U0010ffff]|\u274c|\u2705|\u26A0|🚀|🔥|✅|🔒|⛓️|📦|⏱️|⏳|📈|🛡️|⚠️|💡|🔍|📡|💻|🌍|🏁|🖥️|🦾|⚡|🔗|💡|📡|🧪|🎯|🔥|📊|🛡️|🚨|📝|📡|✅|🔒|📦|📡|🚀|🏁")
    clean_content = emoji_pattern.sub("", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    print(f"Cleaned: {filepath}")

remove_emojis_from_file('network_sender.py')
remove_emojis_from_file('network_receiver.py')
