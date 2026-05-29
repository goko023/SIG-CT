"""
SIG Config Generator v5
Visual configurator for SimpleItemGenerator Minecraft plugin.
Plugin DEV: Balerii (hes a good dev)
Made with Claude (ima new to coding dont jugde)
From: Turkiye
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import yaml
import json
import re
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------------------------------------
#  DATA
# ---------------------------------------------

MATERIALS = [
    "DIAMOND_SWORD","NETHERITE_SWORD","IRON_SWORD","GOLD_SWORD","STONE_SWORD","WOODEN_SWORD",
    "DIAMOND_PICKAXE","NETHERITE_PICKAXE","IRON_PICKAXE","GOLD_PICKAXE","STONE_PICKAXE","WOODEN_PICKAXE",
    "DIAMOND_AXE","NETHERITE_AXE","IRON_AXE","GOLD_AXE","STONE_AXE","WOODEN_AXE",
    "DIAMOND_SHOVEL","NETHERITE_SHOVEL","IRON_SHOVEL","GOLD_SHOVEL","STONE_SHOVEL","WOODEN_SHOVEL",
    "DIAMOND_HOE","NETHERITE_HOE","IRON_HOE","GOLD_HOE","STONE_HOE","WOODEN_HOE",
    "DIAMOND_HELMET","NETHERITE_HELMET","IRON_HELMET","GOLD_HELMET","CHAINMAIL_HELMET","LEATHER_HELMET",
    "DIAMOND_CHESTPLATE","NETHERITE_CHESTPLATE","IRON_CHESTPLATE","GOLD_CHESTPLATE","CHAINMAIL_CHESTPLATE","LEATHER_CHESTPLATE",
    "DIAMOND_LEGGINGS","NETHERITE_LEGGINGS","IRON_LEGGINGS","GOLD_LEGGINGS","CHAINMAIL_LEGGINGS","LEATHER_LEGGINGS",
    "DIAMOND_BOOTS","NETHERITE_BOOTS","IRON_BOOTS","GOLD_BOOTS","CHAINMAIL_BOOTS","LEATHER_BOOTS",
    "BOW","CROSSBOW","TRIDENT","SHIELD","FISHING_ROD","FLINT_AND_STEEL",
    "STICK","BLAZE_ROD","BONE","FEATHER","ARROW",
    "APPLE","GOLDEN_APPLE","ENCHANTED_GOLDEN_APPLE","BREAD","COOKED_BEEF","COOKED_CHICKEN",
    "DIAMOND","EMERALD","AMETHYST_SHARD","NETHER_STAR","HEART_OF_THE_SEA","ECHO_SHARD",
    "BOOK","ENCHANTED_BOOK","WRITABLE_BOOK","KNOWLEDGE_BOOK",
    "POTION","SPLASH_POTION","LINGERING_POTION","TIPPED_ARROW",
    "PAPER","MAP","COMPASS","CLOCK","SPYGLASS","RECOVERY_COMPASS",
    "PLAYER_HEAD","SKELETON_SKULL","WITHER_SKELETON_SKULL","CREEPER_HEAD","ZOMBIE_HEAD",
    "CHEST","BARREL","SHULKER_BOX","ENDER_CHEST","TRAPPED_CHEST",
    "TNT","FIRE_CHARGE","FIREWORK_ROCKET",
    "STONE","COBBLESTONE","OAK_PLANKS","GLASS","OBSIDIAN","CRYING_OBSIDIAN",
    "TOTEM_OF_UNDYING","SADDLE","NAME_TAG","LEAD",
]

ENCHANTMENTS = [
    "minecraft:sharpness","minecraft:smite","minecraft:bane_of_arthropods",
    "minecraft:knockback","minecraft:fire_aspect","minecraft:looting","minecraft:sweeping_edge",
    "minecraft:unbreaking","minecraft:mending","minecraft:vanishing_curse",
    "minecraft:protection","minecraft:fire_protection","minecraft:blast_protection",
    "minecraft:projectile_protection","minecraft:thorns","minecraft:respiration",
    "minecraft:aqua_affinity","minecraft:depth_strider","minecraft:frost_walker",
    "minecraft:feather_falling","minecraft:soul_speed","minecraft:swift_sneak",
    "minecraft:efficiency","minecraft:silk_touch","minecraft:fortune",
    "minecraft:power","minecraft:punch","minecraft:flame","minecraft:infinity",
    "minecraft:luck_of_the_sea","minecraft:lure",
    "minecraft:channeling","minecraft:loyalty","minecraft:riptide","minecraft:impaling",
    "minecraft:multishot","minecraft:piercing","minecraft:quick_charge",
    "minecraft:binding_curse",
]

ITEM_FLAGS = [
    "HIDE_ATTRIBUTES","HIDE_DESTROYS","HIDE_DYE",
    "HIDE_ENCHANTS","HIDE_PLACED_ON","HIDE_POTION_EFFECTS","HIDE_UNBREAKABLE",
]

MINI_COLORS = {
    "White":       "white",
    "Yellow":      "yellow",
    "Gold":        "gold",
    "Red":         "red",
    "Dark Red":    "dark_red",
    "Green":       "green",
    "Dark Green":  "dark_green",
    "Blue":        "blue",
    "Aqua":        "aqua",
    "Dark Aqua":   "dark_aqua",
    "Purple":      "light_purple",
    "Dark Purple": "dark_purple",
    "Dark Gray":   "dark_gray",
    "Black":       "black",
}

# ---- TEMA: Siyah / Koyu Gri / Beyaz ----
BG_ROOT   = "#0a0a0a"
BG_PANEL  = "#111111"
BG_HDR    = "#181818"
BG_CARD   = "#1c1c1c"
BG_ROW    = "#222222"
BG_INPUT  = "#141414"
BORDER    = "#2e2e2e"
SEL_BG    = "#2a2a2a"

BTN       = "#2a2a2a"
BTN_H     = "#3e3e3e"
BTN_DEL   = "#3a1010"
BTN_DEL2  = "#5a1a1a"

TXT_MAIN  = "#e0e0e0"
TXT_SUB   = "#777777"
TXT_DIM   = "#3a3a3a"

SCROLL_FG  = "#181818"
SCROLL_BTN = "#383838"
SCROLL_HOV = "#525252"

YAML_TEXT  = "#cccccc"


def slugify(text: str) -> str:
    """Convert display name to a safe YAML key."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9_\-]", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def make_neon_label(parent, text, font_size=18, bg=BG_ROOT):
    """Beyaz metin + beyaz glow efekti için Canvas Label."""
    fw = font_size * len(text) + 60
    fh = font_size + 28
    c = tk.Canvas(parent, width=fw, height=fh,
                  bg=bg, highlightthickness=0)
    cx, cy = fw // 2, fh // 2
    font_spec = ("Consolas", font_size, "bold")
    for off, col in [(4, "#1a1a1a"), (3, "#2e2e2e"), (2, "#4a4a4a"), (1, "#888888")]:
        c.create_text(cx + off, cy + off, text=text, font=font_spec, fill=col, anchor="center")
        c.create_text(cx - off, cy - off, text=text, font=font_spec, fill=col, anchor="center")
    c.create_text(cx, cy, text=text, font=font_spec, fill="#ffffff", anchor="center")
    return c



    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9_]", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "item"


