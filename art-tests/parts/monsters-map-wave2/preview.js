"use strict";

const sceneCanvas = document.getElementById("scene");
const ctx = sceneCanvas.getContext("2d");
const maps = document.getElementById("maps");
const motion = document.getElementById("motion");
const anchors = document.getElementById("anchors");
const attack = document.getElementById("attack");
const note = document.getElementById("note");
const roster = document.getElementById("roster");
const images = new Map();
let active, loaded, playing = !matchMedia("(prefers-reduced-motion: reduce)").matches;
let time = 0, previous = 0, strike = -4, loading = 0;

for (const { id, name } of Scenes) maps.add(new Option(name, id));

function image(path) {
  if (!images.has(path)) {
    const sprite = new Image();
    images.set(path, new Promise((resolve, reject) => {
      sprite.onload = () => resolve(sprite);
      sprite.onerror = () => reject(new Error(path));
      sprite.src = path;
    }));
  }
  return images.get(path);
}

async function showMap() {
  const request = ++loading;
  active = Scenes.find(scene => scene.id === maps.value);
  note.textContent = "Đang nạp ảnh…";
  attack.disabled = true;
  loaded = null;
  ctx.clearRect(0, 0, sceneCanvas.width, sceneCanvas.height);
  sceneCanvas.setAttribute("aria-label", active.name + ", " + active.actors.length + " quái");
  roster.textContent = [...new Set(active.actors.map(actor => RigData[actor.id].name))].join(" · ");
  try {
    const map = await image("../../maps-anh-do/map/" + active.map);
    const actors = await Promise.all(active.actors.map(async (actor, index) => {
      const rig = RigData[actor.id];
      const parts = await Promise.all(rig.parts.map(async part => ({
        ...part, img: await image(rig.folder + "/" + part.file),
      })));
      return { ...actor, rig, parts, phase: index * 1.43 };
    }));
    if (request !== loading) return;
    loaded = { map, actors };
    time = 0;
    strike = -4;
    note.textContent = actors.length + " quái đang trên sân thử.";
    attack.disabled = false;
    draw();
  } catch (error) {
    if (request === loading) note.textContent = "Không mở được ảnh " + error.message;
  }
}

function partAngle(actor, part, t, pulse) {
  const phase = t * 4 + actor.phase;
  const id = part.id;
  const side = /(?:^|_)l(?:_|$)/.test(id) ? 1 : -1;
  if (id.startsWith("wing")) return side * (Math.sin(phase * 2) * .18 + pulse * .20);
  if (id.startsWith("leg") || /^(front|rear)_/.test(id)) {
    const offset = id.endsWith("2") || id.startsWith("rear") ? Math.PI : 0;
    return side * (Math.sin(phase + offset) * .08 + pulse * .11);
  }
  if (id.startsWith("arm") || id.startsWith("foreleg")) return side * (Math.sin(phase) * .06 + pulse * .30);
  if (id === "head") return Math.sin(phase * .6) * .04 + pulse * .15;
  if (id === "tail") return Math.sin(phase) * .13;
  return 0;
}

function drawActor(actor, t) {
  const px = actor.x + Math.sin(t * 1.8 + actor.phase) * actor.dx;
  const py = actor.y + Math.sin(t * 1.8 + actor.phase) * actor.dy;
  const elapsed = t - strike - (actor.phase % 2) * .15;
  const pulse = elapsed > 0 && elapsed < .8 ? Math.sin(elapsed * Math.PI / .8) : 0;
  const scale = actor.h / actor.rig.spriteHeight;
  const relative = new Map(actor.parts.map(part => [part.id, part]));
  const matrices = new Map();
  function transform(part) {
    if (matrices.has(part.id)) return matrices.get(part.id);
    const parent = relative.get(part.parent);
    const current = parent ? transform(parent) : new DOMMatrix();
    const pivot = part.pivot;
    const rotated = current.translate(pivot.x,pivot.y).rotate(partAngle(actor,part,t,pulse) * 180 / Math.PI).translate(-pivot.x,-pivot.y);
    matrices.set(part.id,rotated);
    return rotated;
  }
  ctx.save();
  ctx.fillStyle = "#0b0d0bb0";
  ctx.beginPath();
  ctx.ellipse(px,py,actor.h * .31,Math.max(3,actor.h * .074),0,0,Math.PI*2);
  ctx.fill();
  ctx.translate(px,py);
  ctx.scale(actor.face * scale,scale);
  ctx.translate(-384 + pulse * 20,-620 - Math.sin(t * 4 + actor.phase) * (actor.id === "bat" ? 13 : 2));
  for (const part of actor.parts) {
    ctx.save();
    const m = transform(part);
    ctx.transform(m.a,m.b,m.c,m.d,m.e,m.f);
    ctx.drawImage(part.img,0,0);
    ctx.restore();
  }
  ctx.restore();
  if (anchors.getAttribute("aria-pressed") === "true") {
    ctx.strokeStyle = "#ffe4a3";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(px,py,8,0,Math.PI*2);
    ctx.stroke();
    ctx.font = "600 17px system-ui";
    ctx.textAlign = "center";
    ctx.fillStyle = "#fff3c9";
    ctx.strokeStyle = "#171812";
    ctx.lineWidth = 4;
    ctx.strokeText(actor.rig.name,px,py+28);
    ctx.fillText(actor.rig.name,px,py+28);
  }
}

function draw() {
  if (!loaded) return;
  ctx.drawImage(loaded.map,0,0,sceneCanvas.width,sceneCanvas.height);
  const order = [...loaded.actors].sort((a,b) => a.y-b.y);
  for (const actor of order) drawActor(actor,time);
}
function setMotion(value) {
  playing = value;
  motion.setAttribute("aria-pressed",String(playing));
  motion.textContent = playing ? "Tạm dừng" : "Chạy chuyển động";
}
function animate(timestamp) {
  if (playing && loaded) {
    time += Math.min(.05,(timestamp - (previous || timestamp)) / 1000);
    draw();
  }
  previous = timestamp;
  requestAnimationFrame(animate);
}
maps.onchange = showMap;
motion.onclick = () => setMotion(!playing);
anchors.onclick = () => {
  anchors.setAttribute("aria-pressed",String(anchors.getAttribute("aria-pressed") !== "true"));
  draw();
};
attack.onclick = () => { strike = time; setMotion(true); note.textContent = "Đang thử nhịp ra đòn."; };
setMotion(playing);
showMap();
requestAnimationFrame(animate);
