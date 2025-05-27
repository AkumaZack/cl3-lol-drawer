
import streamlit as st
import random
import os
from PIL import Image, ImageDraw, ImageFont
from io import StringIO, BytesIO

BASE_DIR = "LOL"
CHAMPION_DIR = os.path.join(BASE_DIR, "champions")
SPELL_DIR = os.path.join(BASE_DIR, "spells")
ITEM_DIR = os.path.join(BASE_DIR, "items")

boot_pool = [
    "法師之靴.png", "狂戰士護脛.png", "共生之足.png",
    "輕靈之靴.png", "艾歐尼亞之靴.png", "水星之靴.png", "鍍板鋼蓋.png"
]
lanes = ["上路", "打野", "中路", "下路", "輔助"]

champion_images = os.listdir(CHAMPION_DIR)
spell_images = os.listdir(SPELL_DIR)
item_images = os.listdir(ITEM_DIR)

st.set_page_config(page_title="CL³ 英雄聯盟分組神器", layout="wide")
st.markdown("<h1 style='text-align:center;'>CL³ 英雄聯盟分組神器</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
    textarea {
        width: 600px !important;
        height: 240px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

names_input = st.text_area("請輸入 10 位玩家名稱（每行一位）")

def generate_image(result_data):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 20)
    width, height = 1000, 1200
    bg_color = (15, 15, 26)
    text_color = (255, 255, 255)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    y = 20
    for team in result_data:
        draw.text((20, y), team['name'], fill=(247, 199, 68), font=font)
        y += 40
        for player in team['players']:
            draw.text((40, y), f"{player['name']} - {player['lane']} | 英雄: {player['champ']}", fill=text_color, font=font)
            y += 30
            draw.text((60, y), "技能: " + ", ".join(player['spells']), fill=text_color, font=font)
            y += 30
            draw.text((60, y), "裝備: " + ", ".join(player['items']), fill=text_color, font=font)
            y += 50
        y += 30
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

if names_input.strip():
    names = [name.strip() for name in names_input.split("\n") if name.strip()]
    export_text = StringIO()
    image_data = []

    if len(names) != 10:
        st.warning("請輸入剛好 10 位玩家名稱！")
    else:
        random.shuffle(names)
        teams = [names[:5], names[5:]]
        team_cols = st.columns(2)

        for i, team in enumerate(teams):
            with team_cols[i]:
                st.markdown(f"## 🛡️ 第 {i+1} 隊")
                export_text.write(f"第 {i+1} 隊\n")
                team_result = {"name": f"第 {i+1} 隊", "players": []}
                assigned_lanes = random.sample(lanes, 5)
                for j, name in enumerate(team):
                    lane = assigned_lanes[j]
                    st.markdown(f"**🎮 {name} - {lane}**")
                    export_text.write(f"{name} - {lane}\n")
                    champ_file = random.choice(champion_images)
                    champ_name = os.path.splitext(champ_file)[0]
                    st.image(os.path.join(CHAMPION_DIR, champ_file), caption=champ_name, width=100)
                    export_text.write(f"英雄：{champ_name}\n")
                    spell_sample = random.sample(spell_images, 2)
                    spells = []
                    spell_cols = st.columns(2)
                    for k, spell_file in enumerate(spell_sample):
                        spell_name = os.path.splitext(spell_file)[0]
                        spells.append(spell_name)
                        spell_cols[k].image(os.path.join(SPELL_DIR, spell_file), caption=spell_name, width=70)
                        export_text.write(f"技能：{spell_name}\n")
                    boot_file = random.choice(boot_pool)
                    non_boot_items = [i for i in item_images if i not in boot_pool]
                    other_items = random.sample(non_boot_items, 5)
                    item_sample = [boot_file] + other_items
                    items = []
                    item_cols = st.columns(3)
                    for i, item_file in enumerate(item_sample):
                        item_name = os.path.splitext(item_file)[0]
                        items.append(item_name)
                        item_cols[i % 3].image(os.path.join(ITEM_DIR, item_file), caption=item_name, width=70)
                        export_text.write(f"裝備：{item_name}\n")
                    export_text.write("\n")
                    team_result['players'].append({
                        'name': name,
                        'lane': lane,
                        'champ': champ_name,
                        'spells': spells,
                        'items': items
                    })
                image_data.append(team_result)

        st.download_button(
            label="💾 匯出分組結果",
            data=export_text.getvalue(),
            file_name="CL3_英雄聯盟分組結果.txt",
            mime="text/plain"
        )

        img_bytes = generate_image(image_data)
        st.download_button(
            label="📸 匯出圖片",
            data=img_bytes,
            file_name="CL3_分組結果.png",
            mime="image/png"
        )