def mini(color_label: str, text: str) -> str:
    tag = MINI_COLORS.get(color_label, "white")
    return f"<{tag}>{text}</{tag}>"


def build_yaml_for_item(item: dict) -> dict:
    inner = {}

    # 1. material (required)
    inner["material"] = item.get("material", "STONE")

    # 2. cmd (only if filled)
    cmd_val = item.get("cmd", "").strip()
    if cmd_val:
        try:
            inner["cmd"] = int(cmd_val)
        except ValueError:
            pass

    # 3. name (required)
    name_text = item.get("name_text", "").strip() or "Custom Item"
    inner["name"] = mini(item.get("name_color", "Gold"), name_text)

    # 4. lore (only non-empty lines)
    lore_lines = []
    for line_text, line_color in item.get("lore", []):
        t = line_text.strip()
        if t:
            lore_lines.append(mini(line_color, t))
    if lore_lines:
        inner["lore"] = lore_lines

    # 5. unbreakable
    if item.get("unbreakable", False):
        inner["unbreakable"] = True

    # 6. durability
    dur_val = item.get("durability", "").strip() if isinstance(item.get("durability", ""), str) else ""
    if dur_val:
        try:
            inner["durability"] = int(dur_val)
        except ValueError:
            pass

    # 7. enchantments
    enchs = {k: v for k, v in item.get("enchantments", {}).items() if v > 0}
    if enchs:
        inner["enchantments"] = enchs

    # 8. item-flags
    flags = item.get("flags", [])
    if flags:
        inner["item-flags"] = flags

    # 9. nbt
    nbt_val = item.get("nbt", "").strip()
    if nbt_val:
        inner["nbt"] = nbt_val

    block = {"item": inner}

    # 10. usage (outside item block)
    usages = item.get("usage", [])
    if usages:
        block["usage"] = usages

    return block


# ---------------------------------------------
#  LORE EDITOR
# ---------------------------------------------

class LoreEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.rows: list[tuple[tk.StringVar, tk.StringVar]] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Lore", font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Line", width=80, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_row).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_row(self, text="", color="White"):
        color_var = tk.StringVar(value=color)
        text_var  = tk.StringVar(value=text)

        row_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        row_frame.pack(fill="x", pady=2, padx=4)

        ctk.CTkOptionMenu(row_frame, variable=color_var,
                          values=list(MINI_COLORS.keys()),
                          width=130, height=26, font=("Consolas", 10),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=(6, 4), pady=4)

        entry = ctk.CTkEntry(row_frame, textvariable=text_var,
                             placeholder_text="lore text...",
                             height=26, font=("Consolas", 11))
        entry.pack(side="left", fill="x", expand=True, padx=4)
        text_var.trace_add("write", lambda *_: self.on_change())

        def remove():
            self.rows = [(tv, cv) for tv, cv in self.rows if tv is not text_var]
            row_frame.destroy()
            self.on_change()

        ctk.CTkButton(row_frame, text="X", width=26, height=26,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2,
                      command=remove).pack(side="right", padx=6)

        self.rows.append((text_var, color_var))

    def get_data(self):
        return [(tv.get(), cv.get()) for tv, cv in self.rows]

    def load_data(self, data):
        for w in self.container.winfo_children():
            w.destroy()
        self.rows.clear()
        for text, color in data:
            self.add_row(text, color)


