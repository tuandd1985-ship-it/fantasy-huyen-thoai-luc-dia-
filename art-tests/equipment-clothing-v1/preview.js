"use strict";

const levels = [
  { lv: 1, name: "Khởi Hành", filter: "none" },
  { lv: 20, name: "Băng Lam", filter: "grayscale(1) sepia(.62) hue-rotate(150deg) saturate(2.6) brightness(1.16)" },
  { lv: 40, name: "Hỏa Đồng", filter: "sepia(.9) saturate(2.6) hue-rotate(339deg) brightness(.87) contrast(1.12)" },
  { lv: 60, name: "Thiên Kim", filter: "grayscale(1) sepia(.65) saturate(1.75) brightness(1.36)" },
];
const slots = {
  armor: { name: "Áo giáp", base: lv => ({ def: 3 + lv * 1.15, hp: 22 + lv * 6.5 }) },
  boots: { name: "Giày", base: lv => ({ def: 2 + lv * .8, hp: 10 + lv * 3.2 }) },
};
const armorLayers = new Set(["cape", "torso", "arm_l_upper", "arm_r_upper"]);
const bootLayers = /_shin$|_foot$/;
const get = id => document.getElementById(id);
const profile = Object.fromEntries(Object.keys(wardrobeRigs).map(id => [id, {
  lv: 1, equipped: { armor: 1, boots: 1 }, upgrades: {},
}]));
const hero = get("hero");
for (const [id, { name }] of Object.entries(wardrobeRigs)) hero.add(new Option(name, id));

function stats(slot, lv, up) {
  const base = slots[slot].base(lv);
  const change = value => Math.round(Math.round(value) * (1 + .08 * up));
  return { def: change(base.def), hp: change(base.hp) };
}

function create(tag, text, cssClass) {
  const element = document.createElement(tag);
  if (text) element.textContent = text;
  if (cssClass) element.className = cssClass;
  return element;
}

function render(message = "", focusId) {
  const selected = hero.value;
  const rig = wardrobeRigs[selected];
  const state = profile[selected];
  get("level").value = state.lv;
  const stage = get("rig");
  stage.setAttribute("aria-label", rig.name + " trong trang bị đang chọn");
  if (stage.dataset.hero !== selected) {
    stage.dataset.hero = selected;
    stage.replaceChildren(...rig.parts.map(file => {
      const image = create("img");
      image.src = "../parts/" + rig.folder + "/" + file;
      image.alt = "";
      image.dataset.part = file.replace(".png", "");
      return image;
    }));
  }
  for (const image of stage.children) {
    const part = image.dataset.part;
    const slot = armorLayers.has(part) ? "armor" : bootLayers.test(part) ? "boots" : null;
    const equipped = slot && levels.find(tier => tier.lv === state.equipped[slot]);
    image.style.filter = equipped ? equipped.filter : "none";
  }

  const total = { def: 0, hp: 0 };
  const panels = [];
  for (const [slot, meta] of Object.entries(slots)) {
    const equipped = state.equipped[slot];
    const key = slot + equipped;
    const upgrade = state.upgrades[key] || 0;
    if (equipped) {
      const current = stats(slot, equipped, upgrade);
      total.def += current.def;
      total.hp += current.hp;
    }
    const panel = create("div", "", "slot");
    const header = create("div", "", "slot-head");
    const actions = create("div", "", "slot-actions");
    const raise = create("button", upgrade === 10 ? "+10 tối đa" : "Nâng +" + (upgrade + 1));
    raise.id = "upgrade-" + slot;
    raise.disabled = !equipped || upgrade === 10;
    raise.onclick = () => {
      state.upgrades[key] = upgrade + 1;
      render("Đã nâng " + meta.name.toLowerCase() + " lên +" + (upgrade + 1) + ".", raise.id);
    };
    const remove = create("button", "Tháo");
    remove.disabled = !equipped;
    remove.onclick = () => {
      state.equipped[slot] = null;
      render("Đã tháo " + meta.name.toLowerCase() + ".", "item-" + slot + "-1");
    };
    actions.append(raise, remove);
    header.append(create("h3", meta.name), actions);
    const items = create("div", "", "items");
    for (const tier of levels) {
      const level = tier.lv;
      const itemUp = state.upgrades[slot + level] || 0;
      const current = stats(slot, level, itemUp);
      const button = create("button", "", "item");
      button.id = "item-" + slot + "-" + level;
      button.disabled = level > state.lv;
      button.setAttribute("aria-pressed", String(equipped === level));
      button.setAttribute("aria-label", meta.name + " " + tier.name + " cấp " + level);
      const image = create("img");
      image.alt = "";
      image.src = "icons/" + selected + "/" + slot + "-lv" + level + ".webp";
      button.append(image, create("strong", tier.name + (itemUp ? " +" + itemUp : "")),
        create("span", button.disabled ? "Cần Lv " + level : "Lv " + level + " · " + current.def + " THỦ · " + current.hp + " HP"));
      button.onclick = () => {
        state.equipped[slot] = level;
        render("Đang mặc " + meta.name.toLowerCase() + " " + tier.name + ".", button.id);
      };
      items.append(button);
    }
    panel.append(header, items);
    panels.push(panel);
  }
  get("slots").replaceChildren(...panels);
  get("def").textContent = total.def;
  get("hp").textContent = total.hp;
  get("power").textContent = Math.round(total.def * 2.4 + total.hp * .35);
  get("status").textContent = message;
  if (focusId) get(focusId)?.focus();
}

hero.onchange = () => render();
get("level").onchange = event => {
  const state = profile[hero.value];
  state.lv = Math.max(1, Math.min(60, Math.trunc(Number(event.target.value) || 1)));
  let removed = false;
  for (const slot of Object.keys(slots)) {
    if (state.equipped[slot] > state.lv) {
      state.equipped[slot] = null;
      removed = true;
    }
  }
  render(removed ? "Đã tháo món cao hơn cấp thử nghiệm." : "Cấp thử nghiệm " + state.lv + ".");
};
render();
