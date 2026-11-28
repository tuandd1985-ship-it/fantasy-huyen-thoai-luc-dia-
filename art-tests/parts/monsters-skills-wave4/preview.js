"use strict";

const canvas = document.getElementById("scene");
const ctx = canvas.getContext("2d");
const select = document.getElementById("skill");
const cast = document.getElementById("cast");
const loop = document.getElementById("loop");
const status = document.getElementById("phase");
const detail = document.getElementById("detail");
const heroFile = "../../hero-edge-clean/cleaned_png/hero-swordsman-male.png";
const groundFile = "../../maps-anh-do/map/bossxuan.png";
const cache = new Map();
let current, stage, loadId = 0, started = null, lastPhase = "";

for (const entry of SkillScenes) select.add(new Option(entry.title, entry.id));

function image(path) {
  if (!cache.has(path)) cache.set(path, new Promise((resolve,reject) => {
    const file = new Image();
    file.onload = () => resolve(file);
    file.onerror = () => reject(new Error(path));
    file.src = path;
  }));
  return cache.get(path);
}

async function selectSkill() {
  const requested = ++loadId;
  current = SkillScenes.find(entry => entry.id === select.value);
  const skill = current;
  started = null;
  stage = null;
  cast.disabled = true;
  detail.textContent = skill.hint;
  status.textContent = "Đang nạp ảnh…";
  try {
    const source = MonsterArt[skill.actor];
    const target = skill.ally || skill.summon;
    const [ground, attacker, defender, impact, projectile, warning, parts] = await Promise.all([
      image(groundFile),image(source.file),image(target ? MonsterArt[target].file : heroFile),
      image("fx/" + skill.impact + ".webp"),
      skill.projectile ? image("fx/" + skill.projectile + ".webp") : null,
      skill.mode === "circle" ? image("fx/warn-ring.webp") : null,
      Promise.all((source.parts || []).map(async p => ({...p,img:await image(p.file)}))),
    ]);
    if (requested !== loadId) return;
    stage = { ground, attacker, defender, impact, projectile, warning, parts, art:source };
    cast.disabled = false;
    lastPhase = "";
    draw(0);
  } catch (error) {
    if (requested === loadId) status.textContent = "Thiếu ảnh " + error.message;
  }
}

function drawAnchor(img, x,y,h,squash=1) {
  const w = h * img.width / img.height;
  ctx.drawImage(img,x-w/2,y-h*squash,w,h*squash);
}

function drawEffect(img,x,y,w,opacity=1,heightFactor=1) {
  if (opacity <= 0) return;
  const h = w * img.height / img.width * heightFactor;
  ctx.save();
  ctx.globalAlpha = opacity;
  ctx.drawImage(img,x-w/2,y-h/2,w,h);
  ctx.restore();
}

function shadow(x,y,w) {
  ctx.beginPath();
  ctx.ellipse(x,y,w,10,0,0,Math.PI*2);
  ctx.fillStyle = "#10150dbb";
  ctx.fill();
}

function drawRig(x,y,height,delta) {
  if (!stage.parts.length) {
    drawAnchor(stage.attacker,x,y,height);
    return;
  }
  const parts = new Map(stage.parts.map(part => [part.id,part]));
  const matrices = new Map();
  function pose(part) {
    if (matrices.has(part.id)) return matrices.get(part.id);
    const inherited = parts.has(part.parent) ? pose(parts.get(part.parent)) : new DOMMatrix();
    const {x,y} = part.pivot;
    const matrix = part.id === current.part ? inherited.translate(x,y).rotate(delta).translate(-x,-y) : inherited;
    matrices.set(part.id,matrix);
    return matrix;
  }
  ctx.save();
  ctx.translate(x,y);
  const scale = height / stage.art.height;
  ctx.scale(scale,scale);
  ctx.translate(-384,-stage.art.bottom);
  for (const part of stage.parts) {
    const m=pose(part);
    ctx.save();
    ctx.transform(m.a,m.b,m.c,m.d,m.e,m.f);
    ctx.drawImage(part.img,0,0);
    ctx.restore();
  }
  ctx.restore();
}

function draw(t) {
  const s = current;
  const castActive = t > 0 && t < s.end;
  const startX = s.mode === "melee" ? 382 : s.mode === "circle" ? 440 : 265;
  const targetX = s.mode === "melee" ? 590 : s.mode === "circle" ? 605 : 680;
  const groundY = 382;
  const swing = castActive ? Math.sin(Math.PI * Math.min(1,t/s.end)) : 0;
  const attackShift = s.mode === "melee" ? swing * 75 : s.mode === "line" && t >= s.hit ? Math.min(1,(t-s.hit)/230) * (targetX-startX-15) : 0;
  const effectProgress = Math.max(0,Math.min(1,(t-s.hit)/(s.end-s.hit)));
  ctx.drawImage(stage.ground,0,160,stage.ground.width,stage.ground.height*.66,0,0,canvas.width,canvas.height);
  ctx.fillStyle = "#10191575";
  ctx.fillRect(0,0,canvas.width,canvas.height);

  if (s.warn && t > 0 && t < s.warn) {
    const blink = .84 + .15 * Math.sin(t/95);
    if (s.mode === "circle") drawEffect(stage.warning,startX,groundY,375,blink,.65);
    else {
      ctx.save();
      ctx.globalAlpha = blink;
      ctx.setLineDash([13,8]);
      ctx.lineWidth = 4;
      ctx.strokeStyle = "#ffbe65";
      ctx.fillStyle = "#d34b224f";
      ctx.fillRect(startX,groundY-24,targetX-startX+60,48);
      ctx.strokeRect(startX,groundY-24,targetX-startX+60,48);
      ctx.restore();
    }
  }

  shadow(startX+attackShift,groundY,70);
  const lift = s.actor==="vulture" ? (1-swing)*42 :
    (s.mode==="support" || s.mode==="projectile") ? swing*8 : 0;
  drawRig(startX+attackShift,groundY-lift,s.mode==="circle"?206:175,(s.amount||0)*swing);
  if (!s.summon || t >= s.hit) {
    shadow(targetX,groundY,40);
    drawAnchor(stage.defender,targetX,groundY,130,1);
  }
  if (s.mode === "projectile" && t >= s.release && t < s.hit) {
    const u=(t-s.release)/(s.hit-s.release);
    drawEffect(stage.projectile,startX+55+(targetX-startX-55)*u,groundY-69-Math.sin(u*Math.PI)*24,95);
  }
  if (t >= s.hit && t < s.end) {
    const onCaster=s.mode==="circle";
    const floor=s.mode==="support" || onCaster;
    drawEffect(stage.impact,onCaster?startX:targetX,floor?groundY:groundY-52,onCaster?400+90*effectProgress:90+105*effectProgress,1-effectProgress,floor?.63:1);
    if (s.drain) drawEffect(stage.impact,startX,groundY-58,90+30*effectProgress,1-effectProgress);
  }
  const what = !castActive ? "Sẵn sàng" : t < s.hit ? (s.warn ? "Báo đòn" : "Ra đòn") : "Tác động";
  if (what !== lastPhase) {
    status.textContent = what;
    lastPhase = what;
  }
}

function tick(now) {
  if (stage && started !== null) {
    const time = now-started;
    if (time >= current.end+320) started = loop.checked ? now : null;
    draw(started===null?0:now-started);
  }
  requestAnimationFrame(tick);
}
select.onchange = selectSkill;
cast.onclick = () => { started=performance.now(); };
selectSkill();
requestAnimationFrame(tick);
