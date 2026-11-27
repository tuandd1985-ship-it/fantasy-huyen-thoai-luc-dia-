const {chromium}=require('playwright-core');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const ROOT=__dirname,OUT=path.join(ROOT,'evidence');
const result={started:new Date().toISOString(),transport:'file:// (documented local mode); HTTP localhost attempted but unreachable in this execution environment',cases:[],console:[],requests:[]};
const url=pathToFileURL(path.resolve(ROOT,'../../index.html')).href;
function record(id,data){result.cases.push({id,...data});console.log(id,JSON.stringify(data));fs.writeFileSync(path.join(OUT,'review-tests.json'),JSON.stringify(result,null,2));}
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});result.browser=browser.version();
 try{
  const context=await browser.newContext({viewport:{width:844,height:390},hasTouch:true,deviceScaleFactor:1});
  await context.tracing.start({screenshots:true,snapshots:true,sources:false});
  const page=await context.newPage();
  page.on('pageerror',e=>result.console.push({type:'exception',message:e.message,stack:e.stack}));
  page.on('requestfailed',r=>result.requests.push({url:r.url().slice(0,240),failure:r.failure()}));
  await page.route('https://fonts.googleapis.com/**',r=>r.abort());
  async function boot(){await page.goto(url);await page.waitForFunction(()=>document.querySelector('#introBack').style.display==='none');}
  await boot();
  record('T01-initial-load',await page.evaluate(()=>({created:P.created,paused:uiPause,roster:Roster.chars.length,loadedHeroSheets:Object.keys(Sprites.heroAnim).length,loadedHeroArt:Object.keys(Sprites.heroArt).length})));
  for(const name of ['A','Bad<>','ValidHero']){await page.locator('#charName').fill(name);record('T02-name-'+name,await page.evaluate(()=>({check:UI.nameCheck(),startDisabled:document.querySelector('#createStart').disabled})));}
  const variants=[];
  for(const cid of ['swordsman','mage','archer'])for(const gender of ['male','female']){
   await page.evaluate(({cid,gender})=>{Roster.chars=[];Roster.active=-1;P=Save.load();createSel={classId:cid,gender};UI.openCreate();Roster.settings.muteAll=true;},{cid,gender});
   await page.locator('#charName').fill(cid+gender.slice(0,1));await page.locator('#createStart').click();
   variants.push(await page.evaluate(()=>({classId:P.classId,gender:P.gender,created:P.created,roster:Roster.chars.length,paused:uiPause,stats:{hp:heroStats().maxHp,mp:heroStats().maxMp,atk:heroStats().atk},sheetLoaded:!!Sprites.heroAnim[P.classId+'-'+P.gender]})));
  }
  record('T03-six-variants',{variants});
  await page.screenshot({path:path.join(OUT,'landscape-game.png')});
  const panelChecks=[];
  for(const auto of [false,true])for(const panel of ['char','bag','equip','skill','settings']){
   await page.evaluate(auto=>{P.auto=auto;input.jx=.8;input.jy=.2;},auto);
   await page.locator(`.hud-ico[data-panel="${panel}"]`).click();
   const open=await page.evaluate(()=>({current:PanelManager.current,paused:uiPause,auto:P.auto,input:{...input},panels:document.querySelectorAll('.panel.active').length}));
   await page.evaluate(()=>PanelManager.close());
   const closed=await page.evaluate(()=>({paused:uiPause,auto:P.auto}));panelChecks.push({panel,auto,open,closed});
  }
  record('T04-panels',{checks:panelChecks});
  await page.evaluate(()=>{P.auto=false;uiPause=false;});
  await page.locator('#minimap').click();
  record('T05-big-map-pause',await page.evaluate(()=>({overlayVisible:document.querySelector('#bigMapBack').classList.contains('show'),paused:uiPause,currentPanel:PanelManager.current})));
  await page.screenshot({path:path.join(OUT,'big-map-unpaused.png')});
  record('T05b-big-map-close-position',await page.locator('#bigMapClose').evaluate(e=>({rect:e.getBoundingClientRect().toJSON(),viewport:{w:innerWidth,h:innerHeight}})));
  await page.keyboard.press('Escape');
  await page.evaluate(()=>{hero.atkCd=0;PanelManager.open('char');});
  const attackBefore=await page.evaluate(()=>({paused:uiPause,cooldown:hero.atkCd,projectiles:projectiles.length}));
  await page.keyboard.press('j');
  record('T06-keyboard-during-pause',{before:attackBefore,after:await page.evaluate(()=>({paused:uiPause,cooldown:hero.atkCd,projectiles:projectiles.length}))});
  await page.evaluate(()=>{PanelManager.close();P=Save.fresh();P.created=true;P.name='Fixture';P.classId='swordsman';P.level=25;Save.data=P;resetSkillStates();startStage();monsters=[];const m=spawnMonster('slime',{eliteRoll:false});m.x=hero.x+50;m.y=hero.y;m.hp=m.maxHp=100000;hero.mp=heroStats().maxMp;Skills.cast(3);PanelManager.open('char');});
  const ultBefore=await page.evaluate(()=>({paused:uiPause,hp:monsters[0].hp}));await page.waitForTimeout(300);
  record('T07-ultimate-timer-pause',{before:ultBefore,after:await page.evaluate(()=>({paused:uiPause,hp:monsters[0].hp}))});
  const mechanics=await page.evaluate(()=>{
   PanelManager.close();P=Save.fresh();P.created=true;P.name='Fixture';P.classId='mage';P.level=10;P.alloc.def=45;Save.data=P;resetSkillStates();startStage();Roster.settings.muteAll=true;
   const oldRandom=Math.random;Math.random=()=>.99;hero.mp=50;hero.buffs.manaShieldT=8;const before=hero.mp;const damage=heroTakeDamage(10);const shield={rawAttack:10,def:heroStats().def,beforeMana:before,afterMana:hero.mp,damage};Math.random=oldRandom;
   P=Save.fresh();P.created=true;P.classId='swordsman';Save.data=P;P.equipped.weapon={base:{atk:100},pct:{atk:.30},up:0,gems:[]};const stats=heroStats();const formula={base:stats.baseAtk,flat:stats.flatAtk,pct:stats.pctTotal('atk'),actual:stats.atk,specExpected:stats.baseAtk*(1+stats.pctTotal('atk'))+stats.flatAtk};
   P.equipped.weapon=null;startStage();const left={x:forestEnv.riverX-5,y:200,r:14};Collision.move(left,100,0,.05);const bridge={x:forestEnv.riverX-5,y:forestEnv.bridgeY,r:14};for(let i=0;i<35;i++)Collision.move(bridge,100,0,.05);const edge={x:-100,y:-100,r:14};Collision.resolve(edge);
   const anim={idle:[Sprites.animFrame({},0),Sprites.animFrame({},1)],run:[0,1,2,3].map(i=>Sprites.animFrame({moving:true,walkPh:i*Math.PI/2},0)),attack:[.22,.05].map(t=>Sprites.animFrame({swingT:t},0)),dead:Sprites.animFrame({dead:true},0),cast:Sprites.animFrame({castT:1},0)};
   return {shield,formula,collision:{riverLeft:left,bridge,worldEdge:edge,riverX:forestEnv.riverX,riverRight:forestEnv.riverX+forestEnv.riverW},anim};
  });record('T08-mechanics',mechanics);
  await page.evaluate(()=>{P=Save.fresh();P.created=true;P.name='PersistProbe';Roster.chars=[P];Roster.active=0;Save.data=P;P.gold=4321;Roster.settings.quality='low';Save.persist();});await page.reload();await page.waitForFunction(()=>document.querySelector('#introBack').style.display==='none');
  record('T09-reload-loss',await page.evaluate(()=>({created:P.created,name:P.name,gold:P.gold,roster:Roster.chars.length,quality:Roster.settings.quality})));
  await page.setViewportSize({width:390,height:844});await page.waitForTimeout(150);
  await page.screenshot({path:path.join(OUT,'portrait-rotated.png')});
  await page.locator('#charName').fill('PortraitHero');await page.locator('#createStart').click();
  const joy=await page.locator('#joy').boundingBox();const center={x:joy.x+joy.width/2,y:joy.y+joy.height/2};
  await page.mouse.move(center.x,center.y);await page.mouse.down();await page.mouse.move(center.x,center.y+35,{steps:8});
  record('T10-portrait-joystick',await page.evaluate(()=>({rotated:Rot.on,input:{...input},viewport:{w:innerWidth,h:innerHeight},hud:[...document.querySelectorAll('.hud-ico')].map(x=>x.getBoundingClientRect().toJSON())})));
  await page.mouse.up();await page.screenshot({path:path.join(OUT,'portrait-game.png')});
  await page.setViewportSize({width:844,height:390});await page.waitForTimeout(150);
  record('T11-config',await page.evaluate(()=>({classes:Object.fromEntries(Object.entries(CONFIG.classes).map(([k,v])=>[k,{main:v.skills.map(s=>({id:s.id,unlock:s.unlock,mp:s.mp,cd:s.cd})),support:v.support.map(s=>({id:s.id,type:s.type}))}])),maps:CONFIG.maps.map(m=>({id:m.id,name:m.name,band:m.band,boss:m.boss})),itemSlots:CONFIG.itemSlots,gems:CONFIG.gems,caps:CONFIG.balance.caps,portraitSources:[...document.querySelectorAll('img')].map(i=>({id:i.id,loaded:i.complete&&i.naturalWidth>0,source:i.getAttribute('src')?.slice(0,80)}))})));
  console.log('Running independent seeded gameplay harness (render/UI/audio stubbed only in test page)...');
  const simulations=await page.evaluate(()=>{
   const savedUI={};for(const k of Object.keys(UI))if(typeof UI[k]==='function'){savedUI[k]=UI[k];UI[k]=()=>{};}
   const savedAudio={};for(const k of Object.keys(AudioFX))if(typeof AudioFX[k]==='function'){savedAudio[k]=AudioFX[k];AudioFX[k]=()=>{};}
   const savedMinimap=Minimap.draw;Minimap.draw=()=>{};
   const original=Math.random;let rng;Math.random=()=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng/4294967296;};
   const runs=[];
   function run(cid,seed,stage,level){
    rng=seed>>>0;P=Save.fresh();P.created=true;P.name='Harness';P.classId=cid;P.stage=stage;P.maxStage=stage;P.level=level;P.auto=true;Save.data=P;Roster.chars=[P];Roster.active=0;uiPause=false;input.jx=input.jy=0;for(const k of Object.keys(keys))keys[k]=false;
    for(const k of ['_stuckT','_ignoreDropT','_lx','_ly','_ignoreDrop','_lsAcc'])delete hero[k];resetSkillStates();startStage();hero._atkBuf=false;atkHeld=false;
    let t=0,maxMonsters=0,maxParticles=0;for(;t<600&&stageState==='fighting'&&!hero.dead;t+=.05){update(.05);maxMonsters=Math.max(maxMonsters,monsters.length);maxParticles=Math.max(maxParticles,particles.length);}
    return {classId:cid,seed,initialStage:stage,initialLevel:level,simulationSeconds:Math.round(t*100)/100,outcome:stageState,dead:hero.dead,kills:stageKills,quota:stageQuota(),hp:hero.hp,level:P.level,maxMonsters,maxParticles};
   }
   try{for(const cid of ['swordsman','mage','archer'])for(let s=1;s<=4;s++)runs.push(run(cid,s,1,1));for(let s=101;s<=130;s++)runs.push(run('mage',s,1,1));for(let s=201;s<=204;s++)runs.push(run('swordsman',s,5,10));}
   finally{Math.random=original;Object.assign(UI,savedUI);Object.assign(AudioFX,savedAudio);Minimap.draw=savedMinimap;}
   return {method:'actual update/Combat/Skills/Collision, deterministic LCG, dt .05, timeout 600 virtual seconds; no draw, DOM refresh, audio or minimap rendering during harness; no balance/config modifications; boss fixture swordsman Lv10 stage5 no gear or allocation',runs};
  });record('T12-seeded-harness',simulations);
  await page.evaluate(()=>{P=Save.fresh();P.created=true;P.name='Perf';P.auto=true;Save.data=P;uiPause=false;resetSkillStates();startStage();Roster.settings.muteAll=true;UI.refreshAll();});
  const fps=await page.evaluate(async()=>{
   const bench=()=>new Promise(resolve=>{const times=[];let prev;function tick(t){if(prev!==undefined)times.push(t-prev);prev=t;if(times.length<180)requestAnimationFrame(tick);else{times.sort((a,b)=>a-b);resolve({frames:times.length,meanMs:times.reduce((a,b)=>a+b,0)/times.length,p95Ms:times[Math.floor(times.length*.95)],over33ms:times.filter(x=>x>33.34).length});}}requestAnimationFrame(tick);});
   Roster.settings.quality='high';const high=await bench();Roster.settings.quality='low';const low=await bench();return {high,low,device:'Windows desktop headless Chrome, 844x390 DPR1; not an iPhone FPS result'};
  });record('T13-desktop-frame-probe',fps);
  if(fs.existsSync(path.join(OUT,'production.html'))){
  const prod=await context.newPage();const prodErrors=[];prod.on('pageerror',e=>prodErrors.push(e.message));
  await prod.route('https://fonts.googleapis.com/**',r=>r.abort());await prod.goto(pathToFileURL(path.join(OUT,'production.html')).href);await prod.waitForFunction(()=>document.querySelector('#introBack').style.display==='none');await prod.screenshot({path:path.join(OUT,'production-captured-create.png')});record('T14-captured-production',{errors:prodErrors,source:'Exact HTTP capture, executed locally; no browser interaction with live account or production writes'});
  } else {record('T14-captured-production',{skipped:true,reason:'production.html capture intentionally omitted from public evidence; download explicitly to reproduce'});}
  await context.tracing.stop({path:path.join(OUT,'playwright-trace.zip')});
  result.finished=new Date().toISOString();fs.writeFileSync(path.join(OUT,'review-tests.json'),JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{result.fatal={message:e.message,stack:e.stack};fs.writeFileSync(path.join(OUT,'review-tests.json'),JSON.stringify(result,null,2));console.error(e);process.exit(1)});
