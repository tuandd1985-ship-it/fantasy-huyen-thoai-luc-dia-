const {chromium}=require('playwright-core');
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});const results=[];try{
 for(const seed of [109,130]){
  const page=await browser.newPage({viewport:{width:844,height:390},deviceScaleFactor:1});await page.route('https://fonts.googleapis.com/**',r=>r.abort());
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../index.html')).href);await page.waitForFunction(()=>document.querySelector('#introBack').style.display==='none');
  await page.evaluate(()=>{createSel={classId:'mage',gender:'male'};document.querySelector('#charName').value='StallProbe';UI.createChar();Roster.settings.muteAll=true;});
  const state=await page.evaluate(seed=>{
   const UIold={},Aold={};for(const k of Object.keys(UI))if(typeof UI[k]==='function'){UIold[k]=UI[k];UI[k]=()=>{};}for(const k of Object.keys(AudioFX))if(typeof AudioFX[k]==='function'){Aold[k]=AudioFX[k];AudioFX[k]=()=>{};}const mm=Minimap.draw;Minimap.draw=()=>{};
   let rng=seed>>>0;const original=Math.random;Math.random=()=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng/4294967296;};P=Save.fresh();P.name='StallProbe';P.created=true;P.classId='mage';P.auto=true;Save.data=P;uiPause=false;resetSkillStates();startStage();const samples=[];
   for(let i=0;i<12000&&stageState==='fighting'&&!hero.dead;i++){update(.05);if(i%200===0)samples.push({t:i*.05,kills:stageKills,hero:{x:hero.x,y:hero.y},enemies:monsters.map(m=>({type:m.type,x:m.x,y:m.y,hp:m.hp}))});}
   const data={seed,outcome:stageState,kills:stageKills,quota:stageQuota(),hero:{x:hero.x,y:hero.y,hp:hero.hp,mp:hero.mp},enemies:monsters.map(m=>({type:m.type,x:m.x,y:m.y,hp:m.hp,distance:Math.hypot(m.x-hero.x,m.y-hero.y),blocked:m.blocked})),obstacles,waterRects,samples};
   Math.random=original;Object.assign(UI,UIold);Object.assign(AudioFX,Aold);Minimap.draw=mm;uiPause=true;UI.refreshAll();draw();return data;
  },seed);results.push(state);await page.screenshot({path:path.join(__dirname,`evidence/stall-seed-${seed}.png`)});await page.close();
 }
 fs.writeFileSync(path.join(__dirname,'evidence/stall-reproduction.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results.map(({samples,obstacles,waterRects,...x})=>x)));
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