# ---------------------------------------------
#  ENCHANTMENT EDITOR
# ---------------------------------------------

class EnchantEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.rows: list[tuple[tk.StringVar, tk.IntVar]] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Enchantments", font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Enchant", width=90, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_row).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_HDR, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_row(self, ench=None, level=1):
        ench = ench or ENCHANTMENTS[0]
        row_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        row_frame.pack(fill="x", pady=2, padx=4)

        ench_var  = tk.StringVar(value=ench)
        level_var = tk.IntVar(value=level)

        ctk.CTkOptionMenu(row_frame, variable=ench_var,
                          values=ENCHANTMENTS, width=240, height=26,
                          font=("Consolas", 10),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=(6, 4), pady=4)

        ctk.CTkLabel(row_frame, text="Level:", font=("Consolas", 11)).pack(side="left")

        def inc():
            level_var.set(min(255, level_var.get() + 1))
            self.on_change()

        def dec():
            level_var.set(max(1, level_var.get() - 1))
            self.on_change()

        ctk.CTkButton(row_frame, text="-", width=26, height=26,
                      fg_color=BTN, hover_color=BTN_H, command=dec).pack(side="left", padx=2)
        ctk.CTkLabel(row_frame, textvariable=level_var,
                     font=("Consolas", 12, "bold"), width=30).pack(side="left")
        ctk.CTkButton(row_frame, text="+", width=26, height=26,
                      fg_color=BTN, hover_color=BTN_H, command=inc).pack(side="left", padx=2)

        def remove():
            self.rows = [(ev, lv) for ev, lv in self.rows if ev is not ench_var]
            row_frame.destroy()
            self.on_change()

        ctk.CTkButton(row_frame, text="X", width=26, height=26,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2,
                      command=remove).pack(side="right", padx=6)

        self.rows.append((ench_var, level_var))

    def get_data(self) -> dict:
        return {ev.get(): lv.get() for ev, lv in self.rows}

    def load_data(self, data: dict):
        for w in self.container.winfo_children():
            w.destroy()
        self.rows.clear()
        for ench, level in data.items():
            self.add_row(ench, level)


# ---------------------------------------------
#  USAGE EDITOR
# ---------------------------------------------

class UsageEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.blocks: list[dict] = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Usage / Commands",
                     font=("Consolas", 12, "bold"),
                     text_color=TXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="+ Usage", width=90, height=26,
                      font=("Consolas", 11), fg_color=BTN, hover_color=BTN_H,
                      command=self.add_block).pack(side="right")
        self.container = ctk.CTkFrame(self, fg_color=BG_HDR, corner_radius=4)
        self.container.pack(fill="x", pady=(4, 0))

    def add_block(self, trigger="right", cancel=True, consume=0, cmds=None, at="any"):
        cmds = cmds or []
        block_frame = ctk.CTkFrame(self.container, fg_color=BG_ROW, corner_radius=4)
        block_frame.pack(fill="x", pady=4, padx=4)

        top = ctk.CTkFrame(block_frame, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(6, 2))

        ctk.CTkLabel(top, text="Trigger:", font=("Consolas", 11)).pack(side="left")
        trigger_var = tk.StringVar(value=trigger)
        ctk.CTkOptionMenu(top, variable=trigger_var,
                          values=["right", "left", "middle", "drop", "physical"],
                          width=95, height=26, font=("Consolas", 11),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=6)

        ctk.CTkLabel(top, text="At:", font=("Consolas", 11)).pack(side="left", padx=(8, 2))
        at_var = tk.StringVar(value="any")
        ctk.CTkOptionMenu(top, variable=at_var,
                          values=["any", "air", "block", "entity"],
                          width=80, height=26, font=("Consolas", 11),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=(0, 6))

        cancel_var = tk.BooleanVar(value=cancel)
        ctk.CTkCheckBox(top, text="Cancel", variable=cancel_var,
                        font=("Consolas", 11),
                        command=self.on_change).pack(side="left", padx=8)

        consume_var = tk.IntVar(value=consume)
        ctk.CTkLabel(top, text="Consume:", font=("Consolas", 11)).pack(side="left", padx=(8, 2))
        ctk.CTkEntry(top, textvariable=consume_var, width=50, height=26,
                     font=("Consolas", 11)).pack(side="left")
        consume_var.trace_add("write", lambda *_: self.on_change())

        block_info = {
            "frame":    block_frame,
            "trigger":  trigger_var,
            "at":       at_var,
            "cancel":   cancel_var,
            "consume":  consume_var,
            "cmd_rows": [],
        }

        cmd_container = ctk.CTkFrame(block_frame, fg_color="transparent")
        cmd_container.pack(fill="x", padx=8, pady=(2, 4))

        def add_cmd(ctype="[console]", ctext=""):
            cmd_row = ctk.CTkFrame(cmd_container, fg_color="transparent")
            cmd_row.pack(fill="x", pady=1)
            type_var = tk.StringVar(value=ctype)
            text_var = tk.StringVar(value=ctext)
            ctk.CTkOptionMenu(cmd_row, variable=type_var,
                              values=["[console]", "[player]", "[op]"],
                              width=90, height=24, font=("Consolas", 10),
                              command=lambda _: self.on_change()
                              ).pack(side="left", padx=(0, 4))
            e = ctk.CTkEntry(cmd_row, textvariable=text_var,
                             placeholder_text="command...",
                             height=24, font=("Consolas", 10))
            e.pack(side="left", fill="x", expand=True)
            text_var.trace_add("write", lambda *_: self.on_change())

            def rm_cmd():
                block_info["cmd_rows"] = [r for r in block_info["cmd_rows"]
                                          if r[0] is not type_var]
                cmd_row.destroy()
                self.on_change()

            ctk.CTkButton(cmd_row, text="X", width=24, height=24,
                          fg_color=BTN_DEL, hover_color=BTN_DEL2,
                          command=rm_cmd).pack(side="right", padx=4)
            block_info["cmd_rows"].append((type_var, text_var))

        btn_row = ctk.CTkFrame(block_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=8, pady=(0, 6))

        ctk.CTkButton(btn_row, text="+ Command", width=95, height=24,
                      fg_color=BTN, hover_color=BTN_H,
                      font=("Consolas", 10),
                      command=add_cmd).pack(side="left")

        def remove_block():
            self.blocks = [b for b in self.blocks if b is not block_info]
            block_frame.destroy()
            self.on_change()

        ctk.CTkButton(btn_row, text="Remove Usage", width=110, height=24,
                      fg_color=BTN_DEL, hover_color=BTN_DEL2,
                      font=("Consolas", 10),
                      command=remove_block).pack(side="right")

        for ctype, ctext in cmds:
            add_cmd(ctype, ctext)

        self.blocks.append(block_info)

    def get_data(self) -> list:
        result = []
        for b in self.blocks:
            cmds = []
            for type_var, text_var in b["cmd_rows"]:
                t = text_var.get().strip()
                if t:
                    cmds.append(f"{type_var.get()} {t}")
            if not cmds:
                continue
            try:
                consume = int(b["consume"].get())
            except Exception:
                consume = 0
            predicate = {"button": b["trigger"].get()}
            at_val = b["at"].get()
            if at_val != "any":
                predicate["at"] = at_val
            entry = {
                "predicate": [predicate],
                "commands":  cmds,
                "cancel":    b["cancel"].get(),
            }
            if consume > 0:
                entry["consume"] = consume
            result.append(entry)
        return result

    def load_data(self, data: list):
        for b in list(self.blocks):
            b["frame"].destroy()
        self.blocks.clear()
        for entry in data:
            trigger  = entry.get("predicate", [{}])[0].get("button", "right")
            at       = entry.get("predicate", [{}])[0].get("at", "any")
            cancel   = entry.get("cancel", True)
            consume  = entry.get("consume", 0)
            raw_cmds = entry.get("commands", [])
            cmds = []
            for c in raw_cmds:
                parts = c.split(" ", 1)
                if len(parts) == 2 and parts[0] in ("[console]", "[player]", "[op]"):
                    cmds.append((parts[0], parts[1]))
                else:
                    cmds.append(("[console]", c))
            self.add_block(trigger, cancel, consume, cmds, at)


# ---------------------------------------------
#  ITEM EDITOR
# ---------------------------------------------

class ItemEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change):
        super().__init__(parent, fg_color=BG_PANEL)
        # Inner scrollable — single scrollbar, no duplicates
        self._scroll = ctk.CTkScrollableFrame(self, fg_color=BG_PANEL,
                                               scrollbar_fg_color=BG_HDR,
                                               scrollbar_button_color=SCROLL_BTN,
                                               scrollbar_button_hover_color=SCROLL_HOV)
        self._scroll.pack(fill="both", expand=True)
        self.on_change = on_change
        self._build()

    def _build(self):
        P = {"padx": 14, "pady": 5}

        self._section("Basic Info")

        r = self._row()
        ctk.CTkLabel(r, text="Item Key:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.key_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.key_var,
                     placeholder_text="e.g: dragon_sword",
                     font=("Consolas", 12)).pack(side="left", fill="x", expand=True)
        self.key_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Material:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.mat_var = tk.StringVar(value="DIAMOND_SWORD")
        ctk.CTkOptionMenu(r, variable=self.mat_var, values=MATERIALS,
                          width=240, height=32, font=("Consolas", 11),
                          command=lambda _: self.on_change()
                          ).pack(side="left")

        r = self._row()
        ctk.CTkLabel(r, text="CMD:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.cmd_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.cmd_var,
                     placeholder_text="e.g: 1001  (optional)",
                     width=180, font=("Consolas", 12)).pack(side="left")
        self.cmd_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Display Name:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.name_color_var = tk.StringVar(value="Gold")
        ctk.CTkOptionMenu(r, variable=self.name_color_var,
                          values=list(MINI_COLORS.keys()),
                          width=110, height=32, font=("Consolas", 11),
                          command=lambda _: self.on_change()
                          ).pack(side="left", padx=(0, 6))
        self.name_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.name_var,
                     placeholder_text="item name...",
                     font=("Consolas", 12)).pack(side="left", fill="x", expand=True)
        self.name_var.trace_add("write", lambda *_: self.on_change())

        r = self._row()
        ctk.CTkLabel(r, text="Amount:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.amount_var = tk.IntVar(value=1)
        ctk.CTkEntry(r, textvariable=self.amount_var,
                     width=55, font=("Consolas", 12)).pack(side="left", padx=(0, 20))
        self.unbreakable_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(r, text="Unbreakable",
                        variable=self.unbreakable_var,
                        font=("Consolas", 12),
                        command=self.on_change).pack(side="left")

        r = self._row()
        ctk.CTkLabel(r, text="Durability:", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.durability_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.durability_var,
                     placeholder_text="e.g: 100  (optional, requires SIG 1.9.0+)",
                     font=("Consolas", 12)).pack(side="left", fill="x", expand=True)
        self.durability_var.trace_add("write", lambda *_: self.on_change())

        self._sep()

        self.lore_editor = LoreEditor(self._scroll, self.on_change)
        self.lore_editor.pack(fill="x", **P)

        self._sep()

        self.ench_editor = EnchantEditor(self._scroll, self.on_change)
        self.ench_editor.pack(fill="x", **P)

        self._sep()

        self._section("Item Flags")
        flags_frame = ctk.CTkFrame(self._scroll, fg_color=BG_HDR, corner_radius=4)
        flags_frame.pack(fill="x", **P)
        self.flag_vars: dict[str, tk.BooleanVar] = {}
        grid = ctk.CTkFrame(flags_frame, fg_color="transparent")
        grid.pack(padx=10, pady=8)
        for i, flag in enumerate(ITEM_FLAGS):
            v = tk.BooleanVar(value=False)
            self.flag_vars[flag] = v
            ctk.CTkCheckBox(grid, text=flag, variable=v,
                            font=("Consolas", 11),
                            command=self.on_change
                            ).grid(row=i // 2, column=i % 2, sticky="w", padx=14, pady=3)

        self._sep()

        self._section("NBT")
        r = self._row()
        ctk.CTkLabel(r, text="NBT (raw):", width=115, anchor="w",
                     font=("Consolas", 12)).pack(side="left")
        self.nbt_var = tk.StringVar()
        ctk.CTkEntry(r, textvariable=self.nbt_var,
                     placeholder_text='{CustomTag: "value"}',
                     font=("Consolas", 11)).pack(side="left", fill="x", expand=True)
        self.nbt_var.trace_add("write", lambda *_: self.on_change())

        self._sep()

        self.usage_editor = UsageEditor(self._scroll, self.on_change)
        self.usage_editor.pack(fill="x", **P)

        self._sep()

    def _section(self, title):
        ctk.CTkLabel(self._scroll, text=title,
                     font=("Consolas", 13, "bold"),
                     text_color=TXT_MAIN).pack(anchor="w", padx=14, pady=(10, 2))

    def _row(self):
        f = ctk.CTkFrame(self._scroll, fg_color="transparent")
        f.pack(fill="x", padx=14, pady=4)
        return f

    def _sep(self):
        ctk.CTkFrame(self._scroll, fg_color=BORDER, height=1).pack(fill="x", pady=6)

    def get_item_data(self) -> dict:
        return {
            "key":          slugify(self.key_var.get()) or "item",
            "material":     self.mat_var.get(),
            "cmd":          self.cmd_var.get(),
            "name_text":    self.name_var.get(),
            "name_color":   self.name_color_var.get(),
            "amount":       self.amount_var.get(),
            "unbreakable":  self.unbreakable_var.get(),
            "lore":         self.lore_editor.get_data(),
            "enchantments": self.ench_editor.get_data(),
            "flags":        [f for f, v in self.flag_vars.items() if v.get()],
            "durability":   self.durability_var.get(),
            "nbt":          self.nbt_var.get(),
            "usage":        self.usage_editor.get_data(),
        }

    def load_item_data(self, data: dict):
        self.key_var.set(data.get("key", ""))
        self.mat_var.set(data.get("material", "DIAMOND_SWORD"))
        self.cmd_var.set(data.get("cmd", ""))
        self.name_var.set(data.get("name_text", ""))
        self.name_color_var.set(data.get("name_color", "Gold"))
        self.amount_var.set(data.get("amount", 1))
        self.unbreakable_var.set(data.get("unbreakable", False))
        self.lore_editor.load_data(data.get("lore", []))
        self.ench_editor.load_data(data.get("enchantments", {}))
        for flag, v in self.flag_vars.items():
            v.set(flag in data.get("flags", []))
        self.durability_var.set(str(data.get("durability", "")))
        self.nbt_var.set(data.get("nbt", ""))
        self.usage_editor.load_data(data.get("usage", []))




# ---------------------------------------------
#  MAIN APP
# ---------------------------------------------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIG Config Tool")
        self.geometry("1300x840")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_ROOT)

        # Pencere ikonu
        try:
            import sys
            base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
            ico_path = os.path.join(base, "sword-template.ico")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
            else:
                from PIL import Image, ImageTk
                img = Image.open(os.path.join(base, "eh.png")).resize((32, 32), Image.NEAREST)
                icon_img = ImageTk.PhotoImage(img)
                self.iconphoto(True, icon_img)
                self._icon_img = icon_img
        except Exception:
            pass

        self.project_name = ""
        self.items: list[dict] = []
        self.selected_idx: int | None = None
        self.unsaved = False
        self.item_editor = None

        self._build_header()
        self._build_welcome()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=BG_PANEL, height=52, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        self.back_btn = ctk.CTkButton(hdr, text="<", width=36, height=34,
                                      font=("Consolas", 14, "bold"),
                                      fg_color=BTN, hover_color=BTN_H,
                                      command=self._go_home)
        self.back_btn.pack(side="left", padx=(6, 0), pady=9)
        self.back_btn.pack_forget()  # başta gizli

        neon = make_neon_label(hdr, "SIG Config Tool", font_size=16, bg="#111111")
        neon.pack(side="left", padx=18)

        self.project_label = ctk.CTkLabel(hdr, text="",
                                          font=("Consolas", 13, "bold"),
                                          text_color=TXT_MAIN)
        self.project_label.pack(side="left", padx=20)

        for txt, cmd in [
            ("💾 Save",        self._save_project),
            ("📂 Open",        self._load_project),
            ("📋 YAML Export", self._export_yaml),
        ]:
            ctk.CTkButton(hdr, text=txt, command=cmd, height=34, width=120,
                          font=("Consolas", 12),
                          fg_color=BTN, hover_color=BTN_H
                          ).pack(side="right", padx=6, pady=9)

    def _build_welcome(self):
        self.welcome_frame = ctk.CTkFrame(self, fg_color=BG_ROOT)
        self.welcome_frame.pack(fill="both", expand=True)

        # Center container
        center = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(center, fg_color="transparent")
        inner.pack()

        # Left: Dynaimc blursuz pixel art container
        img_label = ctk.CTkLabel(inner, text="")
        img_label.pack(side="left", padx=(0, 40))

        # Yükleme ve blursuz büyütme mantığı (Nearest Neighbor)
        try:
            # 16x16 orijinal dosyayı yükle
            src_img = tk.PhotoImage(file="eh.png")
            # 16x16 görseli piksellerini bozmadan tam 13 kat büyütür (Yaklaşık 208x208 yapar)
            expanded_img = src_img.zoom(13, 13)
            img_label.configure(image=expanded_img)
            img_label.image = expanded_img  # Garbage collection koruması
        except Exception:
            # Dosya bulunamazsa çökmesin diye boş yedek alan bırakır
            img_label.configure(text="[ eh.png not found ]", font=("Consolas", 12), text_color="#cc4444")

        # Right: title + buttons
        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="left")

        neon2 = make_neon_label(right, "SIG Config Tool", font_size=24, bg="#0a0a0a")
        neon2.pack(anchor="w")
        ctk.CTkLabel(right, text="Visual configurator for SimpleItemGenerator",
                     font=("Consolas", 12),
                     text_color=TXT_DIM).pack(anchor="w", pady=(4, 32))

        ctk.CTkButton(right, text="New Project",
                      height=50, width=280,
                      font=("Consolas", 15, "bold"),
                      fg_color=BTN, hover_color=BTN_H,
                      corner_radius=4,
                      command=self._new_project).pack(pady=(0, 10))
        ctk.CTkButton(right, text="Open Project",
                      height=44, width=280,
                      font=("Consolas", 13),
                      fg_color=BTN, hover_color=BTN,
                      corner_radius=4,
                      border_width=1, border_color=BORDER,
                      command=self._load_project).pack()

        ctk.CTkLabel(right, text="v6.0  --  SimpleItemGenerator Config Tool",
                     font=("Consolas", 10),
                     text_color=TXT_DIM).pack(anchor="w", pady=(28, 0))

        # Sol alt köşe imza
        sig_label = ctk.CTkLabel(self.welcome_frame, text="by Goko0023",
                                 font=("Consolas", 11),
                                 text_color="#3a3a3a")
        sig_label.place(relx=0.0, rely=1.0, anchor="sw", x=14, y=-12)

    def _build_main_layout(self):
        if hasattr(self, "welcome_frame"):
            self.welcome_frame.destroy()

        self.back_btn.pack(side="left", padx=(6, 0), pady=9)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_panel = ctk.CTkFrame(self.main_frame,
                                       fg_color=BG_PANEL, corner_radius=4)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.right_panel = ctk.CTkFrame(self.main_frame,
                                        fg_color=BG_PANEL, corner_radius=4, width=400)
        self.right_panel.pack(side="right", fill="both")
        self.right_panel.pack_propagate(False)

        self._build_left_panel()
        self._build_right_panel()

    def _build_left_panel(self):
        # --- Üst: Item listesi (sabit yükseklik) ---
        list_hdr = ctk.CTkFrame(self.left_panel, fg_color=BG_HDR,
                                height=40, corner_radius=0)
        list_hdr.pack(fill="x")
        list_hdr.pack_propagate(False)
        ctk.CTkLabel(list_hdr, text="Items",
                     font=("Consolas", 13, "bold"),
                     text_color="#ffffff").pack(side="left", padx=12)
        ctk.CTkButton(list_hdr, text="+ New Item", height=28, width=110,
                      font=("Consolas", 12),
                      fg_color=BTN, hover_color=BTN_H,
                      command=self._add_item).pack(side="right", padx=8, pady=6)

        self.item_list_frame = ctk.CTkScrollableFrame(
            self.left_panel, height=140, fg_color=BG_PANEL,
            scrollbar_fg_color=BG_HDR,
            scrollbar_button_color=SCROLL_BTN,
            scrollbar_button_hover_color=SCROLL_HOV,
        )
        self.item_list_frame.pack(fill="x", padx=6, pady=4)

        ctk.CTkFrame(self.left_panel, fg_color=BORDER, height=1).pack(fill="x")

        # --- Alt: Editor alanı (tüm kalan alan) ---
        self.editor_container = ctk.CTkFrame(self.left_panel, fg_color=BG_PANEL)
        self.editor_container.pack(fill="both", expand=True)

        self.editor_label = ctk.CTkLabel(
            self.editor_container,
            text="Select an item or add a new one",
            font=("Consolas", 12), text_color=TXT_SUB
        )
        self.editor_label.pack(pady=20)

    def _build_right_panel(self):
        top = ctk.CTkFrame(self.right_panel, fg_color=BG_HDR,
                           height=40, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkLabel(top, text="Live YAML Preview",
                     font=("Consolas", 13, "bold"),
                     text_color="#ffffff").pack(side="left", padx=12, pady=10)
        ctk.CTkButton(top, text="Copy", height=26, width=80,
                      font=("Consolas", 11),
                      fg_color=BTN, hover_color=BTN_H,
                      command=self._copy_yaml).pack(side="right", padx=8, pady=7)

        self.yaml_box = ctk.CTkTextbox(
            self.right_panel,
            font=("Consolas", 11),
            fg_color=BG_ROOT,
            text_color=YAML_TEXT,
            wrap="none",
            state="disabled",
        )
        self.yaml_box.pack(fill="both", expand=True, padx=8, pady=8)

    # -- PROJECT OPS ---------------------------

    def _go_home(self):
        if self.unsaved and self.items:
            if not messagebox.askyesno("Go Home", "You have unsaved changes. Go to home screen anyway?"):
                return
        if hasattr(self, "main_frame"):
            self.main_frame.destroy()
        self.project_name = ""
        self.items.clear()
        self.selected_idx = None
        self.unsaved = False
        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None
        self.project_label.configure(text="")
        self.back_btn.pack_forget()
        self._build_welcome()

    def _new_project(self):
        name = simpledialog.askstring("New Project", "Enter project name:",
                                      initialvalue="MyServer")
        if not name:
            return
        self.project_name = name.strip()
        self.items.clear()
        self.selected_idx = None
        self.unsaved = False
        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None
        self.project_label.configure(text=f"[ {self.project_name} ]")
        self._build_main_layout()
        self._refresh_yaml()

    def _save_project(self):
        if not self.project_name:
            messagebox.showwarning("Warning", "Create a project first!")
            return
        self._flush_editor()
        path = filedialog.asksaveasfilename(
            defaultextension=".sigproj",
            filetypes=[("SIG Project", "*.sigproj"), ("JSON", "*.json")],
            initialfile=f"{self.project_name}.sigproj",
            title="Save Project"
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"project": self.project_name, "items": self.items},
                          f, ensure_ascii=False, indent=2)
        except OSError as e:
            messagebox.showerror("Error", f"Could not save:\n{e}")
            return
        self.unsaved = False
        messagebox.showinfo("Saved", f"Project saved:\n{path}")

    def _load_project(self):
        path = filedialog.askopenfilename(
            filetypes=[("SIG Project", "*.sigproj"), ("JSON", "*.json")],
            title="Open Project"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            messagebox.showerror("Error", f"Could not load project:\n{e}")
            return
        self.project_name = data.get("project", "Project")
        self.items = data.get("items", [])
        self.selected_idx = None
        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None
        self.project_label.configure(text=f"[ {self.project_name} ]")
        if hasattr(self, "welcome_frame"):
            self._build_main_layout()
        else:
            self._rebuild_item_list()
        self._refresh_yaml()

    def _export_yaml(self):
        if not self.items:
            messagebox.showwarning("Warning", "No items in project!")
            return
        self._flush_editor()
        path = filedialog.asksaveasfilename(
            defaultextension=".yml",
            filetypes=[("YAML", "*.yml")],
            initialfile="items.yml",
            title="YAML Export"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._build_full_yaml())
        messagebox.showinfo("Export", f"YAML exported:\n{path}")

    # -- ITEM OPS ------------------------------

    def _add_item(self):
        self._flush_editor()
        new_idx = len(self.items)
        self.items.append({
            "key":          f"item_{new_idx + 1}",
            "material":     "DIAMOND_SWORD",
            "cmd":          "",
            "name_text":    "",
            "name_color":   "Gold",
            "amount":       1,
            "unbreakable":  False,
            "lore":         [],
            "enchantments": {},
            "flags":        [],
            "durability":   "",
            "nbt":          "",
            "usage":        [],
        })
        self.unsaved = True
        self._select_item(new_idx)

    def _select_item(self, idx: int):
        if self.selected_idx != idx:
            self._flush_editor()
        self.selected_idx = idx

        if self.item_editor is not None:
            try:
                self.item_editor.destroy()
            except Exception:
                pass
            self.item_editor = None

        if hasattr(self, "editor_label"):
            try:
                if self.editor_label.winfo_exists():
                    self.editor_label.destroy()
            except Exception:
                pass

        self.item_editor = ItemEditor(self.editor_container, self._on_editor_change)
        self.item_editor.pack(fill="both", expand=True)
        self.item_editor.load_item_data(self.items[idx])

        self._rebuild_item_list()
        self._refresh_yaml()

    def _delete_item(self, idx: int):
        if not messagebox.askyesno("Delete", f"Delete '{self.items[idx]['key']}'?"):
            return
        self.items.pop(idx)
        if self.selected_idx == idx:
            self.selected_idx = None
            if self.item_editor:
                self.item_editor.destroy()
                self.item_editor = None
            self.editor_label = ctk.CTkLabel(
                self.editor_container,
                text="Select an item or add a new one",
                font=("Consolas", 12), text_color=TXT_SUB
            )
            self.editor_label.pack(pady=20)
        elif self.selected_idx is not None and self.selected_idx > idx:
            self.selected_idx -= 1
        self._rebuild_item_list()
        self._refresh_yaml()

    def _rebuild_item_list(self):
        for w in self.item_list_frame.winfo_children():
            w.destroy()

        if not self.items:
            ctk.CTkLabel(self.item_list_frame,
                         text="No items yet  --  click + New Item",
                         font=("Consolas", 11), text_color=TXT_SUB
                         ).pack(pady=10)
            return

        for i, item in enumerate(self.items):
            is_sel = (i == self.selected_idx)
            row = ctk.CTkFrame(self.item_list_frame,
                               fg_color=SEL_BG if is_sel else BG_HDR,
                               corner_radius=4)
            row.pack(fill="x", pady=2, padx=4)

            ctk.CTkLabel(row,
                         text=(">> " if is_sel else "   ") + item.get("key", "?"),
                         font=("Consolas", 12, "bold" if is_sel else "normal"),
                         text_color="#ffffff" if is_sel else TXT_SUB,
                         anchor="w").pack(side="left", padx=10, pady=6,
                                         fill="x", expand=True)

            ctk.CTkLabel(row, text=item.get("material", ""),
                         font=("Consolas", 10),
                         text_color=TXT_SUB).pack(side="left", padx=6)

            ctk.CTkButton(row, text="X", width=26, height=26,
                          fg_color=BTN_DEL, hover_color=BTN_DEL2,
                          command=lambda i=i: self._delete_item(i)
                          ).pack(side="right", padx=6, pady=4)
            ctk.CTkButton(row, text="Select", width=60, height=26,
                          fg_color=BTN_H if is_sel else BTN,
                          hover_color=BTN_H,
                          font=("Consolas", 11),
                          command=lambda i=i: self._select_item(i)
                          ).pack(side="right", padx=4, pady=4)

    # -- YAML ----------------------------------

    def _flush_editor(self):
        if self.item_editor and self.selected_idx is not None:
            data = self.item_editor.get_item_data()
            if 0 <= self.selected_idx < len(self.items):
                self.items[self.selected_idx] = data

    def _on_editor_change(self):
        self._flush_editor()
        if self.selected_idx is not None:
            self._rebuild_item_list()
        self._refresh_yaml()

    def _build_full_yaml(self) -> str:
        all_blocks = {}
        for item in self.items:
            key = item.get("key") or "item"
            all_blocks[key] = build_yaml_for_item(item)
        return yaml.dump(all_blocks, allow_unicode=True,
                         default_flow_style=False, sort_keys=False, indent=2)

    def _refresh_yaml(self):
        if not hasattr(self, "yaml_box"):
            return
        try:
            text = self._build_full_yaml() if self.items else "# No items yet\n"
        except Exception as e:
            text = f"# Error: {e}\n"
        self.yaml_box.configure(state="normal")
        self.yaml_box.delete("1.0", "end")
        self.yaml_box.insert("1.0", text)
        self.yaml_box.configure(state="disabled")

    def _copy_yaml(self):
        self.yaml_box.configure(state="normal")
        content = self.yaml_box.get("1.0", "end")
        self.yaml_box.configure(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("Copied", "YAML copied to clipboard!")


    def on_close(self):
        self._flush_editor()
        if self.unsaved and self.items:
            if messagebox.askyesno("Exit", "You have unsaved changes. Exit anyway?"):
                self.quit()
                self.destroy()
        else:
            self.quit()
            self.destroy()


# ---------------------------------------------
#  ENTRY POINT
# ---------------------------------------------

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()